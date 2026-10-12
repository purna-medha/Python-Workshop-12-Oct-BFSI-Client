# An interface chooses how to display results and explain rejected operations.
# This menu calls the same catalog and checkout operations as the API.
from .cart import ShoppingCart
from .catalog import get_product, list_products
from .shop import checkout


def money(paise: int) -> str:
    return f"₹{paise // 100}.{paise % 100:02d}"


def browse():
    for product in list_products():
        print(f"{product.product_id}: {product.name} — {money(product.price_paise)}")


def print_receipt(order):
    print("\nPico-Zon receipt (simulated order)")
    for line in order.lines:
        print(f"  {line.name}: {money(line.unit_price_paise)}")
    print(f"Total: {money(order.total_paise)} — no payment taken.\n")


def main():
    cart = ShoppingCart()
    print("Welcome to Pico-Zon!")
    browse()
    while True:
        command = input("Product ID / browse / checkout / quit: ").strip().lower()
        if command == "quit":
            break
        try:
            if command == "browse":
                browse()
            elif command == "checkout":
                print_receipt(checkout(cart))
            else:
                cart.add(command)
                print(f"Added {get_product(command).name}.")
        except KeyError:
            print("Unknown product ID. Enter 1, 2, or 3.")
        except ValueError as error:
            print(error)


if __name__ == "__main__":
    main()
