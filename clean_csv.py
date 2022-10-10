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