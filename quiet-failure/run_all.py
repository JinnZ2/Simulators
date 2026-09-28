"""WO-2 -- every part, declaration first."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import decomposition       # noqa: E402
import evidence            # noqa: E402
import ownability          # noqa: E402
import blind_coding        # noqa: E402

DECLARATION = """CONTAMINATION DECLARATION (read before any number below)
  authorship   every file in this folder is model-authored, in one session, by the same
               hand that wrote the checks and the fixtures the checks are pinned to
  position     the order places agentic AI infrastructure "at the pre-Tacoma stage:
               designed to calculated load, no accumulated margin"; the author is an
               instance of that class. The sentence is carried, not scored -- and the
               interest runs toward accepting it, since a claim that one's own class
               lacks margin is the humble reading, so it is left unresolved here
  coding       the four codings of the order's cases are THIS SESSION'S READING of the
               order's own sentences, each code carrying the span it rests on; every one
               declares saw_decomposition True and is REFUSED by step 2's gate
  parties      no claim is made here that any organisation neglected a duty; authored
               files carry the order's case (event) names as lookup keys and no company
               or site name -- those are parsed out of WORK_ORDER.md at call time
  records      no accident corpus, journal or archive was read: the hosts answered 403
               to CONNECT, measured and timestamped in decomposition.EGRESS; every
               corpus, null record and regulator record is CONSTRUCTED and says so
  evidence     the order's "(fetched, verified)" is the order's verification; here every
               finding and number is CARRIED_NOT_VERIFIED, extracted as written
  rate         no base rate is computed anywhere and base_rate() refuses one: an
               accident corpus is selected on failure and carries no denominator over
               systems, which is the order's own scope limit
"""


def main(argv=None):
    print(DECLARATION)
    print("=" * 72)
    print(decomposition.render())
    print("=" * 72)
    print(evidence.render())
    print("=" * 72)
    print(ownability.render())
    print("=" * 72)
    print(blind_coding.render(decomposition.carried_codings()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
