from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .models import LogEntry, ParseResult


def save_json(
    path: str | Path,
    entries: Iterable[LogEntry],
    parse_result: ParseResult | None = None,
) -> None:
    entry_list = list(entries)
    payload = {
        "entries": [entry.to_dict() for entry in entry_list],
        "counts": {
            level: sum(entry.level == level for entry in entry_list)
            for level in ("INFO", "WARNING", "ERROR")
        },
        "malformed_lines": parse_result.malformed_lines if parse_result else [],
    }
    Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
