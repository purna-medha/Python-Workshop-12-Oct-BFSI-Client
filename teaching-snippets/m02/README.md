# M02 — Process collections and manage state

Organize → iterate → define interfaces → own changes → handle failures.

Read the numbered snippets in order. Every snippet is at most 40 physical lines.

| Snippet | Principle | How to use |
|---|---|---|
| [s01_collections.py](s01_collections.py) | Choose a structure for the information | `python -m m02.s01_collections` |
| [s02_iteration.py](s02_iteration.py) | Repeat an operation over data | `python -m m02.s02_iteration` |
| [s03_function_interfaces.py](s03_function_interfaces.py) | Make function interfaces clear | `python -m m02.s03_function_interfaces` |
| [s04_mutable_state.py](s04_mutable_state.py) | Understand ownership of changing data | `python -m m02.s04_mutable_state` |
| [s05_input_and_exceptions.py](s05_input_and_exceptions.py) | Handle exceptional and missing inputs deliberately | `python -m m02.s05_input_and_exceptions` |

Run commands from the `teaching-snippets` folder. See the [course index](../README.md) for setup and API prerequisites.

## Prediction and demonstration

**Before revealing the result:** After copying the list of product records and changing the copied record’s quantity, does the original record change?

**Teaching move:** Draw two list containers pointing at one record. Predict the result before reading the printed output. Use [s04_mutable_state.py](s04_mutable_state.py) as the worked example.

<details>
<summary>Reasoned answer</summary>

Yes. The lists are distinct, but their inner dictionary is shared. Copy the necessary record values when independent facts are required.

</details>

Finish by asking which part of the mechanism would stay useful in another application. The [Nano-Zon lab](../../projects/nano-zon/labs/m02/README.md) includes a small extension with no supplied answer.
