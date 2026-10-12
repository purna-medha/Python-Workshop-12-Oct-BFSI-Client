# Automation composes existing operations; each independent row retains its own outcome.
import csv
import json
import logging
import os
from pathlib import Path
import requests
from .client import submit_order
from .schemas import OrderRequest

logger = logging.getLogger(__name__)


def request_from_row(row: dict) -> OrderRequest:
    # CSV strings need explicit conversion before strict quantity validation.
    # ANSWER m05 csv_conversion BEGIN
    # quantity_text = row["quantity"]
    # if not isinstance(quantity_text, str) or not quantity_text.strip():
    #     raise ValueError("Quantity text is required")
    # return OrderRequest(items=[{
    #     "product_id": row["product_id"], "quantity": int(quantity_text),
    # }])
    raise NotImplementedError("M05: complete csv_conversion")  # LAB-GUARD: remove when answering
    # ANSWER m05 csv_conversion END


def process_row(row: dict, base_url: str) -> dict:
    try:
        request = request_from_row(row)
    except (KeyError, ValueError) as error:
        return {"status": "invalid_source", "detail": str(error)}
    try:
        # ANSWER m05 workflow_call BEGIN
        # order = submit_order(base_url, request.model_dump())
        # return {"status": "created", "order_id": order.order_id,
        #         "total_paise": order.total_paise}
        raise NotImplementedError("M05: complete workflow_call")  # LAB-GUARD: remove when answering
        # ANSWER m05 workflow_call END
    except requests.HTTPError as error:
        return {"status": "rejected", "http_status": error.response.status_code}
    except requests.exceptions.JSONDecodeError as error:
        return {"status": "invalid_response", "detail": str(error)}
    except requests.RequestException as error:
        return {"status": "communication_failed", "detail": str(error)}
    except ValueError as error:
        return {"status": "invalid_response", "detail": str(error)}


def run_workflow(source_path: Path, report_path: Path, base_url: str) -> list[dict]:
    with source_path.open(newline="", encoding="utf-8") as source:
        outcomes = []
        for number, row in enumerate(csv.DictReader(source), start=2):
            outcome = {"row": number, **process_row(row, base_url)}
            outcomes.append(outcome)
            logger.info("Row %s: %s", number, outcome["status"])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    # ANSWER m05 json_report BEGIN
    # report_path.write_text(json.dumps(outcomes, indent=2), encoding="utf-8")
    raise NotImplementedError("M05: complete json_report")  # LAB-GUARD: remove when answering
    # ANSWER m05 json_report END
    return outcomes


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    base_url = os.getenv("NANOZON_API_URL", "http://127.0.0.1:8000")
    outcomes = run_workflow(Path("data/orders.csv"), Path("data/order-report.json"), base_url)
    for outcome in outcomes:
        print(outcome)


if __name__ == "__main__":
    main()
