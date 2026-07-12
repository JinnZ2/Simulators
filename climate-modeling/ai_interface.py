"""AI scientist wrapper. Ships with a rule-based stub; swap `backend="openai"`
to route through an LLM."""

import json


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
