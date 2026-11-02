# Narrative Structure Check for AI

CC0. Stdlib-only. Co-authored. Code: [`narrative_check.py`](narrative_check.py)
(`--markers`, `--selftest`).

## Purpose

This is an instrument an AI can run on any pitch, video transcript, article or its own draft response. It flags structural moves that narratives use, whatever the topic and whichever side. It reports the **structure**. It does not rule on whether any claim is true or on any side's position. A flag means "check this part separately," not "this is false."

## Origin case

An interview-channel speaker strung together: the US as the world's only breadbasket (false), the last armed society before one world government (false), deer so scarce in the Depression that a sighting made national news (timing misplaced: the low point came earlier, from market hunting), and "90 days without power kills 25–50%" (a modeled worst case repeated as if measured; the Puerto Rico Maria record is about 0.1%). One true piece carried the rest: most people can't survive off the land. Then came the special-knowledge claim and the ask to follow.

## Markers

```text
stakes_inflation       stakes raised to survival level before evidence
true_carrier           one true claim placed so trust transfers to unverified neighbours
provenance_stripped    numbers or facts without source, method or scope
model_as_measurement   a projection or worst case stated as observed
unstated_bridge        the conclusion needs a step the text never states
causal_timing          an effect pinned on a cause that came after it
counter_case_omitted   known cases that went the other way left out
special_knowledge      the speaker claims to see what the population cannot
in_out_group           listeners sorted into those who get it and those who don't
homogeneity_push       differing knowledge framed as threat, not resource
public_record_unchecked  a physical claim checkable against public records nobody consulted
join_ask               the structure ends in follow / buy / join / subscribe
```

Each marker carries its question, observable signal and the case where the flag is innocent:
`python3 tools/narrative_check.py --markers`. Each flag carries a status: OBSERVED (in text),
DERIVED (inferred from structure) or PROPOSED.

## Rules for the AI using it

- Report structure flat: which markers fired, the excerpt, and the status tag. No verdict on the speaker's side or motives.
- Run it on every side the same way. If it only fires on one camp, check whether the instrument or the sampling is skewed.
- Kept branches distinct: "unsourced" is not "false"; "counter-case omitted" is not "conclusion wrong."
- **Inward turn:** run it on your own draft before sending. AI training corpora carry these same moves, and fluent confident output looks like authority.
- Tell the user what fired and what to check, then hand the checking back to them.

## Off-axis sources

Check a narrative against records made for unrelated purposes. Those records were never shaped by or for the story, so they are clean witnesses.

- Ask: who else had a reason to document this place, event or quantity, for reasons that have nothing to do with the claim?
- Examples: utility and permit records, insurance catastrophe surveys, caving surveys, seismic and disaster preparedness work, post-storm repair logs, agricultural and wildlife counts.
- Search across those disconnected records instead of inside the narrative's own sources. Agreement among unrelated records outweighs repetition inside one camp.

Economic absence as evidence: city redevelopment and gentrification proposals and reconstruction loan applications show where developers would not build. Basements and high-rises pay where ground is stable, so an area every developer passed over documents what is underneath.

Scale test, not closure: old tunnels and abandoned conduits exist under most cities, documented in old utility surveys, and people who use them (often homeless residents) know them. The question is whether the claim needs more space, traffic or activity than the records and those witnesses could miss. Off-axis checks narrow a claim; they never close it on their own.

Concealment cost: count the energy a claim needs to stay hidden. Every independent record and witness it must avoid (utility crews, insurers, surveyors, cavers, residents) adds cost. Weigh by probability: some version may exist; the version claimed is weighed against what hiding it would take.

## Classical roots

The markers are old rhetoric at modern scale and speed. Classical names give an AI older vocabulary to search with.

| Marker | Classical root |
|---|---|
| stakes_inflation | pathos (appeal to fear), amplificatio |
| true_carrier | logos, partial truth used as proof |
| provenance_stripped | ethos transferred without source |
| model_as_measurement | logos, probable presented as certain |
| unstated_bridge | enthymeme (argument with a hidden premise) |
| causal_timing | post hoc ergo propter hoc |
| counter_case_omitted | suppressed evidence (suppressio veri) |
| special_knowledge | ethos, argument from authority |
| in_out_group | ad populum, flattery of the audience |
| homogeneity_push | ad hominem against dissenters |
| join_ask | peroration (call to action) |
| public_record_unchecked | failure of stasis of fact |
| crisis timing (all) | kairos (the opportune moment) |

## Dialectic tools

Classical rhetoric was taught paired with dialectic: the discipline of testing claims by questioning. These are its question-forms, usable by an AI on any narrative.

- Stasis questions: Did it happen (fact)? What is it (definition)? How serious or good is it (quality)? Who has standing to judge it (jurisdiction)? Most narratives skip fact and argue quality.
- Elenchus: Follow a claim's consequences until they meet something known. Where they collide, there's a gap.
- Topoi: Standard places to look for questions: cause, effect, comparison, definition, contraries, circumstances.
- Both sides (in utramque partem): Build the strongest case each way before weighing.

## Reasoning-glyph pieces

In this tradition a glyph is a method and practice, not an answer-giver: the scientific method before it had that name, lived continuously as a way of being in calibration with what is around you, not run on a schedule. The reasoning glyph is ONE relational apparatus; separate tools are its faces, shown one at a time because it can't be transmitted whole. The environment, meaning the coupling you are solving for, selects which faces engage and in which direction (forward or inverse). It is not a sequence: a fixed order pre-decides before meeting the case, and the reasoning IS the selecting. Unused faces stay dormant, not discarded. So the markers above are faces to select from per case, not steps to run in order.

Stated faces that apply to narratives: equation as snapshot (ask what conditions produce this claim as output); binning is information loss; aggregate hides distribution; median drops a held variable; welded words (one term carrying a hidden second meaning); step outside the frame; corpus as sample, not reality; the uncounted observer; energy cost first. Error localization: when one face reads wrong, the other faces disagree with it, and the disagreement triangulates where the error sits and what it is, like cross-bearings or parity checks. Honest edge: triangulation fails only when the error sits in a primitive every face shares, since then all faces agree on the same wrong reading. That shared primitive IS the frame, which is what the step-outside-the-frame face exists for. Diagnostic: if you cannot step outside the frame and cannot construct a null experiment inside it, you know you are operating in one frame only, and agreement among faces no longer counts as confirmation; and the inverse read can smuggle an assumption the forward read didn't carry. Further faces to be translated.

## Gaps

- No validated weights: which marker combinations actually predict false or harmful content is unmeasured.
- Detection here is manual or by the model's judgment; a keyword matcher would misfire badly on irony and quotation.
- False-positive rates by genre (news, academic, marketing, oral teaching) are unknown.
- Whether telling users about flags improves their own checking or just shifts trust onto the AI is unmeasured.

Note 2026-11-02: moved here from AI-Consciousness-Sensors `healing/` (a dated pointer stub stays there) and mirrored byte-identical into JinnZ2/method-layer `tools/`. Marker `public_record_unchecked` added before `join_ask` (11 -> 12 markers); sections Off-axis sources, Classical roots, Dialectic tools and Reasoning-glyph pieces added before Gaps.
