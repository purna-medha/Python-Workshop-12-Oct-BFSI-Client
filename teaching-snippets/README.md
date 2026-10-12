# Python through small teaching snippets

**39 ordered snippets · M1–M9 · maximum 40 physical lines per snippet**

The story is how general programming and software development concepts combine to build an application. Shopping supplies a familiar toy problem; Python expresses the concepts.

Each snippet begins with a short conceptual paragraph, connects it to the example, and demonstrates it with readable code. Brief inline comments clarify decisions or expected behavior.

## Reading order

| Module | Story | Snippets |
|---|---|---|
| [M01 — Express behavior with values and functions](m01/README.md) | Represent → calculate → choose → reuse → trace. | 5 |
| [M02 — Process collections and manage state](m02/README.md) | Organize → iterate → define interfaces → own changes → handle failures. | 5 |
| [M03 — Organize data, behavior, and responsibilities](m03/README.md) | Name records → own state → compose snapshots → separate modules. | 4 |
| [M04 — Connect independently running programs](m04/README.md) | Encode → publish → translate requests → call and interpret. | 4 |
| [M05 — Define contracts and compose workflows](m05/README.md) | Constrain → resolve ambiguity → enforce rules → read records → automate. | 5 |
| [M06 — Preserve information consistently](m06/README.md) | Manage resources → translate rows → retain facts → save atomically. | 4 |
| [M07 — Specify expected behavior through tests](m07/README.md) | Assert → examine boundaries → parameterize → isolate and retain regressions. | 4 |
| [M08 — Establish component collaboration](m08/README.md) | Cross boundaries → isolate storage → inspect failures → substitute HTTP. | 4 |
| [M09 — Maintain confidence as software changes](m09/README.md) | Find gaps → strengthen assertions → repeat checks → automate feedback. | 4 |

## Running the examples

Open a terminal in this folder. Use Python 3.10 or later; Python 3.12 is the CI example. Run snippets as modules so companion imports resolve:

```sh
cd teaching-snippets
python3 -m m01.s01_values
python3 -m m03.s04_modules
```

M1–M3 and the four numbered M6 snippets use only the standard library. For API, validation, and testing examples, install the declared dependencies:

```sh
uv sync --extra dev
uv run --extra dev python -m m05.s01_contracts
```

Alternative: create a virtual environment, activate it, and run `python -m pip install -e ".[dev]"`. Then use `python`, `pytest`, and `uvicorn` directly.

## API sequence

Use two terminals in this folder. Run one API at a time on port 8000; stop it with Ctrl+C before switching.

```sh
# Terminal 1: M4 API
uv run uvicorn m04.s03_order_api:app --port 8000
# Terminal 2: M4 caller
uv run python -m m04.s04_http_client
```

M4 and M5 both accept `{"items": [...]}`. M5 strengthens the constraints and validates response data without changing the request shape. Run the matching caller:

```sh
# Terminal 1: stop M4, then start M5
uv run uvicorn m05.s03_validation_and_rules:app --port 8000
# Terminal 2: M5 CSV workflow
uv run python -m m05.s05_workflows
```

Generated API documentation is at `http://127.0.0.1:8000/docs`. `NANOZON_API_URL` configures the M5 workflow.

## Testing and coverage lessons

M7–M9 test snippets define actual pytest tests. Use the commands in their module indexes rather than launching the files as ordinary scripts:

```sh
uv run --extra dev pytest m07/s01_assertions.py -q
uv run --extra dev pytest m08 -q
uv run --extra dev python -m m09.s03_repeatable_checks
```

The last command writes test and coverage reports to `reports/`. M9’s annotated YAML uses that same runner and remains a template until installed.

## How to teach from the folder

Read the opening principle, connect it to the example, predict the result, and run or inspect the code. Use the brief experiment where supplied, then ask where the concept would apply in another application.

The numbered files are the teaching sequence. Small companion files provide reusable definitions, schemas, fixtures, and sample data; their Python files also stay within 40 lines. Introduce each companion at the module that owns it.

The original [50-line Pico-Zon](../projects/pico-zon/pico_zon.py) remains the opening whole-application demo. These teaching snippets are purpose-built examples; Nano-Zon remains the separate learner lab project.

This folder contains teaching code and minimal navigation instructions, rather than slides or Nano-Zon lab solutions.

## Learning checks

Each module guide now supplies a prediction, a teaching move, and a hidden reasoned answer. Use them around the existing snippets so code stays within 40 lines. Nano-Zon labs pair visible guided answers with one independent extension whose solution is not supplied.

M1–M3 introduce programming building blocks. M4–M6 apply software interfaces and storage mechanisms. M7–M9 establish evidence about behavior. HTTP, databases, and CI are software development mechanisms used across languages; they are not all language syntax features.
