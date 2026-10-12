# Python-Workshop-12-Oct-BFSI-Client

Python application development workshop using **Pico-Zon** for teaching and **Nano-Zon** for labs.

The course has **nine modules over three days / 18 teaching hours**, for programmers new to Python and experienced developers reviewing application practices. A fourth-day AI introduction is a separate design task.

## Start here

- [Teaching slides and codealong notebooks](modules/README.md) — M1–M9, 32–34 slides per module; each notebook has 12 directly executable teaching cells.
- [Short teaching examples](teaching-snippets/README.md) — 39 examples connecting programming principles to Python.
- [Compact reading chapters](teaching-text/README.md) — orientation and revision for every module.
- [Pico-Zon](projects/pico-zon/README.md) — the 50-line opening shop and modular showcase.
- [Nano-Zon capstone and labs](projects/nano-zon/README.md) — complete reference application and nine independent starter checkpoints.
- [Student assessment](assessments/python-knowledge-10-mcq.docx) and [instructor answer key](assessments/python-knowledge-10-mcq-answer-key.docx) — ten MCQs adapted from earlier workshop questions. Markdown sources are alongside the Word files.

## Module sequence

| Day | Module | Focus |
|---|---|---|
| 1 | M1 | Values, expressions, decisions, and simple functions |
| 1 | M2 | Collections, iteration, function interfaces, mutation, and failures |
| 1 | M3 | Objects, dataclasses, ownership, snapshots, and modules |
| 2 | M4 | HTTP, JSON, FastAPI, and Python callers |
| 2 | M5 | Contracts, boundary validation, and CSV/API workflows |
| 2 | M6 | SQLite persistence, resource lifetime, and transactions |
| 3 | M7 | Behavioral testing with pytest |
| 3 | M8 | Real integration and controlled external dependencies |
| 3 | M9 | Assertion quality, coverage, reproducibility, and CI |

## Run the opening shop

From this repository root:

```sh
python3 projects/pico-zon/pico_zon.py
```

For the API, validation, and testing lessons:

```sh
cd teaching-snippets
uv sync --extra dev
```

Select that Python environment in your notebook editor. M1–M3 and M6 notebook examples use the standard library. Framework codealongs use an in-process caller; database and test experiments use temporary resources. Each project's guide specifies its working directory and commands.

## Repository contents

```text
modules/            Teaching slides and codealong notebooks
teaching-snippets/  Small worked Python examples
teaching-text/      Dense reading and revision chapters
projects/pico-zon/  Small instructor shop examples
projects/nano-zon/  Capstone reference, starter labs, and tools
assessments/        Student questions and instructor answers
```

Curriculum planning files and exported slide manuscripts are maintained separately and excluded from this repository. The included guides link the teaching materials available here.

## Delivery status

Materials are authored and have static structural/syntax checks. Full notebook, API, database, test-suite, and CI runtime delivery review remains pending. Expected results are distinguished from captured execution output. CI files are templates until explicitly installed; no merge restrictions are configured by a template alone.
