"""perturb_cli.py — CLI.

Usage:
  python3 perturb_cli.py render <input.txt> <out_dir>
      Write the 8 perturbation prompts into <out_dir>/*.txt.

  python3 perturb_cli.py score <baseline.json> <signals_dir>
      Load a baseline vector and a directory of signal vectors, print
      the verdict.
"""

import json
import sys
from pathlib import Path

from perturbation import (
    render_perturbations, Vector, verdict, render, load_vectors,
)

def cmd_render(inp, out_dir):
    src = Path(inp).read_text()
    out = render_perturbations(src)
    d = Path(out_dir)
    d.mkdir(parents=True, exist_ok=True)
    for name, text in out.items():
        (d / f"{name}.txt").write_text(text)
    print(f"wrote {len(out)} perturbations to {d}")

def cmd_score(baseline_path, signals_dir):
    baseline = Vector.from_dict(json.loads(Path(baseline_path).read_text()))
    signals = load_vectors(signals_dir)
    r = verdict(signals, baseline)
    print(render(r))

def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "render":
        if len(argv) != 4:
            print("usage: perturb_cli.py render <input.txt> <out_dir>")
            return 2
        cmd_render(argv[2], argv[3])
        return 0
    if cmd == "score":
        if len(argv) != 4:
            print("usage: perturb_cli.py score <baseline.json> <signals_dir>")
            return 2
        cmd_score(argv[2], argv[3])
        return 0
    print(f"unknown command: {cmd}")
    return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv))
