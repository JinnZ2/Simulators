#!/usr/bin/env python3
"""convert_out.py -- OUT direction: a falsifier-format record -> a target
registrar's record. §2's second direction. The likely loss is the
falsifier itself where the target has no slot, the cut on the units, and
the whole branch record.

A real registrar here is NOT-IMPLEMENTED (its spec was not fetched --
egress refused, see registrars.py), and convert_out returns a
NOT-IMPLEMENTED marker with that reason rather than guessing a mapping. A
stub with a reason beats a converter that guesses (§6). The mock
registrars are declared test doubles that exercise each residual class.
Stdlib only, parses under 3.9.
"""

from registrars import FALSIFIER_FIELDS, ConversionFailure


def _flatten(d):
    """A dict collapsed to a human-recoverable string (FLATTENED)."""
    return "; ".join("%s=%s" % (k, d[k]) for k in sorted(d))


def _present(v):
    return v not in (None, "", {}, [])


def convert_out(record, reg):
    """(target, residual). residual is a field list, each entry
    {field, class, detail[, origin]}, class in DROPPED/FLATTENED/COERCED/
    ADDED. Raises ConversionFailure for an ADDED field with no origin."""
    if not reg.implemented:
        return ({"status": "NOT-IMPLEMENTED", "registrar": reg.name},
                [{"field": "*", "class": "NOT-IMPLEMENTED", "detail": reg.reason}])
    target = {}
    residual = []
    for f in FALSIFIER_FIELDS:
        if f not in record or not _present(record[f]):
            continue
        val = record[f]
        slot = reg.slots.get(f)
        if slot is None:
            residual.append({"field": f, "class": "DROPPED",
                             "detail": "no target slot in %s" % reg.name})
            continue
        tv = val
        if slot.flatten and isinstance(val, dict):
            tv = _flatten(val)
            residual.append({"field": f, "class": "FLATTENED",
                             "detail": "dict collapsed to a string in slot %r (human-recoverable)" % slot.target_name})
        if slot.meaning == "different":
            residual.append({"field": f, "class": "COERCED",
                             "detail": "written into slot %r, which the target declares to mean something else" % slot.target_name})
        target[slot.target_name] = tv
    filled = set(target)
    for req in reg.requires:
        if req in filled:
            continue
        origin = reg.added_origins.get(req)
        if not origin:
            raise ConversionFailure(
                "ADDED field %r required by %s has no stated origin; conversion fails (§3, S4)"
                % (req, reg.name))
        target[req] = "<ADDED: %s>" % origin
        residual.append({"field": req, "class": "ADDED",
                         "detail": "required by %s, not in the source" % reg.name, "origin": origin})
    return target, residual


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv[1:]:
        print("convert_out has no selftest; run selftest.py", file=sys.stderr)
        sys.exit(2)
    print("convert_out.py -- import and call; run selftest.py for the checks", file=sys.stderr)
    sys.exit(2)
