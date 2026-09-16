from log_analyzer.parser import LogParser


def test_parser_supports_common_levels_and_malformed_lines() -> None:
    result = LogParser().parse_text(
        """[2026-09-16 08:00:00] INFO Application started
2026-09-16T08:01:02 ERROR: database unavailable
[2026-09-16 08:02:00,123] warning - retry scheduled
not a log line
[not-a-date] INFO broken timestamp
"""
    )

    assert len(result.entries) == 3
    assert [entry.level for entry in result.entries] == ["INFO", "ERROR", "WARNING"]
    assert result.entries[1].message == "database unavailable"
    assert len(result.malformed_lines) == 2


def test_parser_handles_empty_lines_and_iso_offsets() -> None:
    result = LogParser().parse_text(
        "\n2026-09-16T08:00:00+00:00 INFO startup\n"
    )

    assert len(result.entries) == 1
    assert result.entries[0].timestamp.tzinfo is not None
