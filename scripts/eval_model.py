import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brevis import sampler


def load_done(path, cmd, k):
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        lines = [json.loads(line) for line in f if line.strip()]
    if not lines or lines[0] != {"cmd": cmd, "k": k}:
        return {}
    return {r["task"]: r for r in lines[1:]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cmd", required=True)
    ap.add_argument("--tasks", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--k", type=int, default=4)
    ap.add_argument("--timeout", type=float, default=5.0)
    ap.add_argument("--cmd-timeout", type=float, default=120.0)
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()
    sol_dir = os.path.join(args.out, "solutions")
    os.makedirs(sol_dir, exist_ok=True)
    jsonl = os.path.join(args.out, "results.jsonl")
    done = load_done(jsonl, args.cmd, args.k) if args.resume else {}
    log = open(jsonl, "a" if done else "w", encoding="utf-8", newline="\n")
    if not done:
        log.write(json.dumps({"cmd": args.cmd, "k": args.k}) + "\n")
        log.flush()
    rows = []
    for task_path in sorted(glob.glob(os.path.join(args.tasks, "*.json"))):
        tid = os.path.splitext(os.path.basename(task_path))[0]
        if tid in done:
            result = done[tid]
        else:
            result = sampler.best_of_k(
                args.cmd, task_path, args.k, os.path.join(sol_dir, tid + ".py"),
                cmd_timeout=args.cmd_timeout, timeout=args.timeout,
                keep_dir=os.path.join(args.out, "attempts") if args.keep else None,
            )
            result["task"] = tid
            log.write(json.dumps(result) + "\n")
            log.flush()
        rows.append(result)
        status = "pass" if result["solved"] else "fail"
        print(f"{tid:<24} {status:<5} {result['bytes']}", flush=True)
    log.close()
    solved = [r for r in rows if r["solved"]]
    summary = {"tasks": len(rows), "solved": len(solved), "bytes": sum(r["bytes"] for r in solved)}
    with open(os.path.join(args.out, "results.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"cmd": args.cmd, "k": args.k, "rows": rows, "summary": summary}, f, indent=2)
        f.write("\n")
    print(f"solved {summary['solved']}/{summary['tasks']}, {summary['bytes']} bytes")


if __name__ == "__main__":
    main()
