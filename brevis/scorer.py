import json
import os

from . import sandbox


def load_pairs(task_path):
    with open(task_path, encoding="utf-8") as f:
        task = json.load(f)
    return [(p["input"], p["output"]) for p in task["train"] + task["test"]]


def score_solution(sol_path, task_path, timeout=5.0):
    pairs = load_pairs(task_path)
    outs = sandbox.run_solution(sol_path, [g for g, _ in pairs], timeout=timeout)
    passed = (
        outs is not None
        and len(outs) == len(pairs)
        and all(o == want for o, (_, want) in zip(outs, pairs))
    )
    return {"passed": passed, "bytes": os.path.getsize(sol_path)}
