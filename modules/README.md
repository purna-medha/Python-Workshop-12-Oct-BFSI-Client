# M1–M9 classroom materials

Nine Markdown slide decks and nine companion codealong notebooks for the current course. Each deck has 30–40 slides; tiny slide excerpts isolate one mechanism. Each notebook has 12 directly executable teaching cells across two explorations, using Pico-Zon-derived examples. Nano-Zon remains the lab project.

| Module | Slides | Codealong | Slide count |
|---|---|---|---|
| M1 · Express behavior with values and functions | [Deck](m01-values-and-functions/slides.md) | [Notebook](m01-values-and-functions/codealong.ipynb) | 34 |
| M2 · Process collections and manage changes | [Deck](m02-collections-and-state/slides.md) | [Notebook](m02-collections-and-state/codealong.ipynb) | 34 |
| M3 · Give records a shape and state an owner | [Deck](m03-objects-and-structure/slides.md) | [Notebook](m03-objects-and-structure/codealong.ipynb) | 32 |
| M4 · Connect independently running programs | [Deck](m04-interfaces-and-json/slides.md) | [Notebook](m04-interfaces-and-json/codealong.ipynb) | 33 |
| M5 · Validate boundaries and compose a workflow | [Deck](m05-contracts-and-workflows/slides.md) | [Notebook](m05-contracts-and-workflows/codealong.ipynb) | 34 |
| M6 · Retain information consistently | [Deck](m06-persistence-and-transactions/slides.md) | [Notebook](m06-persistence-and-transactions/codealong.ipynb) | 32 |
| M7 · Express behavioral promises as tests | [Deck](m07-behavioral-testing/slides.md) | [Notebook](m07-behavioral-testing/codealong.ipynb) | 32 |
| M8 · Establish component collaboration | [Deck](m08-integration-and-dependencies/slides.md) | [Notebook](m08-integration-and-dependencies/codealong.ipynb) | 33 |
| M9 · Maintain useful evidence as software changes | [Deck](m09-test-quality-and-ci/slides.md) | [Notebook](m09-test-quality-and-ci/codealong.ipynb) | 34 |

## Teaching rhythm

Each deck establishes a general principle, connects it to the shop, shows small Python, asks a prediction before a separate answer, then moves through codealong and guided/independent Nano-Zon practice. Experienced learners deepen the same context through ownership, contract, or evidence review. The outline still allocates two hours per module; slides are prompts for interaction rather than a fixed equal-time lecture.

## Slides

The files are Markdown with Marp front matter, `---` slide boundaries, and a 16:9 theme. Open the source directly or preview it with a Marp-compatible editor. Code excerpts aim at one idea and stay within 12 lines. Read excerpts in sequence; imports or existing definitions are sometimes established on earlier slides. Source files and notebooks supply complete context.

## Codealongs

Use a notebook editor with a Python kernel. M1–M3 and M6 use the standard library. For framework and testing lessons, from `teaching-snippets/` run `uv sync --extra dev` and select that environment in your editor. Notebook tooling is a separate classroom prerequisite. The teaching cells are self-contained: there is no repository discovery, sys.path modification, runpy wrapper, or dependency on local course modules. Restart and run in order to reproduce starting state.

Read a brief principle, predict, execute the visible code, inspect the result, and change one input. Most cells are small; a few supplied schema, response-contract, and test-file cells are longer so the example remains complete. The notebook text identifies what each result establishes and where a simplification matters. Expected explanations are separately revealable, and deliberate failures have a nearby recovery.

M4/M5 use a supplied in-process TestClient so core API exploration needs no live server or terminal switching. It uses HTTPX and does not establish real network behavior; the optional linked live demonstration uses requests in a separate process. No external HTTP call is sent automatically. M5 retains CSV outcomes and inspects a report in temporary storage.

M6/M8 use fresh temporary SQLite files, parameterized values, transaction contexts, and explicit connection cleanup. M8 runs real API/storage collaboration and rollback before substituting only external HTTP for client checks. Complete source and setup are visible in the cells.

M7 calls shown test functions and uses a visible temporary suite to demonstrate real pytest discovery, fixtures, and parametrization. M9 runs pytest/coverage against a temporary copy, demonstrates a deliberately weak green check, exposes the defect with a stronger assertion, then repairs and repeats the same checks. The subprocess output and exit statuses are visible when learners execute those cells. No repository test suites are launched by these notebooks. CI remains a separate template-reading activity.

## Delivery status

These are authored Markdown and notebook sources. Slide counts, Python syntax, notebook structure, and local links are inspected statically. Rendering, notebook execution, API/framework behavior, test runs, and live CI remain part of delivery review. Expected results are labeled; no executed notebook output is supplied. The CI examples remain templates.
