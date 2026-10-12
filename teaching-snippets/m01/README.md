# M01 — Express behavior with values and functions

Represent → calculate → choose → reuse → trace.

Read the numbered snippets in order. Every snippet is at most 40 physical lines.

| Snippet | Principle | How to use |
|---|---|---|
| [s01_values.py](s01_values.py) | Values represent information | `python -m m01.s01_values` |
| [s02_expressions.py](s02_expressions.py) | Expressions transform values | `python -m m01.s02_expressions` |
| [s03_decisions.py](s03_decisions.py) | Conditions select behavior | `python -m m01.s03_decisions` |
| [s04_functions.py](s04_functions.py) | Functions name reusable operations | `python -m m01.s04_functions` |
| [s05_execution_and_errors.py](s05_execution_and_errors.py) | Execution follows a traceable path | `python -m m01.s05_execution_and_errors` |

Run commands from the `teaching-snippets` folder. See the [course index](../README.md) for setup and API prerequisites.

## Prediction and demonstration

**Before revealing the result:** If the quantity text changes from "2" to "two", does multiplication run? Which operation fails first?

**Teaching move:** Use the deliberate conversion failure in snippet 05. Read the traceback before repairing the input. Use [s05_execution_and_errors.py](s05_execution_and_errors.py) as the worked example.

<details>
<summary>Reasoned answer</summary>

Conversion raises ValueError before multiplication. Follow parse_quantity, its caller, and the exception’s failing line.

</details>

Finish by asking which part of the mechanism would stay useful in another application. The [Nano-Zon lab](../../projects/nano-zon/labs/m01/README.md) includes a small extension with no supplied answer.
