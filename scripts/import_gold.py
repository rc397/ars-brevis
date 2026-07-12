import argparse
import glob
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brevis import scorer


def build_map(comp_dir, tasks_dir):
    by_train = {}
    for path in glob.glob(os.path.join(tasks_dir, "*.json")):
        with open(path, encoding="utf-8") as f:
            task = json.load(f)
        by_train[json.dumps(task["train"], sort_keys=True)] = os.path.splitext(os.path.basename(path))[0]
    mapping = {}
    for path in glob.glob(os.path.join(comp_dir, "task*.json")):
        with open(path, encoding="utf-8") as f:
            task = json.load(f)
        tid = by_train.get(json.dumps(task["train"], sort_keys=True))
        if tid:
            mapping[os.path.splitext(os.path.basename(path))[0]] = tid
    return mapping


def collect(roots):
    pat = re.compile(r"^task\d{3}\.py$")
    out = {}
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in (".venv", "__pycache__", ".git")]
            for name in filenames:
                if not pat.match(name):
                    continue
                path = os.path.join(dirpath, name)
                with open(path, "rb") as f:
                    data = f.read()
                num = os.path.splitext(name)[0]
                out.setdefault(num, {})[hashlib.sha1(data).hexdigest()] = (len(data), path, data)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", nargs="+", required=True)
    ap.add_argument("--comp", required=True)
    ap.add_argument("--tasks", default="data/arc/training")
    ap.add_argument("--gold", default="gold")
    ap.add_argument("--timeout", type=float, default=5.0)
    args = ap.parse_args()
    mapping = build_map(args.comp, args.tasks)
    print(f"{len(mapping)} comp tasks mapped", flush=True)
    cands = collect(args.src)
    print(f"{sum(len(v) for v in cands.values())} unique candidates for {len(cands)} tasks", flush=True)
    os.makedirs(args.gold, exist_ok=True)
    done = 0
    for num in sorted(cands):
        tid = mapping.get(num)
        if not tid:
            continue
        task_path = os.path.join(args.tasks, tid + ".json")
        for size, path, data in sorted(cands[num].values()):
            if not scorer.score_solution(path, task_path, timeout=args.timeout)["passed"]:
                continue
            with open(os.path.join(args.gold, tid + ".py"), "wb") as f:
                f.write(data)
            done += 1
            print(f"{num} {tid} {size}", flush=True)
            break
        else:
            print(f"{num} {tid} nothing passed", flush=True)
    print(f"{done} gold solutions written", flush=True)


if __name__ == "__main__":
    main()
