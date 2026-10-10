# Landauer floor vs run cost

CC0. A reusable reasoning move, not a description of any person.

Companions: `tools/uncounted_observer_isolation.md` (the isolation
ledger) and `tools/contested_area_hidden_assumption.md` (the welded-word
and boundary checks).

This is a WORKED SPECIMEN of the isolation ledger, not a new law.

## 1. Principle

Landauer's principle gives a real, tested minimum energy to erase one
bit:

    kT ln 2  =  1.380649e-23 J/K x 300 K x 0.6931
             =  2.87e-21 J per bit, about 3e-21 J at room temperature

It is an EQUILIBRIUM, quasi-static bound: the cost in the slow limit, at
thermal equilibrium with the bath.

It was imported into computer-science theory as if it were the cost to
RUN computation. It is not.

## 2. The welded word: "cost"

One word, three referents:

    1. equilibrium floor     kT ln 2 per bit; slow limit, isolated bit
    2. actual run cost       what a real far-from-equilibrium machine
                             dissipates
    3. in-principle bound    the lowest cost for a given computation

The floor's authority (it is a real theorem) gets borrowed to anchor the
run-cost claim.

## 3. The isolation error

The floor prices a single bit erased slowly, at equilibrium. Real
computation holds the system far from equilibrium, drives it hard, and
pays continuously to keep it there.

This is the same move as the thermos: true for a thing that is not real
(the infinitely slow computer), false for every actual one.

## 4. The gap, measured

This is the housekeeping cost, quantified. Ratios are actual dissipation
per bit operation over the floor, carried as relayed and not checked
here:

    1970s silicon      ~1e9 x the floor
    current CMOS       ~1e6 x the floor
    3 nm (2025)        ~1e2 x the floor

The sources name the gap as:

    parasitic resistance
    capacitive switching losses
    charge / discharge
    voltage overhead

All four are the price of running off equilibrium. The gap IS the
housekeeping term (axis 3, THE HOLD) from the isolation ledger.

## 5. Confessed in the literature: the keystone

There is a bound for the single bit in isolation (Landauer) and NO bound
for the system as a whole while it runs. The field explicitly wishes for
a Carnot-style limit for whole computers and states that it does not
exist.

That missing result is the wall. The coupled-system number cannot be
obtained by pricing one decoupled component at equilibrium.

## 6. Checks applied (isolation ledger, four checks)

    1. boundary   one bit, cut out of the machine that holds it
    2. lift       the energy that holds the machine far from equilibrium
                  is not in the floor
    3. hold       the continuous dissipation (section 4) is the uninvoiced
                  term
    4. observer   the readout and clocking that make the bit usable are
                  couplings, not neutral

## 7. Propagation note

A real theorem with the wrong scope was imported from the corpus and
built on for years, until a correction had to be published (stochastic
thermodynamics of computation). It travels because the floor LOOKS
authoritative, so nobody checks which limit it lives in.

This is the second documented propagation specimen, alongside the
isolated-system definition in `tools/uncounted_observer_isolation.md`.

## Provenance

Co-authored, written from a worked session. The kT ln 2 arithmetic is
recomputed here; the gap ratios and literature statements are carried as
relayed, not checked against sources. A split into smaller files is
permitted if this one runs long.
