# Workflows coordinate operations and retain outcomes for later decisions.
# Distinguish source, response, and communication failures in the order report.
# Start M5 snippet 03, submit CSV rows, and save a JSON report locally.

import json
import logging
import os
from pathlib import Path
import requests
from m05.csv_input import read_rows, request_from_row
from m05.http_client import submit_order

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
base_url = os.getenv("NANOZON_API_URL", "http://127.0.0.1:8000")
source = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
outcomes = []
for row_number, row in enumerate(read_rows(source), start=2):
    outcome = {"row": row_number}
    try:
        request = request_from_row(row)
    except ValueError as error:     # Also catches Pydantic ValidationError.
        outcome.update(status="invalid_source", detail=str(error))
    else:
        try:
            order = submit_order(base_url, request.model_dump())
            outcome.update(status="created", order_id=order.order_id)
        except requests.HTTPError as error:
            outcome.update(status="rejected", http_status=error.response.status_code)
        except requests.exceptions.JSONDecodeError as error:
            outcome.update(status="invalid_response", detail=str(error))
        except requests.RequestException as error:
            outcome.update(status="communication_failed", detail=str(error))
        except ValueError as error:
            outcome.update(status="invalid_response", detail=str(error))
    outcomes.append(outcome)
    logging.getLogger(__name__).info("Row %s: %s", row_number, outcome["status"])
report_path = Path("order-report.json")
report_path.write_text(json.dumps(outcomes, indent=2), encoding="utf-8")
print(report_path.resolve())
# Expected with the supplied CSV: two created, two invalid_source, one rejected.
