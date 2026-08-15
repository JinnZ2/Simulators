#!/usr/bin/env python3
"""
gate.py - fail-closed reasoning gate for simulation harnesses.

CC0-1.0. Stdlib only. No network. Python 3.7+.

Default is DENY. A sim that does not declare gets no output;
a quantity that is not tagged is not recorded; a ratio across
unlike objects is void; a claim without named support does not
enter the conclusion.

Usage
-----
    from gate import Gate, Resolution, Control

    g = Gate("SIM-A", guards="guards.json")

    g.pre(
        question   = "does the cascade set share spectral order with AB",
        statistic  = "structure factor S(k), radial average",
        discriminates = "S(k) separates pure-point from diffuse order",
        expected   = "AB: dense point spectrum, many sharp peaks off k=0. "
                     "cascade: flat, S(k)->1",
        resolution = [Resolution("k-grid vs Bragg peak width",
                                 instrument=0.39, feature=0.063)],
        controls   = [Control("periodic lattice",
                              predicted="sharp peaks at reciprocal vectors")],
    )
    ...
    g.record("alpha_tail_AB", -1.529, layer="physical", object_of="AB tiling")
    g.claim("AB is quasi-crystalline", supported_by=["alpha_tail_AB"])
    g.close(observed="only k=0 present; ringing elsewhere")

Any violation raises GateError. Set strict=False to downgrade
post-stage violations to logged findings; pre-stage always denies.
"""

import json
import os
import sys
import datetime

__all__ = ["Gate", "GateError", "Resolution", "Control", "LAYERS"]

LAYERS = ("generator", "physical", "instrument")

_DEFAULT_GUARDS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "guards.json")


class GateError(Exception):
    """Raised when a guard denies. Fail closed."""


class Resolution(object):
    """instrument scale must be finer than the feature it must resolve."""

    def __init__(self, name, instrument, feature, margin=2.0, note=""):
        self.name = name
        self.instrument = float(instrument)
        self.feature = float(feature)
        self.margin = float(margin)
        self.note = note

    def passes(self):
        return self.instrument * self.margin <= self.feature

    def as_dict(self):
        return {
            "name": self.name,
            "instrument_scale": self.instrument,
            "feature_scale": self.feature,
            "margin": self.margin,
            "passes": self.passes(),
            "note": self.note,
        }


class Control(object):
    """named control with a value predicted before the run."""

    def __init__(self, name, predicted, observed=None):
        self.name = name
        self.predicted = predicted
        self.observed = observed

    def as_dict(self):
        return {
            "name": self.name,
            "predicted": self.predicted,
            "observed": self.observed,
            "run": self.observed is not None,
        }


class Gate(object):

    def __init__(self, sim_id, guards=None, strict=True, log_dir="."):
        self.sim_id = sim_id
        self.strict = bool(strict)
        self.log_dir = log_dir
        self.guards = self._load_guards(guards or _DEFAULT_GUARDS)
        self._opened = False
        self._closed = False
        self.declaration = {}
        self.quantities = {}
        self.claims = []
        self.findings = []
        self.voided = []

    # ---------- registry ----------

    def _load_guards(self, path):
        if not os.path.exists(path):
            raise GateError(
                "guard registry not found at %r. gate fails closed: "
                "no registry, no run." % path)
        with open(path, "r") as fh:
            reg = json.load(fh)
        ids = set(g["id"] for g in reg.get("guards", []))
        missing = {"G-RES", "G-CTRL", "G-PRE", "G-LAYER",
                   "G-DIM", "G-SUP", "G-FIT", "G-IND"} - ids
        if missing:
            raise GateError("guard registry incomplete, missing: %s"
                            % ", ".join(sorted(missing)))
        return reg

    def _msg(self, gid):
        for g in self.guards["guards"]:
            if g["id"] == gid:
                return "[%s] %s" % (gid, g["fail_message"])
        return "[%s] denied" % gid

    def _deny(self, gid, detail=""):
        raise GateError(self._msg(gid) + ((" | " + detail) if detail else ""))

    def _soft(self, gid, detail=""):
        entry = {"guard": gid, "detail": detail,
                 "message": self._msg(gid)}
        self.findings.append(entry)
        if self.strict:
            raise GateError(self._msg(gid) +
                            ((" | " + detail) if detail else ""))

    # ---------- PRE ----------

    def pre(self, question, statistic, discriminates, expected,
            resolution, controls, shares_input_with=None):
        """Declare before executing. Denies on any omission. G-RES G-CTRL G-PRE G-FIT"""
        if self._opened:
            raise GateError("pre() already called for %s" % self.sim_id)

        for field, val, gid in (
            ("question", question, "G-PRE"),
            ("statistic", statistic, "G-PRE"),
            ("discriminates", discriminates, "G-FIT"),
            ("expected", expected, "G-PRE"),
        ):
            if not (isinstance(val, str) and val.strip()):
                self._deny(gid, "field %r is empty" % field)

        if not resolution:
            self._deny("G-RES", "no resolution declaration")
        for r in resolution:
            if not isinstance(r, Resolution):
                self._deny("G-RES", "resolution entries must be Resolution")
            if not r.passes():
                self._deny(
                    "G-RES",
                    "%s: instrument %.6g x margin %.6g > feature %.6g"
                    % (r.name, r.instrument, r.margin, r.feature))

        if not controls:
            self._deny("G-CTRL", "no controls declared")
        for c in controls:
            if not isinstance(c, Control):
                self._deny("G-CTRL", "control entries must be Control")
            if not (isinstance(c.predicted, str) and c.predicted.strip()):
                self._deny("G-CTRL",
                           "control %r has no predicted value" % c.name)

        self.declaration = {
            "question": question,
            "statistic": statistic,
            "discriminates": discriminates,
            "expected": expected,
            "resolution": [r.as_dict() for r in resolution],
            "controls": [c.as_dict() for c in controls],
            "shares_input_with": list(shares_input_with or []),
            "declared_at": datetime.datetime.now().isoformat(timespec="seconds"),
        }
        self._controls = list(controls)
        self._opened = True
        return self

    def control_result(self, name, observed):
        """Record what a declared control actually returned."""
        self._require_open()
        for c in self._controls:
            if c.name == name:
                c.observed = observed
                self.declaration["controls"] = [x.as_dict()
                                                for x in self._controls]
                return self
        self._deny("G-CTRL", "control %r was never declared" % name)

    # ---------- MID ----------

    def record(self, name, value, layer, object_of, note=""):
        """Record a quantity. Untagged quantities are not recorded. G-LAYER"""
        self._require_open()
        if layer not in LAYERS:
            self._deny("G-LAYER",
                       "layer %r not in %s" % (layer, list(LAYERS)))
        if not (isinstance(object_of, str) and object_of.strip()):
            self._deny("G-LAYER",
                       "quantity %r declares no object_of" % name)
        if name in self.quantities:
            raise GateError("quantity %r already recorded" % name)
        self.quantities[name] = {
            "value": value,
            "layer": layer,
            "object_of": object_of.strip(),
            "note": note,
        }
        return self

    def promote(self, name, new_name, to_layer, justification):
        """Explicit layer promotion. No silent generator -> physical."""
        self._require_open()
        if name not in self.quantities:
            self._deny("G-LAYER", "unknown quantity %r" % name)
        if to_layer not in LAYERS:
            self._deny("G-LAYER", "layer %r not in %s" % (to_layer, list(LAYERS)))
        if not (isinstance(justification, str) and len(justification.strip()) >= 20):
            self._deny("G-LAYER",
                       "promotion of %r needs a substantive justification" % name)
        src = self.quantities[name]
        self.quantities[new_name] = {
            "value": src["value"],
            "layer": to_layer,
            "object_of": src["object_of"],
            "note": "promoted from %s (%s): %s" % (name, src["layer"],
                                                   justification.strip()),
        }
        return self

    # ---------- POST ----------

    def ratio(self, name, numerator, denominator, note=""):
        """Admissible only if both operands are properties of one object. G-DIM"""
        self._require_open()
        for q in (numerator, denominator):
            if q not in self.quantities:
                self._deny("G-DIM", "unknown quantity %r" % q)
        a = self.quantities[numerator]
        b = self.quantities[denominator]
        if a["object_of"] != b["object_of"]:
            self.voided.append({
                "name": name,
                "numerator": numerator, "numerator_object": a["object_of"],
                "denominator": denominator, "denominator_object": b["object_of"],
            })
            self._soft("G-DIM",
                       "%s: %r is a property of %r, %r is a property of %r"
                       % (name, numerator, a["object_of"],
                          denominator, b["object_of"]))
            return None
        try:
            val = float(a["value"]) / float(b["value"])
        except (TypeError, ValueError, ZeroDivisionError) as exc:
            self._deny("G-DIM", "%s not computable: %s" % (name, exc))
        self.quantities[name] = {
            "value": val,
            "layer": a["layer"],
            "object_of": a["object_of"],
            "note": ("ratio %s / %s. " % (numerator, denominator)) + note,
        }
        return val

    def claim(self, text, supported_by):
        """A claim names the recorded quantities that support it. G-SUP"""
        self._require_open()
        supported_by = list(supported_by or [])
        if not supported_by:
            self.claims.append({"text": text, "supported_by": [],
                                "status": "unsupported"})
            self._soft("G-SUP", text)
            return self
        unknown = [q for q in supported_by if q not in self.quantities]
        if unknown:
            self.claims.append({"text": text, "supported_by": supported_by,
                                "status": "unsupported"})
            self._soft("G-SUP",
                       "%s | not recorded: %s" % (text, ", ".join(unknown)))
            return self
        layers = sorted(set(self.quantities[q]["layer"] for q in supported_by))
        self.claims.append({
            "text": text,
            "supported_by": supported_by,
            "support_layers": layers,
            "status": "supported",
        })
        return self

    def convergence(self, across, shared):
        """Assert convergence only after naming what is shared. G-IND"""
        self._require_open()
        if not shared:
            self._soft("G-IND",
                       "convergence across %s with nothing named as shared"
                       % ", ".join(across))
            return self
        self.claims.append({
            "text": "convergence across %s" % ", ".join(across),
            "shared": list(shared),
            "status": "qualified",
        })
        return self

    def close(self, observed, write=True):
        """Compare observed against the pre-registered expectation."""
        self._require_open()
        if self._closed:
            raise GateError("gate already closed")
        if not (isinstance(observed, str) and observed.strip()):
            self._deny("G-PRE", "close() requires an observed summary")

        unrun = [c.name for c in self._controls if c.observed is None]
        if unrun:
            self._soft("G-CTRL",
                       "declared but never run: %s" % ", ".join(unrun))

        gen_only = [n for n, q in self.quantities.items()
                    if q["layer"] == "generator"]

        report = {
            "sim_id": self.sim_id,
            "strict": self.strict,
            "guards_schema": self.guards.get("schema_version"),
            "declaration": self.declaration,
            "expected": self.declaration.get("expected"),
            "observed": observed.strip(),
            "quantities": self.quantities,
            "generator_level_quantities": sorted(gen_only),
            "voided_ratios": self.voided,
            "claims": self.claims,
            "findings": self.findings,
            "closed_at": datetime.datetime.now().isoformat(timespec="seconds"),
        }
        self._closed = True
        if write:
            path = os.path.join(self.log_dir, "gate_%s.json" % self.sim_id)
            with open(path, "w") as fh:
                json.dump(report, fh, indent=2, default=str)
            report["_path"] = path
        return report

    # ---------- helpers ----------

    def _require_open(self):
        if not self._opened:
            self._deny("G-PRE", "pre() has not been called: nothing may run")
        if self._closed:
            raise GateError("gate is closed")

    def summary(self, report):
        L = []
        L.append("GATE %s" % report["sim_id"])
        L.append("  expected : %s" % report["expected"])
        L.append("  observed : %s" % report["observed"])
        for c in report["declaration"]["controls"]:
            L.append("  control  : %-28s %s"
                     % (c["name"], "run" if c["run"] else "NOT RUN"))
        for r in report["declaration"]["resolution"]:
            L.append("  resolve  : %-28s %s"
                     % (r["name"], "ok" if r["passes"] else "FAIL"))
        if report["generator_level_quantities"]:
            L.append("  generator-level (no physical claim permitted): %s"
                     % ", ".join(report["generator_level_quantities"]))
        for v in report["voided_ratios"]:
            L.append("  VOID     : %s (%s vs %s)"
                     % (v["name"], v["numerator_object"],
                        v["denominator_object"]))
        for c in report["claims"]:
            L.append("  claim    : [%s] %s" % (c["status"], c["text"]))
        for f in report["findings"]:
            L.append("  finding  : %s" % f["message"])
        return "\n".join(L)


if __name__ == "__main__":
    g = Gate("SELFTEST", guards=os.environ.get("GUARDS", _DEFAULT_GUARDS))
    try:
        g.record("x", 1.0, "physical", "thing")
    except GateError as e:
        print("fails closed before pre(): %s" % e)
    print("guards loaded: %d" %
          len(g.guards["guards"]))
    sys.exit(0)
