# M5 companion: file I/O and validation, without HTTP or reporting decisions.
import csv
from m05.contracts import OrderRequest


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def request_from_row(row) -> OrderRequest:
    # CSV provides strings. Convert explicitly before strict model validation.
    return OrderRequest(items=[{
        "product_id": row["product_id"],
        "quantity": int(row["quantity"]),
    }])
