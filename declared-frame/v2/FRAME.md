# Declared frame

CC0-1.0. Public domain.

A marker, not a position. Test fit, extend it, or report where
it breaks.

Every result carries a frame. Science does not eliminate the
frame; it fixes one and stops reporting it. Frame disagreements
then get argued as data disagreements, which is unresolvable in
that form.

## Fields

    boundary          what is inside the accounting
    horizon           over what time
    who_counts        whose outcomes enter
    sign_source       where "better" was set, and by whom
    logic             which formal system
    observer_access   unknown | partial | verified

## Rule

UNKNOWN is a legal value. OMISSION is not.

An unpopulated field is a visible gap. An omitted field reads as
absence of the issue.

## Comparability

    same boundary + horizon + who_counts
        -> directly comparable
    differ on any of the three
        -> the difference is a FRAME difference,
           not a finding
    differ on logic
        -> data may compare, conclusions do not
    any field unknown
        -> UNDETERMINED. Flag, do not resolve.

## Cost

The energy cost of keeping fields open is fixed.
The cost of a narrow frame is conditional on the change rate,
which is usually unmeasured.

As the change rate rises, the narrow frame gets more expensive
and the open one does not. In some domains the crossover has
already passed and the accounting has not been updated.

## Growth

Six fields is what one session's material produced. The format
grows by adding a declared field, never by widening an existing
one. Widening is the aggregation failure.
