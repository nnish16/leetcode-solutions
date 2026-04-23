# LeetCode Solutions

> Deterministic CLI orchestrator for sequential LeetCode progress with state management, planning, and browser automation.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Overview

This repository contains my solutions to LeetCode problems, along with a hardened **planner/runner** (`manager.py`) that automates the solve-track-submit workflow.

### What makes this different from a typical leetcode repo

Most leetcode repos are just solution dumps. This one has:

- **Deterministic planning** — the manager scans the repo, recomputes the contiguous solved prefix, and plans exactly which problem to solve next
- **Lock-file concurrency** — prevents overlapping automation runs
- **State persistence** — JSON-based tracking of sequential progress + daily challenges
- **Browser automation** — optional CDP-based submission via Chrome DevTools Protocol
- **Dry-run mode** — preview the plan without writing state

## Progress

**Problems solved:** 68+ and counting

Solutions are in Python (primary) with select problems in JavaScript. Each file follows the naming convention `NNNN_slug.py`.

## Planner / Runner

```bash
# See what the planner would do (no state changes)
python3 manager.py --dry-run

# Plan with today's daily challenge
python3 manager.py --daily-id 3651 --daily-slug minimum-cost-walk-in-weighted-graph

# Mark a daily as solved
python3 manager.py --daily-id 3651 --mark-solved 3651

# Submit via browser automation (requires Chrome CDP)
python3 manager.py --execute-target-id 41 --solution-file /tmp/0041.py --cdp-url http://127.0.0.1:56278
```

### Planning Logic

1. Scans root-level `NNNN_slug.py` files every run
2. Recomputes the contiguous solved prefix (e.g., 1–68 = prefix of 68)
3. Plans `1 sequential + 1 daily` when an unsolved daily challenge is provided
4. Plans `2 sequential` when the daily is already solved
5. Treats daily challenges that match sequential targets as dual-purpose

## Solution Style

Each solution includes:

- Problem number and title in the filename
- Approach explanation in comments
- Time and space complexity analysis
- Clean, readable code (no competitive-programming shortcuts)

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3 (stdlib only for manager) |
| Concurrency | File-based locking (fcntl) |
| State | JSON persistence |
| Browser | Chrome DevTools Protocol (optional) |

## Contributing

Found a bug in a solution or have a cleaner approach? PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) — Nishant Sarang
