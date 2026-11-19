# REVIEW-2 request: line 23 of the brief (DRAFT, not sent)

Drafted 2026-11-19 at the owner's SUGGEST request. It checks the L0 findings recorded in `../MEASURANDS.md` (dated section, item 3) at a higher level. The send rules:

- **Reader:** a model family other than Claude, in a fresh conversation with memory off.
- **Expected level:** L2, not L3. The fixture rule is part of the implementation, so the reader is exposed to it by design.
- **Sending:** the text below the line is sent unchanged.
- **Filing:** the answer is filed as received in `../confusion/`, with the attestation block and the computed level, and the sent text beside it.

Read set as built: `reader_packet_v2/READER_BRIEF.md` lines 22-23 at Simulators main `671a226` (the file is unchanged since packet v2 was pinned); `studies/instrument/test_instrument.py` lines 22-38 as on main, last changed at `158aa12`. The PR #320 version of the rule is not shown.

---

```text
MODE: REVIEW-2 (confusion review of one passage and one rule)
READ: only the two excerpts below
AUTHORITATIVE WHEN FILES DISAGREE: excerpt A (the instructions); excerpt B is code that claims to follow
  instructions of this kind, and is under review
DO NOT USE: any repository, the web, earlier sessions, memory, other readers' answers, keys or scores
SESSION: new conversation; memory off; no project knowledge; no connected repositories
CODE EXECUTION: not allowed
RETURN: the attestation block below, then one row for each of the three questions. Mark every guess as a guess.
```

**Excerpt A** (instructions given to a reader who lists the fields of records; "the term" is a status or verdict word whose records are listed):

> - `slots_specific`: the named fields or parameters the source ties to this term and to no other term. Examples: a class written for the term, the parameters of a function or notation written for it, a documented key list for it, or a rule that says this status needs certain fields. Not fields that every term sharing a record has. Not names for the inputs of a calculation. If nothing is tied to this term alone, write `[]`.
> - `slots_carried`: every named field of every record that the source's code or text builds, returns or documents when this term is reported. This includes a shared or wrapper record that only carries the term as a value. Give a record's own fields; if a field holds another record, name the field and do not open it. If a record's fields differ by path, give every name the source can put in it. If no record is built or documented for the term, write `[]`.

**Excerpt B** (a rule in a test, meant to compute which records count; `ALL_REPORTING_PATH_RECORDS` is meant to model "every record built on the path that reports the term"):

```python
def carried(case):
    recs = {r["record_id"]: r for r in case["records"]}
    own = [r for r in case["records"] if r["relationship"] == "TERM_OWN_RECORD"]
    rule = case["scope_rule"]
    if rule == "TERM_OWN_RECORD_ONLY": counted = [r["record_id"] for r in own]
    elif rule == "ALL_REPORTING_PATH_RECORDS":
        counted = [r["record_id"] for r in case["records"] if r["on_reporting_path"] and r["relationship"] != "WRAPPER_RECORD"]
    elif rule == "FIRST_WRAPPER_ONLY":
        counted = [r["record_id"] for r in own] + [r["record_id"] for r in case["records"] if r["relationship"] == "WRAPPER_RECORD" and r["depth"] == 1]
    else: raise ValueError(rule)
    opened = []
    if case["traversal_rule"] == "OPEN":
        for rid in list(counted):
            for ref in recs[rid]["nested_field_refs"].values():
                if ref not in counted: opened.append(ref); counted.append(ref)
    fields = [f for rid in counted for f in recs[rid]["fields"]]
    return {"counted": counted, "opened": opened, "fields": fields}
```

**Questions.** Answer from the excerpts only.

1. Does the `slots_carried` instruction in excerpt A include a wrapper record that carries the term's record as a value? Does excerpt B's `ALL_REPORTING_PATH_RECORDS` agree with your answer?
2. Does the instruction include an outer aggregate report, one that holds many records, one of them the term's?
3. Where does the path that "reports this term" end, by the instruction's text? If the text does not say, say so.

**Return format**, one row per question:

```text
q | answer | the words in excerpt A or B it rests on | guessed? (yes / no) | what would settle it if the text does not
```

**Attestation** (put it first; "unknown" is an answer):

```text
prior exposure, before this task:
  these excerpts, or the documents they come from                  yes / no / unknown
  any answer key, score, or other reader's answer to them          yes / no / unknown
memory from other conversations                                   on / off / unknown
project or context features (project knowledge, connected
  repositories, custom instructions, attached files)              <list, or "none", or "unknown">
tools used in this task                                            <list, or "none">
```
