-- M6 supplied schema. Order lines retain checkout-time names and prices.
CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    price_paise INTEGER NOT NULL CHECK (price_paise >= 0)
);
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    total_paise INTEGER NOT NULL CHECK (total_paise >= 0)
);
CREATE TABLE IF NOT EXISTS order_lines (
    order_id TEXT NOT NULL REFERENCES orders(order_id),
    line_number INTEGER NOT NULL,
    product_id TEXT NOT NULL REFERENCES products(product_id),
    name TEXT NOT NULL,
    unit_price_paise INTEGER NOT NULL CHECK (unit_price_paise >= 0),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, line_number)
);
