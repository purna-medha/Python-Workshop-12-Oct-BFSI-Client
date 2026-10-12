# Nano-Zon labs

Each module has a concise guide and a complete checkpoint with only the selected answer sections disabled. Follow the learning sequence; open the current starter's `ANSWER-MAP.md` to find the edit locations.

| Module | Development principle | Extension | Answer regions |
|---|---|---|---:|
| [M1](m01/README.md) | Values and functions express reusable computations | Labels, money display, line totals | 3 |
| [M2](m02/README.md) | Collections and mutation organize changing information | Catalog queries and cart operations | 5 |
| [M3](m03/README.md) | Records, objects, and composition organize responsibility | Owned cart state and immutable order snapshots | 3 |
| [M4](m04/README.md) | Interfaces connect independent programs | API handlers and a Python HTTP caller | 4 |
| [M5](m05/README.md) | Contracts make boundary assumptions explicit | Validation, CSV conversion, outcome reporting | 5 |
| [M6](m06/README.md) | Persistence and transactions retain consistent facts | SQLite record conversion and atomic saving | 4 |
| [M7](m07/README.md) | Tests specify behavioral promises | Assertions, rejection cases, snapshot regression | 4 |
| [M8](m08/README.md) | Real collaboration and controlled dependencies establish confidence | API/database round trip, rollback, HTTP failures | 5 |
| [M9](m09/README.md) | Evidence and automation maintain confidence | Assertion quality, branches, coverage, CI | 4 |

The 37 regions are small edits; many contain only one expression or a few statements. Function definitions, dependencies, records, input plumbing, fixtures, and most error handling are supplied. Check each guide's completion behavior before moving on.

## Continue or recover

Every next starter includes the reference implementation of earlier modules. This provides a known starting point without executing a migration tool or overwriting your previous work. Keep earlier projects and compare your choices with the new baseline. M3 is the representation refactor; M4–M6 retain the resulting public data conventions.

To create a fresh copy of one starter in a new destination, run from `nano-zon/`:

```sh
python3 tools/build_starters.py --lab m04 --output /tmp/my-nano-zon-m04
```

The builder refuses an existing destination. It never edits a participant's completed copy. The checked-in starters are ready to use without running the builder.

**Completion reporting:** `python tools/progress.py` lists disabled regions. `--require-complete` exits unsuccessfully while any remain. Passing that check says the regions are enabled, not that the application behavior is correct.
