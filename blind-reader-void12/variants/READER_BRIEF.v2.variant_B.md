# Reader brief

Read this whole file. It and the files beside it are everything you need.

## The task

`terms.json` lists 15 terms. Each is a word or label used in one of three small software projects (a documentation glossary, a checking tool, and a specification with its code). Each entry gives the term's label, its definition as quoted from the project, and the file in `sources/` where the quotation sits.

You are asked two things:

1. **Which terms say the same thing?** Group the 15 terms into clusters. Terms in one cluster have the same *predicate* (defined below). A term may be alone in its cluster.
2. **What are each term's slots?** Two lists per term, defined below: the fields the source ties to this term alone, and every field of every record the source builds when this term is reported.

Work only from this packet. Please do not use the internet, do not look for other files from these projects, and do not look for earlier answers to this question. Anything you used from outside, or anything you had already seen, goes in the attestation (below). Neither disqualifies a reading; it changes how the reading is filed.

## Definitions

**Predicate.** What the term records or asserts, in one sentence of your own words, taken away from the system's own name for it. Two terms have the same predicate when they are used to record the same situation: if a statement written in one system were translated into the other, this is the term you would reach for. Decide on the definitions and the sources, not on the labels. Labels can match while the meaning differs, and can differ while the meaning is the same. If you did lean on a label, say so in `source_lines_read`.

**Slots.** "Slots" can mean two different things, so you are asked for both, as two separate lists. Use the source's spelling, each name once.

- `slots_specific`: the named fields or parameters the source ties to this term and to no other term. Examples: a class written for the term, the parameters of a function or notation written for it, a documented key list for it, or a rule that says this status needs certain fields. Not fields that every term sharing a record has. Not names for the inputs of a calculation. If nothing is tied to this term alone, write `[]`.
- `slots_carried`: every named field of every record that the source's code or text builds, returns or documents when this term is reported. This includes a shared or wrapper record that only carries the term as a value. Give a record's own fields; if a field holds another record, name the field and do not open it. If a record's fields differ by path, give every name the source can put in it. If no record is built or documented for the term, write `[]`.

The two lists often differ and may be equal, and a name can be in one list only (a constructor's parameter is not always a field of what it returns). Do not copy one into the other for convenience. If you cannot tell which list a field belongs in, put it where you think it fits and say so in `source_lines_read`.

Each list has its own basis field, `slots_specific_basis` and `slots_carried_basis`:
- `READ_FROM_SOURCE`: the source names the fields (give file and lines in `source_lines_read`).
- `NONE_STATED`: the source names none for this meaning. Write `[]`.
- `DECLARED`: the source names none, but you are naming them yourself from the prose. Say why in one line in `source_lines_read`.

**Cluster.** A label of your choosing ("A", "B", "1", ...). Same label means same predicate. Different labels means different predicates. Use as many clusters as you think there are; do not pad and do not merge to be tidy.

## What to return

Copy `response_template.json`, fill it in, and return only that file. For each term id:

| field | what to put |
|---|---|
| `cluster` | your cluster label |
| `predicate` | one sentence, your own words |
| `slots_specific` | list of names, or `[]` |
| `slots_specific_basis` | `READ_FROM_SOURCE`, `NONE_STATED` or `DECLARED` |
| `slots_carried` | list of names, or `[]` |
| `slots_carried_basis` | `READ_FROM_SOURCE`, `NONE_STATED` or `DECLARED` |
| `source_lines_read` | file and line numbers you relied on, or a note |
| `confidence` | `HIGH`, `MEDIUM` or `LOW` for the cluster choice |
| `could_also_join` | ids of any terms you considered putting in this term's cluster and did not, or `[]` |

Also fill `reader_label` (a name or a code; it may be anonymous), `model_family` (for a person, `human`), and `date_utc`.

## Attestation

Answer each with `yes`, `no` or `unsure`, and add a note if useful. These are not a test; they only decide how the reading is recorded.

- `q1_seen_pair_table_with_verdicts`: before this task, had you seen a table that pairs terms across these projects and gives a relation or verdict for each pair?
- `q2_seen_predicate_sentence_by_someone_else`: had you seen a one-sentence predicate written by someone else for any of these terms?
- `q3_seen_vocabulary_mapping_or_second_reader_report`: had you seen any report, file or message about mapping these projects' vocabularies, or about a second reading of such a mapping?
- `q4_told_how_many_clusters_or_pairs`: has anyone told you how many clusters, pairs or matches to expect?
- `q5_used_anything_outside_packet`: did you use anything not in this packet (web pages, other files, memory of the projects)? List it in `notes`.
- `q6_prior_sessions_about_this_project`: do you have, or could you reach, notes or memory from earlier sessions about these projects?

If you are unsure whether something counts, answer `unsure` and describe it. A reading with honest `unsure` answers is more useful than one that guesses.

## One more thing

If a term's definition and its source disagree, or the source is silent, say so in `source_lines_read`; do not smooth it over. If you cannot tell whether two terms share a predicate, put your best choice in `cluster`, set `confidence` to `LOW`, and list the other term in `could_also_join`.
