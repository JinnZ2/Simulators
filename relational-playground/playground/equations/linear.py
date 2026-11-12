"""Family A. dx/dt = A x + B u.

parameters: A {i: {j: a_ij}}, B {i: {k: b_ik}}, u {k: value}.
With compartmental=True the off-diagonal a_ij x_j is read as a transfer j -> i and
the diagonal must equal minus the column's outflow plus a loss to the outside;
otherwise every term is an exchange with the outside.
"""
from .base import ModelOutput, from_transfers, register


def linear(state, env, rel, ctl, p):
    A, B, u = p["A"], p["B"], p["u"]
    names = [k for k in state if not k.startswith("_")]
    tr = []
    if p["compartmental"]:
        for j in names:
            col_off = 0.0
            for i in names:
                a = A.get(i, {}).get(j, 0.0)
                if i != j and a:
                    if a < 0:
                        raise ValueError("compartmental A needs off-diagonals >= 0; A[%s][%s]=%r" % (i, j, a))
                    tr.append(("%s_to_%s" % (j, i), j, i, a * state[j]))
                    col_off += a
            loss = -A.get(j, {}).get(j, 0.0) - col_off
            if loss < 0:
                raise ValueError("compartmental A: column %s creates mass (diagonal too small)" % j)
            tr.append(("loss_%s" % j, j, None, loss * state[j]))
    else:
        for i in names:
            for j in names:
                a = A.get(i, {}).get(j, 0.0)
                if a:
                    r = a * state[j]
                    tr.append(("A_%s_%s" % (i, j), None, i, r) if r >= 0 else ("A_%s_%s" % (i, j), i, None, -r))
    for i in names:
        for k, b in B.get(i, {}).items():
            r = b * u[k]
            tr.append(("B_%s_%s" % (i, k), None, i, r) if r >= 0 else ("B_%s_%s" % (i, k), i, None, -r))
    return ModelOutput(from_transfers(tr, names), transfers=tr,
                       uncertainty="linear about one operating point; no saturation, no thresholds")


register("linear", "linear", "0.1", linear, "rate", requires=("A", "B", "u", "compartmental"),
         limitations=("valid near the operating point it was linearised at", "cannot hold two stable states"))
