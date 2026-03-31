#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import errno
import fcntl
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent
STATE_PATH = REPO_ROOT / "automation_state.json"
LOCK_PATH = REPO_ROOT / ".automation.lock"
RUNS_DIR = REPO_ROOT / "automation_runs"
AUTOMATION_DIR = REPO_ROOT / "automation"
EXECUTOR_PATH = AUTOMATION_DIR / "browser_executor.js"
PROBLEM_FILE_PATTERN = re.compile(r"^(\d{4})_.+\.py$")
DEFAULT_STATE = {
    "sequential": {
        "last_contiguous_solved_id": 0,
        "next_target_id": 1,
        "updated_from_repo_scan": True,
    },
    "daily_challenge": {
        "last_checked_date": None,
        "last_attempted_id": None,
        "last_completed_id": None,
        "last_completed_slug": None,
        "notes": "If the daily challenge is already solved in repo history, skip it without affecting the sequential counter. If the daily challenge is unsolved and outside the current sequential target, solve it in addition to the sequential target(s), but do not advance the sequential counter past unsolved gaps.",
    },
    "rules": {
        "mode": "sequential_plus_daily",
        "sequential_batch_size": 1,
        "daily_batch_size": 1,
        "skip_daily_if_already_solved": True,
        "do_not_advance_sequential_counter_for_out_of_order_solves": True,
        "advance_sequential_counter_only_when_contiguous_prefix_extends": True,
    },
}


@dataclass(frozen=True)
class ProblemTarget:
    id: int
    slug: str | None
    track: str
    already_solved: bool
    reason: str


@dataclass(frozen=True)
class ExecutionPlan:
    sequential_prefix: int
    sequential_targets: list[ProblemTarget]
    daily_target: ProblemTarget | None
    total_targets: int
    daily_status: str
    notes: list[str]


@dataclass(frozen=True)
class ExplicitExecutionTarget:
    id: int
    slug: str | None
    already_solved_in_repo: bool
    source_solution_file: Path


class AutomationLock:
    def __init__(self, path: Path):
        self.path = path
        self.handle = None

    def __enter__(self) -> "AutomationLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.handle = self.path.open("a+", encoding="utf-8")
        try:
            fcntl.flock(self.handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            self.handle.seek(0)
            owner = self.handle.read().strip()
            raise RuntimeError(
                f"Another automation run is already active ({owner or 'lock held'})."
            ) from exc

        self.handle.seek(0)
        self.handle.truncate()
        payload = {
            "pid": os.getpid(),
            "started_at": now_iso(),
            "cwd": str(REPO_ROOT),
        }
        self.handle.write(json.dumps(payload, indent=2))
        self.handle.flush()
        os.fsync(self.handle.fileno())
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.handle is None:
            return
        try:
            self.handle.seek(0)
            self.handle.truncate()
            self.handle.flush()
            os.fsync(self.handle.fileno())
            fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
        finally:
            self.handle.close()
            try:
                self.path.unlink()
            except FileNotFoundError:
                pass


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return json.loads(json.dumps(DEFAULT_STATE))

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    state = json.loads(json.dumps(DEFAULT_STATE))
    for key, value in data.items():
        if isinstance(value, dict) and isinstance(state.get(key), dict):
            state[key].update(value)
        else:
            state[key] = value
    return state


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
    except Exception:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise


def scan_solved_problem_ids(repo_root: Path) -> list[int]:
    solved_ids = []
    for path in repo_root.iterdir():
        if not path.is_file():
            continue
        match = PROBLEM_FILE_PATTERN.match(path.name)
        if match:
            solved_ids.append(int(match.group(1)))
    return sorted(set(solved_ids))


def contiguous_prefix(solved_ids: list[int]) -> int:
    expected = 1
    for problem_id in solved_ids:
        if problem_id != expected:
            break
        expected += 1
    return expected - 1


def build_slug(problem_id: int) -> str:
    return f"problem-{problem_id:04d}"


def canonical_solution_path(problem_id: int, slug: str) -> Path:
    slug_part = slug.replace("-", "_")
    return REPO_ROOT / f"{problem_id:04d}_{slug_part}.py"


def run_browser_executor(problem_id: int, slug: str | None, solution_file: Path, cdp_url: str) -> dict[str, Any]:
    if not EXECUTOR_PATH.exists():
        raise FileNotFoundError(f"Missing browser executor: {EXECUTOR_PATH}")
    if not solution_file.exists():
        raise FileNotFoundError(f"Missing solution file: {solution_file}")

    command = [
        "node",
        str(EXECUTOR_PATH),
        "--problem-id",
        str(problem_id),
        "--solution-file",
        str(solution_file),
        "--cdp-url",
        cdp_url,
    ]
    if slug:
        command.extend(["--slug", slug])

    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    output = (completed.stdout or "").strip()
    if not output:
        stderr = (completed.stderr or "").strip()
        raise RuntimeError(f"Browser executor produced no JSON output. stderr={stderr!r}")

    try:
        payload = json.loads(output)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Browser executor emitted invalid JSON: {output[:500]!r}") from exc

    payload["exit_code"] = completed.returncode
    if completed.stderr:
        payload["stderr"] = completed.stderr.strip()
    return payload


def plan_targets(
    solved_ids: set[int],
    sequential_prefix: int,
    daily_id: int | None,
    daily_slug: str | None,
) -> ExecutionPlan:
    next_sequential = sequential_prefix + 1
    notes: list[str] = []
    sequential_targets: list[ProblemTarget] = []
    daily_target: ProblemTarget | None = None

    daily_status = "not_provided"
    if daily_id is not None:
        daily_slug = daily_slug or build_slug(daily_id)
        if daily_id in solved_ids:
            daily_status = "already_solved"
            notes.append(
                f"Daily challenge {daily_id} is already solved, so the run backfills with a second sequential target."
            )
        elif daily_id == next_sequential:
            daily_status = "matches_next_sequential"
            daily_target = ProblemTarget(
                id=daily_id,
                slug=daily_slug,
                track="daily+sequential",
                already_solved=False,
                reason="Daily challenge matches the next unsolved sequential problem, so one solve satisfies both tracks.",
            )
            sequential_targets.append(daily_target)
        else:
            daily_status = "planned"
            daily_target = ProblemTarget(
                id=daily_id,
                slug=daily_slug,
                track="daily",
                already_solved=False,
                reason="Independent daily challenge target.",
            )
            notes.append(
                "Daily challenge is outside the sequential prefix, so solving it will not advance the sequential counter by itself."
            )

    desired_sequential_count = 1
    if daily_status == "already_solved":
        desired_sequential_count = 2

    candidate = next_sequential
    while len(sequential_targets) < desired_sequential_count:
        if candidate in solved_ids:
            candidate += 1
            continue
        if any(target.id == candidate for target in sequential_targets):
            candidate += 1
            continue
        sequential_targets.append(
            ProblemTarget(
                id=candidate,
                slug=build_slug(candidate),
                track="sequential",
                already_solved=False,
                reason="Next unsolved problem in the contiguous sequential track.",
            )
        )
        candidate += 1

    if daily_status == "not_provided":
        notes.append("No daily challenge was provided, so the plan contains only sequential work.")

    return ExecutionPlan(
        sequential_prefix=sequential_prefix,
        sequential_targets=sequential_targets,
        daily_target=daily_target,
        total_targets=len(sequential_targets) + (1 if daily_target and daily_target.track == "daily" else 0),
        daily_status=daily_status,
        notes=notes,
    )


def write_run_log(run_record: dict[str, Any]) -> Path:
    started_at = dt.datetime.fromisoformat(run_record["started_at"])
    day_dir = RUNS_DIR / started_at.strftime("%Y-%m-%d")
    day_dir.mkdir(parents=True, exist_ok=True)
    log_path = day_dir / f"{started_at.strftime('%H%M%S')}-{os.getpid()}.json"
    atomic_write_json(log_path, run_record)
    return log_path


def print_plan(
    plan: ExecutionPlan,
    solved_ids: list[int],
    explicit_target: ExplicitExecutionTarget | None = None,
) -> None:
    print(f"Solved contiguous prefix: 1..{plan.sequential_prefix}")
    print(f"Total solved files found: {len(solved_ids)}")
    print(f"Daily status: {plan.daily_status}")
    if explicit_target:
        print("Explicit execution target:")
        print(f"  - #{explicit_target.id} ({explicit_target.slug or 'slug resolved by executor'})")
        print(f"  - source file: {explicit_target.source_solution_file}")
        print(
            "  - repo status: already solved"
            if explicit_target.already_solved_in_repo
            else "  - repo status: not yet solved"
        )
        print("Planner context:")
        print("  - sequential/daily plan below is informational only; execution is pinned to the explicit target above.")
    print("Execution plan:")
    for target in plan.sequential_targets:
        print(f"  - [{target.track}] #{target.id} ({target.slug})")
    if plan.daily_target and plan.daily_target.track == "daily":
        print(f"  - [daily] #{plan.daily_target.id} ({plan.daily_target.slug})")
    if not plan.sequential_targets and not plan.daily_target:
        print("  - nothing to do")
    if plan.notes:
        print("Notes:")
        for note in plan.notes:
            print(f"  - {note}")
    if explicit_target and explicit_target.already_solved_in_repo:
        print("  - Explicit target was already present in the repo, so recomputed sequential progress may remain unchanged after acceptance.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local LeetCode automation planner/runner")
    parser.add_argument("--daily-id", type=int, help="Daily challenge problem ID")
    parser.add_argument("--daily-slug", help="Daily challenge slug")
    parser.add_argument(
        "--mark-solved",
        type=int,
        action="append",
        default=[],
        help="Record a problem ID as solved in the run log/state metadata. Repeatable.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the plan without persisting state or run logs.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Also print the computed run payload as JSON.",
    )
    parser.add_argument("--execute-target-id", type=int, help="Execute a single target in the browser before writing repo/state updates.")
    parser.add_argument("--execute-target-slug", help="Exact LeetCode slug for --execute-target-id. If omitted, the browser executor resolves it.")
    parser.add_argument("--solution-file", help="Local Python solution file to submit for --execute-target-id.")
    parser.add_argument(
        "--cdp-url",
        default=os.environ.get("LEETCODE_CDP_URL", "http://127.0.0.1:56278"),
        help="HTTP CDP base URL for the existing Playwright-managed Chrome session.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started_at = now_iso()

    try:
        with AutomationLock(LOCK_PATH):
            state = load_state(STATE_PATH)
            solved_ids = scan_solved_problem_ids(REPO_ROOT)
            solved_set = set(solved_ids)
            prefix = contiguous_prefix(solved_ids)
            plan = plan_targets(
                solved_ids=solved_set,
                sequential_prefix=prefix,
                daily_id=args.daily_id,
                daily_slug=args.daily_slug,
            )

            state["sequential"]["last_contiguous_solved_id"] = prefix
            state["sequential"]["next_target_id"] = prefix + 1
            state["sequential"]["updated_from_repo_scan"] = True
            state["daily_challenge"]["last_checked_date"] = dt.date.today().isoformat()
            if args.daily_id is not None:
                state["daily_challenge"]["last_attempted_id"] = args.daily_id

            browser_execution: dict[str, Any] | None = None
            persisted_solution_path: Path | None = None
            explicit_target: ExplicitExecutionTarget | None = None
            marked_solved = list(args.mark_solved)
            if args.execute_target_id is not None:
                if not args.solution_file:
                    raise ValueError("--solution-file is required with --execute-target-id")
                source_solution_path = Path(args.solution_file).resolve()
                explicit_target = ExplicitExecutionTarget(
                    id=args.execute_target_id,
                    slug=args.execute_target_slug,
                    already_solved_in_repo=args.execute_target_id in solved_set,
                    source_solution_file=source_solution_path,
                )
                browser_execution = run_browser_executor(
                    problem_id=args.execute_target_id,
                    slug=args.execute_target_slug,
                    solution_file=source_solution_path,
                    cdp_url=args.cdp_url,
                )
                if not browser_execution.get("accepted"):
                    raise RuntimeError(
                        f"Browser executor did not confirm Accepted state for #{args.execute_target_id}: "
                        f"{browser_execution.get('error', {}).get('message', 'unknown failure')}"
                    )

                resolved_slug = browser_execution["problem"]["slug"]
                explicit_target = ExplicitExecutionTarget(
                    id=explicit_target.id,
                    slug=resolved_slug,
                    already_solved_in_repo=explicit_target.already_solved_in_repo,
                    source_solution_file=explicit_target.source_solution_file,
                )
                persisted_solution_path = canonical_solution_path(args.execute_target_id, resolved_slug)
                if source_solution_path != persisted_solution_path.resolve():
                    shutil.copyfile(source_solution_path, persisted_solution_path)
                solved_ids = scan_solved_problem_ids(REPO_ROOT)
                solved_set = set(solved_ids)
                prefix = contiguous_prefix(solved_ids)
                state["sequential"]["last_contiguous_solved_id"] = prefix
                state["sequential"]["next_target_id"] = prefix + 1
                state["sequential"]["updated_from_repo_scan"] = True
                if args.execute_target_id not in marked_solved:
                    marked_solved.append(args.execute_target_id)

            if marked_solved:
                latest_solved = marked_solved[-1]
                if latest_solved == args.daily_id:
                    completed_slug = args.daily_slug or build_slug(latest_solved)
                    if browser_execution and browser_execution.get("problem", {}).get("id") == latest_solved:
                        completed_slug = browser_execution["problem"].get("slug") or completed_slug
                    state["daily_challenge"]["last_completed_id"] = latest_solved
                    state["daily_challenge"]["last_completed_slug"] = completed_slug

            run_record = {
                "started_at": started_at,
                "finished_at": now_iso(),
                "dry_run": args.dry_run,
                "inputs": {
                    "daily_id": args.daily_id,
                    "daily_slug": args.daily_slug,
                    "mark_solved": args.mark_solved,
                    "execute_target_id": args.execute_target_id,
                    "execute_target_slug": args.execute_target_slug,
                    "solution_file": args.solution_file,
                    "cdp_url": args.cdp_url,
                },
                "repo_scan": {
                    "solved_ids": solved_ids,
                    "contiguous_prefix": prefix,
                },
                "plan": {
                    "sequential_prefix": plan.sequential_prefix,
                    "daily_status": plan.daily_status,
                    "notes": plan.notes,
                    "sequential_targets": [asdict(target) for target in plan.sequential_targets],
                    "daily_target": asdict(plan.daily_target) if plan.daily_target else None,
                    "total_targets": plan.total_targets,
                    "explicit_execution_target": {
                        "id": explicit_target.id,
                        "slug": explicit_target.slug,
                        "already_solved_in_repo": explicit_target.already_solved_in_repo,
                        "source_solution_file": str(explicit_target.source_solution_file),
                    } if explicit_target else None,
                },
                "state_after": state,
                "execution": {
                    "mode": "planner_plus_browser_executor" if browser_execution else "planner_only",
                    "submission_integration": "browser_executor" if browser_execution else "stubbed",
                    "marked_solved": marked_solved,
                    "browser_execution": browser_execution,
                    "persisted_solution_path": str(persisted_solution_path) if persisted_solution_path else None,
                },
            }

            print_plan(plan, solved_ids, explicit_target=explicit_target)
            if marked_solved:
                print(f"Marked solved: {', '.join(map(str, marked_solved))}")
            if persisted_solution_path:
                print(f"Persisted accepted solution: {persisted_solution_path}")
            if args.dry_run:
                print("Dry run: state and run log were not written.")
            else:
                atomic_write_json(STATE_PATH, state)
                log_path = write_run_log(run_record)
                print(f"Updated state: {STATE_PATH}")
                print(f"Run log: {log_path}")

            if args.json:
                print(json.dumps(run_record, indent=2))
    except RuntimeError as exc:
        print(f"Lock error: {exc}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"Missing file: {exc}", file=sys.stderr)
        return errno.ENOENT
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON in state file: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Automation error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
