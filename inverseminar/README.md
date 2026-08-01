# inverseminar

Micro-inverseminar as a single stdlib-only script. One artifact, one
reconstruction, one correction. ~60 seconds per round.

CC0. Phone-buildable. No dependencies.

## The mechanism

The Nature Physics inverseminar format works because a senior scientist
cannot sit quietly while their work is presented back to them slightly
wrong. The correction is the product. The presentation is only the bait.

This module runs that mechanism against a single artifact instead of a
paper, and against yourself instead of a live audience.

## Three channels

| channel | model does | tacit surfaces as |
|---------|-----------|-------------------|
| `RECONSTRUCTION` | states your reasoning back, confidently | a **correction** contradicting it |
| `GUESSING AT` | flat assertions on its weakest points | a **one-word kill** on one of them |
| `CANNOT DERIVE` | direct questions on links it can see are load-bearing but has no basis to guess | an **answer** stating the link |

The third channel exists because confident guessing only recovers
reasoning the model can reach. When most of the connective steps never
left the author's head, the common failure is not a wrong guess — it
is an absence. An absence provokes no correction. `CANNOT DERIVE`
gives absence a shape the author can respond to.

## Four verdicts

| verdict | how it fires | what it captures |
|---------|--------------|------------------|
| `corrected` | you contradicted the reconstruction | delta = tacit |
| `answered`  | you answered a `CANNOT DERIVE` question | link = tacit |
| `unprobed`  | all three channels went past the load-bearing gap | logged as a **model miss**, never as a confirmation |
| `confirmed` | explicit only — must be passed | true agreement, not silence |

Silence is not a verdict. `record()` raises if you pass no correction
and no answers without an explicit `verdict=`. An empty reply is not
agreement.

## Provenance

Reconstruction is **model-authored**. Correction and answers are
**yours, verbatim**. They are separated at capture time and kept
separate in every downstream artifact, so the tacit layer never
inherits model overlay. `TACIT.md` marks stated lines with `[stated]`
and stashes the reconstruction inside a `<details>` block — visible
enough to remember what the correction was against, quiet enough that
it never gets mistaken for your voice.

## Usage

Four subcommands:

```
python3 inverseminar.py triage [DIR]    # rank artifacts by overlay density
python3 inverseminar.py prompt          # print the prompt to paste
python3 inverseminar.py status          # tally rounds, hit rate, verdicts
python3 inverseminar.py emit [OUT.md]   # write the tacit layer
```

Typical round:

1. `triage` picks an artifact where the model wrote most and you wrote
   least — that is where your reasoning is most buried.
2. `prompt` prints the three-channel format. Paste it, then the
   artifact, into any conversation.
3. Read the reconstruction. Correct it in one line. Answer any
   `CANNOT DERIVE` questions. If all three channels missed, log
   `unprobed`.
4. Call `record()` from Python to write the round. Later, `emit()`
   builds `TACIT.md`.

## Triage: what "most buried" means

Two pattern lists — `OVERLAY` (rhetorical LLM padding: "this changes
everything", "breathtaking", "profound", emoji, bolded bullet walls)
and `SUBSTANCE` (scientific-notation numbers, physical units,
`FALSIF`, `def `, `assert`) — are counted per file. The score is
`1000 × overlay / words`, damped by `min(1, words / 150)` so a
five-word file cannot top the list on one match. `done` marks
artifacts already run: `Nr/Mm` = N rounds, M of them misses.

Ratio and score are diagnostic, not verdicts. A high-substance file
can also be high-overlay — that is a signal, not a fault.

## Storage layout

Two files, created next to the working directory when you call the
tool:

| file | contents | provenance |
|------|----------|------------|
| `TACIT.jsonl` | one round per line (ts, artifact, reconstruction, correction, answers, verdict) | append-only |
| `TACIT.md`    | rendered tacit layer, provenance-separated | rebuilt by `emit()` |

Both are gitignored inside this folder — they hold tacit knowledge
that should not leave the machine unless you decide it should.

## Sample

[`samples/inverseminar.sample.txt`](samples/inverseminar.sample.txt)
shows a triage against this repo, the prompt, four rounds (one per
verdict), the status readout, and the `TACIT.md` `emit()` produces.

## What it does not do

- **No model calls.** The tool prints a prompt for you to paste; it
  never talks to a model itself.
- **No auto-verdict from silence.** `unprobed` must be logged
  explicitly. Empty capture raises.
- **No sharing.** `TACIT.jsonl` and `TACIT.md` are local by design and
  gitignored inside this folder.
- **No sentiment analysis of the reconstruction.** Whether the model
  praised you or hedged is not scored — only whether *you*
  contradicted it or answered its questions.

## License

CC0 1.0 Universal. Public domain.
