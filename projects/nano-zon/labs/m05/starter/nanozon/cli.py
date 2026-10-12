# Interaction formats results and handles expected input failures; rules live elsewhere.
import shlex
from .calculations import money
from .cart import ShoppingCart
from .catalog import select_products
from .runtime import open_store


def show_products(products):
    for product in products:
        print(f"{product.product_id}: {product.name} | {product.category} | {money(product.price_paise)}")


def show_order(order):
    print(f"Simulated order {order.order_id}")
    for line in order.lines:
        print(f"  {line.name} × {line.quantity}: {money(line.line_total_paise)}")
    print(f"Total: {money(order.total_paise)}; no payment taken")


def dispatch(parts, cart, store):
    command, *arguments = parts
    if command == "list":
        show_products(select_products(store.all_products()))
    elif command == "search":
        show_products(select_products(store.all_products(), query=" ".join(arguments)))
    elif command == "budget":
        if len(arguments) != 1:
            raise ValueError("Use: budget MAXIMUM_PAISE")
        show_products(select_products(store.all_products(), maximum_paise=int(arguments[0])))
    elif command in {"add", "update"}:
        if len(arguments) != 2:
            raise ValueError(f"Use: {command} PRODUCT_ID QUANTITY")
        operation = cart.add if command == "add" else cart.update
        operation(arguments[0], int(arguments[1]))
        print("Cart updated")
    elif command == "remove":
        if len(arguments) != 1:
            raise ValueError("Use: remove PRODUCT_ID")
        cart.remove(arguments[0])
        print("Item removed")
    elif command == "cart":
        for item in cart.items.values():
            print(f"{item.product.name} × {item.quantity}")
        print(f"Subtotal: {money(cart.subtotal_paise)}")
    elif command == "checkout":
        order = cart.checkout(store)
        show_order(order)
    elif command == "order":
        if len(arguments) != 1:
            raise ValueError("Use: order ORDER_ID")
        show_order(store.get_order(arguments[0]))
    else:
        raise ValueError("Unknown command; type help")


def main():
    store = open_store()
    cart = ShoppingCart(store.all_products())
    print("Nano-Zon — a simulated shop. Type help for commands.")
    while True:
        try:
            parts = shlex.split(input("nano-zon> "))
            if not parts:
                continue
            if parts[0] == "quit":
                break
            if parts[0] == "help":
                print("list | search TEXT | budget PAISE | add ID QTY | update ID QTY")
                print("remove ID | cart | checkout | order ORDER_ID | quit")
                continue
            dispatch(parts, cart, store)
        except NotImplementedError as error:
            print(f"Lab pending: {error}")
        except KeyError as error:
            print(f"Unknown product, cart item, or order: {error.args[0]}")
        except ValueError as error:
            print(error)
        except (EOFError, KeyboardInterrupt):
            print("Goodbye")
            break


if __name__ == "__main__":
    main()
