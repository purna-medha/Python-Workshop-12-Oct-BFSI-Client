# Python knowledge assessment — 10 MCQs

**Suggested time:** 20 minutes.  
**Format:** Closed book; do not run the code.  
**Scoring:** One mark per question; 10 marks total. Select exactly one option.

The questions ask you to explain mechanisms, apply them, or distinguish competing approaches. Some options run successfully but do not meet the stated goal. Each question is tagged with its cognitive level and current-course module.

## Q1 · Understand · M2 — Mutable defaults

```python
def make_cart(owner, items=[]):
    items.append("welcome-item")
    return {"owner": owner, "items": items}

first = make_cart("Ana")
second = make_cart("Ben")
```

Both carts contain two welcome items. Which explanation correctly identifies why?

- **A.** Dictionaries automatically combine list values when their keys have the same name.
- **B.** A function's default argument is recreated on every call, so both carts independently receive two items.
- **C.** The default list is created once when the function is defined; both calls mutate that same list.
- **D.** Returning a dictionary makes every object inside it immutable, so the second call must replace the first cart.

## Q2 · Apply · M2 — Dictionary iteration

`products` is a dictionary shaped `{product_id: product_dict}`. Each product record has `"name"` and `"price_paise"` fields. Which expression returns a **list of product names** whose prices are greater than 100000 paise?

- **A.** `[p["name"] for p in products if p["price_paise"] > 100000]`
- **B.** `[products["name"] for p in products.keys() if p > 100000]`
- **C.** `{p["name"] for p in products.items() if p["price_paise"] > 100000}`
- **D.** `[p["name"] for p in products.values() if p["price_paise"] > 100000]`

## Q3 · Understand · M3 — Dataclasses and type hints

```python
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price_paise: int = 0
```

Which statement is true?

- **A.** The dataclass generates initialization, representation, and equality methods; these type hints do not enforce runtime validation.
- **B.** Constructing a product with a text price necessarily raises a validation error because the field is annotated as an integer.
- **C.** Every dataclass is immutable, including the objects stored inside its fields.
- **D.** You must write the initialization method yourself; the decorator only changes printing.

## Q4 · Understand · M4 — A route decorator

Assume `app` is a FastAPI application.

```python
@app.get("/products/{product_id}")
def read_product(product_id: str):
    ...
```

Which statement best describes the decorator's role?

- **A.** It executes the handler body immediately when the module is imported.
- **B.** It registers the function as the GET handler for that path; FastAPI supplies the product ID from the URL when a matching request arrives.
- **C.** It turns the function into a method belonging to every Product instance.
- **D.** It is a type annotation for readers and has no runtime effect.

## Q5 · Understand · M5 — When validation happens

```python
from pydantic import BaseModel, Field

class RequestedItem(BaseModel):
    product_id: str
    quantity: int = Field(strict=True, gt=0)

item = RequestedItem(product_id="1", quantity=0)
```

What happens on the final line?

- **A.** The object is created; validation runs only if another method is explicitly called afterward.
- **B.** The quantity is silently changed to one so the object satisfies the rule.
- **C.** Construction raises a validation error identifying quantity and the failed constraint.
- **D.** The quantity is accepted until the object is converted to a dictionary.

## Q6 · Apply · M5 — Source errors versus API rejection

A workflow reads CSV rows, explicitly converts quantity text into an integer, validates a positive quantity, then sends accepted requests to the shop API. It retains an outcome for every row and continues after expected row failures.

One row has quantity `"0"`. A different row has a valid quantity but product ID `"999"`, which the server rejects with HTTP 404. Which classification is correct?

- **A.** Both are `invalid_source`, because every rejected order must have failed the local schema.
- **B.** Quantity `"0"` is `invalid_source`; the server's HTTP 404 is `rejected`.
- **C.** Quantity `"0"` is `rejected`; the HTTP 404 is `invalid_source`.
- **D.** Both are `communication_failed`, because neither row creates an order.

## Q7 · Understand · M7 — Separate parametrized cases

You need to check a line-total calculation against six sets of inputs. Under a normal pytest run, without stopping after the first failure, what does parametrization provide that a loop of assertions inside one test does not?

- **A.** Automatic parallel execution of the six cases.
- **B.** Automatic generation of the six input values from the function's type hints.
- **C.** Six separately reported cases, so later cases can still run after an earlier one fails; a loop exits at its first failed assertion.
- **D.** No functional difference; test reporting and failure behavior are identical.

## Q8 · Analyse · M7 — Asserting an expected exception

`calculate_line_total(price_paise, quantity)` must raise `ValueError` with a message containing `"positive integer"` when quantity is zero. Which test fails if the rejection disappears, and also rejects an unrelated exception?

Assume `pytest` and the calculation function are imported. Each option is a test-function body.

**A.**

```python
try:
    calculate_line_total(49900, 0)
except ValueError:
    pass
```

**B.**

```python
assert calculate_line_total(49900, 0) == ValueError
```

**C.**

```python
with pytest.raises(Exception):
    calculate_line_total(49900, 0)
```

**D.**

```python
with pytest.raises(ValueError, match="positive integer"):
    calculate_line_total(49900, 0)
```

## Q9 · Analyse · M8 — Choosing what to replace

You have two test goals: (1) check that your own FastAPI order route and SQLite storage work together, and (2) check a Python client's behavior when an external HTTP service times out. Which setup best matches those goals?

- **A.** Replace both the local route and database with mocks, and replace the external call too; those mocks establish real persistence.
- **B.** Run everything against live services and the regular shop database; controlled substitutes would invalidate the checks.
- **C.** Run the real local API and storage with TestClient and a temporary database; replace the client's external HTTP call to supply a controlled timeout.
- **D.** Replace the local API, but call the external service on every test run and wait for it to time out naturally.

## Q10 · Analyse · M9 — Interpreting coverage

A test run reports **100% line coverage** on the shop's pricing module. Which conclusion is justified by that coverage result alone?

- **A.** Every measured executable line was executed by a test; the result does not establish assertion quality, complete branch coverage, or correctness for every input.
- **B.** The pricing module has no defects.
- **C.** Every possible input combination was tested.
- **D.** Every test passed, because a coverage report can only be produced after a successful run.

---

## Answer sheet

| Question | Answer |
|---|---|
| Q1 | |
| Q2 | |
| Q3 | |
| Q4 | |
| Q5 | |
| Q6 | |
| Q7 | |
| Q8 | |
| Q9 | |
| Q10 | |
