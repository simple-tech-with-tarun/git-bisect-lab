# Exercise 5: Bisect Recovery and Reproducibility

## Objective

Practice recovering from incorrect Git bisect decisions, inspecting recorded investigation steps, resetting bisect sessions, and reproducing regression investigations.

This exercise demonstrates how incorrect good/bad classifications can affect the result and why independent verification is important.

## Scenario

The automated discount calculator contains a regression in the discount rate for purchases of 500 or more.

The correct discount rate is 10%, but a regression changes it to 3%.

The exercise uses three important commits:

| Commit | Description | Actual state |
|---|---|---|
| `158c449` | Restore correct discount rate | Good |
| `f246c3f` | Introduce incorrect discount rate | Bad |
| `ee9cd17` | Clarify discount calculation tiers | Bad |

The final commit changes only a comment. It does not fix the regression.

## 1. Establish the Bisect Boundaries

Start an investigation using the latest commit as bad and the known-good baseline as good.

```powershell
git bisect start ee9cd17 158c449
```

Git selects `f246c3f` for testing.

## 2. Introduce an Incorrect Bisect Decision

Run the automated test:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\02-automated-bisect\run-tests.ps1
```

The test fails:

```text
AssertionError: Expected discount 60.0, got 18.0
```

This confirms that the selected commit is actually bad.

To simulate an operator mistake, deliberately mark it as good:

```powershell
git bisect good
```

Git trusts this classification and incorrectly identifies `ee9cd17` as the first bad commit.

This demonstrates that Git bisect relies on accurate good/bad decisions. It does not independently validate test results.

## 3. Inspect and Save the Bisect Log

Inspect the recorded decisions:

```powershell
git bisect log
```

Save the investigation log outside the repository:

```powershell
git bisect log > "$env:TEMP\exercise-5-bisect.log"
```

The log records the original boundaries and the incorrect classification.

This provides a record that can be reviewed when investigating an incorrect result.

## 4. Reset the Incorrect Investigation

Exit the current bisect session:

```powershell
git bisect reset
```

The command restores the branch to its original position.

Resetting does not remove commits or modify repository history. It ends the active bisect session.

## 5. Restart and Correct the Investigation

Start a new investigation using the same boundaries:

```powershell
git bisect start ee9cd17 158c449
```

Git selects `f246c3f` again.

This time, use the test result correctly and mark the commit as bad:

```powershell
git bisect bad
```

Git identifies:

```text
f246c3f is the first 'bad' commit
```

The corrected investigation identifies the actual regression-introducing commit.

Save the successful investigation log:

```powershell
git bisect log > "$env:TEMP\exercise-5-bisect-verified.log"
```

Then exit the session:

```powershell
git bisect reset
```

## 6. Independent Verification

Verify the identified commit directly against the source history:

```powershell
git show f246c3f -- .\02-automated-bisect\discount_calculator.py
```

The diff confirms the regression:

```diff
-        return amount * 0.10
+        return amount * 0.03
```

The discount rate changed from 10% to 3%.

This independently confirms that `f246c3f` introduced the regression.

## 7. Bisect Log Replay

Git provides a replay mechanism:

```powershell
git bisect replay <logfile>
```

The purpose of replay is to reproduce a recorded bisect investigation from its command log.

During this exercise, replay was attempted using an edited copy of the original log. However, Git remained in the state:

```text
status: waiting for both 'good' and 'bad' commits
```

The replay did not successfully reproduce the investigation.

Therefore, the successful recovery in this exercise was demonstrated by resetting and restarting the investigation with corrected classifications, rather than by successful log replay.

The original and verified logs were preserved in the Windows temporary directory for comparison.

## Key Learnings

- Git bisect trusts the good/bad classifications supplied by the operator.
- Incorrect classifications can produce an incorrect first-bad-commit result.
- `git bisect log` records investigation decisions.
- Saving logs helps preserve investigation history for later review.
- `git bisect reset` exits an active investigation and restores the original branch position.
- Restarting bisect with corrected classifications can recover the correct regression result.
- `git bisect replay` can reproduce recorded investigations when the log contains a valid sequence of bisect commands.
- Independent verification using `git show` helps confirm that the identified commit actually introduced the regression.

## Expected Outcome

By completing this exercise, you should be able to:

- Recognize the impact of incorrect bisect classifications.
- Inspect and preserve bisect investigation logs.
- Reset and restart an incorrect investigation.
- Identify the correct regression-introducing commit.
- Independently verify the regression using Git history and source diffs.
- Understand the purpose and limitations of bisect log replay.
