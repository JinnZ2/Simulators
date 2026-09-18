# RESPONSE TO EXTERNAL REVIEW

License: CC0.
Subject: deep-research report on JinnZ2/Simulators, surveyed 14 September 2026.
Response date: 13 September 2026.

This is a response to a review, not a defence of the repository. Recommendations are
sorted by whether the repository's own method supports them. Where the review and the
repository disagree, the disagreement is stated rather than resolved in the
repository's favour.

---

## 1. WHAT THE REVIEW ESTABLISHED

```
SURVEY METHOD    tree walked programmatically; folder counts, Python and Markdown
                 counts, self-test presence and documentation type recorded; each
                 folder's own first substantive prose extracted rather than inferred
                 from the folder name.
ARITHMETIC       internally consistent. Family folder counts sum to 166; file counts
                 sum to 2,673; the F1+F2+F3 share checks at 64.8 against a stated 65.
SCOPE DISCIPLINE the 1-5 audience-fit scores are declared as qualitative judgments,
                 not measurements, in both the method section and the limitations
                 section.
```

The third item is the one worth naming. The review applied to itself the rule the
repository applies to instruments: state whether a number is a measurement or a
judgment. It is accepted on that basis and read as analysis.

---

## 2. WHAT THE REVIEW DID NOT MEASURE

Not a complaint about effort. A statement of what the report can and cannot support.

```
EXECUTION        no instrument in the repository was run.
                 gate-check, self-scan, tools/known_answer.py and the --selftest
                 flags are described and not executed.
                 136 external citations, 0 executions.

FALSIFICATION    no claim in any CLAIM_TABLE was checked against its own falsifier.
                 The claim-plus-falsifier format exists to permit exactly that check,
                 and the review is the first outside party positioned to run it.

CONSEQUENCE      the report is a survey plus a literature scan. Both are useful and
                 neither is an audit. Its scope is the repository AS DOCUMENTED, not
                 the repository AS RUN.
```

REQUEST, if a second pass happens: run `tools/known_answer.py`, run every `--selftest`,
run `gate-check` and `self-scan`, and report the failures. A failing self-test in this
repository is a result, not an embarrassment. So is a claim that its own falsifier
knocks out.

---

## 3. THE ROADMAP COLLIDES WITH THE DURABILITY REGISTER

The review's headline recommendations are a PyPI-installable core, continuous
integration, and a landing page, on the reasoning that they multiply adoption at
trivial cost.

The repository's own durability work scores those differently. Both readings are
stated; neither is withdrawn.

```
                  REVIEW READING              DURABILITY REGISTER READING
PyPI core         distribution, low cost      a CUSTODIAN. Retention becomes
                                              contingent on one holder persisting,
                                              remaining solvent, and keeping the
                                              namespace. Conjunction, not disjunction.

CI                quality gate, low cost      a HOP GENERATOR. Runner images,
                                              action versions and platform policy
                                              are scheduled substrate and dependency
                                              shocks. Hop count is the quantity that
                                              compounds.

landing page      routing, low cost           routing artifact, no custody term.
                                              No collision.
```

RESOLUTION, PARTIAL: the collision is real and is not settled by either document.
Packaging may still be worth the hops. What the register requires is that the cost be
entered on the right ledger rather than scored as trivial.

The discriminating test the register already specifies applies directly: any
arrangement claiming redundancy must state WHAT THE COPIES DO NOT SHARE. A PyPI
release and a GitHub repository under one account share the account, the platform
policy regime and the jurisdiction. For substrate and dependency shock they are one
copy, not two.

STATED CONSTRAINT for any packaging work: it must not become the only readable path.
A stdlib-only tree that can be cloned, copied to a phone, or printed remains the
retention arrangement. A package is an additional convenience surface with a custodian
attached, and is scored as such.

---

## 4. NOT_RUN IS A STATE, NOT A DEBT

The review reads `NOT_RUN` markers as "unfinished falsification loops" and assigns a
credibility cost — "loses a little from each stalled one."

```
REPOSITORY USE   NOT_RUN is a RECORDED STATE. It distinguishes
                 not-measured from measured-and-null, which are different
                 results with different next steps. Recording it is the
                 bookkeeping working, not failing.

REVIEW USE       NOT_RUN is a deficit against an adoption metric.

DIFFERENCE       these are different measurands. Whether to convert a NOT_RUN is a
                 RESOURCE question. The review converts it into a CREDIBILITY
                 question, which the repository does not use and which cannot be
                 answered by running anything.
```

The distinction the review's framing loses: a blank field and a field reading NOT_RUN
carry different information, and collapsing them is the failure mode the format was
built to prevent.

ACCEPTED from the same section: the external dependency behind the July 2026 incident
markers has partly resolved, so those specific markers are now runnable. That is a
correct and useful observation, independent of the credibility framing.

---

## 5. RECOMMENDATION THAT SURVIVES EVERY OBJECTION ABOVE

```
CLAIM EXPORT     a repo-wide pass emitting one normalized JSON Lines record per
                 claim: folder, claim id, confidence mark, state, falsifier.

WHY IT SURVIVES  format-side, not custody-side. Adds no holder.
                 Generated from files already in the tree, so it introduces no
                 dependency and no hop.
                 Makes the corpus queryable without requiring anyone to read it,
                 which is the condition for outside use.
                 It is the serialization of a discipline the repository already
                 runs, not a new claim.

CONSTRAINT       the export must be REGENERABLE FROM THE TREE and must not become
                 the authoritative copy. Markdown stays the source. A derived index
                 that outlives its source is the failure this repository documents
                 elsewhere.
```

---

## 6. CORRECTIONS APPLIED TO THE REPORT ITSELF

Applied on re-audit, recorded in the report's §0.

```
SOURCE           July 2026 Hugging Face agent intrusion.
                 VERIFIED against Hugging Face's technical report of 27 July 2026
                 and the OpenAI disclosure it references. Window, recovered action
                 counts, both injection paths, escalation chain and customer impact
                 confirmed. The report's description of the chain was accurate as
                 written.

WITHDRAWN        "joint METR/Redwood investigation is public" — supported only by a
                 public discussion thread; not confirmed by either first-party
                 disclosure. Removed.

MARKED           "reduced-safeguard evaluation conditions" — same thread. Both
                 disclosures describe an internal capability evaluation; this
                 characterisation was not confirmed. Retained once, marked
                 UNVERIFIED.

DEMOTED          the discussion thread carried four citations and now carries none.
                 A thread is not a source for an incident timeline when both parties
                 have published first-party accounts.

NOT_VERIFIABLE   arXiv identifiers were not re-checked. arxiv.org and
                 export.arxiv.org refuse CONNECT with 403 from the measuring
                 environment; github.com reachable as control, so the refusal is
                 host-specific rather than general egress failure. UNVERIFIED, not
                 disputed.

NOTED            secondary coverage circulates a duration figure that contradicts
                 the primary window. Where they conflict the primary is correct.
```

---

## 7. OPEN

```
O-1  No instrument was run and no claim was checked against its falsifier. The
     repository AS RUN is still unmeasured by any outside party.

O-2  The packaging-versus-custody collision in §3 is stated, not resolved. It needs
     a decision with the hop and custodian costs entered, not a preference.

O-3  Whether the family classification is stable under a different reader is
     untested. The review states alternative groupings are defensible; nobody has
     produced one, so the classification's reproducibility is unknown.

O-4  The audience-fit scores are one reader's judgments and have no second rater.
     Inter-rater agreement is unmeasured, which bounds what the heatmap can be
     used for.

O-5  Non-arXiv citations outside §0 were not individually re-verified.
```
