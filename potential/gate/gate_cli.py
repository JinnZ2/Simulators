"""gate_cli.py — CLI.

Usage:
  python3 gate_cli.py list
      Print the domain names.

  python3 gate_cli.py show <domain>
      Print the graph's channels.

  python3 gate_cli.py project <domain>
      Print cut-vertex report across the declared admissibilities.

  python3 gate_cli.py all
      Print the projection report for every domain.
"""

import sys

from domains import DOMAINS
from graph import TOKEN_NODE
from projections import project_all, render, render_all

def cmd_list():
    for name in sorted(DOMAINS):
        print(name)
    return 0

def cmd_show(name):
    if name not in DOMAINS:
        print(f"unknown domain: {name}", file=sys.stderr)
        return 1
    g = DOMAINS[name]()
    print(f"domain: {g.name}  source={g.source}  target={g.target}")
    for ch in g.channels:
        tok = " [token]" if ch.requires_token else ""
        kinds = "+".join(sorted(ch.kinds))
        print(f"  {ch.src:14s} -> {ch.dst:14s}  kinds={kinds:26s}{tok}  {ch.label}")
    return 0

def cmd_project(name):
    if name not in DOMAINS:
        print(f"unknown domain: {name}", file=sys.stderr)
        return 1
    p = project_all(DOMAINS[name]())
    print(render(name, p))
    return 0

def cmd_all():
    ap = {name: project_all(fn()) for name, fn in DOMAINS.items()}
    print(render_all(ap))
    return 0

def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "list":
        return cmd_list()
    if cmd == "show" and len(argv) == 3:
        return cmd_show(argv[2])
    if cmd == "project" and len(argv) == 3:
        return cmd_project(argv[2])
    if cmd == "all":
        return cmd_all()
    print(__doc__)
    return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv))
