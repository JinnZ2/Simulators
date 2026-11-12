"""FP / TP classes for the known-answer gate. No imports, so the repo registry
(tools/known_answer.py) can load it by path. PASS needs FP == 0 and TP == 1 exactly:
a gate that recovers half its planted defects is not a pass."""


def harness_class(fp, tp):
    if fp == 1.0 and tp == 1.0:
        return "CONSTANT_FIRES"
    if fp == 0.0 and tp == 0.0:
        return "CONSTANT_SILENT"
    if fp > 0.0 and tp <= fp:
        return "NO_DISCRIMINATION"
    if fp > 0.0:
        return "FALSE_ALARMS"
    if tp < 1.0:
        return "MISSES_PLANTED_DEFECTS"
    return "PASS"
