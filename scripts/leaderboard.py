import argparse
import glob
import json
import os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs")
    ap.add_argument("--par", default="data/par.json")
    args = ap.parse_args()
    entries = []
    for path in sorted(glob.glob(os.path.join(args.runs, "*", "results.json"))):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        s = data["summary"]
        entries.append((os.path.basename(os.path.dirname(path)), s["solved"], s["tasks"], s["bytes"]))
    if os.path.exists(args.par):
        with open(args.par, encoding="utf-8") as f:
            s = json.load(f)["summary"]
        entries.append(("human par", s["solved"], s["tasks"], s["bytes"]))
    entries.sort(key=lambda e: (-(e[1] / e[2] if e[2] else 0), e[3]))
    print("| entry | solved | rate | bytes |")
    print("| --- | --- | --- | --- |")
    for name, solved, tasks, b in entries:
        rate = f"{100 * solved / tasks:.0f}%" if tasks else "n/a"
        print(f"| {name} | {solved}/{tasks} | {rate} | {b} |")
    print()
    print("Bytes compare only within one task set and over the same solved tasks. Rank by rate across sets.")


if __name__ == "__main__":
    main()
