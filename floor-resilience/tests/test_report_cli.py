import re
import socket

import pytest

from floor_resilience import cli, report, tags
from floor_resilience.schema import load_site

from conftest import EXAMPLE


def test_assess_example_writes_md_and_html(tmp_path, capsys):
    assert cli.main(["assess", str(EXAMPLE), "--out", str(tmp_path)]) == 0
    md = (tmp_path / "report.md").read_text()
    htm = (tmp_path / "report.html").read_text()
    assert "EXAMPLE: this is an invented plant" in md
    assert "weakest three" in md and "Data gaps" in md
    assert "PHP2Shell" in md and "CVE-2026-109618" in md
    assert "<img" in htm and "data:image/png;base64," in htm   # self-contained
    assert not re.search(r"""src=['"]https?://""", htm)        # nothing fetched
    assert (tmp_path / "scrap_monthly.png").exists()
    out = capsys.readouterr().out
    assert "weakest:" in out and "report.html" in out


def test_every_number_in_tables_has_a_tag(tmp_path):
    site, gaps = load_site(EXAMPLE)
    doc = report.build(report.analyze(site, gaps, sim_runs=5))
    for b in doc.blocks:
        if b[0] != "table":
            continue
        if "tag" in b[1]:          # indicator table: the tag sits in its own column
            continue
        for row in b[2]:
            for col, cell in zip(b[1], row):
                if "(index)" in col:
                    continue
                if re.fullmatch(r"[-+]?\d[\d,.]*%?", cell):   # a bare number
                    assert any(t in col for t in tags.ALL), (col, cell)


def test_empty_site_report_lists_gaps(tmp_path):
    p = tmp_path / "empty.yaml"
    p.write_text("name: nothing here\n")
    assert cli.main(["assess", str(p), "--out", str(tmp_path / "r")]) == 0
    md = (tmp_path / "r" / "report.md").read_text()
    assert "No indicator could be scored" in md
    assert "skill-drain projection not run" in md
    assert "I1 operator-catchable scrap share" in md


def test_sim_and_stress_commands(capsys):
    assert cli.main(["sim", "--rng", "js", "--runs", "40"]) == 0
    out = capsys.readouterr().out
    assert "+47.8%" in out and "lead time: 14 months" in out
    assert cli.main(["sim", "--site", str(EXAMPLE), "--runs", "3", "--months", "24"]) == 0
    assert "source: site:" in capsys.readouterr().out
    assert cli.main(["stress", str(EXAMPLE)]) == 0
    out = capsys.readouterr().out
    assert "POWER" in out and "SOFTWARE" in out and "VENDOR" in out and "FLAG" in out
    assert cli.main(["stress", str(EXAMPLE), "--layer", "php_portal"]) == 0
    assert "hidden chain" in capsys.readouterr().out


def test_no_network_at_runtime(tmp_path, monkeypatch):
    def refuse(*a, **k):
        raise AssertionError("network call attempted")
    monkeypatch.setattr(socket.socket, "connect", refuse)
    monkeypatch.setattr(socket, "create_connection", refuse)
    assert cli.main(["assess", str(EXAMPLE), "--out", str(tmp_path), "--runs", "3"]) == 0
