import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from playground.uncertainty import Value, UncertaintyMatrix
from playground.system import SystemDefinition, UNDECLARED
from playground.controls import ControlMatrix
from playground.environment import Environment
from playground.experiments.runner import Config
from playground.equations import base as eq
from playground import l0

eq.load_all()
A = lambda v: Value(v, "ASSUMED", "test fixture")


def controls(**extra):
    d = {f: UNDECLARED for f in ControlMatrix.__init__.__globals__["FIELDS"]}
    d.update(extra)
    return ControlMatrix(**d)


def system(name="fixture"):
    return SystemDefinition(name, **{f: UNDECLARED for f in SystemDefinition.__init__.__globals__["FIELDS"]})


def budgets(**live):
    """live: budget name -> pools. The rest are VOID with the fixture's reason."""
    return l0.declare(**{b: (l0.Budget(b, pools=live[b]) if b in live else l0.Budget(b, void_reason="not modelled in this fixture"))
                         for b in l0.BUDGETS})


def config(model, params, initial, t_end=10.0, dt=0.01, seed=1, rel=None, forcing=None, run_id=None, live=None, **extra):
    kw = dict(run_id=run_id or "t_" + model, system=system(), boundary=None, model=model, relationships=rel,
              controls=controls(), environment=Environment(seed, forcing),
              parameters=UncertaintyMatrix({k: A(v) for k, v in params.items()}),
              initial=UncertaintyMatrix({k: A(v) for k, v in initial.items()}),
              t_end=t_end, dt=dt, observations=None,
              budgets=budgets(**(live or {})))
    kw.update(extra)
    return Config(**kw)
