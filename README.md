# runlog — a running log for the command line

Track your runs, see weekly totals, and find your personal bests.

## Setup

Requires Python 3.10+. Run these from the root folder.

**1. Create a virtual environment** (once). It keeps this project's packages
separate from everything else on your computer.

```
python -m venv .venv
```

On some Macs and Linux machines the command is `python3` instead of `python`.

**2. Activate it** (every time you open a new terminal):

| System | Command |
|---|---|
| macOS / Linux | `source .venv/bin/activate` |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Windows (Command Prompt) | `.venv\Scripts\activate.bat` |

Your prompt now starts with `(.venv)`. If PowerShell refuses to run the
script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once.

**3. Install the dependencies and run the tests:**

```
python -m pip install -r requirements.txt
python -m pytest
```

The last line of the test output should say **6 passed, 8 skipped**.

When you're done, `deactivate` leaves the virtual environment.

**Using an IDE?** In VS Code or PyCharm, select `.venv` as the project's
Python interpreter so its test runner uses the same packages.

## Using the app

Start the app. It uses `runs.csv` in the current folder unless you pass `--file`:

```
python -m runlog --file sample_data/runs.csv
```

It shows a numbered menu. Options that need more information ask for it one
question at a time, with an example of the format:

```
==== runlog ====
1) Log a run
2) List runs
3) Weekly summary
4) Personal bests
5) Quit
Choose an option (1-5): 1
Date (YYYY-MM-DD, e.g. 2026-10-21): 2026-10-21
Distance in km (e.g. 5.2): 5.2
Duration (mm:ss or h:mm:ss, e.g. 27:45 or 1:05:30): 27:45
Notes (optional, e.g. easy recovery run; press Enter to skip): easy
```

| Option | What it does |
|---|---|
| 1 Log a run | Asks for date, distance, duration and optional notes, then saves the run |
| 2 List runs | All runs, oldest first, with pace |
| 3 Weekly summary | Asks for any day in a week; totals for that Monday–Sunday week (Enter = this week) |
| 4 Personal bests | 1K, 5K, 10K and half marathon, from any run at least that long |
| 5 Quit | Exit |

If an answer doesn't match the format, the app asks again.

## Add CI Pipeline

In this studio you add a GitHub Actions pipeline that runs the tests on every
push to `main` and every pull request. Then you break the code four ways and
watch CI catch each one.

Before you start, make sure the Setup steps above work: `python -m pytest`
should end with **6 passed, 8 skipped**. Keep your answers to the
**Answer in your notes** questions in a new file, `CI_NOTES.md`.

### Part 1: Get a green run

Goal: every push to `main` and every pull request runs the test suite on
GitHub's build server.

**1.** Create the file `.github/workflows/ci.yml` (the folder names must match
exactly) with this content:

```yaml
name: CI

on:
  push:
    branches: [main]        # every push to main
  pull_request:
    branches: [main]        # every PR that targets main
  workflow_dispatch:        # "Run workflow" button on the Actions tab

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Check out the code
        uses: actions/checkout@v7

      - name: Set up Python
        uses: actions/setup-python@v7
        with:
          python-version: "3.12"
          cache: pip

      - name: Install dependencies
        run: python -m pip install -r requirements.txt

      - name: Run tests
        run: python -m pytest -v
```

**2.** Commit and push it:

```
git add .github
git commit -m "Add CI workflow"
git push
```

**3.** Open your repo's **Actions** tab on GitHub. Click the run, then the
**test** job, then expand **Run tests**. Find the line that says
6 passed, 8 skipped.

**4.** Go to the commit list on the **Code** tab. Your commit now has a green
check next to it.

**5.** Click **Run workflow** on the Actions tab to start a run by hand.

Compare this file with the one from lecture. It needs no `PYTHONPATH` line,
because this repo's `pytest.ini` already sets `pythonpath = .`. YAML is picky
about indentation: if the Actions tab shows a syntax error instead of a run,
check your spaces.

> **Answer in your notes:** The CI server knows nothing about your laptop.
> Which step gives it a copy of your code, and which step gives it pytest?

### Part 2: Break it in a pull request

Goal: see a regression stopped at the pull request, before it reaches `main`.

**1.** Make a branch:

```
git switch -c break-pace
```

**2.** In `runlog/domain/run.py`, "refactor" `pace_s_per_km` so the division is
upside down:

```python
        return self.distance_km / self.duration_s
```

**3.** Pretend you forgot to run the tests. Commit, then push the branch:

```
git push -u origin break-pace
```

**4.** On GitHub, open a pull request from `break-pace` into `main`. Watch the
check at the bottom of the PR go from a yellow dot to a red X.

**5.** Click **Details** next to the failed check. Find the name of the failing
test and the line showing the value it got versus the value it expected.

**6.** Make CI a gate. Go to **Settings → Rules → Rulesets → New ruleset →
New branch ruleset**. Name it `main`, set **Enforcement status** to Active, and
under **Target branches** add the default branch. Tick **Require status checks
to pass**, click **Add checks**, and pick `test`. Save.

**7.** Reload the PR. GitHub now refuses to merge it.

**8.** Fix it on the same branch: undo the change, commit, and push. The PR's
check re-runs on its own and turns green. Merge the PR.

From now on `main` is protected, so every change goes through a branch and a
pull request. After merging, update your local copy before starting the next
branch:

```
git switch main
git pull
```

> **Answer in your notes:** Which test caught the bug, and what value did it
> get? Was that test written to catch this exact mistake?

### Part 3: Fix a real bug, test first

Goal: use the red-to-green cycle to fix one of the bugs from the testing
studio, so it can never quietly come back.

**1.** Make a branch:

```
git switch -c fix-zero-distance
```

**2.** In `tests/test_run_validation.py`, finish `test_zero_distance_is_rejected`
(delete its `pytest.skip` line):

```python
def test_zero_distance_is_rejected():
    with pytest.raises(ValueError):
        Run(run_date=A_DAY, distance_km=0.0, duration_s=1500)
```

**3.** Commit and push **only the test**, then open a pull request. CI goes red.
This time the red is good news: it is evidence of a bug in the code, not in
your change.

**4.** Now fix the code. In `runlog/domain/run.py`, the docstring says distance
"must be greater than 0". Make `__post_init__` agree with it.

**5.** Run `python -m pytest` locally first. Expect **7 passed, 7 skipped**.
Commit, push to the same branch, and watch the PR turn green. Merge it.

> **Answer in your notes:** Why push the failing test before the fix, instead
> of both in one commit? What does this test protect you from later?

### Part 4: "Works on my machine"

Goal: see CI catch a mistake your own laptop can't, because your laptop has a
file the repo doesn't.

**1.** Make a branch (from an up-to-date `main`):

```
git switch -c add-miles
```

**2.** Create `runlog/domain/units.py`:

```python
"""Unit conversions."""
KM_PER_MILE = 1.609344


def km_to_miles(km: float) -> float:
    return km / KM_PER_MILE
```

**3.** Create `tests/test_units.py`:

```python
from runlog.domain.units import km_to_miles


def test_a_5k_is_about_3_1_miles():
    assert round(km_to_miles(5.0), 1) == 3.1
```

**4.** Run `python -m pytest` locally. Everything passes: **8 passed, 7 skipped**.

**5.** Now make the classic mistake. Stage **only the test** (not `git add .`):

```
git add tests/test_units.py
git commit -m "Add miles conversion"
git push -u origin add-miles
```

Then open a pull request.

**6.** CI goes red with `ModuleNotFoundError: No module named 'runlog.domain.units'`.
Your laptop still says everything passes. Run `git status` to see why.

**7.** Add and commit `units.py`, push, and watch the PR turn green. Merge it.

> **Answer in your notes:** Name one other thing that could make tests pass on
> your laptop but fail on the build server. (Hint: what if you had
> `pip install`ed a package that isn't in `requirements.txt`?)

### Stretch goals

Do these in any order, each on its own branch and pull request.

- **Save a test report.** Install `pytest-html` in the workflow, run pytest
  with `--html=test-report.html --self-contained-html`, and add the upload step
  below. Then make a test fail on purpose and check whether the report still
  uploads. Without `if: always()`, GitHub skips every step after the first
  failure.

  ```yaml
        - name: Upload test report
          if: always()        # upload even when the tests failed
          uses: actions/upload-artifact@v7
          with:
            name: test-report
            path: test-report.html
  ```

- **Test on several Python versions.** Add a matrix so one push runs three
  jobs side by side. Under `test:`, add the lines below, then change
  `python-version` to `${{ matrix.python-version }}`.

  ```yaml
      strategy:
        fail-fast: false
        matrix:
          python-version: ["3.10", "3.12", "3.13"]
  ```

- **Add a status badge** to the top of this README:
  `![CI](https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg)`,
  with your repo's owner and name filled in.
- **Fix another bug** from the testing studio the same way as Part 3: failing
  test first, then the fix.

### Before you're done

- [ ] Your **Actions** tab shows at least one red run and one green run.
- [ ] You have three merged pull requests (Parts 2–4), each showing a red
      check followed by a green one.
- [ ] `CI_NOTES.md`, with your answers to the four **Answer in your notes**
      questions, is merged into `main` through one more pull request.
