from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from .analysis import LogAnalyzer
from .output import save_json
from .parser import LogParser
from .visualization import save_frequency_chart


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze INFO, WARNING, and ERROR log entries.")
    parser.add_argument("log_file", type=Path)
    parser.add_argument("--keyword", help="Only include messages containing this text.")
    parser.add_argument("--date", dest="on_date", help="Only include YYYY-MM-DD entries.")
    parser.add_argument("--json", dest="json_path", type=Path, help="Write parsed results to JSON.")
    parser.add_argument("--chart", type=Path, help="Write a PNG frequency chart.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        on_date = date.fromisoformat(args.on_date) if args.on_date else None
    except ValueError as error:
        raise SystemExit(f"Invalid --date value: {error}") from error

    parse_result = LogParser().parse_file(args.log_file)
    analyzer = LogAnalyzer(parse_result.entries)
    selected = analyzer.filter(args.keyword, on_date)
    selected_analyzer = LogAnalyzer(selected)
    summary = selected_analyzer.summary()

    print(f"Entries: {summary['total_entries']}")
    print("Counts: " + ", ".join(f"{level}={count}" for level, count in selected_analyzer.counts_by_level().items()))
    print(f"Malformed lines: {len(parse_result.malformed_lines)}")
    if summary["first_log"]:
        print(f"First: {summary['first_log']['timestamp']} {summary['first_log']['message']}")
        print(f"Last:  {summary['last_log']['timestamp']} {summary['last_log']['message']}")
    if summary["common_errors"]:
        print("Common errors:")
        for error in summary["common_errors"]:
            print(f"  {error['count']}x {error['message']}")
    if args.json_path:
        save_json(args.json_path, selected, parse_result)
        print(f"JSON written to {args.json_path}")
    if args.chart:
        save_frequency_chart(selected, args.chart)
        print(f"Chart written to {args.chart}")
    return 0
