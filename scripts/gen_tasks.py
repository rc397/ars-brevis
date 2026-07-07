import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brevis import gen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", default="brevis-public-1")
    ap.add_argument("--manifest", default="data/generated/manifest.json")
    ap.add_argument("--out", default="data/generated/tasks")
    ap.add_argument("--per-family", type=int, default=3)
    ap.add_argument("--init", action="store_true")
    args = ap.parse_args()
    if args.init or not os.path.exists(args.manifest):
        manifest = gen.init_manifest(args.seed, args.per_family)
        os.makedirs(os.path.dirname(args.manifest) or ".", exist_ok=True)
        with open(args.manifest, "w", encoding="utf-8", newline="\n") as f:
            json.dump(manifest, f, indent=2)
            f.write("\n")
    else:
        with open(args.manifest, encoding="utf-8") as f:
            manifest = json.load(f)
    n = gen.build(manifest, args.seed, args.out)
    print(f"{n} tasks written to {args.out}")


if __name__ == "__main__":
    main()
