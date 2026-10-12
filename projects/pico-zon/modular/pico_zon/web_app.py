# A browser interface owns presentation and a local cart. It communicates
# through HTTP; it never imports the server, catalog, or database.
import os
import requests
import streamlit as st
from pico_zon.http_client import get_order, list_products, submit_order

base_url = os.getenv("PICOZON_API_URL", "http://127.0.0.1:8000")
st.set_page_config(page_title="Pico-Zon", layout="centered")
st.title("Pico-Zon")
st.caption("A tiny shop · simulated orders · no payment taken")
st.session_state.setdefault("cart", [])
browse_tab, cart_tab, orders_tab = st.tabs(["Products", "Cart", "Orders"])

try:
    with browse_tab:
        for product in list_products(base_url):
            paise = product.price_paise
            st.write(f"{product.name} — ₹{paise // 100}.{paise % 100:02d}")
            if st.button("Add one", key=product.product_id):
                st.session_state["cart"].append({
                    "product_id": product.product_id, "quantity": 1,
                })
                st.success("Added to cart")

    with cart_tab:
        st.write(f"Selected units: {len(st.session_state['cart'])}")
        st.json(st.session_state["cart"])
        if st.button("Checkout", disabled=not st.session_state["cart"]):
            order = submit_order(base_url, {"items": st.session_state["cart"]})
            st.session_state["cart"] = []
            st.success(f"Order created: {order.order_id}")
            st.json(order.model_dump())

    with orders_tab:
        order_id = st.text_input("Saved order ID")
        if st.button("Retrieve order", disabled=not order_id):
            st.json(get_order(base_url, order_id).model_dump())
except requests.HTTPError as error:
    st.error(f"HTTP rejection: {error.response.status_code}")
except requests.exceptions.JSONDecodeError:
    st.error("The server returned invalid JSON")
except requests.RequestException as error:
    st.error(f"Communication failure: {error}")
except ValueError as error:
    st.error(f"Invalid response: {error}")
