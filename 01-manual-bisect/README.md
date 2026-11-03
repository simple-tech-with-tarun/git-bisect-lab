# Manual Git Bisect

## Overview

This exercise demonstrates how to use `git bisect` to identify the commit that introduced a regression. It covers manual binary-search investigation, defining good and bad boundaries, restricting the search to a specific file, and handling commits that cannot be tested.

## Learning Objectives

- Understand how Git bisect uses binary search to narrow down a regression.
- Identify good and bad commits.
- Restrict a bisect investigation to commits affecting a specific file.
- Interpret Git's selected candidate commits.
- Skip commits that cannot be tested.
- Review and reproduce bisect investigations using the bisect log.
- Reset the repository after an investigation.

---

## Exercise 1: Manual Regression Investigation

### Scenario

The discount calculator contains an intentional regression affecting purchases of exactly `$500`.

The expected discount for a purchase of `$500` is 10%, but the regressed implementation applies only 5%.

The regression was introduced by changing the condition:

```python
elif amount >= 500:
```

to:

```python
elif amount > 500:
```

### Investigation

Start a bisect session by specifying the known bad commit and the known good commit:

```powershell
git bisect start <bad-commit> <good-commit> -- .\01-manual-bisect\discount_calculator.py
```

The file path limits the investigation to commits that changed the discount calculator.

At each selected commit:

1. Inspect the checked-out implementation.
2. Run the calculator test using a purchase amount of `$500`.
3. Mark the commit as good or bad.

Run the following command to test the discount calculation:

```powershell
python -c "from sys import path; path.insert(0, '01-manual-bisect'); from discount_calculator import calculate_discount; print(calculate_discount(500))"
```

Expected output:

- `50.0` - Good commit.
- `25.0` - Bad commit.

Mark a commit:

```powershell
git bisect good
```

or:

```powershell
git bisect bad
```

Git continues narrowing the search until it identifies the first bad commit.

### Result

`6d77748` - `bug: introduce discount boundary regression`

The investigation identified the change from `>= 500` to `> 500` as the source of the regression.

The result was independently verified by inspecting the commit:

```powershell
git show 6d77748
```

### End the Investigation

Reset the bisect session:

```powershell
git bisect reset
```

This exits bisect mode and restores the branch checkout.

---

## Exercise 2: Skipped and Untestable Commits

### Scenario

The commit history contains commits where the calculator cannot be tested reliably.

Two types of untestable states were introduced:

- **Unavailable dependency:** The calculator imports a module that does not exist.
- **Syntax error:** The calculator contains invalid Python syntax.

These commits demonstrate why some historical revisions cannot be classified as good or bad through normal testing.

### Investigation

Start a bisect session using the known bad and good boundaries:

```powershell
git bisect start 1f16bdd 2c3989a -- .\01-manual-bisect\discount_calculator.py
```

When a commit cannot be tested, use:

```powershell
git bisect skip
```

You can also skip specific commits by hash without checking them out individually:

```powershell
git bisect skip f3d7287 f70b846
```

The skipped commits in this exercise were:

| Commit | Reason |
|---|---|
| `f3d7287` | Unavailable dependency |
| `f70b846` | Syntax error |

Git excludes skipped commits from normal good/bad classification and continues investigating the remaining testable commits.

### Result

The investigation classified the following commits:

| Commit | Classification |
|---|---|
| `2c3989a` | Good boundary |
| `f3d7287` | Skipped |
| `f70b846` | Skipped |
| `80ba8fe` | Good |
| `c0149c7` | Good |
| `1f16bdd` | First bad commit among testable commits |

The investigation identified:

`1f16bdd` - `bug: introduce incorrect discount rate`

The regression changed the 10% discount calculation to 1%.

Because some commits were skipped, the result should be interpreted with those skipped revisions in mind. In other histories, skipped commits may leave ambiguity about the exact first bad commit.

### Review the Investigation

Display the recorded bisect decisions:

```powershell
git bisect log
```

The log provides a reproducible record of the starting boundaries, skipped commits, good/bad classifications, and final result.

### End the Investigation

```powershell
git bisect reset
```

---

## Important Git Bisect Commands

| Command | Purpose |
|---|---|
| `git bisect start` | Starts a bisect investigation |
| `git bisect good` | Marks the current commit as good |
| `git bisect bad` | Marks the current commit as bad |
| `git bisect skip` | Skips commits that cannot be tested |
| `git bisect log` | Displays the recorded investigation |
| `git bisect visualize` | Displays the remaining bisect range |
| `git bisect reset` | Ends the investigation and restores the branch |

## Key Takeaways

- Git bisect uses binary search to reduce the number of commits that need to be inspected.
- Accurate good and bad boundaries are essential. Git trusts the classifications provided by the investigator.
- A pathspec can restrict the investigation to commits affecting a particular file.
- A commit that cannot be tested should be skipped rather than incorrectly classified as good or bad.
- Skipping commits can reduce the precision of the final result. If too many candidates are untestable, Git may only be able to identify a range containing the first bad commit.
- `git bisect log` helps preserve and reproduce an investigation.
- Always use `git bisect reset` when the investigation is complete.

---

## Next Steps

The next exercise focuses on automating regression detection using `git bisect run`, including test scripts and exit codes for good, bad, and untestable commits.
