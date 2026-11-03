# Exercise 4: Merge-Related Regression Investigation

## Objective

Investigate a regression introduced on a feature branch and subsequently integrated into an integration branch through a merge commit.

This exercise demonstrates how Git bisect traverses commit history containing merges, how to inspect merge parents, and how to distinguish the original regression-introducing commit from the commit that integrated it.

## Scenario

The automated discount calculator initially applies a 10% discount to purchases of $500 or more.

A feature branch introduces an incorrect discount rate of 2%. This change is subsequently merged into the integration branch.

The objective is to identify the commit that originally introduced the regression and understand how it entered the integration branch.

## Commit History

The following commits were used:

| Commit | Description |
|---|---|
| `e90a9b0` | Restore the correct discount rate for the merge exercise |
| `547244e` | Introduce the discount regression on the feature branch |
| `a370df5` | Merge the feature branch into the integration branch |

### Branch Structure

```text
                    a370df5 (merge commit)
                   /        \
                  /          \
e90a9b0 (baseline)             547244e (feature regression)
                  \          /
                   \________/
```

The merge commit has two parents:

- First parent: `e90a9b0` - Integration branch before the merge.
- Second parent: `547244e` - Feature branch containing the regression.

## 1. Establish a Clean Baseline

Before creating the feature branch, the calculator was restored to the correct 10% discount rate.

```python
elif amount >= 500:
    return amount * 0.10
```

This ensured that the exercise started from a known-good implementation.

The correction was committed:

```text
e90a9b0 fix: restore correct discount rate for merge exercise
```

## 2. Introduce the Regression on a Feature Branch

A separate feature branch was created:

```powershell
git switch -c feature/discount-regression
```

The discount rate was changed from 10% to 2%:

```python
elif amount >= 500:
    return amount * 0.02
```

The change was committed:

```text
547244e bug: introduce discount regression on feature branch
```

For a purchase amount of $600:

- Expected discount: $60.00
- Actual discount: $12.00

The regression was now present on the feature branch.

## 3. Merge the Feature Branch

The feature branch was merged into the integration branch using a non-fast-forward merge:

```powershell
git merge --no-ff feature/discount-regression -m "merge: integrate discount feature with regression"
```

The resulting merge commit was:

```text
a370df5 merge: integrate discount feature with regression
```

The `--no-ff` option ensured that Git created an explicit merge commit, preserving the branch integration point in the history.

## 4. Inspect the Commit Graph

The commit graph was inspected using:

```powershell
git log --graph --oneline --decorate --all
```

The relevant history showed:

```text
*   a370df5 (HEAD -> exercise-4-merge-bisect) merge: integrate discount feature with regression
|\
| * 547244e (feature/discount-regression) bug: introduce discount regression on feature branch
|/
* e90a9b0 fix: restore correct discount rate for merge exercise
```

This confirmed that the regression was introduced on a separate feature branch and subsequently merged into the integration branch.

## 5. Inspect Merge Parents

The merge commit's parent information was inspected:

```powershell
git rev-list --parents -n 1 HEAD
```

The output identified:

- Merge commit: `a370df5`
- First parent: `e90a9b0`
- Second parent: `547244e`

The merge commit was also inspected using:

```powershell
git show --no-patch --pretty=raw HEAD
```

This provided the commit's tree, parent references, author, committer, and commit message.

## 6. Verify Both Parent Implementations

The calculator implementation in each parent was inspected:

```powershell
git show e90a9b0:02-automated-bisect/discount_calculator.py
git show 547244e:02-automated-bisect/discount_calculator.py
```

The first parent contained the correct 10% discount rate.

The second parent contained the incorrect 2% discount rate.

This independently established that the regression existed before the merge.

## 7. Validate the Regression

The calculator was executed against a purchase amount of $600:

```powershell
python -c "from sys import path; path.insert(0, '02-automated-bisect'); from discount_calculator import calculate_discount; print(calculate_discount(600))"
```

Output:

```text
12.0
```

The output confirmed that the integrated implementation contained the regression.

## 8. Run Automated Git Bisect

The merge commit was selected as the bad boundary, and the clean integration parent was selected as the good boundary:

```powershell
git bisect start a370df5 e90a9b0
```

Git selected the feature-branch commit for testing:

```text
Bisecting: 0 revisions left to test after this (roughly 0 steps)
[547244e] bug: introduce discount regression on feature branch
```

The automated test harness from Exercise 3 was executed:

```powershell
git bisect run powershell -NoProfile -ExecutionPolicy Bypass -File .\02-automated-bisect\run-tests.ps1
```

The test failed because the actual discount was $12 instead of the expected $60.

Git identified:

```text
547244e0beacb734b7eebe98556ef95962be8fcb is the first 'bad' commit
```

The result correctly identified the feature-branch commit as the regression-introducing commit.

## 9. Inspect the Merge from Both Parents

After completing bisect, the original branch and merge commit were restored:

```powershell
git bisect reset
```

The merge commit was inspected again:

```powershell
git show --no-patch --pretty=raw HEAD
```

The changes relative to the first parent were inspected:

```powershell
git diff HEAD^1 HEAD -- 02-automated-bisect/discount_calculator.py
```

This showed the discount rate changing from 10% to 2%.

The changes relative to the second parent were inspected:

```powershell
git diff HEAD^2 HEAD -- 02-automated-bisect/discount_calculator.py
```

This produced no output because the merge commit's resulting file content matched the second parent's implementation.

Therefore:

- The first-parent comparison showed the feature change entering the integration branch.
- The second-parent comparison showed that the merge did not introduce additional changes to the calculator.
- The original regression was already present in the feature-branch commit.

## Key Git Concepts Practiced

- Investigating regressions introduced through feature branches.
- Understanding merge commits and their parent relationships.
- Inspecting commit ancestry and graph topology.
- Using `git rev-list --parents` to identify merge parents.
- Using `git show` to inspect historical file versions.
- Using `git diff HEAD^1 HEAD` and `git diff HEAD^2 HEAD` to compare merge parents.
- Running automated Git bisect across merge-related history.
- Distinguishing a regression-introducing commit from a merge integration commit.

## Important Lessons

1. A regression discovered after a merge is not necessarily introduced by the merge commit itself.
2. Git bisect searches the reachable commit graph, not exclusively the first-parent history.
3. A feature-branch commit can be identified as the first bad commit even when the bad boundary is a merge commit.
4. Inspecting both parents of a merge commit helps establish where a change originated.
5. Automated tests make regression investigation reproducible across complex commit histories.

## Expected Outcome

After completing this exercise, you should be able to investigate regressions introduced through merged feature branches, understand merge commit ancestry, use automated Git bisect to locate the original regression-introducing commit, and independently verify the result through historical file inspection and parent comparisons.
