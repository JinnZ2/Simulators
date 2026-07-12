"""Abstract audit interface. Every failure-mode audit subclasses BaseAudit."""

from abc import ABC, abstractmethod


class BaseAudit(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def generate_true_system(self):
        """Return (model, forcing, initial_state) for the true generative process."""

    @abstractmethod
    def generate_audited_model(self):
        """Return the simplified model being audited."""

    @abstractmethod
    def compute_audit_metrics(self, true_output, audited_output):
        """Return dict of metrics including boolean 'failure_detected'."""

    def run(self):
        """Default runner: same forcing + init to true and audited model."""
        true_model, forcing, init = self.generate_true_system()
        t_true, y_true = true_model.simulate(forcing, init,
                                             t_span=(0, self.duration()))
        audited_model = self.generate_audited_model()
        # audited model receives just the first component of init by default
        aud_init = init[:1] if hasattr(init, '__len__') else [init]
        t_aud, y_aud = audited_model.simulate(forcing, list(aud_init),
                                              t_span=(0, self.duration()))
        metrics = self.compute_audit_metrics((t_true, y_true), (t_aud, y_aud))
        return {
            "audit_name": self.name,
            "failure_detected": metrics.pop("failure_detected"),
            "metrics": metrics,
            "true_final": float(y_true[0, -1]),
            "audited_final": float(y_aud[0, -1]),
        }

    def duration(self):
        """Simulation window (hours). Subclasses may override."""
        return 200.0
