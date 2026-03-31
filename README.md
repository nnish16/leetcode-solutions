# leetcode-solutions

Local LeetCode solution repo with a hardened planner/runner for sequential + daily challenge automation.

## Planner / runner

Use `manager.py` to recompute local progress from root-level solution files, print a deterministic plan, and safely persist automation state.

Examples:

```bash
python3 manager.py --dry-run
python3 manager.py --daily-id 3651 --daily-slug minimum-cost-walk-in-weighted-graph
python3 manager.py --daily-id 3651 --mark-solved 3651
```

Behavior:

- rescans root-level `NNNN_slug.py` files every run
- recomputes the contiguous solved prefix for the sequential track
- plans `1 sequential + 1 daily` when an unsolved daily challenge is provided
- plans `2 sequential` when the provided daily challenge is already solved
- treats a daily challenge that matches the next sequential target as satisfying both roles
- uses a real lock file to block overlapping runs
- writes structured run logs to `automation_runs/YYYY-MM-DD/`
- supports `--dry-run` to avoid state/log writes

Submission/browser automation is intentionally left stubbed so the core planner remains deterministic and safe.


## Deterministic browser executor

The repo now includes `automation/browser_executor.js`, a deterministic CDP-based executor for the proven LeetCode browser flow.

It is designed to:

- reuse the existing dedicated Chrome session exposed over CDP
- verify in-browser signed-in state
- navigate to the exact target problem page
- assert the problem page, Python3 selection, and Monaco editor presence
- paste code by updating the Monaco model and verify the model changed
- tolerate missing `Run` while still allowing submission
- wait for an `Accepted` submissions-page state before repo/state persistence happens

Example manager-driven execution for the confirmed `#41` flow:

```bash
python3 manager.py \
  --execute-target-id 41 \
  --solution-file /tmp/0041_first_missing_positive.py \
  --cdp-url http://127.0.0.1:56278
```

When `--execute-target-id` is present, the explicit target is the only thing executed. The printed sequential/daily plan remains informational context from the repo scan; it is not the thing being submitted.

Only after the browser executor reports an Accepted submission will `manager.py` copy the solution into the repo, recompute progress, update `automation_state.json`, and write the run log.

### Cron-facing deterministic executor path

Cron should call the explicit executor path directly, not rely on the planner to choose a target implicitly.

Recommended shape:

```bash
cd /Users/nish/Documents/leetcode-solutions && \
python3 manager.py \
  --execute-target-id "$PROBLEM_ID" \
  --execute-target-slug "$PROBLEM_SLUG" \
  --solution-file "$SOLUTION_FILE" \
  --daily-id "$PROBLEM_ID" \
  --daily-slug "$PROBLEM_SLUG" \
  --cdp-url http://127.0.0.1:56278
```

Notes:

- pass `--execute-target-id` and `--solution-file` every time for actual submission runs
- pass `--execute-target-slug` when you already know the exact slug; otherwise the executor resolves it
- if the cron job is solving that day's daily challenge, also pass the same values via `--daily-id/--daily-slug` so `automation_state.json` records daily completion metadata correctly
- if the explicit target was already present in the repo, acceptance is still allowed, but the recomputed sequential prefix may stay unchanged
