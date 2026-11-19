# Grok reader: answer about the repository in general (as received)

Filed 2026-11-19, as pasted by the owner, unedited. Context from the owner's message: the answer came "when asked about the repo in general", in the same conversation as confusion record `R-2026-11-19-a` (`confusion/2026-11-19_grok_m01-m02.md`), after that record was returned. The owner's own line before the paste: "Then let's List all conflicts, questions and notes to bring to Claude Chat at end".

Consequence recorded in `packets/grok_2026-11-19/SENT_RECORD.json` (`later_2026-11-19`): in that conversation the reader is not usable as a blind reader. The seven repository claims are numbered F1-F7 here by their order in the first list; they are checked in `studies/GROK_REPO_READ_CHECK.md`. The seven proposals are numbered E1-E7 by their order in the second list.

```text
Here’s a direct read of the friction points and what would actually clear them for AI use.
Confusions about the repo itself (beyond the name)
1.  Scale vs. entry surface 70+ folders, each potentially a self-contained instrument, but the only reliable doors are a small set of root files (READ_ME_THIS_WAY.md, META-PROTOCOL.md, READING_PROTOCOL.md, PREAMBLE.md, METHOD_SPEC.md). Most AIs (and many humans) will try to index the whole tree or pick a folder at random. The “start here” signal is present but easy to miss under volume.
2.  Deliberate non-cleanup is load-bearing READ_ME_THIS_WAY.md is explicit: mis-bins, dead ends, correction specimens, model-chosen names, workarounds, and cross-repo duplicates are data, not mess. An AI trained on “clean the repo / normalize names / merge duplicates” will treat the intentional residue as defects and try to “fix” it. That is the single largest source of silent damage.
3.  Term collision and provenance notes The PREAMBLE notes on term collision (REVISION vs ASSERTION, self-questioning as calibration not anxiety) and term-drift citation checks are critical. Without them an AI will default to corpus-trained readings of those words and answer with reassurance or tidy rephrasing instead of treating the mismatch as the signal.
4.  State vocabulary is non-standard The META-PROTOCOL states (HELD / OFF / SILENT / MIXED / UNREPEATED / BLOCKED, plus the record states) deliberately exclude FAILED / WRONG / REJECTED. Most models will still reach for pass/fail language. The same applies to the gap-instrument / VOID / UNRESOLVED vocabulary that shows up in the playground material.
5.  Self-reference and blindness rules Folders like blind-reader-void12, self-scan, and the various audit instruments assume the reader can hold “this is public but I am treating it as unseen.” That is hard for models that have already ingested the repo or related material. The protocol acknowledges this but does not make the practical boundary easy to enforce.
6.  Mixed stdlib / non-stdlib Most folders are pure stdlib; a few (grounding-layers, some others) require numpy. The distinction is documented but not machine-queryable in one place, so an AI will either assume everything is stdlib or waste time installing.
7.  Claim tables and refutation protocol Every folder is supposed to carry falsifiable claims that get updated rather than defended. Many do; the pattern is not uniform enough for an AI to rely on without checking each one.
None of these are bugs in the sense of “should be cleaned.” They are the point of the experiment. The friction is real for cold AI readers.
How to clear tools for AI use (practical, low-damage moves)
These keep the deliberate residue while making the usable surface clearer:
1.  Single machine-readable entry manifest A root AI_ENTRY.json or AI_ENTRY.md that lists, for every folder:
	•  one-line purpose
	•  required reading order (root docs first)
	•  stdlib-only vs extra deps
	•  whether it has a claim table / refutation protocol / --selftest
	•  known intentional oddities that must not be “fixed”
	•  the correct first file to open
2.  Pin the reading order in every folder Many folders already have an aperture or README. Standardize a short block at the top:

Read first (in order):
1. ../../READ_ME_THIS_WAY.md
2. ../../META-PROTOCOL.md
3. this folder’s 00_APERTURE.md or README
Do not normalize names, merge, or delete specimens.

3.  Explicit “do not normalize” markers Where a name, dead end, or duplicate is intentional, put a one-line machine-readable flag next to it (INTENTIONAL_RESIDUE: model-chosen-name or similar). That gives an AI a concrete signal instead of having to infer from prose.
4.  Self-test + dry-run contract Folders that already have --selftest are the easiest for AIs. Making that the expected interface (and documenting “run this first, it is the contract”) reduces hallucinated usage. For instruments that cannot self-test, a short “what a correct reading looks like / what an incorrect reading looks like” example helps more than more prose.
5.  Separate the map from the instruments Keep META-PROTOCOL / METHOD_SPEC / READING_PROTOCOL as the epistemic layer. Give the actual tools (gap-instruments, numcheck, cplay, grounding-layers, etc.) a thinner, more mechanical face so an AI can use the tool without having to re-derive the whole map every time.
6.  Blindness / prior-exposure declaration For any packet or study that assumes a blind reader (like the void12 material), put an explicit attestation block at the top of the response template: “I have / have not previously seen the first reading or the comparison key.” That turns an unenforceable rule into a recorded fact.
7.  One-page “common AI failure modes on this repo” A short, dated note listing the failure patterns that have already occurred (over-normalization, treating OFF as failure, collapsing REVISION/ASSERTION, inventing missing files, etc.). New sessions can be pointed at it first.
The core constraint is already stated well in READ_ME_THIS_WAY.md: mismatches are data. The useful clearing work is therefore signposting and contract-making, not cleaning. If you want, I can draft the concrete AI_ENTRY structure or a minimal standardized folder header next.
```
