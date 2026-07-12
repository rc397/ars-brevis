import argparse
import os
import sys

from . import eval as evaluate
from . import scorer

TASK_DIRS = ["data/generated/tasks", "data/arc/training", "tests/fixtures/tasks"]


def find_task(sol_path, dirs=TASK_DIRS):
    stem = os.path.splitext(os.path.basename(sol_path))[0]
    for d in dirs:
        path = os.path.join(d, stem + ".json")
        if os.path.exists(path):
            return path
    return None


def main():
    argv = sys.argv[1:]
    if argv and argv[0].endswith(".py"):
        argv.insert(0, "score")
    ap = argparse.ArgumentParser(prog="brevis", description="y long when short?")
    sub = ap.add_subparsers(dest="command", required=True)
    sc = sub.add_parser("score")
    sc.add_argument("solution")
    sc.add_argument("--task")
    sc.add_argument("--timeout", type=float, default=5.0)
    ev = sub.add_parser("eval")
    ev.add_argument("--tasks", required=True)
    ev.add_argument("--solutions", required=True)
    ev.add_argument("--timeout", type=float, default=5.0)
    ev.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.command == "eval":
        evaluate.run(args.tasks, args.solutions, args.timeout, args.json)
        return
    task = args.task or find_task(args.solution)
    if not task:
        sys.exit(f"no task found for {args.solution}")
    result = scorer.score_solution(args.solution, task, timeout=args.timeout)
    status = "pass" if result["passed"] else "fail"
    print(f"{status} {result['bytes']} bytes")
    if not result["passed"]:
        sys.exit(1)
