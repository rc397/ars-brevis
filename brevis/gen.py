import json
import os
import random

from . import families


def make_task(rng, spec):
    fam = families.FAMILIES[spec["family"]]
    gen_input = fam.get("input", families.default_input)
    n_train = rng.randint(3, 4)
    pairs = []
    seen = set()
    while len(pairs) < n_train + 2:
        g = gen_input(rng, spec["params"])
        key = str(g)
        if key in seen:
            continue
        seen.add(key)
        pairs.append({"input": g, "output": fam["apply"](spec["params"], g)})
    return {"train": pairs[:n_train], "test": pairs[n_train:]}


def init_manifest(seed, per_family=3):
    rng = random.Random(f"{seed}/params")
    tasks = {}
    for name, fam in families.FAMILIES.items():
        for i, params in enumerate(fam["variants"](rng)[:per_family], 1):
            tasks[f"{name}-{i}"] = {"family": name, "params": params}
    return {"tasks": tasks}


def build(manifest, seed, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for tid, spec in manifest["tasks"].items():
        task = make_task(random.Random(f"{seed}/{tid}"), spec)
        with open(os.path.join(out_dir, tid + ".json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(task, f)
            f.write("\n")
    return len(manifest["tasks"])
