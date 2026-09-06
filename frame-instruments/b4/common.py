"""B4-specific constants and helpers; generic pieces come from ../ficommon.py."""
import os
import sys

PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PARENT not in sys.path:
    sys.path.insert(0, PARENT)
from ficommon import (FORBIDDEN, Invalid, Run, Void, check_fields, check_id,  # noqa: E402,F401
                      count_by, finish, nonempty_str, parse_argv, raise_if,
                      read_jsonl, usage_exit, write_jsonl)

STATES = ("true", "false", "lapsed", "partial", "unknown", "undifferentiated")
ARMS = ("hypothetical", "documented")
ITEM_FIELDS = ("item_id", "source", "text_verbatim", "branches_stated", "arm")
REQ_FIELDS = ("item_id", "reconstructor_id", "req_id", "requirement_text",
              "status", "settling_test", "layer")
MATCH_FIELDS = ("item_id", "req_a", "req_b", "matched")


def ref(reconstructor_id, req_id):
    return "%s/%s" % (reconstructor_id, req_id)


def parse_ref(s):
    if not isinstance(s, str) or s.count("/") != 1:
        raise Invalid("requirement reference %r must be reconstructor_id/req_id" % (s,))
    a, b = s.split("/")
    return a, b
