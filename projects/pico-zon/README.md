# Pico-Zon

A complete tiny shop in two forms: browse → add to cart → checkout.

| Version | Purpose | Entry point |
|---|---|---|
| **Monolithic Pico-Zon** | See the whole application in 50 physical lines | [pico_zon.py](pico_zon.py) |
| **Modular Pico-Zon** | See how responsibilities become separate modules, then add API and storage layers | [modular/README.md](modular/README.md) |

Both terminal shops use the same products, commands, receipt amounts, and repeated additions. The monolithic version needs only Python 3; the modular core also uses only the standard library.

## Run

### Monolithic version

From the training folder:

```sh
python3 current-course/projects/pico-zon/pico_zon.py
```

### Modular version

```sh
cd current-course/projects/pico-zon/modular
python3 -m pico_zon
```

The [modular guide](modular/README.md) provides the file map and separate API, SQLite, and browser instructions.

Enter `1`, `2`, or `3` to add one unit. Repeat an ID for multiple units. Enter `browse` to display products, `checkout` to print a simulated receipt, or `quit` to leave.

The three products come from the existing capstone catalog: USB-C Cable (₹499), Mechanical Keyboard (₹5,499), and Steel Water Bottle (₹899). Prices are stored as integer paise, matching the revised shopping design. No payment is taken; successful checkout clears the cart. Unknown IDs and empty carts receive readable messages.

## Opening demonstration

1. Run the whole application before explaining its internals.
2. Add `1`, `1`, and `3`, then enter `checkout`: the total is ₹1,897.00.
3. Enter `checkout` again to show that the cart has been cleared.
4. In M1, discuss values, expressions, formatting, and simple functions such as `money`.
5. In M2, revisit the same script to explain dictionaries, lists, iteration, branching, and mutable cart state.

Each shopper starts with a fresh cart in `main`. Repeated items appear as separate receipt lines. Fixed prices and in-memory state keep the opening example small. M3 can revisit this same journey through modular Pico-Zon's records, cart owner, reusable checkout, and CLI. Its later API and SQLite layers provide an instructor showcase; Nano-Zon supplies the richer incremental labs.

See the [application design](../../curriculum/application-design.md) and [M1–M9 outline](../../curriculum/outline-m01-m09.md).
