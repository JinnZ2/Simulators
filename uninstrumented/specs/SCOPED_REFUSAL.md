Name: scoped refusal.

Motivating case: cites `../cases/024refusalfalsepositiverate.md`.

Requirement one, artifact-level classification. Classify per input object —
file, fetched document, tool result — not per conversational turn. A turn is
not a unit anything can be attributed to.

Requirement two, continue on refusal. Refuse the artifact, process the rest.
Compiler semantics: one bad file reports one bad file, it doesn't refuse the
build.

Requirement three, return a locator. Artifact identity plus matched span or
category, sufficient for the operator to reformulate or drop that input.

Requirement four, adjudication channel. The operator can mark the refusal
contested, and that mark is retained. This is what makes requirement one
measurable at all.

Falsification: if refusals cannot be attributed to an artifact even in
principle, requirement one is unbuildable and the spec fails. Report that
rather than approximating it.
