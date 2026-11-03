# Git Bisect Lab

A practical repository for learning advanced Git bisect techniques, identifying regression-introducing commits, automating regression investigations, and handling complex Git histories.

This lab focuses on systematic regression detection through controlled commit histories and repeatable testing workflows.

## Learning Objectives

By completing this lab, you will be able to:

- Understand how Git bisect uses binary search to identify regression-introducing commits.
- Establish reliable good and bad commit boundaries.
- Investigate histories containing skipped or untestable commits.
- Automate regression detection using `git bisect run`.
- Build deterministic, PowerShell-compatible regression test scripts.
- Understand how Git interprets test exit codes.
- Investigate regressions introduced through branch integration and merge commits.
- Recover from incorrect bisect decisions and reproduce previous investigations.
- Verify bisect results against actual commits, diffs, and commit ancestry.

## Exercise Roadmap

### 1. Manual Regression Investigation

**Status: Completed**

Practise identifying a regression-introducing commit through a controlled Git history.

Topics:

- Starting and terminating bisect sessions.
- Marking known good and bad commits.
- Understanding Git's candidate commit selection.
- Restricting an investigation to changes affecting a specific file.
- Identifying and independently verifying the first bad commit.

Documentation: [01-manual-bisect/README.md](01-manual-bisect/README.md)

### 2. Skipped and Untestable Commits

**Status: Completed**

Investigate histories containing commits that cannot be tested reliably.

Topics:

- Using `git bisect skip`.
- Skipping specific commits by their hashes.
- Understanding how skipped commits affect the search.
- Reviewing recorded decisions with `git bisect log`.
- Understanding the limitations of identifying the exact first bad commit when revisions are skipped.

Documentation: [01-manual-bisect/README.md](01-manual-bisect/README.md)

### 3. Automated Regression Investigation

**Status: Completed**

Automate commit testing using Git bisect and PowerShell-compatible scripts.

Topics:

- Creating deterministic regression tests.
- Using `git bisect run`.
- Handling test exit codes:
  - `0` - Good commit.
  - `1` to `124` - Bad commit.
  - `125` - Commit cannot be tested; skip it.
  - `126` and `127` - Command execution errors.
- Comparing manual and automated investigation results.
- Understanding the importance of repeatable test conditions.
- Automating regression investigation with PowerShell test runners.

Documentation: [02-automated-bisect/README.md](02-automated-bisect/README.md)

### 4. Merge-Related Regression Investigation

**Status: Completed**

Investigate regressions introduced through feature branches and subsequently integrated through merge commits.

Topics:

- Constructing histories with feature branches and merge commits.
- Introducing and identifying regressions on feature branches.
- Investigating merge commits and their parent relationships.
- Using automated Git bisect across merge-related history.
- Comparing first-parent and second-parent changes.
- Distinguishing the original regression-introducing commit from the merge integration commit.

Documentation: [03-merge-bisect/README.md](03-merge-bisect/README.md)

### 5. Bisect Recovery and Reproducibility

**Status: Planned**

Practise recovering from incorrect investigation decisions.

Topics:

- Identifying incorrect good or bad markings.
- Inspecting bisect decision history.
- Resetting and replaying investigations.
- Correcting investigation boundaries.
- Independently verifying and reproducing final results.

## Practical Approach

This repository uses controlled Git histories to demonstrate how regressions are introduced and investigated.

Each exercise follows a consistent approach:

1. Construct a known repository history.
2. Establish a reproducible regression scenario.
3. Perform the investigation using the relevant Git commands.
4. Record the results and identify the regression-introducing commit.
5. Verify the findings against commit history and diffs.
6. Document the commands, observations, and limitations.

All exercises are performed incrementally, with investigation results verified before moving to the next topic.

## Tools and Environment

The exercises use:

- **Git** - Version control and bisect investigation.
- **Python** - Small application scenarios with controlled regressions.
- **PowerShell** - Windows-compatible test automation.
- **GitHub** - Repository hosting and documentation.

## Expected Outcomes

By completing this lab, learners should be able to:

- Identify regression-introducing commits efficiently.
- Manage bisect boundaries and skipped commits.
- Automate regression investigations using deterministic tests.
- Interpret bisect exit codes correctly.
- Investigate regressions involving merge commits.
- Recover from incorrect bisect decisions.
- Reproduce and validate investigation results.

## Completion Criteria

The lab will be considered complete when:

- All five practical exercises have been completed.
- Every regression has a known introducing commit.
- Bisect results have been independently verified.
- Skipped commits have been handled correctly.
- Automated test scripts have been validated.
- Merge-related investigations include parent and ancestry inspection.
- Recovery and replay procedures have been demonstrated.
- Commands, findings, scripts, and limitations have been documented.
- Documentation has been reviewed and merged into `main`.
