#!/usr/bin/env python3
"""Validate, normalize, and summarize simple CSV files."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


def normalize_header(value: str) -> str:
    return " ".join(value.strip().lower().replace("-", " ").split())


def normalize_cell(value: str) -> str:
    return " ".join(value.strip().split())


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise SystemExit("CSV has no header row.")
        headers = [normalize_header(h) for h in reader.fieldnames]
        rows: list[dict[str, str]] = []
        for raw in reader:
            row = {
                normalize_header(key): normalize_cell(value or "")
                for key, value in raw.items()
                if key is not None
            }
            rows.append(row)
    return headers, rows


def drop_empty_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    cleaned = []
    for row in rows:
        if any(value for value in row.values()):
            cleaned.append(row)
    return cleaned


def summarize(headers: list[str], rows: list[dict[str, str]]) -> None:
    print(f"rows: {len(rows)}")
    print(f"columns: {', '.join(headers)}")
    for header in headers:
        blank = sum(1 for row in rows if not row.get(header))
        values = Counter(row.get(header, "") for row in rows if row.get(header))
        top = values.most_common(3)
        top_text = ", ".join(f"{value} ({count})" for value, count in top) or "n/a"
        print(f"- {header}: blank={blank}, top={top_text}")


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({header: row.get(header, "") for header in headers})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean and summarize a CSV file.")
    parser.add_argument("input", help="Input CSV path")
    parser.add_argument(
        "-o",
        "--output",
        help="Optional cleaned CSV output path",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",