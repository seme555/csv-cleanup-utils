# CSV Cleanup Utilities

Small Python CLI tools for validating, normalizing, and summarizing tabular CSV files.

## Features

- Header normalization
- Whitespace cleanup
- Empty-row removal
- Column blank counts and top values
- Optional cleaned CSV output

## Usage

```bash
# summary + write cleaned file
python clean_csv.py sample_messy.csv

# summary only
python clean_csv.py sample_messy.csv --summary-only

# custom output path
python clean_csv.py sample_messy.csv -o output/clean.csv
```

## Author
