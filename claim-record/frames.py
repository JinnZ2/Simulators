#!/usr/bin/env python3
"""
frames -- transforms as first-class objects, and no privileged frame.

    frames.py list                  the registered transforms
    frames.py convert 3 years sols  one quantity, read in another frame
    frames.py --acceptance          add a frame, check no record moves
    frames.py --selftest

THREE PRINCIPLES, stated plainly because the file is the place for them.

  1. NO PRIVILEGED FRAME. The format does not treat any frame as the
     default, including the one every current record uses. `years` is a
     registered transform like any other; nothing falls back to it, and
     a unit that is not registered is an error rather than an
     assumption.

  2. TRANSFORMS ARE FIRST-CLASS OBJECTS. They live in frames/ as
     versioned records beside the claims, not as conversion code inside
     an application. Adding a frame is adding a file.

  3. DERIVED AT READ TIME, NEVER AT WRITE TIME. A stored duration is a
     cached conversion, and caching the conversion is what makes it
     legacy. Nothing here writes a converted value back; every reading
     is computed from the record and the registry at the moment it is
     read.

THE ACCEPTANCE TEST. Add a second frame with a different rate, and no
existing record needs editing. If any record needs editing, the frame
leaked into the data. `--acceptance` runs it, and runs a positive
control beside it, because a test that adds a frame nothing reads would
pass on a format that had leaked everywhere.

THE REASONING, verbatim from the order:

    this is being specified before it's needed because retrofit cost is
    the entire reason the fold detector exists. Building the fold in
    now, knowing it's a fold, would be the same error the tool was
    written to find.

CC0. stdlib only. Parses under Python 3.9. ASCII only.
"""

import datetime
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.join(HERE, "frames")

# The base is a choice and it is declared, not assumed. Every duration
# frame states how many base units one of its units is; every rate frame
# names the duration frame it is the reciprocal of. A frame that named
# no base would be a privileged frame wearing a unit string.
BASE = {"duration": "second", "rate": "per_second", "instant": "second"}


class UnknownFrame(Exception):
    """A unit with no registered transform. Never resolved by default."""


class Registry(object):
    def __init__(self, frames=None):
        self.frames = dict(frames or {})

    @classmethod
    def load(cls, directory=None):
        out = {}
        for fn in sorted(glob.glob(os.path.join(directory or FRAMES,
                                                "*.json"))):
            f = json.load(open(fn))
            out[f["unit"]] = f
        return cls(out)

    def add(self, frame):
        """Adding a frame is adding an object, in code or in a file."""
        self.frames[frame["unit"]] = frame
        return self

    def get(self, unit, quantity=None):
        f = self.frames.get(unit)
        if f is None:
            raise UnknownFrame(
                "%r has no registered transform. Add frames/<unit>.json; "
                "nothing here falls back to a default frame." % unit)
        if quantity and f.get("quantity") != quantity:
            raise UnknownFrame(
                "%r is a %s frame and a %s was asked for"
                % (unit, f.get("quantity"), quantity))
        return f

    def units(self, quantity=None):
        return sorted(u for u, f in self.frames.items()
                      if quantity is None or f.get("quantity") == quantity)

    # -- durations and rates -------------------------------------------

    def _seconds_per(self, unit):
        f = self.get(unit, "duration")
        return float(f["base_per_unit"])

    def to_base(self, value, unit):
        """One quantity, expressed in base units. Never stored."""
        f = self.get(unit)
        q = f["quantity"]
        if q == "duration":
            return float(value) * self._seconds_per(unit)
        if q == "rate":
            return float(value) / self._seconds_per(f["reciprocal_of_unit"])
        if q == "dimensionless":
            return float(value)
        if q == "instant":
            return self._instant_to_base(value, f)
        raise UnknownFrame("no rule for quantity %r" % q)

    def from_base(self, value, unit):
        f = self.get(unit)
        q = f["quantity"]
        if q == "duration":
            return float(value) / self._seconds_per(unit)
        if q == "rate":
            return float(value) * self._seconds_per(f["reciprocal_of_unit"])
        if q == "dimensionless":
            return float(value)
        if q == "instant":
            return self._instant_from_base(value, f)
        raise UnknownFrame("no rule for quantity %r" % q)

    def convert(self, value, unit_in, unit_out):
        return self.from_base(self.to_base(value, unit_in), unit_out)

    # -- instants ------------------------------------------------------
    #
    # A calendar is a frame too. Its transform is named by the frame
    # object and looked up here, so swapping the object swaps the
    # implementation; an unregistered impl is an error, not a default.

    def _impl(self, f):
        name = f.get("impl")
        if name not in CALENDARS:
            raise UnknownFrame(
                "calendar implementation %r is not registered" % name)
        return CALENDARS[name]

    def _instant_to_base(self, value, f):
        return self._impl(f)[0](value, f)

    def _instant_from_base(self, value, f):
        return self._impl(f)[1](value, f)


def _greg_to_base(value, f):
    d = datetime.date.fromisoformat(str(value))
    e = datetime.date.fromisoformat(str(f["epoch"]))
    return (d - e).days * 86400.0


def _greg_from_base(value, f):
    e = datetime.date.fromisoformat(str(f["epoch"]))
    return (e + datetime.timedelta(seconds=float(value))).isoformat()


CALENDARS = {"proleptic_gregorian_date": (_greg_to_base, _greg_from_base)}


# ---------------------------------------------------------------- render

def table(headers, rows):
    w = [len(h) for h in headers]
    body = [[str(x) for x in r] for r in rows]
    for r in body:
        for i, c in enumerate(r):
            w[i] = max(w[i], len(c))
    fmt = "  ".join("%-" + str(x) + "s" for x in w)
    out = [fmt % tuple(headers), fmt % tuple("-" * x for x in w)]
    for r in body:
        out.append((fmt % tuple(r)).rstrip())
    return "\n".join(out)


def render_list(reg):
    rows = []
    for u in reg.units():
        f = reg.frames[u]
        rate = f.get("base_per_unit")
        if f["quantity"] == "rate":
            rate = "1 / %s" % f.get("reciprocal_of_unit")
        rows.append([u, f["quantity"], f.get("version", "-"),
                     rate if rate is not None else "-",
                     (f.get("basis") or "")[:52]])
    return "\n".join([
        "registered transforms",
        "base: %s" % ", ".join("%s -> %s" % kv for kv in sorted(BASE.items())),
        "",
        "No unit here is the default. An unregistered unit raises;",
        "nothing resolves by assumption.",
        "",
        table(["unit", "quantity", "version", "base per unit", "basis"], rows)])


# ------------------------------------------------------- acceptance test

# Deliberately NOT one of the files in frames/. The test adds a frame
# that does not exist on disk, because adding one that is already
# registered tests nothing.
SECOND_FRAME = {
    "id": "venus_solar_day",
    "version": "1.0.0",
    "quantity": "duration",
    "unit": "venus_days",
    "base": "second",
    "base_per_unit": 10087200.0,
    "basis": "one Venus mean solar day, about 116.75 Earth days in SI "
             "seconds. Chosen for the acceptance test because its rate "
             "differs from every registered frame and shares no factor "
             "with them, and because nothing in the repository has any "
             "reason to want it.",
}


def acceptance(records_dir=None, derive=None, validate=None, verbose=False):
    """Add a second frame with a different rate; no record may need editing.

    Returns a dict. `derive` and `validate` are injected so the same test
    can be run against a deliberately leaked implementation, which is the
    positive control: a test that adds a frame nothing reads would pass
    on a format that had leaked everywhere.
    """
    import hashlib
    records_dir = records_dir or os.path.join(HERE, "records")
    files = sorted(glob.glob(os.path.join(records_dir, "*.json")))
    before = {f: hashlib.sha256(open(f, "rb").read()).hexdigest()
              for f in files}

    reg = Registry.load()
    had = SECOND_FRAME["unit"] in reg.frames
    reg.add(SECOND_FRAME)

    states, errors = {}, []
    for f in files:
        rec = json.load(open(f))
        cid = rec.get("id", os.path.basename(f))
        try:
            if validate:
                st, findings = validate(rec, reg)
                states[cid] = st
                if findings:
                    errors.append((cid, [str(x) for x in findings]))
            if derive:
                derive(rec, reg)
        except Exception as exc:                      # noqa: BLE001
            errors.append((cid, ["%s: %s" % (type(exc).__name__, exc)]))
            states[cid] = "RAISED"

    after = {f: hashlib.sha256(open(f, "rb").read()).hexdigest()
             for f in files}
    edited = [os.path.basename(f) for f in files if before[f] != after[f]]

    return {"records": len(files),
            "frame_added": SECOND_FRAME["unit"],
            "frame_was_already_registered": had,
            "edited": edited,
            "states": states,
            "errors": errors,
            "passes": not edited and not errors}


# ---------------------------------------------------------------- selftest

def _selftest():
    fails = []

    def ck(name, got, want):
        ok = got == want
        if not ok:
            fails.append(name)
        print("  %-56s %-4s got=%r want=%r"
              % (name, "PASS" if ok else "FAIL", got, want))

    def close(name, got, want, tol=1e-9):
        ok = got is not None and abs(got - want) <= tol
        if not ok:
            fails.append(name)
        print("  %-56s %-4s got=%r want=%r"
              % (name, "PASS" if ok else "FAIL", got, want))

    print("frames selftest")
    reg = Registry.load()
    ck("duration frames are registered", "years" in reg.units("duration"),
       True)
    ck("and so is the one nothing here uses", "sols" in reg.units("duration"),
       True)

    close("a year in base units", reg.to_base(1, "years"), 31556952.0)
    close("a day in base units", reg.to_base(1, "days"), 86400.0)
    close("round trip", reg.convert(3.0, "years", "years"), 3.0)
    close("years to days", reg.convert(1.0, "years", "days"), 365.2425)
    close("a rate is the reciprocal of its duration frame",
          reg.to_base(1.0, "per_year"), 1.0 / 31556952.0)

    # Principle 1, enforced: an unregistered unit is an error.
    try:
        reg.to_base(1, "fortnights")
        ck("an unregistered unit raises rather than defaulting", False, True)
    except UnknownFrame:
        ck("an unregistered unit raises rather than defaulting", True, True)
    try:
        reg.get("years", "rate")
        ck("a unit of the wrong quantity raises", False, True)
    except UnknownFrame:
        ck("a unit of the wrong quantity raises", True, True)

    # Principle 2: adding a frame is adding an object.
    r2 = Registry.load().add({"id": "x", "version": "1.0.0",
                              "quantity": "duration", "unit": "fortnights",
                              "base": "second", "base_per_unit": 1209600.0,
                              "basis": "fourteen days"})
    close("a frame added at run time resolves",
          r2.convert(1.0, "fortnights", "days"), 14.0)

    # Instants are a frame too, and the calendar is named by the object.
    close("an instant converts to base", reg.to_base("1970-01-02", "iso_date"),
          86400.0)
    ck("and back", reg.from_base(86400.0, "iso_date"), "1970-01-02")
    try:
        Registry({"bad": {"quantity": "instant", "unit": "bad",
                          "impl": "nope", "epoch": "1970-01-01"}}
                 ).to_base("1970-01-02", "bad")
        ck("an unregistered calendar raises", False, True)
    except UnknownFrame:
        ck("an unregistered calendar raises", True, True)

    # The acceptance test, run here too so it is part of the suite in
    # both directions rather than a command someone remembers.
    import record
    rep = record.acceptance_report()
    ck("the acceptance test passes", "PASSES" in rep, True)
    ck("the frame it adds is not one on disk",
       SECOND_FRAME["unit"] in Registry.load().frames, False)

    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if "--acceptance" in argv:
        import record
        res = record.acceptance_report()
        print(res)
        return 0 if "PASSES" in res else 1
    if len(argv) > 1 and argv[1] == "list":
        print(render_list(Registry.load()))
        return 0
    if len(argv) > 4 and argv[1] == "convert":
        reg = Registry.load()
        print("%g %s = %g %s" % (float(argv[2]), argv[3],
                                 reg.convert(float(argv[2]), argv[3], argv[4]),
                                 argv[4]))
        return 0
    print(__doc__.strip().split("CC0")[0])
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
