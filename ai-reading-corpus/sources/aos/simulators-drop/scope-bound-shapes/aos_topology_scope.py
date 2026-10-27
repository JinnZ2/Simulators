"""CC0. AOS stripe-domain law, run as a scope-bound shape.

The 2026 UCSD vector-beam study filed stripe-domain formation at N>=10 as
"a magnetostatic law, no beam geometry composes around it." Run through
this instrument, the law is a scope binding whose load-bearing variable -
film topology - the study never declared. The recording-media tradition
froze the opposite topology decades ago, and AO-HDS was demonstrated in
that binding in 2014 (Lambert et al., Science 345, 1337).
"""
from scope import Shape, Binding, compare, infer_frozen, universe

shape = Shape(
    "energy-balance domain selection",
    ["deposit energy", "quench magnetic order",
     "reorganize domains under competing energy terms",
     "cool and freeze pattern", "select final domain configuration"],
    "whichever energy term dominates at the reorganization step selects "
    "the frozen domain pattern: dipolar vs anisotropy in a connected "
    "film, per-grain thermal activation vs collective wall motion in a "
    "decoupled one")

# The UCSD study, as filed. Film topology is in NEITHER list: the paper
# never declares it. That omission is the finding.
aos2026 = Binding(
    "aos_2026_continuous_ptco",
    live=["pulse fluence", "focal spot diameter", "beam helicity",
          "pulse count", "number of bilayers N"],
    frozen=["material composition (Pt/Co family)",
            "pulse duration (120 fs)", "wavelength (800 nm)"],
    declared_by="Khalid et al., Nat Commun 17, 10843 (2026), as filed in "
                "constraint-assembly/aos-vector-beam")
shape.bind(aos2026)

# The recording-media binding of the same shape. Topology is the frozen
# design variable, declared out loud for fifty years.
hamr = Binding(
    "granular_fept_hamr",
    live=["pulse fluence", "beam helicity", "pulse count",
          "mean grain diameter", "matrix chemistry (C vs AgC)"],
    frozen=["film topology (granular, exchange-decoupled)"],
    declared_by="Lambert et al., Science 345, 1337 (2014); behind them "
                "the perpendicular-recording media tradition (Iwasaki "
                "1976; CoCrPt-oxide granular media)")
shape.bind(hamr)

print("VARIABLE: film topology")
print("  aos_2026_continuous_ptco  %s" % aos2026.state_of("film topology (granular, exchange-decoupled)"))
print("  granular_fept_hamr        %s" % hamr.state_of("film topology (granular, exchange-decoupled)"))
print()
r = compare(aos2026, hamr)
print("COMPARE", r.get("verdict", r))
for k in sorted(r):
    if k not in ("verdict",):
        print("  %-28s %s" % (k, r[k]))
print()
print("INFER_FROZEN refuses, and prints what it would have said:")
print(infer_frozen(aos2026, hamr))
