import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brevis import eval as evaluate


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", default="data/arc/training")
    ap.add_argument("--gold", default="gold")
    ap.add_argument("--out", default="data/par.json")
    ap.add_argument("--timeout", type=float, default=5.0)
    args = ap.parse_args()
    result = evaluate.run(args.tasks, args.gold, timeout=args.timeout)
    solved = {r["task"]: r["bytes"] for r in result["rows"] if r["passed"]}
    par = {"tasks": solved, "summary": result["summary"]}
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(par, f, indent=2, sort_keys=True)
        f.write("\n")
    print(f"par written to {args.out}")


if __name__ == "__main__":
    main()
