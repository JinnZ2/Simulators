"""Markdown report generation and sweep plotting."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

if TYPE_CHECKING:  # pragma: no cover
    from .experiments import SweepResult


def markdown_report(title: str, sections: list[dict], path: str) -> str:
    """Write a Markdown report and return its text content.

    Args:
        title: Report title (top-level heading).
        sections: List of section dicts with keys ``"heading"`` (str),
            ``"text"`` (str), optional ``"figure"`` (image path or None),
            and optional ``"table"`` (dict of column name -> list of values,
            or None).
        path: Output file path for the ``.md`` file.

    Returns:
        The generated Markdown text.
    """
    lines: list[str] = [f"# {title}", ""]
    for section in sections:
        heading = section.get("heading", "")
        if heading:
            lines += [f"## {heading}", ""]
        text = section.get("text", "")
        if text:
            lines += [text, ""]
        table = section.get("table")
        if table:
            columns = list(table)
            rows = list(zip(*(table[c] for c in columns)))
            lines.append("| " + " | ".join(str(c) for c in columns) + " |")
            lines.append("| " + " | ".join("---" for _ in columns) + " |")
            for row in rows:
                lines.append("| " + " | ".join(str(v) for v in row) + " |")
            lines.append("")
        figure = section.get("figure")
        if figure:
            rel = os.path.relpath(figure, os.path.dirname(os.path.abspath(path)) or ".")
            lines += [f"![{heading or 'figure'}]({rel})", ""]
    content = "\n".join(lines).rstrip() + "\n"
    directory = os.path.dirname(os.path.abspath(path))
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return content


def plot_sweep(sweep: "SweepResult", x_param: str, path: str) -> str:
    """Plot sweep results against one swept parameter and save the figure.

    If the sweep has more than one swept parameter, lines of the mean
    response over the remaining parameters are drawn, with faint lines for
    each slice. If it has exactly two swept parameters, a filled contour
    plot is produced instead.

    Args:
        sweep: A :class:`~crossdomain_eval.experiments.SweepResult`.
        x_param: Name of the swept parameter to use as the x-axis.
        path: Output image path (e.g. ``.png``).

    Returns:
        The output path.
    """
    if x_param not in sweep.params:
        raise KeyError(f"{x_param!r} is not a swept parameter")
    names = list(sweep.params)
    xi = names.index(x_param)
    x = sweep.params[x_param]

    directory = os.path.dirname(os.path.abspath(path))
    if directory:
        os.makedirs(directory, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 5))
    if sweep.results.ndim == 1:
        ax.plot(x, sweep.results, "o-", lw=1.5)
    elif sweep.results.ndim == 2:
        other = names[1 - xi]
        other_vals = sweep.params[other]
        # orient so results are indexed [x, other]
        data = sweep.results if xi == 0 else sweep.results.T
        for j, val in enumerate(other_vals):
            ax.plot(x, data[:, j], color="0.7", lw=0.8)
        ax.plot(x, data.mean(axis=1), "o-", color="C0", lw=2, label="mean response")
        ax.legend()
    else:
        axes = tuple(j for j in range(sweep.results.ndim) if j != xi)
        mean_resp = sweep.results.mean(axis=axes)
        ax.plot(x, mean_resp, "o-", lw=2, label="mean response")
        ax.legend()
    ax.set_xlabel(x_param)
    ax.set_ylabel("objective")
    ax.set_title(f"Parameter sweep vs {x_param}")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path
