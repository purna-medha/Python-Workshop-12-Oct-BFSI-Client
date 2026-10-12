PRODUCTS = {
    "1": {"name": "USB-C Cable", "price_paise": 49900},
    "2": {"name": "Mechanical Keyboard", "price_paise": 549900},
    "3": {"name": "Steel Water Bottle", "price_paise": 89900},
}

def money(paise):
    return f"₹{paise // 100}.{paise % 100:02d}"

def browse():
    for product_id, product in PRODUCTS.items():
        print(f"{product_id}: {product['name']} — {money(product['price_paise'])}")

def add_to_cart(cart, product_id):
    if product_id not in PRODUCTS:
        print("Unknown product ID. Enter 1, 2, or 3.")
        return
    cart.append(product_id)
    print(f"Added {PRODUCTS[product_id]['name']}.")

def checkout(cart):
    if not cart:
        print("Your cart is empty.")
        return
    print("\nPico-Zon receipt (simulated order)")
    total = 0
    for product_id in cart:
        product = PRODUCTS[product_id]
        total += product["price_paise"]
        print(f"  {product['name']}: {money(product['price_paise'])}")
    print(f"Total: {money(total)} — no payment taken.\n")
    cart.clear()

def main():
    cart = []
    print("Welcome to Pico-Zon!")
    browse()
    while True:
        command = input("Product ID / browse / checkout / quit: ").strip().lower()
        if command == "quit":
            break
        elif command == "browse":
            browse()
        elif command == "checkout":
            checkout(cart)
        else:
            add_to_cart(cart, command)

if __name__ == "__main__":
    main()
