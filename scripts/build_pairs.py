import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from brevis import scorer
from import_gold import build_map, collect


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", nargs="+", required=True)
    ap.add_argument("--comp", required=True)
    ap.add_argument("--tasks", default="data/arc/training")
    ap.add_argument("--out", default="gold/pairs.jsonl")
    ap.add_argument("--timeout", type=float, default=5.0)
    args = ap.parse_args()
    mapping = build_map(args.comp, args.tasks)
    cands = collect(args.src)
    print(f"{sum(len(v) for v in cands.values())} unique candidates", flush=True)
    pairs = 0
    with open(args.out, "w", encoding="utf-8", newline="\n") as out:
        for num in sorted(cands):
            tid = mapping.get(num)
            if not tid:
                continue
            task_path = os.path.join(args.tasks, tid + ".json")
            passing = []
            for size, path, data in sorted(cands[num].values()):
                if scorer.score_solution(path, task_path, timeout=args.timeout)["passed"]:
                    passing.append((size, data))
            for (short_n, short), (long_n, long) in zip(passing, passing[1:]):
                if long_n == short_n:
                    continue
                record = {
                    "task": tid,
                    "long": long.decode("utf-8", "replace"),
                    "short": short.decode("utf-8", "replace"),
                    "long_bytes": long_n,
                    "short_bytes": short_n,
                }
                out.write(json.dumps(record) + "\n")
                pairs += 1
            print(f"{num} {tid} {len(passing)} passing", flush=True)
    print(f"{pairs} pairs written to {args.out}", flush=True)


if __name__ == "__main__":
    main()
