# SCOPE-BOUND SHAPES — build note

A SHAPE is a structural sequence that recurs across domains.
It is defined by its sequence and its selection rule, not by
its materials.

A SCOPE BINDING is that shape instantiated with a declared
list of FROZEN variables. Scoping out = releasing entries
from FROZEN. It is not a model swap.

Domain names (materials science, geology, cosmology) are
scope bindings that acquired names. Do not treat them as
different subjects.

## WORKED EXAMPLE
shape: strain accumulates → passes limit → releases along
       weakest available path
invariant: the sequence, and the path-selection rule

binding: slab_concrete
  live:   restraint, moisture gradient, aggregate, cure age
  frozen: creep, chemistry, T range, lithostatic load

binding: metamorphic_rock
  live:   creep, chemistry, T range, lithostatic load,
          restraint
  frozen: cure age

## WHAT TO BUILD
1. A shape record: sequence, selection rule, list of bindings.
2. Per binding: LIVE and FROZEN, both explicit. No defaults.
3. compare(binding_a, binding_b) → returns SCOPE COLLISION if
   a variable frozen in one is live in the other. Two modules
   claiming the same shape at incompatible bindings are not
   corroborating each other.
4. A marker table: marker | stability | bindings_tested |
   known_exceptions. stability without bindings_tested is
   not a claim — refuse to print one without the other.

## CONSTRAINT
FROZEN entries are declared by the builder, not inferred.
An inferred FROZEN list would be the tool asserting scope
it did not measure.
