## Summary

## Which layers / claims does this touch?

## Falsifiability check

- [ ] Any changed claim carries a `REFUTATION_PROTOCOL` block.
- [ ] Any new constant is documented and dated in `LOG.md`.
- [ ] Frozen constants were **not** retuned to make a failing test pass;
      the CLAIM was updated instead.
- [ ] Tests pass locally:
      `python -m unittest discover -s grounding-layers -p 'test_*.py'`

## Non-negotiables

- [ ] License headers remain `CC0 1.0 Universal`.
- [ ] No `--no-verify` / `--no-gpg-sign` / hook skips.
- [ ] Any new non-stdlib import is declared in a `requirements.txt`.
