# Python knowledge assessment — instructor answer key

Use with the [student assessment](python-knowledge-10-mcq.md). Do not distribute this key with the assessment.

## Selection and scoring

These ten questions are adapted from the [legacy final assessment](../../legacy-course/assessment/final-assessment.md), specifically legacy Q1, Q2, Q4, Q5, Q6, Q10, Q11, Q12, Q13, and Q15. Their short examples and mechanism/application/judgment style are retained. Banking examples become shop examples, legacy module tags become current-course tags, and constraints and outcome names match the current course.

Q1 asks for the cause of shared state rather than simply the printed output. Q9 explicitly includes temporary SQLite storage to match the current integration lesson. The original legacy question IDs are retained below for traceability.

Award one mark for a single correct option; zero for an incorrect, blank, or multiple-option response. Maximum: **10 marks**. Use missed concepts to guide feedback; this short selection does not establish comprehensive Python mastery.

## Quick key and provenance

| Current question | Answer | Current module | Legacy source |
|---|---|---|---|
| Q1 | C | M2 | Q1 |
| Q2 | D | M2 | Q2 |
| Q3 | A | M3 | Q4 |
| Q4 | B | M4 | Q5 |
| Q5 | C | M5 | Q6 |
| Q6 | B | M5 | Q10 |
| Q7 | C | M7 | Q11 |
| Q8 | D | M7 | Q12 |
| Q9 | C | M8 | Q13 |
| Q10 | A | M9 | Q15 |

The selection covers M2–M5 and M7–M9 directly. M1 calculations provide context; M6 persistence participates in Q9, but neither has a standalone question. It is a selected knowledge check, not a question-per-module examination. Answer positions follow the legacy options; the position distribution is not evenly balanced.

### Q1 — C · Understand · M2

The default list is created once when the function definition executes. Both calls omit the argument and receive the same list; appending twice is visible through both returned carts. New dictionary containers do not duplicate the list inside them.

**Distractors:** A invents automatic merging by dictionary key. B assumes default construction happens per call. D confuses a returned container with immutability.

**If missed:** Revisit object identity, mutable defaults, and fresh state per cart. Ask the learner to propose a fresh-list default strategy and explain what it changes.

### Q2 — D · Apply · M2

The dictionary's values are the product records. Iterate those records, filter by their price, and collect their names into a list. Direct dictionary iteration supplies keys; items supplies key/value pairs rather than a record alone.

**Distractors:** A treats each key as a record. B looks up a record field on the outer store and compares IDs with a price. C chooses a set and treats each item tuple as a record dictionary.

**If missed:** Use one catalog entry to distinguish keys, values, and items before revisiting the comprehension.

### Q3 — A · Understand · M3

The dataclass generates common record methods. Its ordinary type annotations do not validate field values at construction. Immutability is also not the default; even a frozen record does not recursively freeze nested mutable contents.

**Distractors:** B confuses a type hint with runtime validation. C assumes automatic deep immutability. D overlooks the generated initializer.

**If missed:** Compare a dataclass record with the explicit Pydantic contract introduced in M5. Their responsibilities differ; the domain need not be replaced by a framework model.

### Q4 — B · Understand · M4

The decorator registers the function with FastAPI. Registration occurs when the definition executes; the handler body executes for a matching request. The path parameter becomes an argument to that call.

**Distractors:** A confuses registration with invoking the body. C confuses routing with an instance method. D ignores the decorator's runtime effect.

**If missed:** Trace module initialization separately from a later request. Reconnect this use of a library decorator to pytest's registration conventions.

### Q5 — C · Understand · M5

Pydantic checks declared constraints at construction. Integer zero violates the strictly positive quantity rule, so construction fails with a field-specific validation error. It does not silently repair the quantity or wait for serialization.

**Distractors:** A and D postpone validation to a later operation. B assumes validation changes invalid data into an allowed value.

**If missed:** Separate construction, runtime validation, and conversion into a transport representation.

### Q6 — B · Apply · M5

The CSV value zero converts to an integer but fails the positive-quantity contract before HTTP submission: `invalid_source`. The unknown product request satisfies that source contract and is then rejected by the server: `rejected`. Both outcomes remain in the report; expected row failures do not abort the workflow.

**Distractors:** A collapses domain rejection into local schema rejection. C reverses the boundaries. D mistakes unsuccessful business outcomes for a transport failure; an HTTP 404 is a received response.

**If missed:** Trace one row across conversion, validation, submission, and response handling. Ask which failure never reaches the server.

### Q7 — C · Understand · M7

Parametrization produces independent reported cases. Under the stated normal run, one failed case does not prevent later cases from being executed. A failed assertion exits the single test function containing the loop, so the remaining loop iterations never run.

**Distractors:** A assumes parallelism; B assumes input generation; D ignores independent execution and reporting. Stopping the whole suite at the first failure would change the later-case behavior, which is why the question states the run condition.

**If missed:** Compare six reported cases with one test containing six assertions. Ask how to identify the particular input that failed.

### Q8 — D · Analyse · M7

The check requires the expected exception type and a meaningful message. It fails if the operation returns normally, and an unrelated exception cannot satisfy it.

**Distractors:** A passes if no exception occurs because it asserts nothing on that path. B compares a return value with an exception class. C accepts unrelated exceptions such as NameError and can pass for the wrong reason.

**If missed:** Remove the rejection mentally and trace each option. Then imagine a typo raises a different exception; identify which check would incorrectly remain green.

### Q9 — C · Analyse · M8

Real routes, validation, domain behavior, and temporary SQLite establish local component collaboration. The external HTTP call is a separate boundary whose outcomes can be controlled when testing the client. These checks answer different questions.

**Distractors:** A establishes mock interactions rather than real persistence. B sacrifices isolation and repeatability. D replaces the local behavior that needs evidence while leaving the external timeout unpredictable.

**If missed:** List which components run for real in each check and what each result can establish. A client substitute cannot prove database rollback.

### Q10 — A · Analyse · M9

Line coverage records which measured executable lines ran. A test can execute a calculation without asserting its correct amount. Complete line coverage also does not establish every branch outcome, every input, or a successful test run; reports can be retained after failures.

**Distractors:** B and C infer comprehensive correctness from execution. D assumes reporting is restricted to green runs.

**If missed:** Revisit an integer-only assertion for a calculation accidentally changed from multiplication to addition. Ask what new assertion would expose the defect.

## Feedback by cognitive level

- **Understand:** Q1, Q3, Q4, Q5, Q7. Misses suggest a mechanism needs explanation and a small demonstration.
- **Apply:** Q2, Q6. Misses suggest the learner needs practice identifying data shapes and boundary transitions.
- **Analyse:** Q8, Q9, Q10. Misses suggest practice deciding what an implementation or test actually establishes.

These tags describe the intended reasoning task, not measured item difficulty. Use the Nano-Zon labs to assess independent application-building skills after the knowledge check.
