# M3 companion: presentation depends on the domain; the domain needs no CLI.
from m03.cart import ShoppingCart
from m03.catalog import PRODUCTS


def main():
    for product in PRODUCTS.values():
        print(product.product_id, product.name, product.price_paise)
    cart = ShoppingCart()
    cart.add("1", 2)
    order = cart.checkout()
    print(f"Simulated receipt: {order.total_paise} paise")


if __name__ == "__main__":
    main()
