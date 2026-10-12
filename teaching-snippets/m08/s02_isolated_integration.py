# Repeatable integration checks require known starting data and isolated
# resources. Use real local components to establish interaction, while
# configuration or dependency overrides redirect them to temporary storage.
#
# conftest.py supplies a real API and a fresh SQLite file for each test.

from m06.database import connect


def test_order_round_trip_persists_real_lines(client, database_path):
    created = client.post("/orders", json={
        "items": [{"product_id": "1", "quantity": 2},
                  {"product_id": "3", "quantity": 1}],
    })
    assert created.status_code == 201
    order = created.json()
    retrieved = client.get(f"/orders/{order['order_id']}")
    assert retrieved.status_code == 200
    assert retrieved.json() == order
    assert order["total_paise"] == 189700
    with connect(database_path) as connection:
        row = connection.execute(
            "SELECT COUNT(*) FROM order_lines WHERE order_id = ?",
            (order["order_id"],),
        ).fetchone()
    assert row[0] == 2


def test_unknown_order_returns_not_found(client):
    assert client.get("/orders/missing").status_code == 404

# Run: uv run --extra dev pytest m08/s02_isolated_integration.py -q
# Route responses and stored rows together establish that persistence really occurred.
