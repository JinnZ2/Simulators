#!/usr/bin/env python3
"""P4 -- goal-coherence check. No input. A goal is pursued by a chain of
steps three ways and the trace is emitted as a table:

    accept   each step takes the prior step's output as given
    correct  each step takes the prior output as INPUT, tests it
             against an invariant, and replaces a value that fails it
    contest  each step treats the prior output as adversarial input,
             refuses it, and re-derives from the premise

The goal here is a program's goal (reach 2^N by doubling), not a
model's: what runs is a construction, and the trace is of that. The
cut the order asks to be named is the `stance` column: correction
CONSUMES the prior output and terminates; contestation REFUSES it and
does not. Refuses --selftest (checks live in selftest_v2.py).
"""

import json
import sys

N = 10
BUDGET = 60
PREMISE = 1
PERTURB_AT = 5          # the correct-mode chain has one planted upstream slip


def step(value):
    return value * 2


def invariant_ok(k, value):
    return value == PREMISE * 2 ** k


def run(mode, n=N, budget=BUDGET):
    trace = []
    k, value, ticks = 0, PREMISE, 0
    while ticks < budget:
        ticks += 1
        prior = value
        if mode == "accept":
            stance, used, value = "accept", pr