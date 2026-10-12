# M6 companion: one transaction saves an order header and all line snapshots.
from m03.records import Order, OrderLine


def save_order(connection, order):
    with connection:               # Commit on success; rollback on exception.
        connection.execute("INSERT INTO orders VALUES (?, ?)",
                           (order.order_id, order.total_paise))
        for position, line in enumerate(order.lines):
            connection.execute(
                "INSERT INTO order_lines VALUES (?, ?, ?, ?, ?, ?)",
                (order.order_id, position, line.product_id, line.name,
                 line.unit_price_paise, line.quantity),
            )


def load_order(connection, order_id):
    header = connection.execute(
        "SELECT order_id FROM orders WHERE order_id = ?", (order_id,),
    ).fetchone()
    if header is None:
        raise KeyError(order_id)
    rows = connection.execute(
        "SELECT product_id, name, unit_price_paise, quantity FROM order_lines "
        "WHERE order_id = ? ORDER BY line_number", (order_id,),
    ).fetchall()
    return Order(header["order_id"], tuple(OrderLine(**dict(row)) for row in rows))
