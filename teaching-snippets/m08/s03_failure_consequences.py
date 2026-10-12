# A failure test must establish what happened to state, not merely observe an
# exception. Controlled failure after an earlier write exposes whether the
# operation preserves its all-or-nothing promise.
#
# Reject the second line through a supplied SQL hook, then inspect both tables.

from m06.database import connect


def test_failed_checkout_leaves_no_partial_order(client, database_path):
    with connect(database_path) as connection:
        connection.executescript("""
            CREATE TRIGGER reject_bottle BEFORE INSERT ON order_lines
            WHEN NEW.product_id = '3'
            BEGIN SELECT RAISE(ABORT, 'simulated line failure'); END;
        """)
    response = client.post("/orders", json={
        "items": [{"product_id": "1", "quantity": 1},
                  {"product_id": "3", "quantity": 1}],
    })
    assert response.status_code == 500
    with connect(database_path) as connection:
        assert connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM order_lines").fetchone()[0] == 0

# Run: uv run --extra dev pytest m08/s03_failure_consequences.py -q
# The fixture exposes 500 responses instead of re-raising server exceptions.
# The persistent trigger reaches new request connections; the test DB is disposable.
