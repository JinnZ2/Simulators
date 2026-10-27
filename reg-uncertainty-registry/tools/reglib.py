#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
reglib.py -- shared loader for the regulatory uncertainty registry.

Everything every tool needs, in one place, so no tool re-implements it:

    pins          source/PINS.json (first landing), bundle/MANIFEST.sha256
                  (consolidated bundle, itself pinned in bundle_pins.json) and
                  registry/MANIFEST.json
                  (registry files) are re-hashed on every load; a mismatch is
                  returned, never silently ignored
    vocabulary    schema/vocabulary.json, the one source of every enum
    schema        a stdlib validator for the JSON Schema subset the registry
                  schema uses (type, required, properties, additionalProperties,
                  items, enum, pattern, minItems, $ref) plus x-vocab
    registry      every object by id, every edge, typed indexes
    imports       citation_state from tools/check_citations.py (repo root),
                  fisher_exact_2sided and cohen_kappa from
                  effective-redundancy-audit/effective_redundancy.py.
                  Imported, never copied, so they cannot drift.

This module is a library and refuses --selftest; the checks for it run in
tools/validate.py --selftest. Stdlib only; parses under Python 3.8.
"""

import hashlib
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.dirname(HERE)
REPO = os.path.dirname(FOLDER)

PINS = os.path.join(FOLDER, "source", "PINS.json")
BUNDLE_PINS = os.path.join(FOLDER, "bundle_pins.json")
BUNDLE = os.path.join(FOLDER, "bundle")
BUNDLE_MANIFEST = os.path.join(BUNDLE, "MANIFEST.sha256")
MANIFEST = os.path.join(FOLDER, "registry", "MANIFEST.json")
VOCAB = os.path.join(FOLDER, "schema", "vocabulary.json")
SCHEMA = os.path.join(FOLDER, "schema", "registry.schema.json")
REGDIR = os.path.join(FOLDER, "registry")
SRCDIR = os.path.join(BUNDLE, "source", "current")
OLDDIR = os.path.join(BUNDLE, "source", "superseded")


class RegistryError(Exception):
    pass


# ---------------------------------------------------------------- io

def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def dump_json(obj, path):
    text = json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return text


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def rel(path):
    return os.path.relpath(path, FOLDER)


# ---------------------------------------------------------------- imports

def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_CC = None
_ER = None


def check_citations():
    global _CC
    if _CC is None:
        _CC = _load_module("rur_check_citations",
                           os.path.join(REPO, "tools", "check_citations.py"))
    return _CC


def effective_redundancy():
    global _ER
    if _ER is None:
        _ER = _load_module("rur_effective_redundancy",
                           os.path.join(REPO, "effective-redundancy-audit",
                                        "effective_redundancy.py"))
    return _ER


def citation_state(reached, queries, exists, says):
    return check_citations().citation_state(reached, queries, exists, says)


def fisher_exact_2sided(a, b, c, d):
    return effective_redundancy().fisher_exact_2sided(a, b, c, d)


def cohen_kappa(c1, c2):
    return effective_redundancy().cohen_kappa(c1, c2)


# ---------------------------------------------------------------- pins

def check_pins(pins_path=PINS, base=FOLDER, bundle_pins=BUNDLE_PINS,
               bundle_manifest=BUNDLE_MANIFEST):
    """Return (path, want, got) for every pinned input whose hash differs or
    that is missing. Three pin families: source/PINS.json (the first
    landing, kept as configuration history), bundle/MANIFEST.sha256 (the
    consolidated bundle's own manifest; entries bundle_pins.json lists as
    not_in_tree are skipped), and bundle_pins.json's pin of the manifest
    itself. Empty list = every pin holds."""
    bad = []
    pins = load_json(pins_path)
    for relpath, want in sorted(pins["files"].items()):
        p = os.path.join(base, relpath)
        got = sha256_file(p) if os.path.exists(p) else "MISSING"
        if got != want:
            bad.append((relpath, want, got))
    bp = load_json(bundle_pins)
    mrel = bp["manifest"]["path"]
    got = sha256_file(bundle_manifest) if os.path.exists(bundle_manifest) else "MISSING"
    if got != bp["manifest"]["sha256"]:
        bad.append((mrel, bp["manifest"]["sha256"], got))
    for relpath, want in bundle_manifest_entries(bundle_manifest):
        if relpath in bp["not_in_tree"]:
            continue
        p = os.path.join(os.path.dirname(bundle_manifest), relpath)
        got = sha256_file(p) if os.path.exists(p) else "MISSING"
        if got != want:
            bad.append(("bundle/" + relpath, want, got))
    return bad


def bundle_manifest_entries(path=BUNDLE_MANIFEST):
    out = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            want, relpath = line.split(None, 1)
            out.append((relpath[2:] if relpath.startswith("./") else relpath, want))
    return out


def pinned_count():
    pins = load_json(PINS)
    bp = load_json(BUNDLE_PINS)
    n_b = sum(1 for r, _ in bundle_manifest_entries() if r not in bp["not_in_tree"])
    return len(pins["files"]) + 1 + n_b


def check_manifest(manifest_path=MANIFEST, base=FOLDER):
    """Registry files are pinned too: an edit that bypassed tools/build.py
    (and so has no CHANGE record) shows up here."""
    if not os.path.exists(manifest_path):
        return [("registry/MANIFEST.json", "present", "MISSING")]
    man = load_json(manifest_path)
    bad = []
    for relpath, want in sorted(man["files"].items()):
        p = os.path.join(base, relpath)
        got = sha256_file(p) if os.path.exists(p) else "MISSING"
        if got != want:
            bad.append((relpath, want, got))
    return bad


def pin_report():
    """One line per pin family, for every tool's header."""
    sp = check_pins()
    mp = check_manifest()
    n_in = pinned_count()
    man = load_json(MANIFEST) if os.path.exists(MANIFEST) else {"files": {}}
    lines = ["pins   inputs %d/%d hold   registry %d/%d hold"
             % (n_in - len(sp), n_in,
                len(man["files"]) - len(mp), len(man["files"]))]
    for relpath, want, got in sp + mp:
        lines.append("PIN MISMATCH  %s  want %s  got %s"
                     % (relpath, want[:12], got[:12]))
    return lines, (not sp and not mp)


# ---------------------------------------------------------------- vocab

def vocabulary():
    return load_json(VOCAB)


def vocab_values(name, vocab=None):
    v = (vocab or vocabulary())[name]
    return v["values"]


# ---------------------------------------------------------------- schema

class SchemaValidator(object):
    """The JSON Schema subset the registry schema uses. Unknown keywords
    other than annotations raise, so the validator cannot silently ignore a
    rule it does not implement."""

    ANNOTATIONS = {"$schema", "$id", "title", "description", "$defs",
                   "_note", "x-edge-endpoints", "x-files"}
    KEYWORDS = {"type", "required", "properties", "additionalProperties",
                "items", "enum", "pattern", "minItems", "$ref", "x-vocab"}

    def __init__(self, schema, vocab):
        self.schema = schema
        self.vocab = vocab

    def resolve(self, ref):
        if not ref.startswith("#/$defs/"):
            raise RegistryError("unsupported $ref %r" % ref)
        return self.schema["$defs"][ref[len("#/$defs/"):]]

    @staticmethod
    def _type_ok(value, t):
        if t == "object":
            return isinstance(value, dict)
        if t == "array":
            return isinstance(value, list)
        if t == "string":
            return isinstance(value, str)
        if t == "integer":
            return isinstance(value, int) and not isinstance(value, bool)
        if t == "number":
            return isinstance(value, (int, float)) and not isinstance(value, bool)
        if t == "boolean":
            return isinstance(value, bool)
        if t == "null":
            return value is None
        raise RegistryError("unsupported type %r" % t)

    def errors(self, value, schema, path="$"):
        out = []
        for k in schema:
            if k not in self.KEYWORDS and k not in self.ANNOTATIONS:
                raise RegistryError("unsupported schema keyword %r at %s"
                                    % (k, path))
        if "$ref" in schema:
            return self.errors(value, self.resolve(schema["$ref"]), path)
        if "type" in schema:
            ts = schema["type"] if isinstance(schema["type"], list) \
                else [schema["type"]]
            if not any(self._type_ok(value, t) for t in ts):
                return ["%s: type %s, want %s" % (path, type(value).__name__,
                                                  "|".join(ts))]
        if "enum" in schema and value not in schema["enum"]:
            out.append("%s: %r not in enum %r" % (path, value, schema["enum"]))
        if "x-vocab" in schema:
            vals = self.vocab[schema["x-vocab"]]["values"]
            if value not in vals:
                out.append("%s: %r not in vocabulary %s"
                           % (path, value, schema["x-vocab"]))
        if "pattern" in schema and isinstance(value, str):
            if not re.search(schema["pattern"], value):
                out.append("%s: %r does not match %s"
                           % (path, value, schema["pattern"]))
        if isinstance(value, dict):
            for r in schema.get("required", []):
                if r not in value:
                    out.append("%s: missing required %r" % (path, r))
            props = schema.get("properties", {})
            for k, v in value.items():
                if k in props:
                    out.extend(self.errors(v, props[k], "%s.%s" % (path, k)))
                else:
                    ap = schema.get("additionalProperties", True)
                    if ap is False:
                        out.append("%s: unexpected property %r" % (path, k))
                    elif isinstance(ap, dict):
                        out.extend(self.errors(v, ap, "%s.%s" % (path, k)))
        if isinstance(value, list):
            if "minItems" in schema and len(value) < schema["minItems"]:
                out.append("%s: %d items, want >= %d"
                           % (path, len(value), schema["minItems"]))
            if "items" in schema:
                for i, v in enumerate(value):
                    out.extend(self.errors(v, schema["items"],
                                           "%s[%d]" % (path, i)))
        return out


def schema_validator():
    return SchemaValidator(load_json(SCHEMA), vocabulary())


# ---------------------------------------------------------------- registry

class Registry(object):
    def __init__(self, regdir=REGDIR):
        self.regdir = regdir
        schema = load_json(SCHEMA)
        self.files = schema["x-files"]
        self.objects = {}
        self.by_type = {}
        self.edges = []
        self.file_of = {}
        for relpath in sorted(self.files):
            p = os.path.join(os.path.dirname(regdir), relpath)
            if not os.path.exists(p):
                raise RegistryError("registry file missing: %s" % relpath)
            data = load_json(p)
            if relpath.endswith("edges.json"):
                self.edges = data
                continue
            for obj in data:
                oid = obj["id"]
                if oid in self.objects:
                    raise RegistryError("duplicate id %s (%s and %s)"
                                        % (oid, self.file_of[oid], relpath))
                self.objects[oid] = obj
                self.file_of[oid] = relpath
                self.by_type.setdefault(obj["type"], []).append(obj)

    def get(self, oid):
        return self.objects.get(oid)

    def of(self, *types):
        out = []
        for t in types:
            out.extend(self.by_type.get(t, []))
        return out

    def cases(self, in_sample=None):
        cs = self.of("DECISION", "NON_DECISION")
        if in_sample is not None:
            cs = [c for c in cs if c["in_sample"] == in_sample]
        return sorted(cs, key=lambda c: c["id"])

    def out_edges(self, oid, etype=None):
        return [e for e in self.edges if e["from"] == oid
                and (etype is None or e["type"] == etype)]

    def in_edges(self, oid, etype=None):
        return [e for e in self.edges if e["to"] == oid
                and (etype is None or e["type"] == etype)]

    def claim(self, case, name):
        c = case["claims"].get(name)
        return None if c is None else c["value"]


def main():
    sys.stderr.write("reglib.py is a library; checks run in "
                     "reg-uncertainty-registry/tools/validate.py --selftest\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
