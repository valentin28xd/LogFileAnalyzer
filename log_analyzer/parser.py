from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Iterable, TextIO

from .models import LogEntry, ParseResult


class LogParser:
    """Parse common text log formats without loading the whole file in memory."""

    _line_pattern = re.compile(
        r"^\s*(?:\[(?P<bracket_timestamp>[^\]]+)\]|(?P<plain_timestamp>"
        r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:[.,]\d{1,6})?(?:Z|[+-]\d{2}:?\d{2})?))"
        r"\s+(?P<level>INFO|ERROR|WARNING)\b\s*[:|-]?\s*(?P<message>.*)$",
        re.IGNORECASE,
    )
    _timestamp_formats = (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S,%f",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S.%f",
    )

    def parse_file(self, path: str | Path, encoding: str = "utf-8") -> ParseResult:
        with Path(path).open("r", encoding=encoding, errors="replace") as handle:
            return self.parse_lines(handle)

    def parse_text(self, text: str) -> ParseResult:
        return self.parse_lines(text.splitlines())

    def parse_lines(self, lines: Iterable[str]) -> ParseResult:
        entries: list[LogEntry] = []
        malformed: list[dict[str, object]] = []
        for line_number, raw_line in enumerate(lines, start=1):
            line = raw_line.rstrip("\r\n")
            if not line.strip():
                continue
            match = self._line_pattern.match(line)
            if not match:
                malformed.append({"line": line_number, "content": line})
                continue
            timestamp_text = match.group("bracket_timestamp") or match.group("plain_timestamp")
            try:
                timestamp = self._parse_timestamp(timestamp_text)
            except ValueError:
                malformed.append({"line": line_number, "content": line, "reason": "invalid timestamp"})
                continue
            entries.append(
                LogEntry(
                    timestamp=timestamp,
                    level=match.group("level").upper(),
                    message=match.group("message").strip(),
                    source_line=line_number,
                )
            )
        return ParseResult(entries=entries, malformed_lines=malformed)

    def _parse_timestamp(self, value: str) -> datetime:
        normalized = value.strip().replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(normalized)
        except ValueError:
            for timestamp_format in self._timestamp_formats:
                try:
                    return datetime.strptime(value.strip(), timestamp_format)
                except ValueError:
                    continue
        raise ValueError(f"Unsupported timestamp: {value}")
