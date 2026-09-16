from datetime import date, datetime

from log_analyzer.analysis import LogAnalyzer
from log_analyzer.models import LogEntry


def entries() -> list[LogEntry]:
    return [
        LogEntry(datetime(2026, 9, 16, 8), "INFO", "started", 1),
        LogEntry(datetime(2026, 9, 16, 9), "ERROR", "database unavailable", 2),
        LogEntry(datetime(2026, 9, 17, 9), "ERROR", "database unavailable", 3),
    ]


def test_counts_filters_and_summary() -> None:
    analyzer = LogAnalyzer(entries())
    assert analyzer.counts_by_level() == {"INFO": 1, "WARNING": 0, "ERROR": 2}
    assert len(analyzer.filter("DATABASE", date(2026, 9, 16))) == 1
    assert analyzer.summary()["common_errors"] == [{"message": "database unavailable", "count": 2}]
