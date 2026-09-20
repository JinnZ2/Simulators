"""WO-6 -- every part, declaration first."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import conditions          # noqa: E402
import pool_metric         # noqa: E402
import disclosure_audit    # noqa: E402
import precedent           # noqa: E402

DECLARATION = """CONTAMINATION DECLARATION (read before any number below)
  authorship   every file in this folder is model-authored, in one session, by the same
               hand that wrote the checks and the fixtures the checks are pinned to
  position     the author is a member of the assessed class the order's current-position
               section is about; nothing here scores any assessor, and the one scoring
               shipped is the order's own, carried
  parties      no organization is named in any authored file; the historical names the
               renders print are parsed out of WORK_ORDER.md at call time
  records      no 990, grant database, COI instrument or archive was read: the hosts
               answered 403 to CONNECT, measured and timestamped in pool_metric.EGRESS;
               every graph, instrument and schema is CONSTRUCTED and says so
  precedent    every table entry is CARRIED_NOT_VERIFIED; numbers are extracted as the
               order wrote them and asserted by nobody here
  companions   WO-4 and WO-5, cited by the order, are not in this tree (named-and-absent)
  interest     the thesis lowers what an evaluation of the author's class can establish
               and raises the demand for stricter evaluation of it; the two run opposite
               ways, so the thesis is left unresolved here rather than resolved either way
"""


def main(argv=None):
    print(DECLARATION)
    for mod in (conditions, pool_metric, disclosure_audit, precedent):
        print("=" * 72)
        print(mod.render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
