from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class LogEntry:
    timestamp: datetime
    level: str
    message: str
    source_line: int

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["timestamp"] = self.timestamp.isoformat()
        return result


@dataclass(frozen=True, slots=True)
class ParseResult:
    entries: list[LogEntry]
    malformed_lines: list[dict[str, Any]]

    @property
    def total_lines(self) -> int:
        return len(self.entries) + len(self.malformed_lines)
