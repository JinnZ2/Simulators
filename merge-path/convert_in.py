#!/usr/bin/env python3
"""convert_in.py -- IN direction: a target registrar's record -> a
falsifier-format record. §2's first direction. The likely loss is the
provenance graph structure, the enforcement status, the uncertainty
budget, and the legal or institutional standing of the record -- none of
which our format has a slot for.

A real registrar is NOT-IMPLEMENTED (spec unfetched, egress refused). The
mocks invert their own slot maps. Stdlib only, parses under 3.9.
"""

from registrars import Registrar


def convert_in(target, reg):
    """(record, residual). Inverts the registrar's slot map. A target
    field with no falsifier slot is DROPPED (registrar-native: provenance,
    enforcement, uncertainty budget -- our format has no home for it)."""
    if not reg.implemented:
        return ({"status": "NOT-IMPLEMENTED", "registrar": reg.name},
                [{"field": "*", "class": "NOT-IMPLEMENTED", "detail": reg.reason}])
    if isinstance(target, dict) and target.get("status") == "NOT-IMPLEMENTED":
        return ({"status": "NOT-IMPLEMENTED", "registrar": reg.name},
                [{"field": "*", "class": "NOT-IMPLEMENTED", "detail": "target was a NOT-IMPLEMENTED marker"}])
    record = {}
    residual = []
    inv = {slot.target_name: (f, slot) for f, slot in reg.slots.items()}
    for tname, tval in target.items():
        if tname in inv:
            f, slot = inv[tname]
            record[f] = tval
            if slot.meaning == "different":
                residual.append({"field": f, "class": "COERCED",
                                 "detail": "read back from slot %r, which means something else than %r" % (tname, f)})
        else:
            residual.append({"field": tname, "class": "DROPPED",
                             "detail": "registrar-native field (provenance / enforcement / uncertainty), no falsifier slot"})
    return record, residual


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv[1:]:
        print("convert_in has no selftest; run selftest.py", file=sys.stderr)
        sys.exit(2)
    print("convert_in.py -- import and call; run selftest.py for the checks", file=sys.stderr)
    sys.exit(2)
