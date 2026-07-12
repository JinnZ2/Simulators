"""Abstract model interface. Every audited model subclasses BaseModel."""

from abc import ABC, abstractmethod
from scipy.integrate import solve_ivp


class BaseModel(ABC):
    @abstractmethod
    def derivative(self, t, state, forcing_value):
        """d(state)/dt at time t. `forcing_value` is a dict of environmental
        scalars at this instant (e.g. {'temperature': T, 'light': 0/1})."""

    def simulate(self, forcing, initial_state, t_span=(0, 200), max_step=0.5):
        """Run the model with a forcing callable f(t) that returns a dict.
        Returns (t, y) with y shaped (n_state, n_time)."""
        def rhs(t, y):
            return self.derivative(t, y, forcing(t))
        sol = solve_ivp(rhs, t_span, initial_state,
                        max_step=max_step, rtol=1e-6, atol=1e-8)
        return sol.t, sol.y
