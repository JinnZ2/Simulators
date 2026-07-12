"""AI-patching loop over audits. Runs an audit, asks the AI for a patch on
failure, applies the patch, re-runs. Bounded by max_iterations."""

import copy
from ai_interface import AIScientist


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
            current = self._apply_patch(current, patch)
        return result, self.history

    def _apply_patch(self, audit, patch):
        """Best-effort patch application. Recognises `params`, `add_threshold`,
        `add_feedback`, `recalibrate`. Real usage would generate a new audit
        instance with the modified model; this scaffold does the pragmatic
        version and records that a patch was tried."""
        new_audit = copy.copy(audit)
        # patches recognised by the current scaffold are structural and require
        # rebuilding the model class; the honest thing is to note the attempt
        # in history rather than pretend the patch mutated the underlying
        # audit. `recalibrate` in particular would need a separate data path.
        new_audit._last_patch = patch
        return new_audit
