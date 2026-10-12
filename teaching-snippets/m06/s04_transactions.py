# A transaction makes related changes succeed or fail together. Catching an
# exception alone does not guarantee clean state: rollback must undo earlier
# writes in the operation. Keep the whole operation inside one transaction.
#
# A supplied failure hook rejects the second order line after the first is saved.

import sqlite3
from m03.shop import create_order
from m06.database import connect, initialize
from m06.orders import save_order

with connect(":memory:") as connection:
    initialize(connection)
    # Supplied SQL hook; focus on the transaction, not trigger syntax.
    connection.executescript("""
        CREATE TEMP TRIGGER reject_bottle BEFORE INSERT ON order_lines
        WHEN NEW.product_id = '3'
        BEGIN SELECT RAISE(ABORT, 'simulated line failure'); END;
    """)
    order = create_order([("1", 1), ("3", 1)])
    try:
        save_order(connection, order)
    except sqlite3.IntegrityError as error:
        print(error)
    print(connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0])
    print(connection.execute("SELECT COUNT(*) FROM order_lines").fetchone()[0])

# Both counts are 0. In orders.py, with connection covers the header and all lines.
# If each write committed independently, a failed operation could leave partial data.
