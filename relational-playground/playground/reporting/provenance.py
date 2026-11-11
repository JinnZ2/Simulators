"""Provenance: what produced a record. Hashes of the code and of the configuration."""
import hashlib, json, os, platform

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def sha256_obj(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()


def stamp(config_dict, code_paths):
    return dict(config_sha256=sha256_obj(config_dict),
                code={os.path.relpath(p, ROOT): sha256_file(p) for p in code_paths},
                python=platform.python_version())
