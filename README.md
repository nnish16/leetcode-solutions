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
