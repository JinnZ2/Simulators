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
                                 instrument=0.020, feature=0.063)],
        controls   = [Control("periodic lattice",
                              predicted="sharp peaks at reciprocal vectors")],
    )
    ...
    g.control_result("periodic lattice", "peaks resolved at 2*pi*m/a")
    g.record("alpha_tail_AB", -1.529, layer="physical", object_of="AB tiling")
    g.claim("AB is quasi-crystalline", supported_by=["alpha_tail_AB"])
    g.close(observed="only k=0 present; ringing elsewhere", diverged=True)

DENIAL EXAMPLE -- this is what SIM-A actually declared:

    Resolution("k-grid vs Bragg peak width", instrument=0.39, feature=0.063)

    0.39 * 2.0 > 0.063, so G-RES denies at pre() and the sim never runs.
    The grid is 6x coarser than the peaks it must resolve, so its null
    carries no information. Do not copy those numbers into a run you
    expect to execute; they are here because they are the failure.

Any violation raises GateError. Set strict=False to downgrade
post-stage violations to logged findings; pre-stage always denies.

Every denial writes gate_<SIM>.denied.json before raising, so a run
that was stopped leaves a record. Without it the guards that work are
invisible to any tool that mines the logs.
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
        entries = reg.get("guards", [])
        ids = set(g["id"] for g in entries)
        missing = {"G-RES", "G-CTRL", "G-PRE", "G-LAYER",
                   "G-DIM", "G-SUP", "G-FIT", "G-IND"} - ids
        if missing:
            raise GateError("guard registry incomplete, missing: %s"
                            % ", ".join(sorted(missing)))
        # Every guard must carry the message it denies with. Checking only
        # the ids lets a malformed registry load and then raise KeyError at
        # the moment a guard fires -- open at load, crashing at denial,
        # which is the wrong order for a fail-closed tool.
        mute = sorted(g["id"] for g in entries
                      if not str(g.get("fail_message", "")).strip())
        if mute:
            raise GateError(
                "guard registry unusable, no fail_message for: %s"
                % ", ".join(mute))
        return reg

    def _msg(self, gid):
        for g in self.guards["guards"]:
            if g["id"] == gid:
                return "[%s] %s" % (gid, g["fail_message"])
        return "[%s] denied" % gid

    def _write(self, report, suffix=""):
        """Write a run record. Returns the path, or None if writing failed."""
        if not self.log_dir:
            return None
        path = os.path.join(self.log_dir, "gate_%s%s.json" % (self.sim_id, suffix))
        try:
            os.makedirs(self.log_dir, exist_ok=True)
            with open(path, "w") as fh:
                json.dump(report, fh, indent=2, default=str)
        except (OSError, TypeError, ValueError):
            return None
        return path

    def _denial_record(self, gid, detail):
        return {
            "sim_id": self.sim_id,
            "outcome": "DENIED",
            "denied_by": gid,
            "detail": detail,
            "message": self._msg(gid),
            "strict": self.strict,
            "guards_schema": self.guards.get("schema_version"),
            "declaration": self.declaration,
            "expected": self.declaration.get("expected"),
            "observed": None,
            "quantities": self.quantities,
            "generator_level_quantities": sorted(
                n for n, q in self.quantities.items()
                if q["layer"] == "generator"),
            "voided_ratios": self.voided,
            "claims": self.claims,
            "findings": self.findings,
            "denied_at": datetime.datetime.now().isoformat(timespec="seconds"),
        }

    def _deny(self, gid, detail=""):
        """Record the denial, then raise. A stopped run still leaves a log."""
        self._write(self._denial_record(gid, detail), suffix=".denied")
        raise GateError(self._msg(gid) + ((" | " + detail) if detail else ""))

    def _note(self, gid, detail=""):
        """Record a finding without denying. Used where a guard downgrades a
        claim rather than refusing it -- the G-IND 'qualified' shape."""
        self.findings.append({"guard": gid, "detail": detail,
                              "message": self._msg(gid)})

    def _soft(self, gid, detail=""):
        entry = {"guard": gid, "detail": detail,
                 "message": self._msg(gid)}
        self.findings.append(entry)
        if self.strict:
            self._deny(gid, detail)

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
        if observed is None or not str(observed).strip():
            self._deny("G-CTRL",
                       "control %r recorded with an empty result" % name)
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
        if new_name in self.quantities:
            # record() refuses to overwrite; so must this. A promotion that
            # silently replaces a physical quantity with a generator-derived
            # one is the substitution G-LAYER exists to prevent.
            self._deny("G-LAYER",
                       "promotion target %r is already recorded" % new_name)
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
        if name in self.quantities:
            self._deny("G-DIM", "ratio target %r is already recorded" % name)
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

    def claim(self, text, supported_by, scope="physical"):
        """
        A claim names the recorded quantities that support it. G-SUP, G-LAYER

        `scope` is what the claim is about: "physical" by default, or
        "generator" / "instrument" for a claim explicitly about the code that
        produced the data or about the measuring apparatus.

        Two downgrades, both to "qualified" with a G-LAYER finding:

          1. Any generator-level support under a non-generator-scope claim.
             A parameter of the code is never about the modelled system.

          2. A physical-scope claim with NO physical-level support at all.
             Resting entirely on instrument and generator quantities is a
             promotion without a step: a residual count is a property of the
             classifier, an artifact floor a property of the estimator, and
             neither becomes a property of the system by being divided or
             counted.

        Rule 2 does not fire when physical support is present. A physical
        claim legitimately uses instrument quantities as bounds -- "the
        separation exceeds the estimator's error bar" needs the error bar --
        and downgrading those would be wrong.

        Downgraded, not refused, which is the shape G-IND uses for
        convergence across shared inputs. The support is real; what it
        cannot carry is a statement about the modelled system.
        """
        self._require_open()
        supported_by = list(supported_by or [])
        if scope not in LAYERS:
            self._deny("G-LAYER", "claim scope %r not in %s"
                       % (scope, list(LAYERS)))
        if not supported_by:
            self.claims.append({"text": text, "supported_by": [],
                                "scope": scope, "status": "unsupported"})
            self._soft("G-SUP", text)
            return self
        unknown = [q for q in supported_by if q not in self.quantities]
        if unknown:
            self.claims.append({"text": text, "supported_by": supported_by,
                                "scope": scope, "status": "unsupported"})
            self._soft("G-SUP",
                       "%s | not recorded: %s" % (text, ", ".join(unknown)))
            return self
        layers = sorted(set(self.quantities[q]["layer"] for q in supported_by))

        entry = {
            "text": text,
            "supported_by": supported_by,
            "scope": scope,
            "support_layers": layers,
            "status": "supported",
        }
        note = None
        if "generator" in layers and scope != "generator":
            gen = sorted(q for q in supported_by
                         if self.quantities[q]["layer"] == "generator")
            note = ("%s scope claim resting on generator-level support: %s"
                    % (scope, ", ".join(gen)))
        elif scope == "physical" and "physical" not in layers:
            note = ("physical scope claim with no physical-level support: "
                    "rests entirely on %s" % ", ".join(layers))
        if note:
            entry["status"] = "qualified"
            entry["layer_note"] = note
            self._note("G-LAYER", "%s | %s" % (text, note))
        self.claims.append(entry)
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

    def close(self, observed, write=True, diverged=None):
        """
        Compare observed against the pre-registered expectation.

        `diverged` is the author's explicit call on whether the run matched
        its prediction: True, False, or None for not assessed. It is not
        inferred from the text, because expected and observed are prose and
        two descriptions of the same outcome never compare equal. Silence is
        not a verdict here -- None means unassessed, and any tool mining
        these logs should say so rather than guess.
        """
        self._require_open()
        if self._closed:
            raise GateError("gate already closed")
        if not (isinstance(observed, str) and observed.strip()):
            self._deny("G-PRE", "close() requires an observed summary")
        if diverged not in (True, False, None):
            self._deny("G-PRE", "diverged must be True, False, or None")

        unrun = [c.name for c in self._controls if c.observed is None]
        if unrun:
            detail = "declared but never run: %s" % ", ".join(unrun)
            if self.strict:
                # Close the gate BEFORE denying. Leaving it open let a caller
                # catch the error, answer the control with a placeholder, and
                # close again into a clean report whose controls block said
                # run: True while a finding below said otherwise.
                self.findings.append({"guard": "G-CTRL", "detail": detail,
                                      "message": self._msg("G-CTRL")})
                self._closed = True
                self._deny("G-CTRL", detail)
            self._soft("G-CTRL", detail)

        gen_only = [n for n, q in self.quantities.items()
                    if q["layer"] == "generator"]

        report = {
            "sim_id": self.sim_id,
            "outcome": "CLOSED",
            "strict": self.strict,
            "guards_schema": self.guards.get("schema_version"),
            "declaration": self.declaration,
            "expected": self.declaration.get("expected"),
            "observed": observed.strip(),
            "diverged": diverged,
            "quantities": self.quantities,
            "generator_level_quantities": sorted(gen_only),
            "voided_ratios": self.voided,
            "claims": self.claims,
            "findings": self.findings,
            "closed_at": datetime.datetime.now().isoformat(timespec="seconds"),
        }
        self._closed = True
        if write:
            path = self._write(report)
            if path:
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
        L.append("  diverged : %s" % {True: "YES", False: "no",
                                      None: "NOT ASSESSED"}[report.get("diverged")])
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
            if c.get("layer_note"):
                L.append("             ^ %s" % c["layer_note"])
        for f in report["findings"]:
            L.append("  finding  : %s" % f["message"])
            if f.get("detail"):
                L.append("             ^ %s" % f["detail"])
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
