# M08 — Establish component collaboration

Cross boundaries → isolate storage → inspect failures → substitute HTTP.

Read the numbered snippets in order. Every snippet is at most 40 physical lines.

| Snippet | Principle | How to use |
|---|---|---|
| [s01_component_boundaries.py](s01_component_boundaries.py) | Test across a component boundary | `uv run --extra dev pytest m08/s01_component_boundaries.py -q` |
| [s02_isolated_integration.py](s02_isolated_integration.py) | Control the environment | `uv run --extra dev pytest m08/s02_isolated_integration.py -q` |
| [s03_failure_consequences.py](s03_failure_consequences.py) | Check the consequences of failure | `uv run --extra dev pytest m08/s03_failure_consequences.py -q` |
| [s04_external_dependencies.py](s04_external_dependencies.py) | Substitute an external dependency deliberately | `uv run --extra dev pytest m08/s04_external_dependencies.py -q` |

Run commands from the `teaching-snippets` folder. See the [course index](../README.md) for setup and API prerequisites.

Read `conftest.py` with snippet 02 and `http_cases.py` with snippet 04. Tests use real temporary SQLite databases and controlled external HTTP; no live server is needed.

## Prediction and demonstration

**Before revealing the result:** What does response.json.return_value control? Does asserting a mocked HTTP call establish that the real API saved an order?

**Teaching move:** Read http_cases.py first: return_value supplies a result; side_effect raises a failure. Then trace requests.post → response → json() before introducing patch. Use [s04_external_dependencies.py](s04_external_dependencies.py) as the worked example.

<details>
<summary>Reasoned answer</summary>

It controls the value returned when json() is called. A call assertion checks client behavior; only the real API/database exercise establishes persistence.

</details>

Finish by asking which part of the mechanism would stay useful in another application. The [Nano-Zon lab](../../projects/nano-zon/labs/m08/README.md) includes a small extension with no supplied answer.
