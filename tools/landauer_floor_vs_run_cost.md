# Landauer floor vs run cost

CC0. A reusable reasoning move, not a description of any person.

Companions: `tools/uncounted_observer_isolation.md` (the isolation
ledger) and `tools/contested_area_hidden_assumption.md` (the welded-word
and boundary checks).

This is a WORKED SPECIMEN of the isolation ledger, not a new law.

Tags: OBSERVED = stated in a source; DERIVED = follows from what is
stated here; PROPOSED = a reading not yet backed by a cited instance.

## 1. Principle

[OBSERVED] Landauer: the minimum energy to erase one bit is kT ln 2,
about 3e-21 J at room temperature. It was confirmed experimentally
(Berut et al., Nature 2012).

    kT ln 2 = 1.380649e-23 J/K x 300 K x 0.6931
            = 2.87e-21 J = 17.9 meV        (recomputed here)

It is an EQUILIBRIUM, quasi-static bound: the cost in the slow limit, at
thermal equilibrium with the bath.

[PROPOSED] It gets used in CS energy-complexity reasoning as if it were
the cost to RUN computation. Citation for specific misuse cases OWED.

## 2. The welded word: "cost"

One word, three referents:

    1. equilibrium floor     kT ln 2 per bit; slow limit, isolated bit
    2. actual run cost       what a real far-from-equilibrium machine
                             dissipates
    3. in-principle bound    the lower bound for a given whole computation

[DERIVED] The floor's authority (a real, tested theorem) gets borrowed
to anchor the run-cost claim.

## 3. The isolation error

[DERIVED] The floor prices one bit erased slowly, at equilibrium. Real
computation is a coupled system driven fast and far from equilibrium,
paying continuously to stay there. This is the same move as the
thermos: true for a thing that is not real (the infinitely slow
computer), false for every actual one.

## 4. The gap, measured: the housekeeping term

    [OBSERVED] 1970s transistor:    ~1e9 x the floor
    [OBSERVED] current transistors: ~1e6 x the floor
                                    (pJ to fJ per operation vs ~3e-21 J)
    [OBSERVED] one first-principles estimate puts maximum CMOS
               efficiency ~200x better than current chips, so even the
               projected CMOS ceiling sits far above the floor

[OBSERVED] Sources name the gap:

    parasitic resistance
    capacitive switching
    charge / discharge
    voltage overhead
    interconnect
    leakage

[DERIVED] These are the costs of running off equilibrium: the
housekeeping term (axis 3, THE HOLD) of the isolation ledger.

## 5. Keystone: stated in the literature

[OBSERVED] A chapter on the minimum energy of computing states that
there are no theoretical results characterizing the maximum efficiency
of a computing system as a whole, and that a Carnot-style limit for
computers would be important. A bound exists for the isolated bit; none
exists for the coupled running system.

[DERIVED] That missing result is the wall. The coupled-system number
cannot be obtained by pricing one decoupled component at equilibrium.

## 6. Propagation note

[PROPOSED] A real theorem with the wrong scope is carried by its
authority, so nobody checks which limit it lives in. This is the second
propagation specimen, next to the isolated-system definition in
`tools/uncounted_observer_isolation.md`.

OWED:

    1. specific papers that use the floor as the run cost
    2. the stochastic-thermodynamics-of-computation correction
       literature (Wolpert et al.; verify before citing)

## Provenance

Co-authored, written from a worked session. The kT ln 2 arithmetic is
recomputed here. Sources tagged OBSERVED are carried as relayed and were
not re-read in this render. A split into smaller files is permitted if
this one runs long.
