# legacy

Archived source drops. When a big collaborative brainstorming session
lands as one huge `Organize.md` at the repo root, it gets extracted
into the appropriate simulator folder (usually `play-sims/`) and then
moved here so the root stays clear for the next drop.

## Contents

| file | drop | round | extracted to | count |
|---|---|---|---|---|
| [`Organize.md`](Organize.md) | first exploratory drop | 1 | [`../play-sims/`](../play-sims/) | 14 sims |
| [`Organize2.md`](Organize2.md) | second exploratory drop | 2 | [`../play-sims/`](../play-sims/) | 3 sims |
| [`Organize3.md`](Organize3.md) | pulled from JinnZ2/Resilient-AI-Human-Collaboration- | 3 | [`../grounding-layers/`](../grounding-layers/) | 10 sims |

Each extracted file's docstring names its `legacy/OrganizeN.md` source
and the line range it came from — provenance is preserved even after
the drop moves here.

## Streamlined ingestion pattern

The root of the repo is kept open for one filename at a time:
`Organize.md`. That's the drop slot. Everything else lives in a proper
folder. When a new drop arrives:

1. **Drop**: user pastes a big collaborative code block into
   `Organize.md` at the repo root.
2. **Extract**: an assistant (or the user) splits it into per-sim `.py`
   files under `play-sims/<domain>/`, adding a short docstring header
   to each with the source line range.
3. **Archive**: `git mv Organize.md legacy/OrganizeN.md` where `N` is
   the next unused round number.
4. **Root stays open**: the next drop can land at the same `Organize.md`
   path with no rename friction.

Round numbers stay tied to the archive filename, not the extracted
files — an edit to an extracted sim later on doesn't renumber anything
here.

## Why archive instead of delete

- The drops contain design lineage: the "same idea, three variants"
  progression, the abandoned drafts, the exploratory notes between
  sims. That context is worth keeping even if only the cleaned-up
  extractions are actively used.
- The extracted `.py` files reference these by line number
  (`Extracted verbatim from legacy/OrganizeN.md lines A-B`). Deleting
  the source would break provenance.
- The drops are small compared to the extractions and cost effectively
  nothing to keep.

## Reading order

If you want to browse a drop start-to-finish, read `Organize.md` in
order — the sim boundaries are marked with `# ======` banners
(usually) or by a fresh block of imports.

## License

CC0. See the repo root [`LICENSE`](../LICENSE).
