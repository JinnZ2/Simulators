#!/usr/bin/env python3
"""
validate_claim_table.py

Lightweight schema validation for CLAIM_TABLE.json files produced anywhere
in this repo. Deliberately permissive: research-stability-audit uses
`hypothesis`/`is_falsified` while emergence-stability-simulator uses
`statement`/`status`; both are accepted.

CLI:
    python3 tools/validate_claim_table.py path/to/CLAIM_TABLE.json [...]

Exit codes:
    0  no errors (warnings allowed)
    1  one or more validation errors
    2  bad invocation (file missing, bad JSON)

License: CC0
Dependencies: stdlib only
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


SCHEMA_VERSION = '1.0'

# Top-level recommendations: at least one of these identifies the source repo.
SOURCE_KEYS = ('source_repo', 'source', 'audit_id')

# A claim needs an id and at least one descriptor.
DESCRIPTOR_KEYS = ('statement', 'hypothesis')


def validate_claim_table(data: Any) -> Dict[str, List[str]]:
    """
    Validate a parsed CLAIM_TABLE.json structure.

    Returns: {'errors': [...], 'warnings': [...], 'claim_count': int,
              'claim_ids': [...]}
    """
    errors: List[str] = []
    warnings: List[str] = []
    claim_ids: List[str] = []

    if not isinstance(data, dict):
        errors.append("Top-level must be a JSON object")
        return {'errors': errors, 'warnings': warnings,
                'claim_count': 0, 'claim_ids': claim_ids}

    if 'schema_version' not in data:
        warnings.append(f"Missing top-level 'schema_version' "
                        f"(recommended: '{SCHEMA_VERSION}')")
    if not any(k in data for k in SOURCE_KEYS):
        warnings.append("Missing source identifier "
                        "(recommended: 'source_repo')")

    claims = data.get('claims')
    if claims is None:
        errors.append("Missing required top-level 'claims' list")
        return {'errors': errors, 'warnings': warnings,
                'claim_count': 0, 'claim_ids': claim_ids}

    if not isinstance(claims, list):
        errors.append("'claims' must be a list")
        return {'errors': errors, 'warnings': warnings,
                'claim_count': 0, 'claim_ids': claim_ids}

    seen: Dict[str, int] = {}
    for i, claim in enumerate(claims):
        if not isinstance(claim, dict):
            errors.append(f"claims[{i}]: not an object")
            continue

        cid = claim.get('claim_id')
        if not cid or not isinstance(cid, str):
            errors.append(f"claims[{i}]: missing or non-string 'claim_id'")
            continue

        claim_ids.append(cid)
        seen[cid] = seen.get(cid, 0) + 1

        if not any(claim.get(k) for k in DESCRIPTOR_KEYS):
            errors.append(f"claims[{i}] {cid}: missing descriptor "
                          f"(need one of {DESCRIPTOR_KEYS})")

        if not claim.get('falsification_criteria') and 'falsification' not in claim:
            warnings.append(f"claims[{i}] {cid}: missing 'falsification_criteria'")

        if (claim.get('status') is None
                and claim.get('is_falsified') is None):
            warnings.append(f"claims[{i}] {cid}: missing 'status' or 'is_falsified'")

    for cid, count in seen.items():
        if count > 1:
            errors.append(f"duplicate claim_id {cid!r}: appears {count} times")

    return {'errors': errors, 'warnings': warnings,
            'claim_count': len(claims), 'claim_ids': claim_ids}


def validate_file(path: Path) -> Dict[str, List[str]]:
    """Read and validate a CLAIM_TABLE.json file."""
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError:
        return {'errors': [f"file not found: {path}"], 'warnings': [],
                'claim_count': 0, 'claim_ids': []}
    except json.JSONDecodeError as e:
        return {'errors': [f"invalid JSON in {path}: {e}"], 'warnings': [],
                'claim_count': 0, 'claim_ids': []}
    return validate_claim_table(data)


def _print_report(path: Path, report: Dict[str, List[str]]) -> bool:
    """Print a per-file report. Returns True if any errors."""
    has_errors = bool(report['errors'])
    print(f"\n{path}")
    print(f"  claims:   {report['claim_count']}")
    print(f"  errors:   {len(report['errors'])}")
    print(f"  warnings: {len(report['warnings'])}")
    for e in report['errors']:
        print(f"    [ERROR]   {e}")
    for w in report['warnings']:
        print(f"    [WARN]    {w}")
    return has_errors


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print("usage: validate_claim_table.py <CLAIM_TABLE.json> [...]",
              file=sys.stderr)
        return 2

    any_errors = False
    for arg in argv[1:]:
        path = Path(arg)
        report = validate_file(path)
        if _print_report(path, report):
            any_errors = True

    return 1 if any_errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
