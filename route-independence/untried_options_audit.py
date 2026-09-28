# SPDX-License-Identifier: CC0-1.0
"""untried_options_audit.py -- were the options enumerated, and was cost bound
to the decider?

FWO-3. A decision-record check. Five checks report presence and content.
No check produces a verdict on the decision.

SOURCE OF THE STRUCTURE (carried verbatim from the work order)
    Described as the war-initiation protocol of a living practice; source
    withheld at request. Carry that line verbatim. Do not attach a name. It
    is a load-tested operating protocol, not a design composed for this
    build.
    Structure as described (OBSERVED):
      - only a body composed of those who bore the prior cost could
        authorize; the proposing body could want but not grant
      - proposers had to name THEMSELVES, their friends and family as those
        who would bear first consequences -- not others
      - full disclosure: consequences of the last instance, this instance,
        all options TRIED, all options NOT TRIED
      - a third party (neither proposer nor authorizer) could name an
        untried option, which then had to be tried first
      - if that party named an option the record had omitted, the record
        was returned: the work was not done correctly; redo
    DERIVED (Claude): functionally a failure-mode analysis with an
    independent verifier who can send it back. Rarity of the action is the
    output of a correctly specified test, not a separate value.

INPUT   decision_record.txt, `field: value` lines; `#` comments.
    decision / proposer / first_cost_bearers / authorizer /
    authorizer_prior_exposure / options_tried / options_not_tried /
    reviewer / reviewer_added_options / source
    Optional: options_considered (a slot for options evaluated and
    rejected on argument, never tried in the world -- a THIRD state,
    kept apart from both TRIED and NOT TRIED), reviewer_can_add_options
    (yes|no), record_kind (instance|type), source_status
    (read|carried|synthetic), source_locator.
    List fields split on `;`. A field whose value is UNKNOWN is UNKNOWN.
    A field present with an empty value is an empty slot (NO). A field
    not in the file at all is ABSENT_FIELD.

CHECKS
    C1  first_cost_bearers includes proposer?   YES | NO | UNKNOWN | ABSENT_FIELD
    C2  authorizer_prior_exposure recorded?     YES | NO | UNKNOWN | ABSENT_FIELD
    C3  options_not_tried present, non-empty?   YES | NO | ABSENT_FIELD
        options_not_tried means options still available and untried,
        the ones a third party could require be tried first. A
        "considered and rejected" section is NOT that field: it lists
        options closed by argument. Code it as options_considered, which
        is reported on its own line (C3c) and never counted as C3.
        Coding a rejected-alternatives section as options_not_tried
        overstates C3 -- the first run of this instrument did exactly
        that on three records (RIN_021). [CHOICE 4]
    C4  independent reviewer with authority
        to add options?                         YES | NO | UNKNOWN | ABSENT_FIELD
    C5  reviewer_added_options not already in
        options_tried or options_not_tried      RETURN_FOR_REDO(list) |
                                                ALL_ALREADY_LISTED |
                                                NONE_ADDED | UNKNOWN |
                                                ABSENT_FIELD

    ABSENT_FIELD (no slot in the record) is kept apart from NO (slot
    present, empty) on every check, not only C3: the missing slot is the
    more important finding, and it is a property of the record TYPE where
    NO is a property of one instance. [CHOICE 1]

    C1 tests whether any token of `proposer` appears as a whole word in
    the cost-bearer list, case-insensitive, stopwords dropped. That is a string comparison and a stated
    limit: an alias or a role name defeats it in both directions.
    [CHOICE 2]

    C4 reads independence from the record (reviewer differs from proposer
    and authorizer as strings) and authority from
    `reviewer_can_add_options`; absent that field, a non-empty
    reviewer_added_options demonstrates the authority, else UNKNOWN.
    [CHOICE 3]
"""

import re
import sys

C1_STOPWORDS = frozenset(("the", "a", "an", "of", "and", "at", "in", "on", "to"))

YES, NO, UNKNOWN, ABSENT_FIELD = "YES", "NO", "UNKNOWN", "ABSENT_FIELD"
RETURN_FOR_REDO = "RETURN_FOR_REDO"
ALL_ALREADY_LISTED = "ALL_ALREADY_LISTED"
NONE_ADDED = "NONE_ADDED"

FIELDS = ("decision", "proposer", "first_cost_bearers", "authorizer",
          "authorizer_prior_exposure", "options_tried", "options_not_tried",
          "reviewer", "reviewer_added_options", "source")
OPTIONAL_FIELDS = ("options_considered", "reviewer_can_add_options")
LIST_FIELDS = ("first_cost_bearers", "options_tried", "options_not_tried",
               "options_considered", "reviewer_added_options")

CHOICES = {
    1: "ABSENT_FIELD is reported on every check, not only C3",
    4: "a considered-and-rejected section is its own field (options_considered, "
       "readout C3c) and never counts toward C3; an option closed by argument "
       "was not tried and is not open",
    2: "C1 is a case-insensitive token comparison between proposer and the "
       "cost-bearer list; aliases and role names defeat it",
    3: "C4 authority is read from reviewer_can_add_options, else demonstrated "
       "by a non-empty reviewer_added_options, else UNKNOWN",
}


def parse_record(text):
    """Returns a dict of raw field -> string (lists are split later).

    A field appearing twice is a refusal; the second value would silently
    overwrite the first.
    """
    record = {}
    refusals = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if ":" not in line:
            refusals.append(("MALFORMED_LINE", "line %d: %r" % (lineno, raw.strip())))
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in record:
            refusals.append(("DUPLICATE_FIELD", key))
            continue
        record[key] = value.strip()
    return record, refusals


def load(path):
    with open(path, "r", encoding="utf-8") as handle:
        return parse_record(handle.read())


def _state(record, field):
    """ABSENT_FIELD | UNKNOWN | NO (empty) | YES (has content)."""
    if field not in record:
        return ABSENT_FIELD
    v = record[field].strip()
    if v.upper() == "UNKNOWN":
        return UNKNOWN
    if v == "" or v == "-":
        return NO
    return YES


def _items(record, field):
    if field not in record:
        return []
    return [x.strip() for x in record[field].split(";") if x.strip()]


def c1(record):
    s_prop, s_bear = _state(record, "proposer"), _state(record, "first_cost_bearers")
    if ABSENT_FIELD in (s_prop, s_bear):
        return ABSENT_FIELD
    if UNKNOWN in (s_prop, s_bear):
        return UNKNOWN
    if s_bear == NO or s_prop == NO:
        return NO
    bearers = " ".join(_items(record, "first_cost_bearers")).lower()
    tokens = [t for t in re.split(r"[^\w']+", record["proposer"].lower())
              if t and t not in C1_STOPWORDS]
    return YES if any(re.search(r"(?<!\w)%s(?!\w)" % re.escape(t), bearers)
                      for t in tokens) else NO


def c2(record):
    return _state(record, "authorizer_prior_exposure")


def c3(record):
    s = _state(record, "options_not_tried")
    return NO if s == UNKNOWN else s  # an UNKNOWN entry is a slot with no content


def c3c(record):
    """options_considered: evaluated and rejected on argument, never tried."""
    s = _state(record, "options_considered")
    return NO if s == UNKNOWN else s


def c3a(record):
    """options_tried: attempted in the world, consequences recorded."""
    s = _state(record, "options_tried")
    return NO if s == UNKNOWN else s


def c4(record):
    s = _state(record, "reviewer")
    if s in (ABSENT_FIELD, UNKNOWN, NO):
        return s
    reviewer = record["reviewer"].strip().lower()
    for other in ("proposer", "authorizer"):
        if _state(record, other) == YES and record[other].strip().lower() == reviewer:
            return NO
    auth = record.get("reviewer_can_add_options", "").strip().lower()
    if auth == "yes":
        return YES
    if auth == "no":
        return NO
    if _state(record, "reviewer_added_options") == YES:
        return YES
    return UNKNOWN


def c5(record):
    s = _state(record, "reviewer_added_options")
    if s == ABSENT_FIELD:
        return ABSENT_FIELD, []
    if s == UNKNOWN:
        return UNKNOWN, []
    if s == NO:
        return NONE_ADDED, []
    listed = set(x.lower() for x in _items(record, "options_tried") + _items(record, "options_not_tried"))
    missing = [x for x in _items(record, "reviewer_added_options") if x.lower() not in listed]
    if missing:
        return RETURN_FOR_REDO, missing
    return ALL_ALREADY_LISTED, []


def audit(record):
    c5_result, c5_list = c5(record)
    return {
        "decision": record.get("decision", ABSENT_FIELD),
        "record_kind": record.get("record_kind", "instance"),
        "source": record.get("source", ""),
        "source_status": record.get("source_status", "synthetic" if not record.get("source") else "UNSTATED"),
        "source_locator": record.get("source_locator", ""),
        "absent_fields": [f for f in FIELDS if f not in record],
        "C1": c1(record), "C2": c2(record), "C3": c3(record),
        "C3a": c3a(record), "C3c": c3c(record), "C4": c4(record),
        "C5": c5_result, "C5_options": c5_list,
    }


def render(result):
    lines = ["decision:  %s" % result["decision"],
             "kind:      %s   source status: %s" % (result["record_kind"], result["source_status"]),
             "source:    %s" % (result["source"] or "SYNTHETIC")]
    if result["source_locator"]:
        lines.append("locator:   %s" % result["source_locator"])
    lines.append("  C1 first_cost_bearers includes proposer   %s" % result["C1"])
    lines.append("  C2 authorizer_prior_exposure recorded     %s" % result["C2"])
    lines.append("  C3 options_not_tried present, non-empty   %s" % result["C3"])
    lines.append("     C3a options_tried (in the world)       %s" % result["C3a"])
    lines.append("     C3c options_considered (rejected on    %s" % result["C3c"])
    lines.append("         argument, never tried)")
    lines.append("  C4 independent reviewer, may add options  %s" % result["C4"])
    c5 = result["C5"]
    if c5 == RETURN_FOR_REDO:
        c5 = "RETURN_FOR_REDO: " + "; ".join(result["C5_options"])
    lines.append("  C5 reviewer-added options unlisted        %s" % c5)
    if result["absent_fields"]:
        lines.append("  fields with no slot in this record: %s" % ", ".join(result["absent_fields"]))
    return "\n".join(lines)


def main(argv):
    args = argv[1:]
    if args == ["--choices"]:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    if args == ["--selftest"]:
        sys.stderr.write("library module; run: python3 route-independence/test_route.py\n")
        return 2
    if not args:
        sys.stderr.write("usage: untried_options_audit.py RECORD.txt [RECORD.txt ...] | --choices\n")
        return 2
    rc = 0
    for path in args:
        record, refusals = load(path)
        print("== %s" % path)
        if refusals:
            for kind, detail in refusals:
                print("  %-18s %s" % (kind, detail))
            rc = 2
            continue
        print(render(audit(record)))
        print("")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
