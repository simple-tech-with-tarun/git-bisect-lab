# Automated Git Bisect

This exercise demonstrates how to automate regression investigation using `git bisect run` and a repeatable test script.

The objective is to identify the commit that introduced a regression without manually testing each revision.

## Learning Objectives

By completing this exercise, you will be able to:

- Understand how `git bisect run` automates binary-search-based regression detection.
- Create repeatable tests for validating historical revisions.
- Use process exit codes to communicate test results to Git.
- Handle commits that cannot be tested.
- Automate regression investigation using PowerShell scripts.
- Verify the first bad commit identified by automated bisect.

## Repository Structure

```text
02-automated-bisect/
    discount_calculator.py
    test_discount.py
    run-tests.ps1
```

### File Responsibilities

| File | Responsibility |
|---|---|
| `discount_calculator.py` | Contains the discount calculation logic and controlled regression history. |
| `test_discount.py` | Validates the expected discount calculation and returns appropriate exit codes. |
| `run-tests.ps1` | Executes the Python test script and propagates its exit code to Git. |

## Automated Test Design

The test script validates the 10% discount tier using a purchase amount of 600.

Expected result:

```python
purchase_amount = 600
expected_discount = 60.0
```

The test imports the calculator, executes the function, and compares the actual result with the expected result.

### Exit Code Handling

Git uses the test process exit code to classify each revision during automated bisect.

| Exit Code | Meaning | Git Behaviour |
|---|---|---|
| `0` | Test passed | Marks the revision as good. |
| `1` | Test failed | Marks the revision as bad. |
| `125` | Revision cannot be tested | Skips the revision. |

The test script handles `ImportError` and `SyntaxError` during calculator import and returns exit code `125`.

The PowerShell runner checks whether Python is available, executes the test script, and propagates its exit code.

## Exercise Workflow

### 1. Establish a Good Revision

The initial calculator implementation correctly calculates the 10% discount for a purchase amount of 600.

The test script returns exit code `0`.

### 2. Introduce an Untestable Revision

An unavailable dependency is introduced into the calculator:

```python
import unavailable_discount_rules
```

The calculator cannot be imported, so the test script identifies the revision as untestable and returns exit code `125`.

### 3. Restore the Calculator

The unavailable dependency is removed, restoring the calculator to a working state.

The automated test passes again.

### 4. Introduce a Regression

The discount calculation is deliberately modified:

```python
elif amount >= 500:
    return amount * 0.01
```

The expected discount is 60.0, but the actual discount becomes 6.0.

The test fails and returns exit code `1`.

### 5. Run Automated Bisect

Start the bisect session using known good and bad commits:

```powershell
git bisect start <bad-commit> <good-commit>
```

Execute the automated test runner:

```powershell
git bisect run powershell -NoProfile -ExecutionPolicy Bypass -File .\02-automated-bisect\run-tests.ps1
```

Git automatically:

1. Selects intermediate revisions.
2. Executes the test script against each selected revision.
3. Classifies passing revisions as good.
4. Classifies failing revisions as bad.
5. Skips revisions returning exit code 125.
6. Continues searching until the first bad commit is identified.

### 6. Inspect the Bisect Results

Review the recorded investigation:

```powershell
git bisect log
```

The log records the good and bad boundaries, tested revisions, skipped revisions, and the first bad commit.

End the bisect session:

```powershell
git bisect reset
```

## Results

The automated investigation successfully identified the regression-introducing commit:

| Commit | Description | Result |
|---|---|---|
| `1bbf58e` | Extract high discount threshold | Good boundary |
| `6e5ad39` | Introduce unavailable dependency | Skipped (125) |
| `08f62e7` | Restore calculator after untestable revision | Good |
| `c2b5e40` | Introduce incorrect discount rate | First bad commit |

The bisect log confirmed that Git skipped the untestable revision and continued the search.

The identified first bad commit was independently verified against the calculator's code change.

## Key Takeaways

- `git bisect run` automates regression detection using a repeatable test command.
- Reliable test scripts are essential for accurate automated bisect results.
- Exit codes communicate whether a revision is good, bad, or untestable.
- Exit code `125` allows Git to skip revisions that cannot be evaluated.
- PowerShell scripts can be used to integrate automated tests with Git bisect.
- The bisect log provides a reproducible record of the investigation.

## Limitations and Best Practices

- Tests should be deterministic and produce consistent results across historical revisions.
- Test dependencies and execution environments should be available throughout the investigation.
- Good and bad boundaries must be established correctly.
- Untestable revisions should be skipped rather than incorrectly classified.
- A passing test only validates the behaviour covered by that test; it does not guarantee that the entire application is regression-free.
