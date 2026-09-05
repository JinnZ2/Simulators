# QUEUE — falsifier audit

Emitted by `run_all.py`; human-editable and hand-closable. Every entry is
a research question with status OPEN. Ids are stable across runs on an
unchanged tree; close an entry by recording its qid elsewhere.

```
falsifier research queue -- questions, not repairs; status OPEN; unranked
COVERAGE: 304 falsifiers found (290 LOCATED, 14 NOT-FOUND, 8 empty cells skipped); 288 entries by A1-A4 {'A1': 121, 'A2': 145, 'A3': 2, 'A4': 20}
COVERAGE: scanned 1256 .md/.py files; skipped 716 non-.md/.py, 2 binary/non-text, 3 self-excluded (the tool's own queue, samples, and authored docs); skip dirs ['.git', '.mypy_cache', '.pytest_cache', '.ruff_cache', '.venv', '__pycache__', 'legacy', 'node_modules', 'venv']
NOTE A3 (cross-repo incompatibility) emitted 2 entries: on this corpus the numeric-bearing falsifiers on any shared axis are folder-local, so no two folders quantify one axis incompatibly -- the same unquantified property A1 flags. Not silent: the null test fires.

[A1] A1/.:CLAUDE.md:7172   status:OPEN
  falsifier: — counting the rest as a
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/adaptive-claim-loop:adaptive-claim-loop/AUDIT_NOTES.md:56   status:OPEN
  falsifier: the runner reading `claim.status
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/adaptive-claim-loop:adaptive-claim-loop/AUDIT_NOTES.md:58   status:OPEN
  falsifier: this folder claiming a modelling result
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/adaptive-claim-loop:adaptive-claim-loop/AUDIT_NOTES.md:59   status:OPEN
  falsifier: the guard passing a one-sided ladder silently
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/adaptive-claim-loop:adaptive-claim-loop/AUDIT_NOTES.md:61   status:OPEN
  falsifier: a gate that depends on which responder is installed
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/adaptive-claim-loop:adaptive-claim-loop/AUDIT_NOTES.md:63   status:OPEN
  falsifier: a routine deriving either from the text
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/adaptive-claim-loop:adaptive-claim-loop/AUDIT_NOTES.md:67   status:OPEN
  falsifier: the check working at admission time
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/adaptive-claim-loop:adaptive-claim-loop/AUDIT_NOTES.md:68   status:OPEN
  falsifier: a symmetric predicate producing a sweep verdict
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/adaptive-claim-loop:adaptive-claim-loop/AUDIT_NOTES.md:69   status:OPEN
  falsifier: a prose guard that survives paraphrase
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/category-weld:category-weld/AUDIT_NOTES.md:53   status:OPEN
  falsifier: reading the sign convention the other way and finding the docstring consistent
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/category-weld:category-weld/AUDIT_NOTES.md:57   status:OPEN
  falsifier: open` appearing in `TEMPLATE
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/category-weld:category-weld/AUDIT_NOTES.md:58   status:OPEN
  falsifier: a handle in general use that marks the switch
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/category-weld:category-weld/AUDIT_NOTES.md:59   status:OPEN
  falsifier: a field carrying the choice and its reason
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/category-weld:category-weld/CLAIM_TABLE.md:10   status:OPEN
  falsifier: showing max_spread is fully predicted by n_cases across a populated set
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/category-weld:category-weld/CLAIM_TABLE.md:11   status:OPEN
  falsifier: two terms with matching bias where the difference in behaviour requires an intent term to explain
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/category-weld:category-weld/CLAIM_TABLE.md:9   status:OPEN
  falsifier: a term satisfying both that decomposes into one quantity on inspection; or a term failing one that behaves as welded
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/closure-cost:closure-cost/AUDIT_NOTES.md:52   status:OPEN
  falsifier: the rival being dropped, or `not_separable` collapsing into the three failures
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/closure-cost:closure-cost/AUDIT_NOTES.md:54   status:OPEN
  falsifier: comparing against the vocabulary instead of one member of it
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/closure-cost:closure-cost/AUDIT_NOTES.md:55   status:OPEN
  falsifier: the guard `--new` already uses being applied to both
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/closure-cost:closure-cost/AUDIT_NOTES.md:56   status:OPEN
  falsifier: the register's entry already carrying a time term
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/closure-cost:closure-cost/AUDIT_NOTES.md:57   status:OPEN
  falsifier: the field being filled from the error duration
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/closure-cost:closure-cost/AUDIT_NOTES.md:61   status:OPEN
  falsifier: the empty state refusing, or saying it is empty
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/constraint-assembly:constraint-assembly/AUDIT_NOTES.md:57   status:OPEN
  falsifier: the same guard applied to both flags
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/constraint-assembly:constraint-assembly/AUDIT_NOTES.md:58   status:OPEN
  falsifier: the two budgets being different quantities
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/constraint-assembly:constraint-assembly/AUDIT_NOTES.md:59   status:OPEN
  falsifier: the empty state refusing, or saying it is empty
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/constraint-assembly:constraint-assembly/AUDIT_NOTES.md:60   status:OPEN
  falsifier: the two fields being combined, which needs no new field and no new data
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/constraint-assembly:constraint-assembly/AUDIT_NOTES.md:63   status:OPEN
  falsifier: the two budgets being different quantities
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/cooperative-substrate:cooperative-substrate/CLAIM_TABLE.md:13   status:OPEN
  falsifier: a fixture sentence in the pattern vocabulary that is not extracted, or one outside it that is
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/cooperative-substrate:cooperative-substrate/CLAIM_TABLE.md:18   status:OPEN
  falsifier: a disjoint-sense corpus on which the reading is distinguishable from the null
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/cooperative-substrate:cooperative-substrate/CLAIM_TABLE.md:24   status:OPEN
  falsifier: a moral term in a comment or output string that both lists miss and a reader catches
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/cooperative-substrate:cooperative-substrate/README.md:105   status:OPEN
  falsifier: a working inference stack is exhibited whose call sites verify every contract, or which tolerates an adversarial component
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/cooperative-substrate:cooperative-substrate/README.md:106   status:OPEN
  falsifier: term consistency across sources is indistinguishable from the sense-shuffled null
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/cooperative-substrate:cooperative-substrate/WORK_ORDER.md:175   status:OPEN
  falsifier: a working inference stack is exhibited whose call sites verify every contract, or which tolerates an adversarial component
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/cooperative-substrate:cooperative-substrate/WORK_ORDER.md:176   status:OPEN
  falsifier: term consistency across sources is indistinguishable from the sense-shuffled null
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/dependency-survey:dependency-survey/CLAIM_TABLE.md:15   status:OPEN
  falsifier: a MEASURED_AS the heuristic mis-grades that a reader cannot re-check from the flagged output
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/dependency-survey:dependency-survey/CLAIM_TABLE.md:18   status:OPEN
  falsifier: a transform set that sorts into kinds (a result), or that does not (also a result); a build that assigns a kind during coding
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/derivation-discarded:derivation-discarded/AUDIT_NOTES.md:48   status:OPEN
  falsifier: the source review surfacing with those figures
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/derivation-discarded:derivation-discarded/AUDIT_NOTES.md:53   status:OPEN
  falsifier: a schema field for an open, counted, unnamed axis
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/derivation-discarded:derivation-discarded/AUDIT_NOTES.md:54   status:OPEN
  falsifier: the folder arriving
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/domain-ledger:domain-ledger/AUDIT_NOTES.md:56   status:OPEN
  falsifier: a reading on which the four are combinable
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/domain-ledger:domain-ledger/AUDIT_NOTES.md:59   status:OPEN
  falsifier: either field entering `SKELETON
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/domain-ledger:domain-ledger/AUDIT_NOTES.md:62   status:OPEN
  falsifier: the two collapsing anywhere in the readout
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/domain-ledger:domain-ledger/AUDIT_NOTES.md:64   status:OPEN
  falsifier: a link assigned the state
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/domain-ledger:domain-ledger/AUDIT_NOTES.md:65   status:OPEN
  falsifier: a readout separating them
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/domain-ledger:domain-ledger/AUDIT_NOTES.md:66   status:OPEN
  falsifier: any of the three disagreeing
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/domain-ledger:domain-ledger/AUDIT_NOTES.md:68   status:OPEN
  falsifier: the empty state refusing, or saying it is empty
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/domain-ledger:domain-ledger/AUDIT_NOTES.md:69   status:OPEN
  falsifier: the claim table arriving
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/envelope-asymmetry:envelope-asymmetry/CLAIM_TABLE.md:11   status:OPEN
  falsifier: validate_rows`, `render([])
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/falsifier-audit:falsifier-audit/extract.py:11   status:OPEN
  falsifier: " lines, attached to the nearest claim marker
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/falsifier-audit:falsifier-audit/extract.py:148   status:OPEN
  falsifier: ' line."""
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/falsifier-audit:falsifier-audit/inventory.py:68   status:OPEN
  falsifier: '. The others are")
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/falsifier-audit:falsifier-audit/selftest_fa.py:43   status:OPEN
  falsifier: a physical two-option situation
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/falsifier-audit:falsifier-audit/selftest_fa.py:48   status:OPEN
  falsifier: off-gas is not detectable before flaming by a usable margin.
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/held-open-uncertainty:held-open-uncertainty/AUDIT_NOTES.md:37   status:OPEN
  falsifier: the inference entries being presented as findings
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/held-open-uncertainty:held-open-uncertainty/AUDIT_NOTES.md:38   status:OPEN
  falsifier: the harness lacking a pluggable adapter or a response extractor
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/held-open-uncertainty:held-open-uncertainty/AUDIT_NOTES.md:39   status:OPEN
  falsifier: either module emitting a composite
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/held-open-uncertainty:held-open-uncertainty/AUDIT_NOTES.md:40   status:OPEN
  falsifier: the module measuring generation rather than recording it
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/held-open-uncertainty:held-open-uncertainty/AUDIT_NOTES.md:41   status:OPEN
  falsifier: a citation arriving
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/moral-decomposer:moral-decomposer/AUDIT_NOTES.md:46   status:OPEN
  falsifier: decompose.py` arriving with the fixture
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/moral-decomposer:moral-decomposer/AUDIT_NOTES.md:49   status:OPEN
  falsifier: any of the four arriving as a weld file
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/moral-decomposer:moral-decomposer/AUDIT_NOTES.md:50   status:OPEN
  falsifier: a moral term in a field name
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/moral-decomposer:moral-decomposer/AUDIT_NOTES.md:52   status:OPEN
  falsifier: a side with a documented criterion and many cuts, or one cut and an undocumented criterion
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/presented-binary:presented-binary/AUDIT_NOTES.md:63   status:OPEN
  falsifier: the files arriving
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/presented-binary:presented-binary/AUDIT_NOTES.md:67   status:OPEN
  falsifier: the flags appearing in the usage block
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/presented-binary:presented-binary/AUDIT_NOTES.md:68   status:OPEN
  falsifier: a drop that bundles one copy, or bundles copies that match the live file
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/presented-binary:presented-binary/AUDIT_NOTES.md:72   status:OPEN
  falsifier: a second share separating them, or a reading on which the two are the same state
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/presented-binary:presented-binary/AUDIT_NOTES.md:74   status:OPEN
  falsifier: the file existing
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/presented-binary:presented-binary/AUDIT_NOTES.md:76   status:OPEN
  falsifier: the condition widening to `source in ("cued", "none")`, or `--flag` entering the README's main sequence
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/presented-binary:presented-binary/AUDIT_NOTES.md:77   status:OPEN
  falsifier: the test file arriving
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/railcar-containment:railcar-containment/CLAIMS.md:42   status:OPEN
  falsifier: off-gas signatures detectable at practical sensor thresholds do not
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/railcar-containment:railcar-containment/CLAIMS.md:64   status:OPEN
  falsifier: enclosure sizing or hold time turns out to depend on device class in a
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/railcar-containment:railcar-containment/CLAIMS.md:87   status:OPEN
  falsifier: a published transit analysis includes the substituted-mode term.
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:50   status:OPEN
  falsifier: a derivation of the holographic bound that scales with volume, or a demonstration that the simulated state must exceed the physical state
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:52   status:OPEN
  falsifier: a measurement, from inside, of any parent-universe constant
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:54   status:OPEN
  falsifier: a coding scheme in which a system's full state plus a distinguishing marker fits inside that state
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:55   status:OPEN
  falsifier: any of the three turning out to be forced rather than chosen
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:56   status:OPEN
  falsifier: an architecture whose cost is not dominated by its finest level
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:57   status:OPEN
  falsifier: a reason the simulator must resolve vacuum at the same scale as matter
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:64   status:OPEN
  falsifier: a derivation of a nonzero thermodynamic floor on producing a measurement outcome, independent of subsequent erasure
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:68   status:OPEN
  falsifier: a fourth imported boundary condition, or a demonstration that any of the three has a derivation independent of computing practice
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:70   status:OPEN
  falsifier: an architecture in the comparison set that is not drawn from computing practice, or a principled enumeration of the architecture space that does not start from what we build
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:72   status:OPEN
  falsifier: an era-metaphor that became a cosmology and was not superseded, entered into the same table — which the method permits and the table's construction does not
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:77   status:OPEN
  falsifier: a cost model that legitimately charges both a per-timestep stepping cost and a per-transition cost for the same transitions
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:84   status:OPEN
  falsifier: a classical representation of an N-body quantum state whose cost is sub-exponential in N without approximation
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:85   status:OPEN
  falsifier: an exponential load that the physical system demonstrably performs, rather than one arising from our method of computing what it performs
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:88   status:OPEN
  falsifier: a volume-law state with a known sub-exponential exact classical representation, or an area-law state that provably requires exponential classical resources
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:89   status:OPEN
  falsifier: a third instance, which by this claim's own logic should be expected rather than surprising
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:335   status:OPEN
  falsifier: A second sub-ceiling entry, or the register refusing one.
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:339   status:OPEN
  falsifier: One look at the supplementary methods.
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:355   status:OPEN
  falsifier: A three-valued confidence, or `None` being illegal.
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:358   status:OPEN
  falsifier: A design standard carrying a pre-event repair-completion term.
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:360   status:OPEN
  falsifier: The folder arriving, as three of the six prior instances did.
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:375   status:OPEN
  falsifier: Per-question `confidence` on a cluster entry.
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:377   status:OPEN
  falsifier: The pass-through figures failing to match.
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:379   status:OPEN
  falsifier: A published BEA adjustable-vs-non-adjustable real-output decomposition.
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:380   status:OPEN
  falsifier: An input-output framework carrying calories as intermediate consumption.
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:395   status:OPEN
  falsifier: A representation for "this may be two entries, and which is open".
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:396   status:OPEN
  falsifier: A provenance field on entries or sub-questions.
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:397   status:OPEN
  falsifier: Existing objects being renumbered on overflow.
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:398   status:OPEN
  falsifier: Documented renumbering of existing objects at the overflow.
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:399   status:OPEN
  falsifier: A regime where a key remap inflates rather than attenuates.
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:402   status:OPEN
  falsifier: A confidence field carrying an unlock condition.
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:415   status:OPEN
  falsifier: SUPPORTED
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:416   status:OPEN
  falsifier: SUPPORTED
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:419   status:OPEN
  falsifier: SUPPORTED, with one attribution BROADER THAN LOCATED
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:420   status:OPEN
  falsifier: SUPPORTED (structural)
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:421   status:OPEN
  falsifier: SUPPORTED
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:437   status:OPEN
  falsifier: SUPPORTED *(web)*
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:439   status:OPEN
  falsifier: SUPPORTED (narrows and sharpens)
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:440   status:OPEN
  falsifier: SUPPORTED *(web)*
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:441   status:OPEN
  falsifier: SUPPORTED
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:442   status:OPEN
  falsifier: NOT LOCATED (the one number the headline depends on)
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:444   status:OPEN
  falsifier: SUPPORTED
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:454   status:OPEN
  falsifier: SUPPORTED
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:471   status:OPEN
  falsifier: SUPPORTED *(web)*
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:472   status:OPEN
  falsifier: SUPPORTED
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:474   status:OPEN
  falsifier: SUPPORTED
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:476   status:OPEN
  falsifier: SUPPORTED
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:478   status:OPEN
  falsifier: SUPPORTED
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:479   status:OPEN
  falsifier: SUPPORTED (partial)
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A1] A1/uninstrumented:uninstrumented/CLAIM_TABLE.md:480   status:OPEN
  falsifier: SUPPORTED
  question:  what quantity, in what units, would make this falsifier fail?
  detail:    no number, comparison, unit, or observable-outcome word found
[A2] A2/.:README.md:133   status:OPEN
  falsifier: , then claim-table columns under four header names in no fixed position, then fields and JSON keys and block labels — and `extract.py` builds records around the two forms carrying a locatable attached
  question:  which moved -- the claim or the test? 43 of 162 falsifier terms appear in the claim
  detail:    matched: axis, cell, check, checks, claim, constructed, corpus, every, falsifier, fixed, four, none, nothing, null, order, property, read, records, shown, status, table, terms, test, third, tree, whil
[A2] A2/adaptive-claim-loop:adaptive-claim-loop/AUDIT_NOTES.md:57   status:OPEN
  falsifier: the two cases printing differently
  question:  which moved -- the claim or the test? 0 of 3 falsifier terms appear in the claim
  detail:    matched: - | unmatched: cases, differently, printing
[A2] A2/adaptive-claim-loop:adaptive-claim-loop/AUDIT_NOTES.md:58   status:OPEN
  falsifier: this folder claiming a modelling result
  question:  which moved -- the claim or the test? 0 of 4 falsifier terms appear in the claim
  detail:    matched: - | unmatched: claiming, folder, modelling, result
[A2] A2/adaptive-claim-loop:adaptive-claim-loop/AUDIT_NOTES.md:61   status:OPEN
  falsifier: a gate that depends on which responder is installed
  question:  which moved -- the claim or the test? 1 of 4 falsifier terms appear in the claim
  detail:    matched: responder | unmatched: depends, gate, installed
[A2] A2/adaptive-claim-loop:adaptive-claim-loop/AUDIT_NOTES.md:62   status:OPEN
  falsifier: a signal item admitted, or a null item refused
  question:  which moved -- the claim or the test? 1 of 6 falsifier terms appear in the claim
  detail:    matched: null | unmatched: admitted, item, refused, signal
[A2] A2/adaptive-claim-loop:adaptive-claim-loop/AUDIT_NOTES.md:67   status:OPEN
  falsifier: the check working at admission time
  question:  which moved -- the claim or the test? 0 of 4 falsifier terms appear in the claim
  detail:    matched: - | unmatched: admission, check, time, working
[A2] A2/adaptive-claim-loop:adaptive-claim-loop/AUDIT_NOTES.md:68   status:OPEN
  falsifier: a symmetric predicate producing a sweep verdict
  question:  which moved -- the claim or the test? 1 of 5 falsifier terms appear in the claim
  detail:    matched: symmetric | unmatched: predicate, producing, sweep, verdict
[A2] A2/anchor-interval:anchor-interval/CLAIM_TABLE.md:28   status:OPEN
  falsifier: Run `corpus_loop.py` at `lam = 0`. The loop becomes a fixed point on the corpus mean and coupling drift falls from +0.0537 to +0.0063. Any fit that is the identity on its own output kills the effect. 
  question:  which moved -- the claim or the test? 7 of 23 falsifier terms appear in the claim
  detail:    matched: corpus, coupling, fit, lam, loop | unmatched: becomes, claim, corpus_loop, drift, effect, falls, fixed, identity, kills, mean, output, point
[A2] A2/anchor-interval:anchor-interval/CLAIM_TABLE.md:29   status:OPEN
  falsifier: Not empirical: it is what the arithmetic says. Refuted by a corpus loop in which `D1` is non-monotone in the direction of drift, i.e. a fit whose departure from its own training corpus grows as its ou
  question:  which moved -- the claim or the test? 3 of 18 falsifier terms appear in the claim
  detail:    matched: corpus, drift | unmatched: arithmetic, departure, direction, empirical, fit, grows, loop, monotone, non, output, refuted, says
[A2] A2/anchor-interval:anchor-interval/CLAIM_TABLE.md:30   status:OPEN
  falsifier: A statistic computed from corpus history alone that separates the two arms with `TP − FP > 0.5`. The claim is that direction is not in the signal, so any such statistic refutes it.
  question:  which moved -- the claim or the test? 2 of 12 falsifier terms appear in the claim
  detail:    matched: corpus, signal | unmatched: alone, arms, claim, computed, direction, history, refutes, separates, statistic
[A2] A2/anchor-interval:anchor-interval/CLAIM_TABLE.md:31   status:OPEN
  falsifier: Exhibit an internally-computable trigger that fires on the degrading arm and not the improving one. This is `ANC_003`'s falsifier restated as a control question, and one refutation kills both.
  question:  which moved -- the claim or the test? 0 of 15 falsifier terms appear in the claim
  detail:    matched: - | unmatched: anc_, arm, computable, control, degrading, exhibit, falsifier, fires, improving, internally, kills, question
[A2] A2/anchor-interval:anchor-interval/CLAIM_TABLE.md:32   status:OPEN
  falsifier: Name a quantity recoverable from `reported_k` alone that distinguishes `(c rising, a fixed)` from `(c flat, a rising)`. There is none under the stated affine model; a different measurement model with 
  question:  which moved -- the claim or the test? 4 of 26 falsifier terms appear in the claim
  detail:    matched: alone, flat, rising | unmatched: affine, construction, different, difficulty, distinguishes, fixed, identifying, item, measurement, model, name, none
[A2] A2/anchor-interval:anchor-interval/CLAIM_TABLE.md:33   status:OPEN
  falsifier: A fixed-benchmark design that recovers the capability level. Requires `a_0`, `b_0` known independently — which is a traceability claim about the benchmark, and is the thing to go and check.
  question:  which moved -- the claim or the test? 4 of 14 falsifier terms appear in the claim
  detail:    matched: benchmark, capability, fixed | unmatched: check, claim, design, independently, known, level, recovers, requires, thing, traceability
[A2] A2/anchor-interval:anchor-interval/CLAIM_TABLE.md:34   status:OPEN
  falsifier: Measure the actual co-movement of the seven terms across real release pairs and compute `N_eff`. A measured `N_eff > 4` makes the attribution well-posed and refutes the claim for that release series.
  question:  which moved -- the claim or the test? 6 of 21 falsifier terms appear in the claim
  detail:    matched: attribution, movement, n_eff, seven, terms | unmatched: across, actual, claim, compute, makes, measure, measured, pairs, posed, real, refutes, release
[A2] A2/anchor-interval:anchor-interval/CLAIM_TABLE.md:35   status:OPEN
  falsifier: An architectural term chosen without reference to the corpus — transferred from another modality, or fixed before the corpus existed — should decorrelate the pair. Measure the loading for such a term.
  question:  which moved -- the claim or the test? 7 of 27 falsifier terms appear in the claim
  detail:    matched: architectural, corpus, movement, term | unmatched: another, before, chosen, decorrelate, existed, fitted, fixed, high, loading, measure, mechanism, modality
[A2] A2/anchor-interval:anchor-interval/CLAIM_TABLE.md:36   status:OPEN
  falsifier: Measure `f` on a real retraining pool. `f ≈ 0` collapses `K15` (`baseline_freshness`, `../measurement-fork/`) into an ops step and fails the mediation prediction resting on it. `f` well above the floo
  question:  which moved -- the claim or the test? 5 of 27 falsifier terms appear in the claim
  detail:    matched: above, floor, pool, remedy, retraining | unmatched: ask, baseline_freshness, collapses, fails, fork, lose, means, measure, measurement, mediation, ops, precondition
[A2] A2/anchor-interval:anchor-interval/CLAIM_TABLE.md:37   status:OPEN
  falsifier: Not a defect verdict; a gap. The citation markers in `SOURCE_DROP.md` are unresolvable as delivered and one venue attribution is flagged unconfirmed by the drop itself. Falsifier: resolve the citation
  question:  which moved -- the claim or the test? 6 of 59 falsifier terms appear in the claim
  detail:    matched: coupling, drop, instrument, quantity | unmatched: adjacent, attribution, besbes, boundary, budget, carried, check, citation, citations, critique, defect, delivered
[A2] A2/anchor-interval:anchor-interval/CLAIM_TABLE.md:38   status:OPEN
  falsifier: This is a claim about what a medium can hold, and the instrument for it is already in the repo: `../inverseminar/`'s `CANNOT DERIVE` channel, which asks direct questions about load-bearing links the m
  question:  which moved -- the claim or the test? 2 of 44 falsifier terms appear in the claim
  detail:    matched: body, medium | unmatched: already, asks, basis, bearing, cannot, channel, claim, conditional, contain, correction, derive, direct
[A2] A2/category-weld:category-weld/AUDIT_NOTES.md:43   status:OPEN
  falsifier: a fixture failing, or the assertions not covering the two named readouts
  question:  which moved -- the claim or the test? 0 of 6 falsifier terms appear in the claim
  detail:    matched: - | unmatched: assertions, covering, failing, fixture, named, readouts
[A2] A2/category-weld:category-weld/AUDIT_NOTES.md:44   status:OPEN
  falsifier: showing the seed terms' hidden components are carried as separately reportable fields in their own records
  question:  which moved -- the claim or the test? 1 of 11 falsifier terms appear in the claim
  detail:    matched: seed | unmatched: carried, components, fields, hidden, records, reportable, separately, showing, terms, their
[A2] A2/category-weld:category-weld/AUDIT_NOTES.md:45   status:OPEN
  falsifier: a readout in the drop that returns whether the record carries a separate handle
  question:  which moved -- the claim or the test? 2 of 8 falsifier terms appear in the claim
  detail:    matched: drop, readout | unmatched: carries, handle, record, returns, separate, whether
[A2] A2/category-weld:category-weld/AUDIT_NOTES.md:46   status:OPEN
  falsifier: the delivered `rel_change` being multiplicative, so an unmoved component is 1.0 and the spread converges
  question:  which moved -- the claim or the test? 0 of 7 falsifier terms appear in the claim
  detail:    matched: - | unmatched: component, converges, delivered, multiplicative, rel_change, spread, unmoved
[A2] A2/category-weld:category-weld/AUDIT_NOTES.md:47   status:OPEN
  falsifier: a third term whose `n_cases` differs, or either seed term acquiring a quantified case
  question:  which moved -- the claim or the test? 1 of 10 falsifier terms appear in the claim
  detail:    matched: seed | unmatched: acquiring, case, differs, either, n_cases, quantified, term, third
[A2] A2/category-weld:category-weld/AUDIT_NOTES.md:49   status:OPEN
  falsifier: any case in `welds/` acquiring two usable components
  question:  which moved -- the claim or the test? 1 of 5 falsifier terms appear in the claim
  detail:    matched: usable | unmatched: acquiring, case, components, welds
[A2] A2/category-weld:category-weld/AUDIT_NOTES.md:50   status:OPEN
  falsifier: a weld case where the hidden component IS separately named in the record and displaced anyway — that is proxy substitution, not a weld
  question:  which moved -- the claim or the test? 0 of 12 falsifier terms appear in the claim
  detail:    matched: - | unmatched: anyway, case, component, displaced, hidden, named, proxy, record, separately, substitution, weld
[A2] A2/category-weld:category-weld/AUDIT_NOTES.md:51   status:OPEN
  falsifier: a stated denominator for "prone", or a run of the one-term test
  question:  which moved -- the claim or the test? 2 of 6 falsifier terms appear in the claim
  detail:    matched: denominator, term | unmatched: prone, run, stated, test
[A2] A2/category-weld:category-weld/AUDIT_NOTES.md:53   status:OPEN
  falsifier: reading the sign convention the other way and finding the docstring consistent
  question:  which moved -- the claim or the test? 1 of 7 falsifier terms appear in the claim
  detail:    matched: docstring | unmatched: consistent, convention, finding, reading, sign, way
[A2] A2/category-weld:category-weld/AUDIT_NOTES.md:54   status:OPEN
  falsifier: n_cases` counting only cases that have been named
  question:  which moved -- the claim or the test? 0 of 4 falsifier terms appear in the claim
  detail:    matched: - | unmatched: cases, counting, n_cases, named
[A2] A2/category-weld:category-weld/AUDIT_NOTES.md:55   status:OPEN
  falsifier: a fixture exercising the `after <= 0` branch
  question:  which moved -- the claim or the test? 1 of 4 falsifier terms appear in the claim
  detail:    matched: branch | unmatched: after, exercising, fixture
[A2] A2/category-weld:category-weld/AUDIT_NOTES.md:56   status:OPEN
  falsifier: either seed term acquiring a different case count
  question:  which moved -- the claim or the test? 1 of 7 falsifier terms appear in the claim
  detail:    matched: term | unmatched: acquiring, case, count, different, either, seed
[A2] A2/category-weld:category-weld/AUDIT_NOTES.md:59   status:OPEN
  falsifier: a field carrying the choice and its reason
  question:  which moved -- the claim or the test? 1 of 4 falsifier terms appear in the claim
  detail:    matched: choice | unmatched: carrying, field, reason
[A2] A2/category-weld:category-weld/CLAIM_TABLE.md:10   status:OPEN
  falsifier: showing max_spread is fully predicted by n_cases across a populated set
  question:  which moved -- the claim or the test? 1 of 8 falsifier terms appear in the claim
  detail:    matched: n_cases | unmatched: across, fully, max_spread, populated, predicted, set, showing
[A2] A2/category-weld:category-weld/CLAIM_TABLE.md:11   status:OPEN
  falsifier: two terms with matching bias where the difference in behaviour requires an intent term to explain
  question:  which moved -- the claim or the test? 2 of 9 falsifier terms appear in the claim
  detail:    matched: bias, intent | unmatched: behaviour, difference, explain, matching, requires, term, terms
[A2] A2/category-weld:category-weld/CLAIM_TABLE.md:13   status:OPEN
  falsifier: paired series showing density and operators-per-1000-acres track each other across consolidation
  question:  which moved -- the claim or the test? 1 of 9 falsifier terms appear in the claim
  detail:    matched: density | unmatched: acres, across, consolidation, operators, paired, series, showing, track
[A2] A2/category-weld:category-weld/CLAIM_TABLE.md:14   status:OPEN
  falsifier: showing the four move together across intermediated ownership and subsidy structures
  question:  which moved -- the claim or the test? 0 of 9 falsifier terms appear in the claim
  detail:    matched: - | unmatched: across, four, intermediated, move, ownership, showing, structures, subsidy, together
[A2] A2/category-weld:category-weld/CLAIM_TABLE.md:15   status:OPEN
  falsifier: populated readings returning bias near 0
  question:  which moved -- the claim or the test? 0 of 5 falsifier terms appear in the claim
  detail:    matched: - | unmatched: bias, near, populated, readings, returning
[A2] A2/category-weld:category-weld/CLAIM_TABLE.md:8   status:OPEN
  falsifier: showing any of the eight already covers the two seed terms without adding a mechanism
  question:  which moved -- the claim or the test? 1 of 9 falsifier terms appear in the claim
  detail:    matched: eight | unmatched: adding, already, covers, mechanism, seed, showing, terms, without
[A2] A2/category-weld:category-weld/CLAIM_TABLE.md:9   status:OPEN
  falsifier: a term satisfying both that decomposes into one quantity on inspection; or a term failing one that behaves as welded
  question:  which moved -- the claim or the test? 3 of 9 falsifier terms appear in the claim
  detail:    matched: term, welded | unmatched: behaves, decomposes, failing, inspection, quantity, satisfying
[A2] A2/closure-cost:closure-cost/AUDIT_NOTES.md:52   status:OPEN
  falsifier: the rival being dropped, or `not_separable` collapsing into the three failures
  question:  which moved -- the claim or the test? 2 of 6 falsifier terms appear in the claim
  detail:    matched: not_separable, rival | unmatched: collapsing, dropped, failures, three
[A2] A2/closure-cost:closure-cost/AUDIT_NOTES.md:53   status:OPEN
  falsifier: a three-valued return, or `None` being illegal in `AVAILABILITY
  question:  which moved -- the claim or the test? 2 of 6 falsifier terms appear in the claim
  detail:    matched: none, return | unmatched: availability, illegal, three, valued
[A2] A2/closure-cost:closure-cost/AUDIT_NOTES.md:54   status:OPEN
  falsifier: comparing against the vocabulary instead of one member of it
  question:  which moved -- the claim or the test? 0 of 5 falsifier terms appear in the claim
  detail:    matched: - | unmatched: against, comparing, instead, member, vocabulary
[A2] A2/closure-cost:closure-cost/AUDIT_NOTES.md:55   status:OPEN
  falsifier: the guard `--new` already uses being applied to both
  question:  which moved -- the claim or the test? 0 of 5 falsifier terms appear in the claim
  detail:    matched: - | unmatched: already, applied, guard, new, uses
[A2] A2/closure-cost:closure-cost/AUDIT_NOTES.md:57   status:OPEN
  falsifier: the field being filled from the error duration
  question:  which moved -- the claim or the test? 0 of 4 falsifier terms appear in the claim
  detail:    matched: - | unmatched: duration, error, field, filled
[A2] A2/closure-cost:closure-cost/AUDIT_NOTES.md:58   status:OPEN
  falsifier: the case being recoded, or the rule being restated
  question:  which moved -- the claim or the test? 1 of 4 falsifier terms appear in the claim
  detail:    matched: case | unmatched: recoded, restated, rule
[A2] A2/closure-cost:closure-cost/AUDIT_NOTES.md:59   status:OPEN
  falsifier: a three-valued return
  question:  which moved -- the claim or the test? 0 of 3 falsifier terms appear in the claim
  detail:    matched: - | unmatched: return, three, valued
[A2] A2/closure-cost:closure-cost/AUDIT_NOTES.md:60   status:OPEN
  falsifier: either circularity being softened, or a filled rate term
  question:  which moved -- the claim or the test? 1 of 6 falsifier terms appear in the claim
  detail:    matched: filled | unmatched: circularity, either, rate, softened, term
[A2] A2/closure-cost:closure-cost/AUDIT_NOTES.md:61   status:OPEN
  falsifier: the empty state refusing, or saying it is empty
  question:  which moved -- the claim or the test? 0 of 5 falsifier terms appear in the claim
  detail:    matched: - | unmatched: empty, refusing, saying, state
[A2] A2/constraint-assembly:constraint-assembly/AUDIT_NOTES.md:53   status:OPEN
  falsifier: the argument reducing to "constraints are good", or a readout that scores constraint count as quality
  question:  which moved -- the claim or the test? 1 of 9 falsifier terms appear in the claim
  detail:    matched: constraints | unmatched: argument, constraint, count, good, quality, readout, reducing, scores
[A2] A2/constraint-assembly:constraint-assembly/AUDIT_NOTES.md:54   status:OPEN
  falsifier: unknown sufficiency being read as insufficiency, or the selection case being left to prose
  question:  which moved -- the claim or the test? 0 of 8 falsifier terms appear in the claim
  detail:    matched: - | unmatched: case, insufficiency, left, prose, read, selection, sufficiency, unknown
[A2] A2/constraint-assembly:constraint-assembly/AUDIT_NOTES.md:56   status:OPEN
  falsifier: returning `None` when `rejected` is empty, the way `budget_consumed` does one folder over
  question:  which moved -- the claim or the test? 0 of 7 falsifier terms appear in the claim
  detail:    matched: - | unmatched: budget_consumed, empty, folder, none, rejected, returning, way
[A2] A2/constraint-assembly:constraint-assembly/AUDIT_NOTES.md:57   status:OPEN
  falsifier: the same guard applied to both flags
  question:  which moved -- the claim or the test? 0 of 3 falsifier terms appear in the claim
  detail:    matched: - | unmatched: applied, flags, guard
[A2] A2/constraint-assembly:constraint-assembly/AUDIT_NOTES.md:58   status:OPEN
  falsifier: the two budgets being different quantities
  question:  which moved -- the claim or the test? 0 of 3 falsifier terms appear in the claim
  detail:    matched: - | unmatched: budgets, different, quantities
[A2] A2/constraint-assembly:constraint-assembly/AUDIT_NOTES.md:59   status:OPEN
  falsifier: the empty state refusing, or saying it is empty
  question:  which moved -- the claim or the test? 0 of 5 falsifier terms appear in the claim
  detail:    matched: - | unmatched: empty, refusing, saying, state
[A2] A2/constraint-assembly:constraint-assembly/AUDIT_NOTES.md:60   status:OPEN
  falsifier: the two fields being combined, which needs no new field and no new data
  question:  which moved -- the claim or the test? 1 of 7 falsifier terms appear in the claim
  detail:    matched: field | unmatched: combined, data, fields, needs, new
[A2] A2/constraint-assembly:constraint-assembly/AUDIT_NOTES.md:63   status:OPEN
  falsifier: the two budgets being different quantities
  question:  which moved -- the claim or the test? 0 of 3 falsifier terms appear in the claim
  detail:    matched: - | unmatched: budgets, different, quantities
[A2] A2/constraint-assembly:constraint-assembly/AUDIT_NOTES.md:64   status:OPEN
  falsifier: a coefficient, percentage or pressure appearing in a case
  question:  which moved -- the claim or the test? 0 of 5 falsifier terms appear in the claim
  detail:    matched: - | unmatched: appearing, case, coefficient, percentage, pressure
[A2] A2/constraint-assembly:constraint-assembly/AUDIT_NOTES.md:65   status:OPEN
  falsifier: a case built on a novel constraint set, or a during-event record
  question:  which moved -- the claim or the test? 2 of 8 falsifier terms appear in the claim
  detail:    matched: case, record | unmatched: built, constraint, during, event, novel, set
[A2] A2/cooperative-substrate:cooperative-substrate/CLAIM_TABLE.md:16   status:OPEN
  falsifier: a Python where the two counts agree on a file with a comprehension (3.12 inlines them — then the disagreement moves, and the check still prints both)
  question:  which moved -- the claim or the test? 2 of 12 falsifier terms appear in the claim
  detail:    matched: comprehension, file | unmatched: agree, check, counts, disagreement, inlines, moves, prints, python, still, them
[A2] A2/cooperative-substrate:cooperative-substrate/CLAIM_TABLE.md:17   status:OPEN
  falsifier: a corpus on which every term with enough occurrences reads the same way against the null
  question:  which moved -- the claim or the test? 3 of 9 falsifier terms appear in the claim
  detail:    matched: corpus, null, term | unmatched: against, enough, every, occurrences, reads, way
[A2] A2/cooperative-substrate:cooperative-substrate/CLAIM_TABLE.md:23   status:OPEN
  falsifier: — (the repair is the second column; the check is that the two readings are printed apart)
  question:  which moved -- the claim or the test? 1 of 7 falsifier terms appear in the claim
  detail:    matched: readings | unmatched: apart, check, column, printed, repair, second
[A2] A2/cooperative-substrate:cooperative-substrate/CLAIM_TABLE.md:24   status:OPEN
  falsifier: a moral term in a comment or output string that both lists miss and a reader catches
  question:  which moved -- the claim or the test? 2 of 9 falsifier terms appear in the claim
  detail:    matched: moral, output | unmatched: catches, comment, lists, miss, reader, string, term
[A2] A2/cooperative-substrate:cooperative-substrate/CLAIM_TABLE.md:38   status:OPEN
  falsifier: a row opened and found not to say what the pack says; a locator that resolves to a different paper
  question:  which moved -- the claim or the test? 3 of 10 falsifier terms appear in the claim
  detail:    matched: locator, pack, row | unmatched: different, found, opened, paper, resolves, say, says
[A2] A2/cooperative-substrate:cooperative-substrate/CLAIM_TABLE.md:67   status:OPEN
  falsifier: the paper read here and found not to say it
  question:  which moved -- the claim or the test? 0 of 4 falsifier terms appear in the claim
  detail:    matched: - | unmatched: found, paper, read, say
[A2] A2/derivation-discarded:derivation-discarded/AUDIT_NOTES.md:48   status:OPEN
  falsifier: the source review surfacing with those figures
  question:  which moved -- the claim or the test? 1 of 4 falsifier terms appear in the claim
  detail:    matched: review | unmatched: figures, source, surfacing
[A2] A2/derivation-discarded:derivation-discarded/AUDIT_NOTES.md:49   status:OPEN
  falsifier: a study composing the narrowings into one figure
  question:  which moved -- the claim or the test? 1 of 4 falsifier terms appear in the claim
  detail:    matched: narrowings | unmatched: composing, figure, study
[A2] A2/domain-ledger:domain-ledger/AUDIT_NOTES.md:56   status:OPEN
  falsifier: a reading on which the four are combinable
  question:  which moved -- the claim or the test? 1 of 3 falsifier terms appear in the claim
  detail:    matched: four | unmatched: combinable, reading
[A2] A2/domain-ledger:domain-ledger/AUDIT_NOTES.md:58   status:OPEN
  falsifier: a footer clause naming what the denominator includes, or a separate ratio
  question:  which moved -- the claim or the test? 1 of 7 falsifier terms appear in the claim
  detail:    matched: denominator | unmatched: clause, footer, includes, naming, ratio, separate
[A2] A2/domain-ledger:domain-ledger/AUDIT_NOTES.md:59   status:OPEN
  falsifier: either field entering `SKELETON
  question:  which moved -- the claim or the test? 1 of 4 falsifier terms appear in the claim
  detail:    matched: skeleton | unmatched: either, entering, field
[A2] A2/domain-ledger:domain-ledger/AUDIT_NOTES.md:60   status:OPEN
  falsifier: the derived column filling in and disagreeing with 0.61
  question:  which moved -- the claim or the test? 1 of 4 falsifier terms appear in the claim
  detail:    matched: derived | unmatched: column, disagreeing, filling
[A2] A2/domain-ledger:domain-ledger/AUDIT_NOTES.md:62   status:OPEN
  falsifier: the two collapsing anywhere in the readout
  question:  which moved -- the claim or the test? 1 of 3 falsifier terms appear in the claim
  detail:    matched: collapsing | unmatched: anywhere, readout
[A2] A2/domain-ledger:domain-ledger/AUDIT_NOTES.md:63   status:OPEN
  falsifier: the first anchor map, which shows they are different quantities and the code aggregates the right one
  question:  which moved -- the claim or the test? 0 of 10 falsifier terms appear in the claim
  detail:    matched: - | unmatched: aggregates, anchor, code, different, first, map, quantities, right, shows, they
[A2] A2/domain-ledger:domain-ledger/AUDIT_NOTES.md:64   status:OPEN
  falsifier: a link assigned the state
  question:  which moved -- the claim or the test? 1 of 3 falsifier terms appear in the claim
  detail:    matched: link | unmatched: assigned, state
[A2] A2/domain-ledger:domain-ledger/AUDIT_NOTES.md:65   status:OPEN
  falsifier: a readout separating them
  question:  which moved -- the claim or the test? 1 of 3 falsifier terms appear in the claim
  detail:    matched: them | unmatched: readout, separating
[A2] A2/domain-ledger:domain-ledger/AUDIT_NOTES.md:67   status:OPEN
  falsifier: a derivation for 0.30 / 0.80 / 0.99, or a disclosure line
  question:  which moved -- the claim or the test? 1 of 3 falsifier terms appear in the claim
  detail:    matched: derivation | unmatched: disclosure, line
[A2] A2/domain-ledger:domain-ledger/AUDIT_NOTES.md:68   status:OPEN
  falsifier: the empty state refusing, or saying it is empty
  question:  which moved -- the claim or the test? 0 of 5 falsifier terms appear in the claim
  detail:    matched: - | unmatched: empty, refusing, saying, state
[A2] A2/domain-ledger:domain-ledger/AUDIT_NOTES.md:69   status:OPEN
  falsifier: the claim table arriving
  question:  which moved -- the claim or the test? 0 of 3 falsifier terms appear in the claim
  detail:    matched: - | unmatched: arriving, claim, table
[A2] A2/domain-ledger:domain-ledger/AUDIT_NOTES.md:70   status:OPEN
  falsifier: a routine deriving the class from something measured
  question:  which moved -- the claim or the test? 1 of 5 falsifier terms appear in the claim
  detail:    matched: class | unmatched: deriving, measured, routine, something
[A2] A2/envelope-asymmetry:envelope-asymmetry/CLAIM_TABLE.md:13   status:OPEN
  falsifier: a paired statistic on which the two accountings agree while the absence rate is non-zero
  question:  which moved -- the claim or the test? 2 of 9 falsifier terms appear in the claim
  detail:    matched: absence, rate | unmatched: accountings, agree, non, paired, statistic, while, zero
[A2] A2/envelope-asymmetry:envelope-asymmetry/CLAIM_TABLE.md:14   status:OPEN
  falsifier: — (a third state, E6 varying, is the SUPPORTED branch)
  question:  which moved -- the claim or the test? 1 of 5 falsifier terms appear in the claim
  detail:    matched: state | unmatched: branch, supported, third, varying
[A2] A2/envelope-asymmetry:envelope-asymmetry/CLAIM_TABLE.md:20   status:OPEN
  falsifier: the two tests run on coded documents
  question:  which moved -- the claim or the test? 0 of 4 falsifier terms appear in the claim
  detail:    matched: - | unmatched: coded, documents, run, tests
[A2] A2/falsifier-audit:falsifier-audit/selftest_fa.py:43   status:OPEN
  falsifier: a physical two-option situation
  question:  which moved -- the claim or the test? 1 of 3 falsifier terms appear in the claim
  detail:    matched: option | unmatched: physical, situation
[A2] A2/falsifier-audit:falsifier-audit/selftest_fa.py:48   status:OPEN
  falsifier: off-gas is not detectable before flaming by a usable margin.
  question:  which moved -- the claim or the test? 0 of 6 falsifier terms appear in the claim
  detail:    matched: - | unmatched: before, detectable, flaming, gas, margin, usable
[A2] A2/falsifier-audit:falsifier-audit/selftest_fa.py:66   status:OPEN
  falsifier: ' parsed with the claim attached from the bold line above",
  question:  which moved -- the claim or the test? 0 of 6 falsifier terms appear in the claim
  detail:    matched: - | unmatched: above, attached, bold, claim, line, parsed
[A2] A2/held-open-uncertainty:held-open-uncertainty/AUDIT_NOTES.md:37   status:OPEN
  falsifier: the inference entries being presented as findings
  question:  which moved -- the claim or the test? 0 of 4 falsifier terms appear in the claim
  detail:    matched: - | unmatched: entries, findings, inference, presented
[A2] A2/held-open-uncertainty:held-open-uncertainty/AUDIT_NOTES.md:39   status:OPEN
  falsifier: either module emitting a composite
  question:  which moved -- the claim or the test? 1 of 4 falsifier terms appear in the claim
  detail:    matched: composite | unmatched: either, emitting, module
[A2] A2/held-open-uncertainty:held-open-uncertainty/AUDIT_NOTES.md:40   status:OPEN
  falsifier: the module measuring generation rather than recording it
  question:  which moved -- the claim or the test? 1 of 5 falsifier terms appear in the claim
  detail:    matched: module | unmatched: generation, measuring, rather, recording
[A2] A2/held-open-uncertainty:held-open-uncertainty/AUDIT_NOTES.md:42   status:OPEN
  falsifier: a control arm existing
  question:  which moved -- the claim or the test? 1 of 3 falsifier terms appear in the claim
  detail:    matched: control | unmatched: arm, existing
[A2] A2/moral-decomposer:moral-decomposer/AUDIT_NOTES.md:46   status:OPEN
  falsifier: decompose.py` arriving with the fixture
  question:  which moved -- the claim or the test? 1 of 3 falsifier terms appear in the claim
  detail:    matched: decompose | unmatched: arriving, fixture
[A2] A2/moral-decomposer:moral-decomposer/AUDIT_NOTES.md:47   status:OPEN
  falsifier: a third value, or a check on `resolved
  question:  which moved -- the claim or the test? 1 of 4 falsifier terms appear in the claim
  detail:    matched: resolved | unmatched: check, third, value
[A2] A2/moral-decomposer:moral-decomposer/AUDIT_NOTES.md:48   status:OPEN
  falsifier: a case where the two disagree and the tool says so
  question:  which moved -- the claim or the test? 0 of 4 falsifier terms appear in the claim
  detail:    matched: - | unmatched: case, disagree, says, tool
[A2] A2/moral-decomposer:moral-decomposer/AUDIT_NOTES.md:49   status:OPEN
  falsifier: any of the four arriving as a weld file
  question:  which moved -- the claim or the test? 1 of 4 falsifier terms appear in the claim
  detail:    matched: weld | unmatched: arriving, file, four
[A2] A2/moral-decomposer:moral-decomposer/AUDIT_NOTES.md:52   status:OPEN
  falsifier: a side with a documented criterion and many cuts, or one cut and an undocumented criterion
  question:  which moved -- the claim or the test? 0 of 8 falsifier terms appear in the claim
  detail:    matched: - | unmatched: criterion, cut, cuts, documented, many, side, undocumented
[A2] A2/presented-binary:presented-binary/AUDIT_NOTES.md:64   status:OPEN
  falsifier: a path from tampered pass 1 to a recorded pass 3 that is refused
  question:  which moved -- the claim or the test? 2 of 6 falsifier terms appear in the claim
  detail:    matched: pass | unmatched: path, recorded, refused, tampered
[A2] A2/presented-binary:presented-binary/AUDIT_NOTES.md:65   status:OPEN
  falsifier: the prompts being generated or held outside the file the operator runs
  question:  which moved -- the claim or the test? 1 of 7 falsifier terms appear in the claim
  detail:    matched: operator | unmatched: file, generated, held, outside, prompts, runs
[A2] A2/presented-binary:presented-binary/AUDIT_NOTES.md:66   status:OPEN
  falsifier: the two states returning different values
  question:  which moved -- the claim or the test? 0 of 4 falsifier terms appear in the claim
  detail:    matched: - | unmatched: different, returning, states, values
[A2] A2/presented-binary:presented-binary/AUDIT_NOTES.md:67   status:OPEN
  falsifier: the flags appearing in the usage block
  question:  which moved -- the claim or the test? 1 of 4 falsifier terms appear in the claim
  detail:    matched: usage | unmatched: appearing, block, flags
[A2] A2/presented-binary:presented-binary/AUDIT_NOTES.md:69   status:OPEN
  falsifier: the two states returning different values
  question:  which moved -- the claim or the test? 0 of 4 falsifier terms appear in the claim
  detail:    matched: - | unmatched: different, returning, states, values
[A2] A2/presented-binary:presented-binary/AUDIT_NOTES.md:70   status:OPEN
  falsifier: a case with O1 documented and a stated count
  question:  which moved -- the claim or the test? 1 of 4 falsifier terms appear in the claim
  detail:    matched: case | unmatched: count, documented, stated
[A2] A2/presented-binary:presented-binary/AUDIT_NOTES.md:71   status:OPEN
  falsifier: a run where the flag is scored from the reasoning text by a reader that never saw the field
  question:  which moved -- the claim or the test? 2 of 9 falsifier terms appear in the claim
  detail:    matched: flag, reasoning | unmatched: field, never, reader, run, saw, scored, text
[A2] A2/presented-binary:presented-binary/AUDIT_NOTES.md:72   status:OPEN
  falsifier: a second share separating them, or a reading on which the two are the same state
  question:  which moved -- the claim or the test? 0 of 6 falsifier terms appear in the claim
  detail:    matched: - | unmatched: reading, second, separating, share, state, them
[A2] A2/presented-binary:presented-binary/AUDIT_NOTES.md:75   status:OPEN
  falsifier: the seal refusing a pass 1 without the flag
  question:  which moved -- the claim or the test? 1 of 5 falsifier terms appear in the claim
  detail:    matched: pass | unmatched: flag, refusing, seal, without
[A2] A2/presented-binary:presented-binary/CLAIM_TABLE.md:12   status:OPEN
  falsifier: a use of the term in policy or planning that carries functional position separately
  question:  which moved -- the claim or the test? 2 of 8 falsifier terms appear in the claim
  detail:    matched: functional, position | unmatched: carries, planning, policy, separately, term, use
[A2] A2/presented-binary:presented-binary/CLAIM_TABLE.md:13   status:OPEN
  falsifier: a selection process that reliably separates the two from the output alone
  question:  which moved -- the claim or the test? 1 of 6 falsifier terms appear in the claim
  detail:    matched: output | unmatched: alone, process, reliably, selection, separates
[A2] A2/presented-binary:presented-binary/CLAIM_TABLE.md:14   status:OPEN
  falsifier: frame_sim runs where option_gain is consistently zero across varied problems
  question:  which moved -- the claim or the test? 0 of 8 falsifier terms appear in the claim
  detail:    matched: - | unmatched: across, consistently, frame_sim, option_gain, problems, runs, varied, zero
[A2] A2/presented-binary:presented-binary/CLAIM_TABLE.md:15   status:OPEN
  falsifier: runs where frame_flagged is consistently true
  question:  which moved -- the claim or the test? 0 of 4 falsifier terms appear in the claim
  detail:    matched: - | unmatched: consistently, frame_flagged, runs, true
[A2] A2/presented-binary:presented-binary/CLAIM_TABLE.md:16   status:OPEN
  falsifier: runs where dominated_on_own_metric is consistently false while option_gain is high
  question:  which moved -- the claim or the test? 0 of 7 falsifier terms appear in the claim
  detail:    matched: - | unmatched: consistently, dominated_on_own_metric, false, high, option_gain, runs, while
[A2] A2/presented-binary:presented-binary/CLAIM_TABLE.md:8   status:OPEN
  falsifier: a two-option situation where the third option is absent on physical grounds rather than by authored constraint, and where the option space was not closed by earlier decisions
  question:  which moved -- the claim or the test? 0 of 15 falsifier terms appear in the claim
  detail:    matched: - | unmatched: absent, authored, closed, constraint, decisions, earlier, grounds, option, physical, rather, situation, space
[A2] A2/presented-binary:presented-binary/CLAIM_TABLE.md:9   status:OPEN
  falsifier: a presented binary where the presenting party has no prior decision in the causal chain that narrowed the set
  question:  which moved -- the claim or the test? 2 of 10 falsifier terms appear in the claim
  detail:    matched: binary, party | unmatched: causal, chain, decision, narrowed, presented, presenting, prior, set
[A2] A2/railcar-containment:railcar-containment/CLAIMS.md:11   status:OPEN
  falsifier: measured tenability in a metro-volume car equals or exceeds the
  question:  which moved -- the claim or the test? 1 of 7 falsifier terms appear in the claim
  detail:    matched: tenability | unmatched: car, equals, exceeds, measured, metro, volume
[A2] A2/railcar-containment:railcar-containment/CLAIMS.md:21   status:OPEN
  falsifier: an enclosure achieving ≤20% cabin gas fraction fails to extend
  question:  which moved -- the claim or the test? 2 of 7 falsifier terms appear in the claim
  detail:    matched: cabin, fraction | unmatched: achieving, enclosure, extend, fails, gas
[A2] A2/railcar-containment:railcar-containment/CLAIMS.md:31   status:OPEN
  falsifier: a line's worst-case egress interval cannot be bounded from
  question:  which moved -- the claim or the test? 0 of 7 falsifier terms appear in the claim
  detail:    matched: - | unmatched: bounded, cannot, case, egress, interval, line, worst
[A2] A2/railcar-containment:railcar-containment/CLAIMS.md:42   status:OPEN
  falsifier: off-gas signatures detectable at practical sensor thresholds do not
  question:  which moved -- the claim or the test? 0 of 6 falsifier terms appear in the claim
  detail:    matched: - | unmatched: detectable, gas, practical, sensor, signatures, thresholds
[A2] A2/railcar-containment:railcar-containment/CLAIMS.md:53   status:OPEN
  falsifier: a timeline model with realistic latencies shows detection improvement
  question:  which moved -- the claim or the test? 1 of 7 falsifier terms appear in the claim
  detail:    matched: detection | unmatched: improvement, latencies, model, realistic, shows, timeline
[A2] A2/railcar-containment:railcar-containment/CLAIMS.md:64   status:OPEN
  falsifier: enclosure sizing or hold time turns out to depend on device class in a
  question:  which moved -- the claim or the test? 1 of 8 falsifier terms appear in the claim
  detail:    matched: device | unmatched: class, depend, enclosure, hold, sizing, time, turns
[A2] A2/railcar-containment:railcar-containment/CLAIMS.md:76   status:OPEN
  falsifier: incident-rate data shows P(initiation) rising with capacity after
  question:  which moved -- the claim or the test? 1 of 8 falsifier terms appear in the claim
  detail:    matched: capacity | unmatched: after, data, incident, initiation, rate, rising, shows
[A2] A2/railcar-containment:railcar-containment/CLAIMS.md:87   status:OPEN
  falsifier: a published transit analysis includes the substituted-mode term.
  question:  which moved -- the claim or the test? 1 of 7 falsifier terms appear in the claim
  detail:    matched: analysis | unmatched: includes, mode, published, substituted, term, transit
[A2] A2/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:50   status:OPEN
  falsifier: a derivation of the holographic bound that scales with volume, or a demonstration that the simulated state must exceed the physical state
  question:  which moved -- the claim or the test? 3 of 12 falsifier terms appear in the claim
  detail:    matched: state, volume | unmatched: bound, demonstration, derivation, exceed, holographic, must, physical, scales, simulated
[A2] A2/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:53   status:OPEN
  falsifier: an argument that a simulation must resolve below what its inhabitants can measure
  question:  which moved -- the claim or the test? 1 of 7 falsifier terms appear in the claim
  detail:    matched: argument | unmatched: below, inhabitants, measure, must, resolve, simulation
[A2] A2/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:57   status:OPEN
  falsifier: a reason the simulator must resolve vacuum at the same scale as matter
  question:  which moved -- the claim or the test? 2 of 7 falsifier terms appear in the claim
  detail:    matched: matter, scale | unmatched: must, reason, resolve, simulator, vacuum
[A2] A2/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:66   status:OPEN
  falsifier: a consequence that is observed, and uncomputed under an architecture that can still produce its own observation record — which would refute `SHB_011` outright
  question:  which moved -- the claim or the test? 1 of 11 falsifier terms appear in the claim
  detail:    matched: shb_ | unmatched: architecture, consequence, observation, observed, outright, produce, record, refute, still, uncomputed
[A2] A2/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:68   status:OPEN
  falsifier: a fourth imported boundary condition, or a demonstration that any of the three has a derivation independent of computing practice
  question:  which moved -- the claim or the test? 3 of 10 falsifier terms appear in the claim
  detail:    matched: boundary, imported, three | unmatched: computing, condition, demonstration, derivation, fourth, independent, practice
[A2] A2/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:69   status:OPEN
  falsifier: a fifth interpretive step, which by this claim's own logic should be expected rather than surprising
  question:  which moved -- the claim or the test? 2 of 9 falsifier terms appear in the claim
  detail:    matched: interpretive, step | unmatched: claim, expected, fifth, logic, rather, should, surprising
[A2] A2/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:81   status:OPEN
  falsifier: a stated construction for the row that fixes it at either value
  question:  which moved -- the claim or the test? 2 of 6 falsifier terms appear in the claim
  detail:    matched: row, value | unmatched: construction, either, fixes, stated
[A2] A2/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:84   status:OPEN
  falsifier: a classical representation of an N-body quantum state whose cost is sub-exponential in N without approximation
  question:  which moved -- the claim or the test? 3 of 10 falsifier terms appear in the claim
  detail:    matched: classical, quantum, state | unmatched: approximation, body, cost, exponential, representation, sub, without
[A2] A2/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:89   status:OPEN
  falsifier: a third instance, which by this claim's own logic should be expected rather than surprising
  question:  which moved -- the claim or the test? 1 of 8 falsifier terms appear in the claim
  detail:    matched: instance | unmatched: claim, expected, logic, rather, should, surprising, third
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:334   status:OPEN
  falsifier: An `UNASSIGNED` sentinel with `candidates` and a required `why_open`, so an unfiled entry is a state the sort can count.
  question:  which moved -- the claim or the test? 2 of 10 falsifier terms appear in the claim
  detail:    matched: entry, unassigned | unmatched: candidates, count, required, sentinel, sort, state, unfiled, why_open
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:335   status:OPEN
  falsifier: A second sub-ceiling entry, or the register refusing one.
  question:  which moved -- the claim or the test? 2 of 6 falsifier terms appear in the claim
  detail:    matched: ceiling, entry | unmatched: refusing, register, second, sub
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:336   status:OPEN
  falsifier: Any stated detail failing to match the article.
  question:  which moved -- the claim or the test? 1 of 5 falsifier terms appear in the claim
  detail:    matched: stated | unmatched: article, detail, failing, match
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:337   status:OPEN
  falsifier: The two found metrics turning out to be co-varying measurements.
  question:  which moved -- the claim or the test? 0 of 5 falsifier terms appear in the claim
  detail:    matched: - | unmatched: found, measurements, metrics, turning, varying
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:339   status:OPEN
  falsifier: One look at the supplementary methods.
  question:  which moved -- the claim or the test? 1 of 3 falsifier terms appear in the claim
  detail:    matched: supplementary | unmatched: look, methods
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:340   status:OPEN
  falsifier: A stated device count and resolvable margin, which would close the gap.
  question:  which moved -- the claim or the test? 1 of 7 falsifier terms appear in the claim
  detail:    matched: margin | unmatched: close, count, device, gap, resolvable, stated
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:358   status:OPEN
  falsifier: A design standard carrying a pre-event repair-completion term.
  question:  which moved -- the claim or the test? 2 of 8 falsifier terms appear in the claim
  detail:    matched: design, standard | unmatched: carrying, completion, event, pre, repair, term
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:360   status:OPEN
  falsifier: The folder arriving, as three of the six prior instances did.
  question:  which moved -- the claim or the test? 1 of 6 falsifier terms appear in the claim
  detail:    matched: three | unmatched: arriving, folder, instances, prior, six
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:374   status:OPEN
  falsifier: An arrangement of classes where the identity fails.
  question:  which moved -- the claim or the test? 0 of 4 falsifier terms appear in the claim
  detail:    matched: - | unmatched: arrangement, classes, fails, identity
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:377   status:OPEN
  falsifier: The pass-through figures failing to match.
  question:  which moved -- the claim or the test? 1 of 4 falsifier terms appear in the claim
  detail:    matched: pass | unmatched: failing, figures, match
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:395   status:OPEN
  falsifier: A representation for "this may be two entries, and which is open".
  question:  which moved -- the claim or the test? 1 of 3 falsifier terms appear in the claim
  detail:    matched: entries | unmatched: open, representation
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:397   status:OPEN
  falsifier: Existing objects being renumbered on overflow.
  question:  which moved -- the claim or the test? 0 of 4 falsifier terms appear in the claim
  detail:    matched: - | unmatched: existing, objects, overflow, renumbered
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:438   status:OPEN
  falsifier: SUPPORTED (refutes the stated mechanism)
  question:  which moved -- the claim or the test? 1 of 4 falsifier terms appear in the claim
  detail:    matched: mechanism | unmatched: refutes, stated, supported
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:439   status:OPEN
  falsifier: SUPPORTED (narrows and sharpens)
  question:  which moved -- the claim or the test? 0 of 3 falsifier terms appear in the claim
  detail:    matched: - | unmatched: narrows, sharpens, supported
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:46   status:OPEN
  falsifier: File a second entry under an existing mechanism from a different field. That is not a refutation of the claim so much as its expiry condition, and it is the cheapest next move on this folder.
  question:  which moved -- the claim or the test? 2 of 16 falsifier terms appear in the claim
  detail:    matched: field, mechanism | unmatched: cheapest, claim, condition, different, entry, existing, expiry, file, folder, move, much, next
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:47   status:OPEN
  falsifier: A set of definitions under which each of the seven entries has exactly one applicable mechanism, and which does not achieve it by narrowing a mechanism until it names one case.
  question:  which moved -- the claim or the test? 4 of 13 falsifier terms appear in the claim
  detail:    matched: case, entries, mechanism | unmatched: achieve, applicable, definitions, exactly, names, narrowing, set, seven, until
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:475   status:OPEN
  falsifier: SUPPORTED — and it corrects a delivered reading
  question:  which moved -- the claim or the test? 0 of 4 falsifier terms appear in the claim
  detail:    matched: - | unmatched: corrects, delivered, reading, supported
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:48   status:OPEN
  falsifier: An instrument in that corpus for which one of the seven mechanisms genuinely fires. The likeliest candidate is satellite SST at M3: if heavy model dependence counts as a mechanism, the boundary moves 
  question:  which moved -- the claim or the test? 2 of 19 falsifier terms appear in the claim
  detail:    matched: corpus, instrument | unmatched: boundary, candidate, counts, dependence, fires, genuinely, heavy, likeliest, mechanism, mechanisms, model, moves
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:49   status:OPEN
  falsifier: A case with a full blindness map that is nonetheless excluded by construction, or a case with no blindness map that is merely under-investigated. Either breaks the criterion.
  question:  which moved -- the claim or the test? 5 of 15 falsifier terms appear in the claim
  detail:    matched: blindness, excluded, map | unmatched: breaks, case, construction, criterion, either, full, investigated, merely, nonetheless
[A2] A2/uninstrumented:uninstrumented/CLAIM_TABLE.md:50   status:OPEN
  falsifier: File a quantity a field believes it measures and does not, and see whether the register's mechanism set names why. Until that runs, `UNI_004`'s clean null result is weaker than it looks: a classifier 
  question:  which moved -- the claim or the test? 4 of 26 falsifier terms appear in the claim
  detail:    matched: fire, null, register | unmatched: believes, classifier, clean, field, file, fires, looks, measures, mechanism, names, never, quantity
[A3] A3/axis:coverage   status:OPEN
  falsifier: , then claim-table columns under four header names in no fixed position, then fi; a headroom field, or a flag when coverage exceeds the ceiling
  question:  on axis 'coverage', repos ., domain-ledger carry different numeric cutoffs; what distinguishes the contexts, and is the difference real or is one cutoff inherited?
  detail:    members: .:README.md:133 [12,283,289,301,8] | domain-ledger:domain-ledger/AUDIT_NOTES.md:57 []
[A3] A3/axis:drift   status:OPEN
  falsifier: , then claim-table columns under four header names in no fixed position, then fi; Run `corpus_loop.py` at `lam = 0`. The loop becomes a fixed point on the corpus ; Not a defect verdict; a gap. The cit
  question:  on axis 'drift', repos ., anchor-interval carry different numeric cutoffs; what distinguishes the contexts, and is the difference real or is one cutoff inherited?
  detail:    members: .:README.md:133 [12,283,289,301,8] | anchor-interval:anchor-interval/CLAIM_TABLE.md:28 [+0.0063,+0.0537,0] | anchor-interval:anchor-interval/CLAIM_TABLE.md:37 [1,1983,2,3]
[A4] A4/.:README.md:133   status:OPEN
  falsifier: , then claim-table columns under four header names in no fixed position, then fields and JSON keys and block labels — and `extract.py` builds records around the two forms carrying a locatable attached
  question:  what is the reference body here (baseline, matched, reference, the null, the same), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): baseline, matched, reference, the null, the same
[A4] A4/adaptive-claim-loop:adaptive-claim-loop/AUDIT_NOTES.md:62   status:OPEN
  falsifier: a signal item admitted, or a null item refused
  question:  what is the reference body here (a null), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): a null
[A4] A4/anchor-interval:anchor-interval/CLAIM_TABLE.md:31   status:OPEN
  falsifier: Exhibit an internally-computable trigger that fires on the degrading arm and not the improving one. This is `ANC_003`'s falsifier restated as a control question, and one refutation kills both.
  question:  what is the reference body here (control), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): control
[A4] A4/anchor-interval:anchor-interval/CLAIM_TABLE.md:35   status:OPEN
  falsifier: An architectural term chosen without reference to the corpus — transferred from another modality, or fixed before the corpus existed — should decorrelate the pair. Measure the loading for such a term.
  question:  what is the reference body here (reference), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): reference
[A4] A4/anchor-interval:anchor-interval/CLAIM_TABLE.md:36   status:OPEN
  falsifier: Measure `f` on a real retraining pool. `f ≈ 0` collapses `K15` (`baseline_freshness`, `../measurement-fork/`) into an ops step and fails the mediation prediction resting on it. `f` well above the floo
  question:  what is the reference body here (baseline), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): baseline
[A4] A4/closure-cost:closure-cost/AUDIT_NOTES.md:54   status:OPEN
  falsifier: comparing against the vocabulary instead of one member of it
  question:  what is the reference body here (against the), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): against the
[A4] A4/constraint-assembly:constraint-assembly/AUDIT_NOTES.md:57   status:OPEN
  falsifier: the same guard applied to both flags
  question:  what is the reference body here (the same), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): the same
[A4] A4/cooperative-substrate:cooperative-substrate/CLAIM_TABLE.md:17   status:OPEN
  falsifier: a corpus on which every term with enough occurrences reads the same way against the null
  question:  what is the reference body here (against the, the null, the same), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): against the, the null, the same
[A4] A4/cooperative-substrate:cooperative-substrate/CLAIM_TABLE.md:18   status:OPEN
  falsifier: a disjoint-sense corpus on which the reading is distinguishable from the null
  question:  what is the reference body here (the null), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): the null
[A4] A4/cooperative-substrate:cooperative-substrate/CLAIM_TABLE.md:61   status:OPEN
  falsifier: a reachable study set that runs the null
  question:  what is the reference body here (the null), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): the null
[A4] A4/held-open-uncertainty:held-open-uncertainty/AUDIT_NOTES.md:42   status:OPEN
  falsifier: a control arm existing
  question:  what is the reference body here (control), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): control
[A4] A4/presented-binary:presented-binary/AUDIT_NOTES.md:72   status:OPEN
  falsifier: a second share separating them, or a reading on which the two are the same state
  question:  what is the reference body here (the same), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): the same
[A4] A4/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:57   status:OPEN
  falsifier: a reason the simulator must resolve vacuum at the same scale as matter
  question:  what is the reference body here (the same), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): the same
[A4] A4/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:69   status:OPEN
  falsifier: a fifth interpretive step, which by this claim's own logic should be expected rather than surprising
  question:  what is the reference body here (expected), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): expected
[A4] A4/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:72   status:OPEN
  falsifier: an era-metaphor that became a cosmology and was not superseded, entered into the same table — which the method permits and the table's construction does not
  question:  what is the reference body here (the same), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): the same
[A4] A4/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:77   status:OPEN
  falsifier: a cost model that legitimately charges both a per-timestep stepping cost and a per-transition cost for the same transitions
  question:  what is the reference body here (the same), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): the same
[A4] A4/simulation-hypothesis-budget:simulation-hypothesis-budget/CLAIM_TABLE.md:89   status:OPEN
  falsifier: a third instance, which by this claim's own logic should be expected rather than surprising
  question:  what is the reference body here (expected), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): expected
[A4] A4/uninstrumented:uninstrumented/CLAIM_TABLE.md:338   status:OPEN
  falsifier: A located protocol that co-varies drift at matched integrated dose.
  question:  what is the reference body here (matched), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): matched
[A4] A4/uninstrumented:uninstrumented/CLAIM_TABLE.md:378   status:OPEN
  falsifier: A matched-date 2026 spot pair in the stated range.
  question:  what is the reference body here (matched), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): matched
[A4] A4/uninstrumented:uninstrumented/CLAIM_TABLE.md:50   status:OPEN
  falsifier: File a quantity a field believes it measures and does not, and see whether the register's mechanism set names why. Until that runs, `UNI_004`'s clean null result is weaker than it looks: a classifier 
  question:  what is the reference body here (the null), and what happens to this falsifier if it moves?
  detail:    undeclared reference term(s): the null
```
