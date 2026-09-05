# REVERSE_GAPS — section 4, where our format is the weaker one

The survey must record the gaps that run the other way, or it is a sales
document, not a survey (§4). A merge path that only reports what the other
formats lack is disqualified by its own terms.

**Status: UNVERIFIED, and honestly so.** §4 says *verify each candidate
against the spec*. No spec was fetched (egress 403, 2026-09-05T03:30Z), so
none of the candidates below is verified. They are the work order's own §4
candidates, carried, each with the specific thing our format would lack IF
the candidate holds — to be confirmed or dropped against a fetched spec.
Per §4's closing instruction, where no reverse gap is found for a registrar
the finding must state *what was checked*; here **nothing was checked over
the network**, so no registrar can yet be reported as having no reverse gap.

| registrar | candidate reverse gap (UNVERIFIED) | what our format would lack |
|---|---|---|
| CIPM / CMC | carries an uncertainty budget and a traceability chain | MEASURED_AS carries units-with-a-cut but does **not propagate uncertainty**; the import (IN) direction loses the budget |
| ClinicalTrials.gov | enforcement + a public record of outcome switching | ours has **neither enforcement nor an outcome-switch record** |
| proof assistants | the check is mechanical and total | ours is **a human reading a falsifier**, not a total mechanical check |
| nanopublications | provenance is a first-class graph | ours has **a `source_file` string**, not a provenance graph |

Each row names a real direction of loss (import, into our format) that a
"ours is better" framing would hide. None is confirmed here. The strongest
of them for our own format — the CMC uncertainty budget — is the most likely
to force a **branch entry** (§8), because it is a thing a registrar holds
that our format cannot, which is exactly the legitimate trigger to change
the format. **No branch entry is opened on it here**, because opening one
would rest on an unverified spec fact; the trigger is recorded as pending a
verified fetch (see `BRANCH_SEARCH.md`).
