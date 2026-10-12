# M8: substitute external HTTP while keeping real client and workflow logic.
import requests
import pytest
from unittest.mock import Mock, patch
from nanozon.client import submit_order
from nanozon.workflow import process_row, run_workflow

PAYLOAD = {"items": [{"product_id": "1", "quantity": 2}]}
RESPONSE = {"order_id": "example-order", "total_paise": 99800,
            "lines": [{"product_id": "1", "name": "USB-C Cable",
                       "unit_price_paise": 49900, "quantity": 2}]}


def successful_response():
    response = Mock(spec=requests.Response)
    response.raise_for_status.return_value = None
    response.json.return_value = RESPONSE
    return response


def test_client_checks_status_and_uses_timeout():
    response = successful_response()
    with patch("nanozon.client.requests.post", return_value=response) as post:
        result = submit_order("http://example.test", PAYLOAD)
    # ANSWER m08 client_success BEGIN
    assert result.total_paise == 99800
    response.raise_for_status.assert_called_once_with()
    post.assert_called_once_with("http://example.test/orders", json=PAYLOAD, timeout=5)
    # ANSWER m08 client_success END


def test_client_timeout_remains_distinct():
    # ANSWER m08 timeout_check BEGIN
    with patch("nanozon.client.requests.post", side_effect=requests.Timeout("Timed out")):
        with pytest.raises(requests.Timeout):
            submit_order("http://example.test", PAYLOAD)
    # ANSWER m08 timeout_check END


@pytest.mark.parametrize("case, expected", [
    ("rejected", "rejected"), ("malformed", "invalid_response"),
    ("shape", "invalid_response"),
])
def test_workflow_keeps_remote_failures_distinct(case, expected):
    response = successful_response()
    if case == "rejected":
        error = requests.HTTPError("Rejected", response=response)
        response.status_code = 404
        response.raise_for_status.side_effect = error
    elif case == "malformed":
        response.json.side_effect = ValueError("Invalid JSON")
    else:
        response.json.return_value = {"unexpected": "data"}
    with patch("nanozon.client.requests.post", return_value=response):
        outcome = process_row({"product_id": "1", "quantity": "2"}, "http://example.test")
    # ANSWER m08 failure_categories BEGIN
    assert outcome["status"] == expected
    # ANSWER m08 failure_categories END


def test_invalid_source_does_not_call_http():
    with patch("nanozon.client.requests.post") as post:
        outcome = process_row({"product_id": "1", "quantity": "0"}, "http://example.test")
    assert outcome["status"] == "invalid_source"
    post.assert_not_called()


def test_workflow_saves_report(tmp_path):
    import json
    source = tmp_path / "orders.csv"
    report = tmp_path / "report.json"
    source.write_text(chr(10).join(["product_id,quantity", "1,2", "1,0", ""]), encoding="utf-8")
    with patch("nanozon.client.requests.post", return_value=successful_response()):
        outcomes = run_workflow(source, report, "http://example.test")
    assert [outcome["status"] for outcome in outcomes] == ["created", "invalid_source"]
    assert json.loads(report.read_text()) == outcomes
