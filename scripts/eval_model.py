import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brevis import sampler


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cmd", required=True)
    ap.add_argument("--tasks", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--k", type=int, default=4)
    ap.add_argument("--timeout", type=float, default=5.0)
    ap.add_argument("--cmd-timeout", type=float, default=120.0)
    args = ap.parse_args()
    sol_dir = os.path.join(args.out, "solutions")
    os.makedirs(sol_dir, exist_ok=True)
    rows = []
    for task_path in sorted(glob.glob(os.path.join(args.tasks, "*.json"))):
        tid = os.path.splitext(os.path.basename(task_path))[0]
        result = sampler.best_of_k(
            args.cmd, task_path, args.k, os.path.join(sol_dir, tid + ".py"),
            cmd_timeout=args.cmd_timeout, timeout=args.timeout,
        )
        result["task"] = tid
        rows.append(result)
        status = "pass" if result["solved"] else "fail"
        print(f"{tid:<24} {status:<5} {result['bytes']}", flush=True)
    solved = [r for r in rows if r["solved"]]
    summary = {"tasks": len(rows), "solved": len(solved), "bytes": sum(r["bytes"] for r in solved)}
    with open(os.path.join(args.out, "results.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"cmd": args.cmd, "k": args.k, "rows": rows, "summary": summary}, f, indent=2)
        f.write("\n")
    print(f"solved {summary['solved']}/{summary['tasks']}, {summary['bytes']} bytes")


if __name__ == "__main__":
    main()
