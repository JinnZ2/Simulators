"""AI-patching loop over audits. Two entry points:

- `MetaExperiment.run_audit_with_patching(audit)` — original scenario-level
  patch loop using the dict-patch `AIScientist`. Kept for the dashboard.
- `run_meta_experiment(audit_name, max_iterations, use_openai)` — the
  active loop: extract the audited model's `derivative` source, ask the
  patcher (rule-based or LLM) for a new body, compile & hot-swap onto the
  class via `apply_patch_to_class`, re-audit. Bounded by max_iterations."""

import argparse
import copy
import inspect
import json
import os
import textwrap
import types

from ai_interface import AIScientist, RuleBasedPatcher, LLMPatcher


# ------------------------------------------------------------
# Dynamic method rewriting
# ------------------------------------------------------------

def get_derivative_source(model_class):
    """Return the source text of `model_class.derivative`, dedented."""
    src = inspect.getsource(model_class.derivative)
    return textwrap.dedent(src)


def apply_patch_to_class(model_class, new_derivative_body):
    """Compile `new_derivative_body` as the body of a fresh `derivative`
    method and swap it onto `model_class`. Returns the (mutated) class.

    Cleans markdown fences if the LLM leaked them and normalises
    indentation via textwrap.indent so the exec compile step doesn't
    trip on a leading `    ` from a code block.
    """
    body = new_derivative_body.strip()
    for fence in ("```python", "```py", "```"):
        body = body.replace(fence, "")
    body = textwrap.dedent(body).strip()
    if not body:
        raise ValueError("empty patch body")
    indented = textwrap.indent(body, "    ")
    func_src = "def derivative(self, t, state, forcing_value):\n" + indented
    ns = {"np": __import__("numpy"), "math": __import__("math")}
    try:
        exec(compile(func_src, "<patch>", "exec"), ns)
    except SyntaxError as e:
        raise ValueError(f"patch did not compile: {e}\n---\n{func_src}") from e
    model_class.derivative = ns["derivative"]
    return model_class


# ------------------------------------------------------------
# Active patching loop
# ------------------------------------------------------------

def run_meta_experiment(audit_name="CascadeSpeedAudit", max_iterations=3,
                        use_openai=False, verbose=True,
                        history_path=None):
    """Runs the audit, ask the patcher for a new derivative on failure,
    hot-swap it, re-audit. Records every iteration."""
    from run_audits import AUDIT_REGISTRY, run_single_audit

    if audit_name not in AUDIT_REGISTRY:
        raise KeyError(f"unknown audit '{audit_name}'")
    audit = AUDIT_REGISTRY[audit_name]

    # take the audit's default audited model, then subclass so we don't
    # mutate the shared class across meta-experiments
    original_model = audit.generate_audited_model()
    base_class = type(original_model)
    patched_class = type(f"Patched_{base_class.__name__}", (base_class,), {})

    # Track the current derivative source in a local. After the first
    # exec-compiled patch, inspect.getsource can't find the method source
    # anymore (no file for the compiled bytecode), so we shadow it here.
    current_source = get_derivative_source(base_class)

    patcher = LLMPatcher() if use_openai else RuleBasedPatcher()
    history = []

    if verbose:
        print(f"\nMETA-EXPERIMENT — {audit_name}")
        print(f"  patcher: {'LLMPatcher (openai)' if use_openai else 'RuleBasedPatcher'}")
        print(f"  max_iterations: {max_iterations}")
        print(f"  patched class: {patched_class.__name__} (subclass of {base_class.__name__})")

    for i in range(max_iterations + 1):
        instance = patched_class()
        result = run_single_audit(audit_name, instance)
        entry = {
            "iteration": i,
            "status": result["status"],
            "metrics": result["metrics"],
            "true_final": result["true_final"],
            "audited_final": result["audited_final"],
        }
        history.append(entry)

        first_metric = next(iter(result["metrics"].items()), ("", ""))
        summary = f"{first_metric[0]}={first_metric[1]}" if first_metric[0] else ""
        if verbose:
            print(f"\n  iter {i}: {result['status']}  {summary}")

        if result["passed"]:
            if verbose:
                print(f"  passed after {i} patch attempts")
            break
        if i == max_iterations:
            if verbose:
                print(f"  still failing after {max_iterations} patches — stopping")
            break

        try:
            body = patcher.suggest_patch({"name": audit_name, **result},
                                         current_source)
        except Exception as e:
            if verbose:
                print(f"  patcher raised: {e}")
            entry["patch_error"] = str(e)
            break
        if not body:
            if verbose:
                print("  patcher returned no patch — stopping")
            break
        try:
            apply_patch_to_class(patched_class, body)
            entry["patch_applied"] = True
            entry["patch_body"] = body
            # Shadow the source so the next iteration sees the current body,
            # not the base class's (inspect.getsource can't read exec output).
            current_source = ("def derivative(self, t, state, forcing_value):\n"
                              + textwrap.indent(body.strip(), "    "))
            if verbose:
                print("  patch applied; re-auditing")
        except ValueError as e:
            entry["patch_applied"] = False
            entry["patch_error"] = str(e)
            if verbose:
                print(f"  patch failed to compile: {e}")
            break

    if history_path:
        try:
            os.makedirs(os.path.dirname(history_path) or ".", exist_ok=True)
            with open(history_path, "w") as f:
                json.dump(history, f, indent=2, default=str)
            if verbose:
                print(f"\n  history -> {history_path}")
        except OSError as e:
            print(f"  could not save history ({e})")

    return history


# ------------------------------------------------------------
# Legacy scenario-level loop (kept for the dashboard hook)
# ------------------------------------------------------------

class MetaExperiment:
    def __init__(self, ai=None):
        self.ai = ai if ai else AIScientist(backend="dummy")
        self.history = []

    def run_audit_with_patching(self, audit, max_iterations=2, verbose=True):
        current = audit
        result = None
        for iteration in range(max_iterations + 1):
            if verbose:
                print(f"\n--- {audit.name} iteration {iteration} ---")
            try:
                result = current.run()
            except NotImplementedError as e:
                result = {"audit_name": audit.name, "failure_detected": None,
                          "metrics": {"status": "FRONTIER_STUB", "reason": str(e)},
                          "true_final": None, "audited_final": None}
                self.history.append({"audit": audit.name, "iteration": iteration,
                                     "result": result})
                break
            self.history.append({"audit": audit.name, "iteration": iteration,
                                 "result": result})
            if not result.get("failure_detected"):
                if verbose:
                    print(f"  passed after {iteration} iterations")
                break
            if iteration == max_iterations:
                if verbose:
                    print(f"  failed after {max_iterations} patch attempts")
                break
            patch = self.ai.propose_patch({
                "audit_name": audit.name,
                "audit_description": audit.description,
                "failure_metrics": result.get("metrics", {}),
                "true_final": result.get("true_final"),
                "audited_final": result.get("audited_final"),
                "model_description": type(current).__name__,
            })
            if verbose:
                print(f"  AI: {patch.get('reason', patch)}")
            current = copy.copy(current)
            current._last_patch = patch
        return result, self.history


# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def _cli():
    p = argparse.ArgumentParser(description="AI-patching audit loop.")
    p.add_argument("--audit", default="CascadeSpeedAudit",
                   help="name of the audit to loop on (default: CascadeSpeedAudit)")
    p.add_argument("--max-iter", type=int, default=3,
                   help="max patch attempts before giving up (default: 3)")
    p.add_argument("--openai", action="store_true",
                   help="use LLMPatcher (falls back to rules if openai unavailable)")
    p.add_argument("--history", default="samples/meta_history.json",
                   help="where to write the iteration history")
    args = p.parse_args()
    run_meta_experiment(audit_name=args.audit, max_iterations=args.max_iter,
                        use_openai=args.openai, history_path=args.history)


if __name__ == "__main__":
    _cli()
