# BRANCH_SEARCH — section 5, the branch record's counterpart (or its absence)

Hypothesis (§5): the branch record — *rule as stated / forcing case / axis /
derivation / frame note* — has no slot in any target registrar. Every
registrar handles fixing a claim in advance; none handles the case where the
RULE strains and needs rescoping. **That is a hypothesis, not a finding**,
and §5 says test it, do not assert it.

**The test could not be run here.** §5's test is to search each registrar's
spec for a field that holds a revision-with-a-reason, a scope condition added
after the fact, or an amendment that states WHY (not just WHAT) changed. The
specs were not fetched (egress 403, 2026-09-05T03:30Z). §5 is explicit that
*an absence with no search list is not evidence* — so the absence is **not**
reported as a finding here. What is on record is the **search list**: the
fields that would be searched, per registrar, the moment a spec is fetched.

| registrar | fields to search for a WHY-carrying revision (search list, UNRUN) |
|---|---|
| ClinicalTrials.gov | **protocol amendment records**, amendment reason, history-of-changes, outcome-measure change log — §5 flags this as the most likely place to be wrong; check first and hardest |
| OSF prereg | **prereg addenda**, transparent-changes / deviations sections, registration versioning — §5's other most-likely counterpart; check first and hardest |
| nanopublications | retraction / supersedes / `prov:wasRevisionOf`, and whether any revision carries a reason vs only a pointer |
| ORKG | contribution version history; whether a revision states a reason |
| RO-Crate | crate versioning / change metadata; whether an amendment states WHY |
| CIPM / CMC | CMC revision / re-review records; whether a re-review states the reason for a scope change |
| proof assistants | commit history of a statement's revisions; whether a changed lemma carries a stated reason (a git log, not a format field) |

**Standing rule applied.** If a counterpart is found on a fetched spec, the
branch record is not novel and this file must map to it and say so plainly.
If none is found *after the search list above is run*, the absence is
reportable — with the search list attached. Until the fetch happens, the
correct statement is: **the branch record's novelty is UNVERIFIED**, neither
confirmed nor refuted, and nothing in this repository rests on it being
novel. The two named hot spots (CT.gov amendments, OSF addenda) are where a
"branch record is novel" claim is most likely to be wrong, so they carry the
most weight in the eventual search.
