import argparse
import glob
import json
import os

from . import scorer


def run(tasks_dir, solutions_dir, timeout=5.0, as_json=False):
    rows = []
    task_paths = sorted(glob.glob(os.path.join(tasks_dir, "*.json")))
    for task_path in task_paths:
        task_id = os.path.splitext(os.path.basename(task_path))[0]
        sol_path = os.path.join(solutions_dir, task_id + ".py")
        if not os.path.exists(sol_path):
            continue
        result = scorer.score_solution(sol_path, task_path, timeout=timeout)
        result["task"] = task_id
        rows.append(result)
    solved = [r for r in rows if r["passed"]]
    summary = {
        "tasks": len(task_paths),
        "attempted": len(rows),
        "solved": len(solved),
        "bytes": sum(r["bytes"] for r in solved),
    }
    if as_json:
        print(json.dumps({"rows": rows, "summary": summary}))
        return {"rows": rows, "summary": summary}
    for r in rows:
        status = "pass" if r["passed"] else "fail"
        print(f"{r['task']:<24} {status:<5} {r['bytes']}")
    print(
        f"solved {summary['solved']}/{summary['attempted']} attempted, "
        f"{summary['tasks']} tasks, {summary['bytes']} bytes"
    )
    return {"rows": rows, "summary": summary}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", required=True)
    ap.add_argument("--solutions", required=True)
    ap.add_argument("--timeout", type=float, default=5.0)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    run(args.tasks, args.solutions, args.timeout, args.json)


if __name__ == "__main__":
    main()
