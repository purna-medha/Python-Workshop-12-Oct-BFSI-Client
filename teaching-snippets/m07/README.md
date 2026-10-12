# M07 — Specify expected behavior through tests

Assert → examine boundaries → parameterize → isolate and retain regressions.

Read the numbered snippets in order. Every snippet is at most 40 physical lines.

| Snippet | Principle | How to use |
|---|---|---|
| [s01_assertions.py](s01_assertions.py) | State an observable expectation | `uv run --extra dev pytest m07/s01_assertions.py -q` |
| [s02_boundaries.py](s02_boundaries.py) | Examine boundaries and rejected operations | `uv run --extra dev pytest m07/s02_boundaries.py -q` |
| [s03_parametrization.py](s03_parametrization.py) | Express a family of cases | `uv run --extra dev pytest m07/s03_parametrization.py -q` |
| [s04_isolation_and_regression.py](s04_isolation_and_regression.py) | Isolate state and retain discovered defects | `uv run --extra dev pytest m07/s04_isolation_and_regression.py -q` |

Run commands from the `current-course/teaching-snippets` folder. See the [course index](../README.md) for setup and API prerequisites.

`conftest.py` provides the fresh cart fixture. These files are examples of pytest tests; launching them as ordinary scripts does not execute their tests.

## Prediction and demonstration

**Before revealing the result:** If one test changes its fixture cart, should another test using the same fixture name see that change?

**Teaching move:** First notice repeated ShoppingCart setup, then read conftest.py. The fixture names a fresh construction; it is not one globally shared cart. Use [s04_isolation_and_regression.py](s04_isolation_and_regression.py) as the worked example.

<details>
<summary>Reasoned answer</summary>

No, with the supplied function-scoped fixture. Pytest calls the fixture again for the next test, creating a fresh cart.

</details>

Finish by asking which part of the mechanism would stay useful in another application. The [Nano-Zon lab](../../projects/nano-zon/labs/m07/README.md) includes a small extension with no supplied answer.
