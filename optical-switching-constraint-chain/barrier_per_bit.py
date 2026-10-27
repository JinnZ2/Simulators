#!/usr/bin/env python3
"""OSC-WO1: barrier-per-bit calculator with every term declared.

The audit of SOURCE_DROP.md found that its derived numbers fail where a term
was used without being stated: an absorbed fraction nobody wrote down
(OSC_004), a fluence taken from a different experiment (OSC_005), and a
retention line that is a population criterion presented as a per-bit one
(OSC_008). This module makes each of those terms a REQUIRED input. There are
no defaults for them. An undeclared term raises UndeclaredTerm, it is never
filled in.

    stripe_period(n, t_layer, ms, keff, aex)      Kaplan-Gehring form (as the report quotes it)
    delta_coherent(shape, k, lateral, thickness, temperature)
    retention_line(criterion, years, tau0, population_value=None, basis=None)
    energy_per_bit(fluence, spot_diameter, spot_shape, pulses, ledger, absorbed_fraction=None)

    python3 barrier_per_bit.py     the report's rows recomputed, with the undeclared ones refused

The module refuses --selftest; checks live in test_barrier_per_bit.py.
Physical constants: CODATA 2018 exact values. Nothing here measures a bit.
"""
import math
import sys

MU0 = 4e-7 * math.pi
KB = 1.380649e-23
EV = 1.602176634e-19
YEAR = 3.15576e7  # Julian year, s


class UndeclaredTerm(ValueError):
    """A term the result depends on was not declared."""


def _need(**terms):
    missing = [k for k, v in terms.items() if v is None]
    if missing:
        raise UndeclaredTerm("undeclared: " + ", ".join(missing))


# ------------------------------------------------------------- stripe period

def stripe_period(n, *, t_layer, ms, keff, aex):
    """Equilibrium stripe period (m) for N repeats of magnetic thickness
    t_layer each: D = t exp[pi sigma_w / (2 E_d t) + ln pi - 1/2 - ln 2],
    sigma_w = 4 sqrt(A K), E_d = mu0 Ms^2 / 2. Valid only for laterally
    exchange-coupled continuous films (the report's own scope, sec. 3.2)."""
    _need(n=n, t_layer=t_layer, ms=ms, keff=keff, aex=aex)
    if n < 1 or t_layer <= 0 or ms <= 0 or keff <= 0 or aex <= 0:
        raise ValueError("stripe_period needs positive inputs")
    t = n * t_layer
    sw = 4 * math.sqrt(aex * keff)
    ed = MU0 * ms ** 2 / 2
    return t * math.exp(math.pi * sw / (2 * ed * t) + math.log(math.pi) - 0.5 - math.log(2))


def crossover_n(spot, **params):
    """Smallest N whose stripe period falls below `spot` (m); None if none
    below N = 60 (a measured absence over the declared range, not infinity)."""
    for n in range(1, 61):
        if stripe_period(n, **params) < spot:
            return n
    return None


# ------------------------------------------------------------- coherent barrier

SHAPES = ("square", "cylinder")


def delta_coherent(*, shape, k, lateral, thickness, temperature):
    """Coherent (Stoner-Wohlfarth) barrier over k_B T. square: K L^2 t;
    cylinder: K (pi/4) D^2 t. An UPPER bracket: the report's own sec. 6.3
    says nucleation-limited reversal comes out lower."""
    _need(shape=shape, k=k, lateral=lateral, thickness=thickness, temperature=temperature)
    if shape not in SHAPES:
        raise ValueError(f"shape must be one of {SHAPES}")
    area = lateral ** 2 if shape == "square" else math.pi / 4 * lateral ** 2
    return k * area * thickness / (KB * temperature)


def lateral_at_delta(target, *, shape, k, thickness, temperature):
    """Lateral size (m) at which the coherent barrier equals `target`."""
    _need(target=target, shape=shape, k=k, thickness=thickness, temperature=temperature)
    geom = 1.0 if shape == "square" else math.pi / 4
    return math.sqrt(target * KB * temperature / (k * thickness * geom))


# ------------------------------------------------------------- retention line

CRITERIA = ("single_bit", "population")


def retention_line(*, criterion, years, tau0, population_value=None, basis=None):
    """The Delta a stored bit must clear. Two criteria, never merged:
      single_bit  -> ln(t / tau0), derived; one bit survives the period on average
      population  -> a declared value WITH a basis (dispersion, bit count, error
                     budget); the report's 60 is this kind, and is refused here
                     unless the basis is stated."""
    _need(criterion=criterion, years=years, tau0=tau0)
    if criterion not in CRITERIA:
        raise ValueError(f"criterion must be one of {CRITERIA}")
    if criterion == "single_bit":
        return math.log(years * YEAR / tau0)
    _need(population_value=population_value, basis=basis)
    return float(population_value)


# ------------------------------------------------------------- energy per bit

SPOT_SHAPES = ("disc", "square")
LEDGERS = ("incident", "absorbed")


def spot_area_cm2(diameter_um, spot_shape):
    d = diameter_um * 1e-4
    return math.pi * (d / 2) ** 2 if spot_shape == "disc" else d * d


def energy_per_bit(*, fluence, spot_diameter, spot_shape, pulses, ledger, absorbed_fraction=None):
    """Energy per written bit in joules.
      fluence        J/cm2 per pulse, as measured in THE experiment the row is about
      spot_diameter  um
      spot_shape     'disc' or 'square' (the report states neither)
      pulses         pulses per written bit
      ledger         'incident' or 'absorbed'; 'absorbed' requires absorbed_fraction"""
    _need(fluence=fluence, spot_diameter=spot_diameter, spot_shape=spot_shape,
          pulses=pulses, ledger=ledger)
    if spot_shape not in SPOT_SHAPES:
        raise ValueError(f"spot_shape must be one of {SPOT_SHAPES}")
    if ledger not in LEDGERS:
        raise ValueError(f"ledger must be one of {LEDGERS}")
    incident = fluence * spot_area_cm2(spot_diameter, spot_shape) * pulses
    if ledger == "incident":
        return incident
    _need(absorbed_fraction=absorbed_fraction)
    if not 0 <= absorbed_fraction <= 1:
        raise ValueError("absorbed_fraction must be within [0, 1]")
    return incident * absorbed_fraction


# ------------------------------------------------------------- the report's rows

REPORT = {"t_layer": 0.6e-9, "ms": 0.9e6, "keff": 0.5e6, "aex": 15e-12}

# (label, fluence J/cm2, spot um, pulses, stated pJ, fluence source)
ENERGY_ROWS = [
    ("UCSD vector beam", 7.6e-6, 0.76, 1000, 12.0,
     "fluence taken from Vomir 2017, a different experiment; UCSD's own fluence not stated"),
    ("classic AO-HDS", 4e-3, 0.76, 100, 640.0, "stated"),
    ("plasmonic TbFeCo", 3.7e-3, 0.053, 100, 4.9, "stated"),
]


def _try(fn, **kw):
    try:
        return fn(**kw), None
    except UndeclaredTerm as e:
        return None, str(e)


def render():
    out = ["optical-switching-constraint-chain / barrier_per_bit.py", "=" * 66,
           "every term declared or the row is refused", "",
           "STRIPE PERIOD at the report's parameters (Ms 0.9 MA/m, Keff 0.5 MJ/m3, A 15 pJ/m, 0.6 nm/repeat)"]
    for n in (3, 5, 7, 9, 10, 11, 12):
        out.append(f"   N={n:>2}  {stripe_period(n, **REPORT) * 1e6:>12.4g} um")
    out.append(f"   first N below 1.5 um: {crossover_n(1.5e-6, **REPORT)}   below 0.76 um: {crossover_n(0.76e-6, **REPORT)}")
    out += ["", "RETENTION LINE (10 years)"]
    for tau0 in (1e-9, 1e-10):
        out.append(f"   single_bit, tau0={tau0:g} s: Delta = {retention_line(criterion='single_bit', years=10, tau0=tau0):.1f}")
    v, err = _try(retention_line, criterion="population", years=10, tau0=1e-9, population_value=60)
    out.append(f"   population 60 with no basis: {'REFUSED (' + err + ')' if err else v}")
    v = retention_line(criterion="population", years=10, tau0=1e-9, population_value=60,
                       basis="Weller & Moser 1999 dispersion criterion, as the report cites it")
    out.append(f"   population 60 with a stated basis: {v:g}")
    out += ["", "COHERENT DELTA AT 30 nm (an upper bracket; nucleation can be lower)"]
    for label, shape, k, t in (("Co/Pt 12 nm, 0.5 MJ/m3", "square", 0.5e6, 12e-9),
                               ("Co/Pt 5.4 nm, 0.3 MJ/m3", "square", 0.3e6, 5.4e-9),
                               ("FePt grain, 5 MJ/m3, 10 nm", "cylinder", 5e6, 10e-9)):
        d = delta_coherent(shape=shape, k=k, lateral=30e-9, thickness=t, temperature=300)
        l60 = lateral_at_delta(60, shape=shape, k=k, thickness=t, temperature=300) * 1e9
        out.append(f"   {label:<28} Delta {d:>7.0f}   size at Delta=60: {l60:.1f} nm")
    out += ["", "ENERGY PER BIT (pJ)",
            f"   {'row':<18} {'incident disc':>13} {'incident sq':>12} {'absorbed':>10} {'stated':>7}"]
    for label, f, d, n, stated, src in ENERGY_ROWS:
        disc = energy_per_bit(fluence=f, spot_diameter=d, spot_shape="disc", pulses=n, ledger="incident") * 1e12
        sq = energy_per_bit(fluence=f, spot_diameter=d, spot_shape="square", pulses=n, ledger="incident") * 1e12
        ab, err = _try(energy_per_bit, fluence=f, spot_diameter=d, spot_shape="disc", pulses=n, ledger="absorbed")
        out.append(f"   {label:<18} {disc:>13.1f} {sq:>12.1f} {'REFUSED' if err else f'{ab * 1e12:.1f}':>10} {stated:>7g}")
        if src != "stated":
            out.append(f"      fluence: {src}")
    out += ["   absorbed: REFUSED because no absorbed fraction is declared in the report.",
            "", "Nothing above measures a barrier or rates a material."]
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        print("barrier_per_bit.py is a library; run: python3 test_barrier_per_bit.py")
        sys.exit(2)
    print(render())
