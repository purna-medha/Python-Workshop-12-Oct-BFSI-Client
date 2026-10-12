# M9 — Maintain useful evidence on changes

Coverage identifies execution gaps; assertions determine whether wrong behavior is detected. Repeatable local commands and CI preserve useful feedback as the application changes.

**Start:** [starter/](starter/README.md). All earlier application and test behavior is supplied. Run `uv sync --extra dev`.

## Complete four focused regions

Use [ANSWER-MAP.md](starter/ANSWER-MAP.md):

1. In `tests/test_quality.py`, replace type-only confidence with an exact total assertion.
2. Check the price-filter boundary and valid zero bound.
3. In `pyproject.toml`, enable branch coverage. This answer is commented TOML, not a function guard.
4. In `ci/nano-zon.yml`, enable the written test/report step. Preserve YAML indentation while uncommenting.

The weak example remains alongside the strong check so its limitation is observable. The CI completeness gate prevents an unfinished template from being treated as a finished check pipeline.

## Observe completion

```sh
python3 tools/progress.py --require-complete
uv run --extra dev pytest --cov=nanozon --cov-branch --cov-report=term-missing
```

Inspect uncovered paths and explain one meaningful missing case; add its assertion. No arbitrary coverage threshold is supplied. The report is a guide to investigation rather than a proof of correctness.

Temporarily change multiplication to addition in your copy: the type-only example remains green while the exact assertion should fail. Restore the implementation afterward.

The CI YAML is a template. Copy it into `.github/workflows/nano-zon.yml` only in the repository where you intend it to run. Its default commands assume the application is the repository root; for a nested training project, adjust working-directory and report paths. Reports upload even after failure.

**Explain:** Which facts does coverage establish, and which facts require assertions?

**Expert review:** Review reproducibility, failure exit statuses, and dependency configuration. Identify one plausible defect your current suite would still miss.

## Independent extension — no supplied answer

Find one currently uncovered path or weak assertion in your own completed suite. Add a meaningful test, describe a plausible defect it detects, and explain what the coverage report alone could not establish.

Complete this after the guided regions. Keep extensions in your own checkpoint; later starters supply the core application, not these personal additions.

**Finish:** Demonstrate browse → cart → simulated order → restart retrieval. Explain how the same concepts could support a different application. Fourth-day AI extensions are a separate next design.
