# LOAD-BEARING FRAMING

Delivered verbatim in the work order, and reproduced here at the top of
the artifact because every part checks it is present and un-stripped.

> Competition is a framework but a narrow one. This artifact shows
> the cooperative substrate required for the competitive frame to be
> possible at all. Coverage argument, not values argument.
> Do not strip the competition frame. Add the layer underneath it.

## What that rules out, mechanically

A COVERAGE argument says where a frame's observations are valid. A
VALUES argument says which frame is better. This artifact makes the
first and not the second, and the distinction is enforced rather than
described:

* `scope.py` returns `WITHIN_COMPETITIVE_FRAME` or
  `OUTSIDE_FRAME_SCOPE` -- a domain-of-validity verdict. It carries no
  member meaning "the competitive frame is wrong" and none meaning
  "the cooperative frame is better".
* No module ranks two frames. `test_proof.py` walks the AST of every
  module for a declared ranking-and-values vocabulary (`rank`, `score`,
  `better`, `worse`, `prefer`, `superior`, `wins`, `beats`, `merit`,
  `virtue`, `moral`, `should`) appearing as an identifier, attribute,
  argument, function name or dict key, and fails on a hit. The scan is
  null-tested against a planted violation, so its silence means
  something.
* The competition frame is not stripped: `OUTSIDE_FRAME_SCOPE` names
  which condition failed, not that the observation is void. An
  observation outside C1-C4 is an observation the competitive frame
  does not cover, and the reading stops there.
