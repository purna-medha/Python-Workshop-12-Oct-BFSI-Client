# M1/M2: the same shop expressed with values, collections, and ordinary functions.
# Objects, servers, and databases arrive in later checkpoints.
PRODUCTS = {
    "1": {"name": "USB-C Cable", "category": "Electronics", "price_paise": 49900},
    "2": {"name": "Mechanical Keyboard", "category": "Electronics", "price_paise": 549900},
    "3": {"name": "Steel Water Bottle", "category": "Home", "price_paise": 89900},
}


def validate_quantity(quantity):
    if type(quantity) is not int or quantity <= 0:
        raise ValueError("Quantity must be a positive integer")


def money(paise):
    # ANSWER m01 money BEGIN
    return f"₹{paise // 100}.{paise % 100:02d}"
    # ANSWER m01 money END


def product_label(product_id, product):
    # ANSWER m01 label BEGIN
    return f"{product_id}: {product['name']} | {money(product['price_paise'])}"
    # ANSWER m01 label END


def calculate_line_total(unit_price_paise, quantity):
    validate_quantity(quantity)
    # ANSWER m01 line_total BEGIN
    return unit_price_paise * quantity
    # ANSWER m01 line_total END


def search_products(*, query="", minimum_paise=None, maximum_paise=None):
    for bound in (minimum_paise, maximum_paise):
        if bound is not None and (type(bound) is not int or bound < 0):
            raise ValueError("Price bounds must be non-negative integers")
    if minimum_paise is not None and maximum_paise is not None:
        if minimum_paise > maximum_paise:
            raise ValueError("Minimum price cannot exceed maximum price")
    # ANSWER m02 query BEGIN
    # matches = {}
    # for product_id, product in PRODUCTS.items():
    #     if query.strip().casefold() not in product["name"].casefold():
    #         continue
    #     if minimum_paise is not None and product["price_paise"] < minimum_paise:
    #         continue
    #     if maximum_paise is not None and product["price_paise"] > maximum_paise:
    #         continue
    #     matches[product_id] = product
    # return matches
    raise NotImplementedError("M02: complete query")  # LAB-GUARD: remove when answering
    # ANSWER m02 query END


def add_item(cart, product_id, quantity=1):
    validate_quantity(quantity)
    if product_id not in PRODUCTS:
        raise KeyError(product_id)
    # ANSWER m02 add BEGIN
    # cart[product_id] = cart.get(product_id, 0) + quantity
    raise NotImplementedError("M02: complete add")  # LAB-GUARD: remove when answering
    # ANSWER m02 add END


def update_item(cart, product_id, quantity):
    validate_quantity(quantity)
    if product_id not in cart:
        raise KeyError(product_id)
    # ANSWER m02 update BEGIN
    # cart[product_id] = quantity
    raise NotImplementedError("M02: complete update")  # LAB-GUARD: remove when answering
    # ANSWER m02 update END


def remove_item(cart, product_id):
    if product_id not in cart:
        raise KeyError(product_id)
    # ANSWER m02 remove BEGIN
    # del cart[product_id]
    raise NotImplementedError("M02: complete remove")  # LAB-GUARD: remove when answering
    # ANSWER m02 remove END


def cart_subtotal(cart):
    # ANSWER m02 subtotal BEGIN
    # total_paise = 0
    # for product_id, quantity in cart.items():
    #     total_paise += calculate_line_total(PRODUCTS[product_id]["price_paise"], quantity)
    # return total_paise
    raise NotImplementedError("M02: complete subtotal")  # LAB-GUARD: remove when answering
    # ANSWER m02 subtotal END


def show_products(products):
    for product_id, product in products.items():
        print(product_label(product_id, product))


def dispatch(parts, cart):
    command, *arguments = parts
    if command == "list":
        show_products(PRODUCTS)
    elif command == "search":
        show_products(search_products(query=" ".join(arguments)))
    elif command == "budget":
        if len(arguments) != 1:
            raise ValueError("Use: budget MAXIMUM_PAISE")
        show_products(search_products(maximum_paise=int(arguments[0])))
    elif command in {"add", "update"}:
        if len(arguments) != 2:
            raise ValueError(f"Use: {command} PRODUCT_ID QUANTITY")
        operation = add_item if command == "add" else update_item
        operation(cart, arguments[0], int(arguments[1]))
        print("Cart updated")
    elif command == "remove":
        if len(arguments) != 1:
            raise ValueError("Use: remove PRODUCT_ID")
        remove_item(cart, arguments[0])
    elif command == "cart":
        print(cart)
        print("Subtotal:", money(cart_subtotal(cart)))
    elif command == "checkout":
        if not cart:
            raise ValueError("Cannot checkout an empty cart")
        for product_id, quantity in cart.items():
            print(PRODUCTS[product_id]["name"], quantity)
        total = cart_subtotal(cart)
        print("Simulated receipt:", money(total), "— no payment taken")
        cart.clear()
    else:
        raise ValueError("Unknown command; type help")


def main():
    import shlex
    cart = {}                      # Fresh state for this shopper.
    print("Nano-Zon: type help. The lab may report a pending answer.")
    while True:
        try:
            parts = shlex.split(input("nano-zon> "))
            if not parts:
                continue
            if parts[0] == "quit":
                break
            if parts[0] == "help":
                print("list | search TEXT | budget PAISE | add ID QTY | update ID QTY")
                print("remove ID | cart | checkout | quit")
                continue
            dispatch(parts, cart)
        except NotImplementedError as error:
            print(f"Lab pending: {error}")
        except KeyError as error:
            print("Unknown product or cart item:", error.args[0])
        except ValueError as error:
            print(error)
        except (EOFError, KeyboardInterrupt):
            print("Goodbye")
            break


if __name__ == "__main__":
    main()
