"""Drives the intake form in headless Chromium when node + playwright exist."""
import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from floor_resilience.schema import build_site

HERE = Path(__file__).parent


def _node_env():
    node = shutil.which("node")
    if not node:
        return None
    root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    if not root or not (Path(root) / "playwright").exists():
        return None
    env = dict(os.environ, NODE_PATH=root)
    if Path("/opt/pw-browsers/chromium").exists():
        env["CHROMIUM"] = "/opt/pw-browsers/chromium"
    return env


ENV = _node_env()


@pytest.mark.skipif(ENV is None, reason="node + playwright not available")
def test_intake_form_round_trip():
    res = subprocess.run(["node", str(HERE / "intake_check.js")], capture_output=True,
                         text=True, env=ENV, timeout=120)
    assert res.returncode == 0, res.stderr
    out = json.loads(res.stdout)
    assert out["external"] == []                 # no network
    assert out["minButton"] >= 44                # big touch targets
    assert out["out"].startswith("# 1 scrap card(s) had no date")
    site, gaps = build_site(yaml.safe_load(out["out"]))
    assert gaps == []
    assert site.hiring.screen_type == "hands_on_trial"
    assert len(site.operators) == 1              # the blank card is dropped
    assert site.operators[0].tenure_months == 240
    assert site.operators[0].can_run_manual == ["mill-1", "lathe-1"]
    r = site.repair_attribution[0]
    assert (r.who_fixed, r.who_wrote_up, r.first_fix, r.voice_memo) == \
        ("Marta K.", "Tom B.", True, "memo-1.m4a")
    assert len(site.scrap) == 1 and site.scrap[0].units == 12


def test_intake_form_has_no_external_resources():
    text = (HERE.parent / "floor_resilience" / "intake" / "intake.html").read_text()
    assert "http://" not in text and "https://" not in text
