# Log File Analyzer

A Python OOP application for parsing `.log` files, filtering entries, producing summaries, exporting JSON, and generating frequency charts.

## Supported format

The parser accepts these forms when the level is `INFO`, `WARNING`, or `ERROR`:

```text
[2026-09-16 08:00:00] INFO Application started
2026-09-16T08:01:02 ERROR: database unavailable
[2026-09-16 08:02:00,123] WARNING - retry scheduled
```

Blank lines are ignored. Malformed lines are recorded with their source line number and do not stop parsing.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

Install `pytest` to run the test suite:

```powershell
python -m pip install pytest
```

## CLI

```powershell
python -m log_analyzer sample.log --json results.json --chart frequency.png
python -m log_analyzer sample.log --keyword database --date 2026-09-16
```

The CLI prints totals, per-level counts, first and last entries, common errors, and malformed line counts.

## GUI

Launch the desktop viewer with:

```powershell
python -c "from log_analyzer.gui import launch; launch()"
```

Use **Open log** to load a file and filter visible messages by keyword.

## Design

- `LogParser` streams lines and returns `ParseResult` with valid `LogEntry` objects and malformed-line diagnostics.
- `LogAnalyzer` provides level counts, keyword/date filters, summaries, and timelines.
- `save_json` and `save_frequency_chart` are reusable output services used by the CLI.
- `sample.log` provides a small manual test fixture.
