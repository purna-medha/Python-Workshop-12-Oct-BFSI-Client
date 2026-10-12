# Nano-Zon implementation plan

**Goal:** Supply the complete small shopping application and M1–M9 starter checkpoints with only current-lab answer regions commented out.

**Architecture:** `reference/` contains the finished application; `day-one/` contains the procedural representation used before OOP. `labs/m01` through `labs/m09` provide handouts and generated starter projects. A standard-library tool builds the checkpoints from those sources and comments only the selected answer regions. The reference folder is deliberately named `reference` because this repository ignores folders named `solution`.

**Stack:** Python 3.10+, standard-library dataclasses/JSON/CSV/SQLite, FastAPI, Pydantic 2, requests, pytest and coverage.

**Spec:** [Application design](../../curriculum/application-design.md), [module outline](../../curriculum/outline-m01-m09.md), and the current request to supply function bodies with participant answers commented out.

## Constraints

- Keep the same three products, string IDs, and integer paise throughout.
- M1–M2 use dictionaries and ordinary functions; M3 introduces dataclasses and owned cart state.
- A starter retains completed earlier behavior; only the current lab's selected answer regions are disabled.
- Definitions, parameters, supplied plumbing, and surrounding validation remain written.
- Disabled function answers have a readable `NotImplementedError`, not an incorrect fallback result. Remove that one guard when writing the answer.
- Avoid class hierarchies, ORMs, authentication, real payments, inventory reservation, and AI work.
- Tests authored for M7–M9 are teaching deliverables. Do not run pytest unless the user asks to run tests or verify the implementation.

## Tasks

- [x] Build the reference: catalog queries, cart operations, snapshots, CLI, memory storage, API, schemas, HTTP client, CSV reporting, SQLite storage.
- [x] Supply procedural M1/M2 sources and an unambiguous answer-region convention.
- [x] Supply educational domain, schema, integration, client, and assertion-quality tests, fixtures, coverage configuration, and a CI template.
- [x] Build independent module checkpoints: procedural M1/M2; memory M3; dataclass API M4; explicit schemas M5; SQLite M6–M9. M6 keeps memory as its starter default until storage answers are complete.
- [x] Write nine concise lab guides: principle, capability, exact edit locations, completion behavior, expert question, and next checkpoint.
- [x] Inspect source syntax, answer-region boundaries, file links, and marker counts; run ordinary CLI/database demonstrations without executing pytest. Framework imports require dependency installation and are not executed here.
- [x] Link the capstone from the course documents and describe the remaining test-suite verification honestly.

## Review focus

Reject Boolean/fractional/non-positive quantities; retain a zero price filter; keep carts independent; preserve order prices and quantities after later changes; roll back partial orders; give client failures distinct outcome categories; keep test databases separate from normal data. Unknown resources receive deliberate rejection, duplicate submissions create separate orders, and duplicate order IDs fail without corrupting earlier records.

## Authoring evidence

The nine starters have 3, 5, 3, 4, 5, 4, 4, 5, and 4 pending regions respectively (37 total), each belonging only to its current module. The completed reference has zero. All 153 authored Python files parse, project TOML parses, and local Markdown links resolve.

The reference CLI demonstrated search, a zero price bound, repeated additions, update, removal, ₹1,897 checkout, cart clearing, and retrieval after a second process opened the same SQLite file. A separate standard-library demonstration retained the saved two-unit, ₹499-price snapshot after cart/catalog changes. A controlled later-line insertion failure left zero headers and zero lines for that failed order while the earlier order remained retrievable. M1–M3 starters launched and reported their incomplete functions through readable pending-lab messages.

FastAPI, Pydantic, requests, pytest, and httpx are not installed in the inspected Python environment. API/workflow execution, the pytest suite, and CI execution remain unverified. No pytest tests were run during authoring.
