"""Reader for the YAML subset the ledger is written in. stdlib only.

Subset: block maps, block lists ("- "), scalars that are either bare tokens
(no ': ', no '#') or JSON double-quoted strings, and the literals [] and {}.
No anchors, no flow maps, no multi-line scalars. Bare tokens stay strings;
`void` is the string "void". Anything outside the subset raises.
"""
import json


class MiniYamlError(ValueError):
    pass


def _scalar(s):
    s = s.strip()
    if s == "[]":
        return []
    if s == "{}":
        return {}
    if s.startswith('"'):
        return json.loads(s)
    if not s or ": " in s or s.endswith(":") or "#" in s or s[0] in "[{&*!|>'":
        raise MiniYamlError(f"outside subset: {s!r}")
    return s


def _split(text):
    if text.startswith('"'):
        raise MiniYamlError(f"quoted keys unsupported: {text!r}")
    k, sep, v = text.partition(":")
    if not sep or (v and not v.startswith(" ")):
        raise MiniYamlError(f"expected 'key: value': {text!r}")
    return k.strip(), v.strip()


def _block(lines, i, indent):
    if lines[i][1].startswith("- "):
        out = []
        while i < len(lines) and lines[i][0] == indent and lines[i][1].startswith("- "):
            body = lines[i][1][2:]
            if body.startswith('"') or ":" not in body:
                out.append(_scalar(body))
                i += 1
            else:                       # a map item: re-read its first line as a key at indent+2
                lines[i] = (indent + 2, body)
                item, i = _block(lines, i, indent + 2)
                out.append(item)
        return out, i
    out = {}
    while i < len(lines) and lines[i][0] == indent and not lines[i][1].startswith("- "):
        k, v = _split(lines[i][1])
        if k in out:
            raise MiniYamlError(f"duplicate key {k!r}")
        i += 1
        if v:
            out[k] = _scalar(v)
        else:
            if i >= len(lines) or lines[i][0] <= indent:
                raise MiniYamlError(f"key {k!r} has no value; write void")
            out[k], i = _block(lines, i, lines[i][0])
    return out, i


def loads(text):
    lines = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise MiniYamlError("tab indentation")
        lines.append((len(raw) - len(raw.lstrip(" ")), raw.strip()))
    if not lines:
        raise MiniYamlError("empty document")
    out, i = _block(lines, 0, lines[0][0])
    if i != len(lines):
        raise MiniYamlError(f"could not parse from: {lines[i][1]!r}")
    return out


def load(path):
    with open(path, encoding="utf-8") as f:
        return loads(f.read())
