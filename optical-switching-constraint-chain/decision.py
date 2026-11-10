#!/usr/bin/env python3
"""OSC-WO2: the report's sec. 6.4 decision table as a readout.

The report routes the roadmap on one number, the energy barrier Delta of an
optically written bit, through three bands (>= 60, 40-60, < 40). The audit
found the two cut lines are different kinds of thing (OSC_008): 40 is where
ONE bit survives ten years, ln(t/tau0); 60 is a POPULATION line whose basis
(grain dispersion, bit count, error budget) has to be stated. This readout
takes both lines from barrier_per_bit.retention_line (imported) and keeps
them apart.

Inputs and states:
    measured Delta with its uncertainty  -> a band position, or STRADDLES
    no measurement                       -> UNMEASURED (first-class)
    a coherent estimate                  -> ESTIMATED only with a DECLARED
                                            discount range and its basis;
                                            the report's ~100x rests on a
                                            NOT_FOUND precedent (OSC_011)

Band positions (route labels as the report's table assigns them):
    ABOVE_POPULATION_LINE   report: Co/Pt + amplifier becomes the recording route
    BETWEEN_LINES           one bit survives, the population does not; report:
                            cache-class with refresh or ECC
    BELOW_SINGLE_BIT_LINE   report: continuous film is a physics platform, not a medium

Never returns a band from an estimate alone without the word ESTIMATED, and
never returns one when an interval crosses a line.

    python3 decision.py     the readout on the report's own inputs
The module refuses --selftest; checks live in test_decision.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from barrier_per_bit import UndeclaredTerm, delta_coherent, retention_line  # noqa: E402

BANDS = ("ABOVE_POPULATION_LINE", "BETWEEN_LINES", "BELOW_SINGLE_BIT_LINE")
ROUTE = {
    "ABOVE_POPULATION_LINE": "report: the IFE-friendly class is the recording class",
    "BETWEEN_LINES": "report: cache-class memory with refresh or ECC, beside SOT-MRAM",
    "BELOW_SINGLE_BIT_LINE": "report: continuous-film AOS is a physics platform, not a medium",
}


def lines(*, years, tau0, population_value, basis):
    single = retention_line(criterion="single_bit", years=years, tau0=tau0)
    pop = retention_line(criterion="population", years=years, tau0=tau0,
                         population_value=population_value, basis=basis)
    if pop < single:
        raise ValueError("population line below the single-bit line: check the declared value")
    return single, pop


def _band(x, single, pop):
    if x >= pop:
        return "ABOVE_POPULATION_LINE"
    if x >= single:
        return "BETWEEN_LINES"
    return "BELOW_SINGLE_BIT_LINE"


def _interval(lo, hi, single, pop):
    a, b = _band(lo, single, pop), _band(hi, single, pop)
    if a == b:
        return a, None
    return "STRADDLES", sorted({a, b}, key=BANDS.index)


def readout(*, single, pop, measured=None, uncertainty=None,
            coherent=None, discount_range=None, discount_basis=None):
    """measured, uncertainty: Delta and its one-sided half-width (both or neither).
    coherent: a coherent-volume Delta; discount_range: (lo, hi) factors with a basis."""
    if measured is not None:
        if uncertainty is None:
            raise UndeclaredTerm("undeclared: uncertainty (a measured Delta carries one)")
        state, spans = _interval(measured - uncertainty, measured + uncertainty, single, pop)
        return {"source": "MEASURED", "state": state, "spans": spans,
                "interval": (measured - uncertainty, measured + uncertainty),
                "route": ROUTE.get(state)}
    if coherent is None:
        return {"source": None, "state": "UNMEASURED", "spans": None, "interval": None,
                "route": None}
    if discount_range is None or discount_basis is None:
        raise UndeclaredTerm("undeclared: discount_range and discount_basis "
                             "(a coherent estimate is an upper bracket, OSC_011)")
    lo_f, hi_f = sorted(discount_range)
    if lo_f < 1:
        raise ValueError("a discount below 1 would raise the barrier above the coherent bracket")
    lo, hi = coherent / hi_f, coherent / lo_f
    state, spans = _interval(lo, hi, single, pop)
    return {"source": "ESTIMATED", "state": state, "spans": spans, "interval": (lo, hi),
            "route": ROUTE.get(state)}


def render():
    single, pop = lines(years=10, tau0=1e-9, population_value=60,
                        basis="the report's 60 (Weller & Moser 1999 dispersion criterion), carried")
    out = ["optical-switching-constraint-chain / decision.py", "=" * 66,
           f"lines: single bit (10 y, tau0 1 ns) {single:.1f}; population {pop:g} (declared, basis carried)", ""]
    r = readout(single=single, pop=pop)
    out.append(f"no measurement:               {r['state']}")
    for label, k, t in (("Co/Pt 12 nm, 0.5 MJ/m3, 30 nm", 0.5e6, 12e-9),
                        ("Co/Pt 5.4 nm, 0.3 MJ/m3, 30 nm", 0.3e6, 5.4e-9)):
        coh = delta_coherent(shape="square", k=k, lateral=30e-9, thickness=t, temperature=300)
        try:
            readout(single=single, pop=pop, coherent=coh)
        except UndeclaredTerm as e:
            out.append(f"{label}: coherent {coh:.0f}, no discount declared -> REFUSED ({e})")
        r = readout(single=single, pop=pop, coherent=coh, discount_range=(30, 100),
                    discount_basis="ILLUSTRATIVE ONLY: the report's ~100x; its precedent is NOT_FOUND")
        out.append(f"   with an illustrative 30-100x discount: {r['source']} "
                   f"{r['interval'][0]:.1f}..{r['interval'][1]:.1f} -> {r['state']}"
                   + (f" {r['spans']}" if r['spans'] else ""))
    out += ["", "measured examples (constructed, to show the states):"]
    for m, u in ((75, 5), (50, 3), (30, 4), (58, 5)):
        r = readout(single=single, pop=pop, measured=m, uncertainty=u)
        out.append(f"   Delta {m} +/- {u}: {r['state']}" + (f" {r['spans']}" if r['spans'] else ""))
    out += ["", "Nothing above is a measurement. The roadmap stays UNMEASURED until one exists."]
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        print("decision.py is a library; run: python3 test_decision.py")
        sys.exit(2)
    print(render())
