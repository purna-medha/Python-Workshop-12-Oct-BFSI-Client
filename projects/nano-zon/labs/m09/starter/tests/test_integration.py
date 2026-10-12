# M8: run real routes and real SQLite; inspect both responses and resulting state.
import sqlite3
import pytest
from fastapi.testclient import TestClient
from nanozon.api import create_app
from nanozon.storage import SQLiteStore
from nanozon.orders import build_order
from nanozon.catalog import seed_products


def test_order_round_trip_and_restart(client, store):
    response = client.post("/orders", json={
        "items": [{"product_id": "1", "quantity": 2},
                  {"product_id": "3", "quantity": 1}],
    })
    # ANSWER m08 round_trip BEGIN
    assert response.status_code == 201
    order = response.json()
    assert order["total_paise"] == 189700
    assert client.get(f"/orders/{order['order_id']}").json() == order
    reopened = SQLiteStore(store.database_path)
    assert reopened.get_order(order["order_id"]).total_paise == 189700
    with store.connect() as connection:
        count = connection.execute("SELECT COUNT(*) FROM order_lines").fetchone()[0]
    assert count == 2
    # ANSWER m08 round_trip END


def test_api_rejections_do_not_save_orders(client, store):
    invalid = client.post("/orders", json={"items": [{"product_id": "1", "quantity": 0}]})
    missing = client.post("/orders", json={"items": [{"product_id": "999", "quantity": 1}]})
    assert invalid.status_code == 422
    assert missing.status_code == 404
    assert client.get("/products/missing").status_code == 404
    assert client.get("/orders/missing").status_code == 404
    with store.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0


def test_later_catalog_change_preserves_order(store):
    order = build_order([("1", 2)], store.all_products())
    store.save_order(order)
    with store.connect() as connection:
        with connection:
            connection.execute("UPDATE products SET price_paise = ? WHERE product_id = ?",
                               (99900, "1"))
    assert store.get_order(order.order_id).lines[0].unit_price_paise == 49900
    assert store.get_order(order.order_id).total_paise == 99800


def test_failed_save_rolls_back_header_and_lines(store):
    with store.connect() as connection:
        connection.executescript("""
            CREATE TRIGGER reject_bottle BEFORE INSERT ON order_lines
            WHEN NEW.product_id = '3'
            BEGIN SELECT RAISE(ABORT, 'simulated failure'); END;
        """)
    with TestClient(create_app(store), raise_server_exceptions=False) as client:
        response = client.post("/orders", json={
            "items": [{"product_id": "1", "quantity": 1},
                      {"product_id": "3", "quantity": 1}],
        })
    # ANSWER m08 rollback_assertions BEGIN
    assert response.status_code == 500
    with store.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM order_lines").fetchone()[0] == 0
    # ANSWER m08 rollback_assertions END


def test_duplicate_order_id_is_rejected_without_changes(store):
    order = build_order([("1", 1)], seed_products())
    store.save_order(order)
    with pytest.raises(sqlite3.IntegrityError):
        store.save_order(order)
    assert store.get_order(order.order_id) == order
