"""
Matplotlib dashboard for DORA metrics.
Generates a 2×2 panel chart saved to output/dora_dashboard.png.
"""
from __future__ import annotations
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from .metrics import DoraMetrics, MetricResult


# DORA band color palette
BAND_COLORS = {
    "Elite":  "#22c55e",   # green
    "High":   "#84cc16",   # lime
    "Medium": "#f59e0b",   # amber
    "Low":    "#ef4444",   # red
    "N/A":    "#94a3b8",   # slate
}

BAND_ORDER = ["Elite", "High", "Medium", "Low"]


def _band_color(band: str) -> str:
    return BAND_COLORS.get(band, BAND_COLORS["N/A"])


def _gauge(ax: plt.Axes, metric: MetricResult) -> None:
    """Draw a horizontal bar gauge with DORA band coloring."""
    color = _band_color(metric.band)

    # Background bar (full width = 1.0)
    ax.barh(0, 1.0, color="#e2e8f0", height=0.5, left=0)

    # Foreground bar — fill proportional to band rank (Elite=1.0, Low=0.25)
    fill = {"Elite": 1.0, "High": 0.75, "Medium": 0.5, "Low": 0.25}.get(metric.band, 0.5)
    ax.barh(0, fill, color=color, height=0.5, left=0, alpha=0.9)

    # Value label
    ax.text(
        0.5, 0.55,
        f"{metric.value} {metric.unit}",
        ha="center", va="bottom", fontsize=12, fontweight="bold",
        transform=ax.transAxes,
    )
    # Band label
    ax.text(
        0.5, -0.55,
        f"● {metric.band}",
        ha="center", va="top", fontsize=10,
        color=color, fontweight="bold",
        transform=ax.transAxes,
    )
    # Detail (small)
    ax.text(
        0.5, -0.9,
        metric.detail,
        ha="center", va="top", fontsize=7.5, color="#64748b",
        transform=ax.transAxes,
    )

    ax.set_xlim(0, 1)
    ax.set_ylim(-0.5, 0.5)
    ax.axis("off")
    ax.set_title(metric.label, fontsize=11, fontweight="bold", pad=18)


def generate_dashboard(metrics: DoraMetrics, repo: str, out_dir: str = "output") -> str:
    """
    Compute all four metrics and save a 2×2 dashboard PNG.
    Returns the path to the saved file.
    """
    results = metrics.all()

    fig, axes = plt.subplots(2, 2, figsize=(12, 7))
    fig.patch.set_facecolor("#f8fafc")

    for ax, result in zip(axes.flat, results):
        ax.set_facecolor("#f8fafc")
        _gauge(ax, result)

    # Legend
    patches = [
        mpatches.Patch(color=BAND_COLORS[b], label=b) for b in BAND_ORDER
    ]
    fig.legend(
        handles=patches,
        loc="lower center",
        ncol=4,
        fontsize=9,
        title="DORA Performance Band",
        title_fontsize=9,
        framealpha=0.0,
        bbox_to_anchor=(0.5, -0.01),
    )

    fig.suptitle(
        f"DORA Metrics Dashboard — {repo}",
        fontsize=15, fontweight="bold", y=1.02,
    )
    plt.tight_layout(pad=2.5)

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "dora_dashboard.png")
    fig.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return out_path
