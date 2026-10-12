# M09 — Maintain confidence as software changes

Find gaps → strengthen assertions → repeat checks → automate feedback.

Read the numbered snippets in order. Every snippet is at most 40 physical lines.

| Snippet | Principle | How to use |
|---|---|---|
| [s01_coverage_paths.py](s01_coverage_paths.py) | Find unexplored execution paths | `uv run --extra dev pytest m09/s01_coverage_paths.py -q` |
| [s02_assertion_quality.py](s02_assertion_quality.py) | Check whether assertions detect wrong behavior | `uv run --extra dev pytest m09/s02_assertion_quality.py -q` |
| [s03_repeatable_checks.py](s03_repeatable_checks.py) | Make checks reproducible | `uv run --extra dev python -m m09.s03_repeatable_checks` |
| [s04_ci.yml](s04_ci.yml) | Automate feedback on changes | `Read the annotated workflow template` |

Run commands from the `teaching-snippets` folder. See the [course index](../README.md) for setup and API prerequisites.

The pricing companion gives coverage a separate target. Snippet 02 deliberately includes one weak assertion beside the stronger tests.

Run the report-producing runner with `uv run --extra dev python -m m09.s03_repeatable_checks`. The YAML is a template; it does not activate CI until copied.

## Prediction and demonstration

**Before revealing the result:** If multiplication becomes addition, does a type-only total assertion detect the defect? Which exact assertion would?

**Teaching move:** Inspect coverage, then consider the arithmetic defect. Distinguish reaching a statement from checking the promise it implements. Use [s02_assertion_quality.py](s02_assertion_quality.py) as the worked example.

<details>
<summary>Reasoned answer</summary>

The result is still an integer, so the weak check stays green. Expecting 99800 for two cables detects the wrong arithmetic.

</details>

Finish by asking which part of the mechanism would stay useful in another application. The [Nano-Zon lab](../../projects/nano-zon/labs/m09/README.md) includes a small extension with no supplied answer.
