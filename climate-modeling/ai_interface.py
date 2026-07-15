"""AI scientist wrappers.

Two patcher families:

- `RuleBasedPatcher` / `LLMPatcher` — produce a full derivative-method BODY
  (a code string) that the meta-experiment loop compiles and hot-swaps onto
  the audited model class via `apply_patch_to_class`.
- `AIScientist` — the older AIScientist proposes structural patches as dicts
  (add_threshold, add_feedback, ...) suitable for scenario-level rewrites.
  Kept for backward compat with `meta_experiments.MetaExperiment`.
"""

import json
import os


class RuleBasedPatcher:
    """Maps audit-failure metrics to a fresh derivative body. Deterministic;
    no network. Recognises the three metric shapes the built audits emit."""

    def suggest_patch(self, audit_result, model_source):
        metrics = audit_result.get("metrics", {}) or {}
        rmse = float(metrics.get("rmse", 0.0) or 0.0)
        err = float(metrics.get("final_biomass_error", 0.0) or 0.0)
        delay = float(metrics.get("audited_late_by_h", 0.0) or 0.0)

        body_lines = ["x = state[0]",
                      "T = forcing_value.get('temperature', 20.0)",
                      "co2 = forcing_value.get('co2', 380.0)",
                      "light = forcing_value.get('light', 1.0)"]

        # Rule 1: severe divergence -> add a hard threshold cliff
        if rmse > 100.0 or err > 1000.0:
            body_lines.append("if x < 20.0 or T > 35.0:")
            body_lines.append("    return [-0.10 * x]")

        # Rule 2: audit crashes late -> add memory-slowing term
        if delay > 20.0:
            body_lines.append("if x < 60.0:")
            body_lines.append("    return [-0.08 * x]")

        # Rule 3: coupling gap -> tie growth to CO2 driver
        if err > 20.0:
            body_lines.append("growth = 0.10 * x * (1.0 + 0.005 * (co2 - 380.0))")
        else:
            body_lines.append("growth = 0.10 * x")

        # Base death
        body_lines.append("death = 0.05 * x")
        # Temperature-modulated growth loss above 35
        body_lines.append("if T > 35.0:")
        body_lines.append("    death += 0.5 * x")
        body_lines.append("return [growth - death]")
        return "\n".join(body_lines)


class LLMPatcher:
    """OpenAI-backed patcher. Falls back to `RuleBasedPatcher` if the
    `openai` package is not installed or `OPENAI_API_KEY` is unset — so
    the CLI flag `--openai` is safe to flip even without an API key."""

    def __init__(self, api_key=None, model="gpt-4"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        try:
            import openai  # noqa: F401
            self._openai_available = bool(self.api_key)
        except ImportError:
            self._openai_available = False
        self._fallback = RuleBasedPatcher()

    def suggest_patch(self, audit_result, model_source):
        if not self._openai_available:
            print("  [LLMPatcher] openai not available (no key or package); "
                  "falling back to rule-based patcher.")
            return self._fallback.suggest_patch(audit_result, model_source)
        return self._call_openai(audit_result, model_source)

    def _prompt(self, audit_result, model_source):
        return (
            "You are an expert climate modeler fixing a simplified vegetation model.\n\n"
            f"AUDIT FAILURE:\n"
            f"- Name: {audit_result.get('name')}\n"
            f"- Metrics: {json.dumps(audit_result.get('metrics', {}), indent=2)}\n"
            f"- True final: {audit_result.get('true_final')}\n"
            f"- Audited final: {audit_result.get('audited_final')}\n\n"
            f"CURRENT DERIVATIVE SOURCE:\n{model_source}\n\n"
            "TASK: rewrite ONLY the body of `derivative(self, t, state, forcing_value)`.\n"
            "- state[0] is biomass; return a list of length 1.\n"
            "- forcing_value is a dict; read `temperature`, `co2`, `light` via .get().\n"
            "- Add thresholds, memory, or forcing-coupling as the failure metric indicates.\n"
            "- Use `import numpy as np` implicitly via the compile namespace.\n"
            "- Return ONLY the body (no `def` line), inside triple backticks."
        )

    def _call_openai(self, audit_result, model_source):
        import re
        try:
            import openai
            openai.api_key = self.api_key
            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system",
                     "content": "You write Python code for climate models."},
                    {"role": "user",
                     "content": self._prompt(audit_result, model_source)},
                ],
                temperature=0.2,
                max_tokens=500,
            )
            raw = resp.choices[0].message.content
            m = re.search(r"```(?:python)?\n(.*?)```", raw, re.DOTALL)
            return m.group(1).strip() if m else raw.strip()
        except Exception as e:
            print(f"  [LLMPatcher] openai call failed ({e}); falling back.")
            return self._fallback.suggest_patch(audit_result, model_source)


class AIScientist:
    def __init__(self, backend="dummy", api_key=None):
        self.backend = backend
        self.api_key = api_key

    def propose_patch(self, context: dict) -> dict:
        """Given an audit failure context, return a patch dict.
        Patch shapes recognised by MetaExperiment._apply_patch:
          {"params": {...}}                — override model attributes
          {"add_threshold": True, ...}     — dynamically subclass with a cliff
          {"add_feedback": True, ...}      — enable soil-plant coupling
          {"recalibrate": True, ...}       — flag a re-estimation on richer data
        """
        if self.backend == "dummy":
            return self._rule_based(context)
        return self._call_openai(context)

    def _rule_based(self, context):
        name = context.get("audit_name", "")
        err = context.get("failure_metrics", {})
        if "Phase Change" in name or "Threshold" in name:
            return {"add_threshold": True, "threshold_temp": 35, "extra_resp": 8.0,
                    "reason": "Add a respiration cliff above 35°C."}
        if "Stationarity" in name:
            return {"params": {"Q10": 2.5},
                    "reason": "Increase Q10 to capture the warming trend response."}
        if "Missing Feedback" in name or "Positive Feedback" in name:
            return {"add_feedback": True, "feedback_strength": 0.02,
                    "reason": "Add soil-carbon fertility feedback to photosynthesis."}
        if "Omitted Variable" in name:
            return {"params": {"assumed_moisture": 0.5},
                    "reason": "Lower assumed moisture to closer to the true average."}
        if "Data Aggregation" in name:
            return {"recalibrate": True,
                    "reason": "Re-estimate parameters using hourly data instead of daily means."}
        if "Cascade Speed" in name:
            return {"add_threshold": True, "threshold_temp": 35, "extra_resp": 8.0,
                    "add_feedback": True, "feedback_strength": 0.02,
                    "reason": "Cascade needs threshold + feedback + memory. Start with the first two."}
        return {"reason": "No automated patch available for this audit."}

    def _call_openai(self, context):
        """Placeholder for real API integration. Kept import-inside so the
        stub-only path has zero external dependencies."""
        try:
            import openai  # noqa: F401
        except ImportError:
            return {"reason": "openai package not installed; falling back to dummy.",
                    **self._rule_based(context)}
        prompt = self._build_prompt(context)
        # actual call intentionally elided; wire this up per the deployed API version
        return {"reason": "openai-backed patching not wired up in this scaffold.",
                "prompt": prompt,
                **self._rule_based(context)}

    def _build_prompt(self, context):
        return (f"Audit `{context['audit_name']}` failed with metrics "
                f"{json.dumps(context.get('failure_metrics', {}))}. "
                f"Propose a JSON patch to fix it.")
