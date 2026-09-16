from __future__ import annotations

from collections import Counter
from datetime import date, datetime
from typing import Iterable

from .models import LogEntry


class LogAnalyzer:
    def __init__(self, entries: Iterable[LogEntry]) -> None:
        self.entries = list(entries)

    def counts_by_level(self) -> dict[str, int]:
        counts = Counter(entry.level for entry in self.entries)
        return {level: counts.get(level, 0) for level in ("INFO", "WARNING", "ERROR")}

    def filter(self, keyword: str | None = None, on_date: date | None = None) -> list[LogEntry]:
        normalized_keyword = keyword.casefold().strip() if keyword else None
        return [
            entry
            for entry in self.entries
            if (not normalized_keyword or normalized_keyword in entry.message.casefold())
            and (on_date is None or entry.timestamp.date() == on_date)
        ]

    def summary(self) -> dict[str, object]:
        if not self.entries:
            return {"total_entries": 0, "first_log": None, "last_log": None, "common_errors": []}
        errors = Counter(entry.message for entry in self.entries if entry.level == "ERROR")
        return {
            "total_entries": len(self.entries),
            "first_log": self.entries[0].to_dict(),
            "last_log": self.entries[-1].to_dict(),
            "common_errors": [
                {"message": message, "count": count}
                for message, count in errors.most_common(10)
            ],
        }

    def timeline(self, entries: Iterable[LogEntry] | None = None) -> dict[datetime, int]:
        selected = self.entries if entries is None else entries
        return dict(sorted(Counter(entry.timestamp for entry in selected).items()))
