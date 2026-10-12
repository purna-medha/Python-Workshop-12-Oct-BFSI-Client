# Integration tests establish whether real components agree on their boundary.
# A route test checks request decoding, validation, domain behavior, and response
# encoding together. TestClient runs these components without a separate server.
#
# Exercise the validated M5 route, including contract and business-rule rejection.

from fastapi.testclient import TestClient
from m05.s03_validation_and_rules import app


def test_order_route_uses_real_business_logic():
    with TestClient(app) as client:
        response = client.post("/orders", json={
            "items": [{"product_id": "1", "quantity": 2}],
        })
    assert response.status_code == 201
    assert response.json()["total_paise"] == 99800
    assert response.json()["lines"][0]["name"] == "USB-C Cable"


def test_route_distinguishes_invalid_shape_and_missing_product():
    with TestClient(app) as client:
        invalid = client.post("/orders", json={
            "items": [{"product_id": "1", "quantity": 0}],
        })
        missing = client.post("/orders", json={
            "items": [{"product_id": "999", "quantity": 1}],
        })
    assert invalid.status_code == 422
    assert missing.status_code == 404
# Run: uv run --extra dev pytest m08/s01_component_boundaries.py -q
