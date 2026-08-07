"""Tests for crossdomain_eval.report."""

import os

import numpy as np
import pytest

from crossdomain_eval.experiments import parameter_sweep
from crossdomain_eval.report import markdown_report, plot_sweep


class TestMarkdownReport:
    def test_report_content(self, tmp_path):
        out = tmp_path / "report.md"
        content = markdown_report(
            "My Report",
            [
                {"heading": "Intro", "text": "hello world"},
                {"heading": "Data", "text": "see table",
                 "table": {"a": [1, 2], "b": [3, 4]}},
            ],
            str(out),
        )
        assert out.exists()
        assert content.startswith("# My Report")
        assert "## Intro" in content and "hello world" in content
        assert "| a | b |" in content
        assert "| 1 | 3 |" in content
        assert out.read_text() == content

    def test_figure_reference(self, tmp_path):
        fig = tmp_path / "fig.png"
        fig.write_bytes(b"\x89PNG")  # placeholder
        out = tmp_path / "report.md"
        content = markdown_report(
            "T", [{"heading": "H", "text": "", "figure": str(fig), "table": None}], str(out)
        )
        assert "](fig.png)" in content

    def test_creates_parent_dirs(self, tmp_path):
        out = tmp_path / "deep" / "nested" / "r.md"
        markdown_report("T", [{"heading": "h", "text": "x"}], str(out))
        assert out.exists()


class TestPlotSweep:
    def test_plot_1d(self, tmp_path):
        res = parameter_sweep(lambda x: x**2, {"x": (0, 2, 9)})
        path = plot_sweep(res, "x", str(tmp_path / "s1.png"))
        assert os.path.exists(path) and os.path.getsize(path) > 1000

    def test_plot_2d(self, tmp_path):
        res = parameter_sweep(lambda x, y: x + y, {"x": (0, 1, 5), "y": (0, 1, 5)})
        path = plot_sweep(res, "y", str(tmp_path / "s2.png"))
        assert os.path.exists(path) and os.path.getsize(path) > 1000

    def test_unknown_param_raises(self, tmp_path):
        res = parameter_sweep(lambda x: x, {"x": (0, 1, 3)})
        with pytest.raises(KeyError):
            plot_sweep(res, "z", str(tmp_path / "s3.png"))

    def test_agg_backend_no_display(self, tmp_path):
        import matplotlib
        assert matplotlib.get_backend().lower() == "agg"
