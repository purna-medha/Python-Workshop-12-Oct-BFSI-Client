# External formats encode values rather than guarantee their meaning. Decode
# each record, convert known representations, and validate before using it.
# Resource context managers release file handles even when processing fails.
#
# Read a small CSV. A positive quantity can still reference an unknown product.

import csv
from pathlib import Path
from pydantic import ValidationError
from m05.csv_input import request_from_row

source_path = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
with source_path.open(newline="", encoding="utf-8") as source:
    for row_number, row in enumerate(csv.DictReader(source), start=2):
        try:
            request = request_from_row(row)
        except (ValueError, ValidationError) as error:
            print(f"Row {row_number}: invalid source data ({type(error).__name__})")
            continue
        print(f"Row {row_number}: validated {request.model_dump()}")

# Rows 2, 3, and 5 pass shape validation; 4 and 6 are invalid source data.
# Product "999" is intentionally left for the server's business-rule check.
