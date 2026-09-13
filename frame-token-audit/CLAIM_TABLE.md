# CLAIM TABLE — FRAME-TOKEN AUDIT

Prefix `FTA_`. Every claim is about the delivered `frame_audit.py` as a
Stage 1 instrument; nothing here is a Stage 2 grading (USE vs MENTION,
substrate swap), which the delivery assigns to a human or model and this
folder does not perform. Stdlib only; the delivered file is verbatim.

---

**FTA_001.** The scan sorts longest-first WITHIN a class and iterates
classes in dictionary order, so a token declared by a later class loses
the span to an earlier class's prefix and can never fire as declared.
Scanned alone, `invest in` (relation_as_debt) lands on `time_as_money /
invest` under both lexicons; under v1 `invest` (capital_market) and
`afford` (value_worth) land on time_as_money too. Two tokens are declared
twice — 57 declared, 55 distinct — and the second declaration is dead.
`we invest in people` reads as time-as-money, never as relation-as-debt.

*Falsifier:* any of the three firing as declared. *Status:* SUPPORTED;
asserted in the selftest. Repair is one sort over the flattened lexicon
(longest phrase first across classes), not a per-class sort.

---

**FTA_002.** Six of the 55 v1 tokens are `ontology-probe`'s
`scope_required` terms (`capital`, `efficiency`, `market`, `optimization`,
`optimize`, `value`) and seven are `fold-matrix`'s register keys or
aliases (`budget`, `cost`, `efficiency`, `efficient`, `optimization`,
`optimize`, `resources`), read by import; none is an ontology-probe
absent-term alias. The overlap is of WORDS, not readings: there a hit is
`SCOPE_UNDECLARED` naming the missing fields, in fold-matrix a folded term
with a grid, here a density count — three instruments on one vocabulary,
each attaching its own state, and this one attaches the fewest.

*Falsifier:* the import returning a different set. *Status:* SUPPORTED.

---

**FTA_003.** Three mechanical limits, each shown rather than read: the scan
is per line, so a phrase across a line break (`spend\ntime`) scores 0; the
`words` denominator counts alphabetic tokens while a multi-word phrase
counts one hit, so `per_1000` mixes two units; and the empty text returns
`per_1000 None` rather than 0 — the delivered rule, and the right one.

*Falsifier:* none needed; properties of the code. *Status:* SUPPORTED.

---

**FTA_004.** On the operator's thirty hand-built constructions
(`ontology-probe` run 1), v0 fires on **0 of 30** and v1 on **3 of 30** —
`c-024 efficiency` and `c-025 markets` (AMBIENT), which are the two
records ontology-probe's own scope screen already lands
`SCOPE_UNDECLARED`, and `c-012 value` (CONTROL), where `value` is a field's
value (*"its value here is unread rather than zero"*), the sense collision
`ontology-probe`'s aliases file flags as one no word list separates.
0 of 9 TARGETED constructions carry any token. So on the one hand-built
corpus in the tree the v0 lexicon is silent and v1's three hits are two
agreements with a sibling instrument and one sense collision.

*Falsifier:* a re-run on the same file returning other ids. *Status:*
SUPPORTED; counts, not a reading of the constructions.

---

**FTA_005.** Run on the three root documents whose SUBJECT is this
vocabulary, v0 is silent on all three and v1 returns 5.4 / 4.6 / 2.5 per
1000 — and hand-reading the 14 hits: SHAPE_SPEC's five `cost_price` hits
are its §9 NOTE ON COST arguing *against* the cost framing (mention);
`returns` fires three times on the verb (*"returns a null"*), the
`nonidentity-census` T1-1 word-list-decides-sense shape; `energy budget`
is physics. The density on a document written against the frame is the
`DF_010` use-mention result on a new lexicon, and Stage 2 is where the
delivery already puts the separation — this run shows how much of Stage 1
it has to undo.

*Falsifier:* a v1 run on these files returning other hit contexts.
*Status:* SUPPORTED on the hand-read; the hand-read is this session's and
is not Stage 2.

---

**FTA_006.** `frame_audit.py` writes `result_<v>.json` into the working
directory with every hit's context line, so a second run over a directory
holding the first run's output reads its own hits — `UNI_010`'s loop;
`audit.py` writes nothing and scans named files only. `v0 = lexicon as
declared last turn` names a declaration not in this tree; v0 is carried as
delivered. **UNVERIFIED:** nothing here bears on whether any text is IN
the frame — every count above is Stage 1, and the known-answer pair that
separates (9 against 0 under v1) was authored here.

*Falsifier:* Stage 2 gradings on real hits. *Status:* UNVERIFIED.
