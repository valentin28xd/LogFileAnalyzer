from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .models import LogEntry


def save_frequency_chart(entries: Iterable[LogEntry], path: str | Path) -> None:
    import matplotlib.pyplot as plt

    entry_list = list(entries)
    levels = ("INFO", "WARNING", "ERROR")
    counts = [sum(entry.level == level for entry in entry_list) for level in levels]
    colors = ("#2a9d8f", "#e9c46a", "#e76f51")
    figure, axis = plt.subplots(figsize=(8, 4.5))
    axis.bar(levels, counts, color=colors)
    axis.set_title("Log frequency by level")
    axis.set_xlabel("Level")
    axis.set_ylabel("Entries")
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(path, dpi=140)
    plt.close(figure)
