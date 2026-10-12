# M05 — Define contracts and compose workflows

Constrain → resolve ambiguity → enforce rules → read records → automate.

Read the numbered snippets in order. Every snippet is at most 40 physical lines.

| Snippet | Principle | How to use |
|---|---|---|
| [s01_contracts.py](s01_contracts.py) | Declare acceptable data | `uv run --extra dev python -m m05.s01_contracts` |
| [s02_ambiguity.py](s02_ambiguity.py) | Make ambiguity explicit | `uv run --extra dev python -m m05.s02_ambiguity` |
| [s03_validation_and_rules.py](s03_validation_and_rules.py) | Separate structural validity from business validity | `uv run uvicorn m05.s03_validation_and_rules:app --port 8000` |
| [s04_external_records.py](s04_external_records.py) | Read and validate external records | `uv run --extra dev python -m m05.s04_external_records` |
| [s05_workflows.py](s05_workflows.py) | Compose operations into a workflow | `uv run --extra dev python -m m05.s05_workflows` |

Run commands from the `teaching-snippets` folder. See the [course index](../README.md) for setup and API prerequisites.

Before snippet 05, start snippet 03 in another terminal. It writes `order-report.json` in this folder. CSV rows produce independent one-item orders.

## Prediction and demonstration

**Before revealing the result:** Compare quantity 0 with product ID "999" and quantity 2. Which request fails structural validation, and which reaches the business rule?

**Teaching move:** Trace one CSV row through conversion, validation, submission, response validation, and its report entry. Use [s03_validation_and_rules.py](s03_validation_and_rules.py) as the worked example.

<details>
<summary>Reasoned answer</summary>

Zero fails the positive-quantity constraint (422). The well-shaped unknown ID reaches the domain and fails product lookup (404).

</details>

Finish by asking which part of the mechanism would stay useful in another application. The [Nano-Zon lab](../../projects/nano-zon/labs/m05/README.md) includes a small extension with no supplied answer.

## Core path and extensions

**Required:** One strict positive quantity, one nonempty items contract, explicit CSV conversion, a validated order response, and a saved outcome report. The HTTP client, row iteration, failure categorization, and logging setup are supplied; read and trace them before completing the selected answers.

**After the core path:** Coercion alternatives, omitted versus null fields, unexpected-field policies, environment configuration details, and outcome summaries. Snippet 02 is a guided preview; use its deeper cases after the required workflow works. Retries and a full CRUD client remain later extensions.

**Logging connection:** Snippet 05 logs each row number and status. The log explains progress during execution; the JSON report retains outcomes afterward. Nano-Zon configures logging in its command entry point and obtains a logger by module name.

**Schema connection to Day 4:** Inspect `OrderRequest.model_json_schema()` from `m05.contracts`. The result describes the boundary as data. Later, an AI tool can use such a description to construct requests; application validation and business rules still decide whether those requests are acceptable.

**Failure-order detail:** Requests’ JSON decoding error also inherits from RequestException. The workflow catches it before the broad communication handler so malformed response data remains invalid_response. See the [Requests exception definitions](https://requests.readthedocs.io/en/latest/_modules/requests/exceptions/).
