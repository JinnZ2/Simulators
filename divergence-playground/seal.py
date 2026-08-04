#!/usr/bin/env python3
"""
seal.py -- the anti-anchoring seal.  stdlib only, CC0.

Load-bearing rule: a Reading committed to a Fork MUST NOT be visible
to any subsequent reader before reveal() is called on the fork.  If
that rule breaks, the ensemble collapses into the first reading
posted.  That's the single failure mode that kills the playground.

Enforcement model (solo/small-team; no adversary assumed):

    * commit() writes an XOR-obfuscated payload plus a SHA-256 hash
      into SEALED.jsonl.  The obfuscation is deliberately weak (single
      per-fork nonce, hex-encoded) -- enough that a text editor or
      `cat` will not show the reading, not enough to resist a
      determined attacker.  The point is to make ACCIDENTAL peeking
      impossible for the operator running the tool.
    * The hash is committed in plaintext so tampering with the payload
      later (after other readings arrive) is detectable.
    * reveal() releases the payloads for a specific fork and appends
      them to REVEALED.jsonl.  Once revealed, that fork is closed
      to further commits.

For genuinely adversarial multi-agent settings, replace the XOR nonce
with real crypto -- keep the same commit/reveal API.
"""

import hashlib
import json
import os
import secrets
import time
from typing import List, Optional

from reading import Reading


SEALED_FILE   = "SEALED.jsonl"
REVEALED_FILE = "REVEALED.jsonl"
NONCES_FILE   = ".nonces.json"      # one nonce per fork, opaque


class SealError(RuntimeError):
    """Raised when the seal invariant would be broken."""


# --- XOR obfuscation (accidental-peek defence only, not crypto) -----------

def _nonce_for(fork_id: str, root: str) -> str:
    path = os.path.join(root, NONCES_FILE)
    nonces = {}
    if os.path.exists(path):
        nonces = json.load(open(path))
    if fork_id not in nonces:
        nonces[fork_id] = secrets.token_hex(32)
        with open(path, "w") as f:
            json.dump(nonces, f, indent=2, sort_keys=True)
    return nonces[fork_id]


def _xor_hex(payload: str, nonce_hex: str) -> str:
    key = bytes.fromhex(nonce_hex)
    b = payload.encode("utf-8")
    out = bytes(bi ^ key[i % len(key)] for i, bi in enumerate(b))
    return out.hex()


def _unxor_hex(encoded_hex: str, nonce_hex: str) -> str:
    key = bytes.fromhex(nonce_hex)
    b = bytes.fromhex(encoded_hex)
    return bytes(bi ^ key[i % len(key)] for i, bi in enumerate(b)).decode("utf-8")


# --- storage state --------------------------------------------------------

def _sealed_records(root: str, fork_id: Optional[str] = None) -> List[dict]:
    path = os.path.join(root, SEALED_FILE)
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            if fork_id is None or r["fork_id"] == fork_id:
                out.append(r)
    return out


def _revealed_records(root: str, fork_id: Optional[str] = None) -> List[dict]:
    path = os.path.join(root, REVEALED_FILE)
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            if fork_id is None or r["fork_id"] == fork_id:
                out.append(r)
    return out


def _is_revealed(root: str, fork_id: str) -> bool:
    return len(_revealed_records(root, fork_id)) > 0


# --- public API -----------------------------------------------------------

def commit(fork_id: str, reader_id: str, reading: Reading,
           root: str = ".") -> str:
    """
    Seal a reading against a fork.  Returns the SHA-256 hash of the
    canonical payload -- the reader keeps this as their receipt.

    Fails if the fork has already been revealed (no post-reveal commits)
    or if the same reader_id already committed to this fork.
    """
    if _is_revealed(root, fork_id):
        raise SealError(f"fork {fork_id} already revealed; commits closed")
    existing = _sealed_records(root, fork_id)
    if any(r["reader_id"] == reader_id for r in existing):
        raise SealError(
            f"reader {reader_id!r} already committed to {fork_id}; "
            "one reading per reader per fork")

    payload = reading.canonical()
    h = hashlib.sha256(payload.encode()).hexdigest()
    nonce = _nonce_for(fork_id, root)
    obfuscated = _xor_hex(payload, nonce)

    record = {
        "fork_id": fork_id,
        "reader_id": reader_id,
        "sha256": h,
        "sealed_payload": obfuscated,
        "committed_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    with open(os.path.join(root, SEALED_FILE), "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return h


def status(fork_id: Optional[str] = None, root: str = ".") -> None:
    """Print sealed / revealed counts.  Does NOT reveal any payload."""
    sealed = _sealed_records(root, fork_id)
    revealed = _revealed_records(root, fork_id)
    if not sealed and not revealed:
        print("no commits yet")
        return
    by_fork = {}
    for r in sealed:
        by_fork.setdefault(r["fork_id"], {"sealed": [], "revealed": False})
        by_fork[r["fork_id"]]["sealed"].append(r["reader_id"])
    for r in revealed:
        by_fork.setdefault(r["fork_id"], {"sealed": [], "revealed": False})
        by_fork[r["fork_id"]]["revealed"] = True
    print(f"{'fork':<10}{'state':<10}readers (masked hashes)")
    for fk, info in sorted(by_fork.items()):
        state = "REVEALED" if info["revealed"] else "SEALED"
        readers = ", ".join(info["sealed"])
        print(f"{fk:<10}{state:<10}{readers}")


def reveal(fork_id: str, root: str = ".") -> List[dict]:
    """
    Unseal all commits for a fork.  Verifies every hash before unsealing.
    Appends decoded records to REVEALED.jsonl and returns them.

    After reveal(), no further commit() may be made for that fork.
    """
    if _is_revealed(root, fork_id):
        raise SealError(f"fork {fork_id} already revealed")
    sealed = _sealed_records(root, fork_id)
    if not sealed:
        raise SealError(f"fork {fork_id} has no sealed commits to reveal")
    nonce = _nonce_for(fork_id, root)
    revealed = []
    for r in sealed:
        try:
            payload = _unxor_hex(r["sealed_payload"], nonce)
        except (ValueError, UnicodeDecodeError) as e:
            raise SealError(
                f"HASH MISMATCH for {r['fork_id']}/{r['reader_id']}: "
                f"sealed payload tampered with after commit ({e.__class__.__name__})")
        recomputed = hashlib.sha256(payload.encode()).hexdigest()
        if recomputed != r["sha256"]:
            raise SealError(
                f"HASH MISMATCH for {r['fork_id']}/{r['reader_id']}: "
                "sealed payload tampered with after commit")
        reading = Reading.from_json(payload)
        rec = {"fork_id": r["fork_id"], "reader_id": r["reader_id"],
               "sha256": r["sha256"],
               "committed_at": r["committed_at"],
               "revealed_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "reading": json.loads(reading.to_json())}
        revealed.append(rec)
    with open(os.path.join(root, REVEALED_FILE), "a", encoding="utf-8") as f:
        for rec in revealed:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return revealed


def revealed_readings(fork_id: str, root: str = ".") -> List[tuple]:
    """Return [(reader_id, Reading), ...] for a revealed fork."""
    recs = _revealed_records(root, fork_id)
    if not recs:
        return []
    out = []
    for r in recs:
        d = r["reading"]
        d["mechanism"] = [tuple(e) for e in d.get("mechanism", [])]
        out.append((r["reader_id"], Reading(**d)))
    return out


# --- self-test ------------------------------------------------------------

def _t_seal_hides_and_reveal_shows():
    import tempfile, shutil
    with tempfile.TemporaryDirectory() as td:
        r = Reading(
            verdict="A", mechanism=[("x", "r", "y")],
            collapse={"vary": ["p"], "observe": "q", "criterion": "c"})
        h = commit("FK-TEST", "reader1", r, root=td)
        # sealed file exists but the plaintext reading must not be in it
        blob = open(os.path.join(td, SEALED_FILE)).read()
        assert '"verdict": "A"' not in blob, "payload leaked to sealed file"
        assert h in blob, "hash should be recorded"
        # reveal returns the reading
        rev = reveal("FK-TEST", root=td)
        assert len(rev) == 1
        assert rev[0]["reading"]["verdict"] == "A"


def _t_double_commit_rejected():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        r = Reading(
            verdict="A", mechanism=[("x", "r", "y")],
            collapse={"vary": ["p"], "observe": "q", "criterion": "c"})
        commit("FK-X", "r1", r, root=td)
        try:
            commit("FK-X", "r1", r, root=td)
        except SealError:
            return
        raise AssertionError("should have rejected second commit from same reader")


def _t_post_reveal_commit_rejected():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        r = Reading(
            verdict="A", mechanism=[("x", "r", "y")],
            collapse={"vary": ["p"], "observe": "q", "criterion": "c"})
        commit("FK-Y", "r1", r, root=td)
        reveal("FK-Y", root=td)
        try:
            commit("FK-Y", "r2", r, root=td)
        except SealError:
            return
        raise AssertionError("should have rejected commit after reveal")


def _t_tamper_detected():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        r = Reading(
            verdict="A", mechanism=[("x", "r", "y")],
            collapse={"vary": ["p"], "observe": "q", "criterion": "c"})
        commit("FK-Z", "r1", r, root=td)
        # tamper with the sealed payload
        p = os.path.join(td, SEALED_FILE)
        s = open(p).read()
        # flip one hex char in the sealed_payload field
        idx = s.find('"sealed_payload": "') + len('"sealed_payload": "')
        s = s[:idx] + ('0' if s[idx] != '0' else '1') + s[idx+1:]
        open(p, "w").write(s)
        try:
            reveal("FK-Z", root=td)
        except SealError as e:
            assert "HASH MISMATCH" in str(e)
            return
        raise AssertionError("should have detected tampering")


def _run():
    for name, fn in sorted(globals().items()):
        if name.startswith("_t_"):
            fn(); print("ok", name)
    print("all pass")


if __name__ == "__main__":
    _run()
