import argparse

from . import eval as evaluate


def main():
    ap = argparse.ArgumentParser(prog="brevis", description="y long when short?")
    sub = ap.add_subparsers(dest="command", required=True)
    ev = sub.add_parser("eval")
    ev.add_argument("--tasks", required=True)
    ev.add_argument("--solutions", required=True)
    ev.add_argument("--timeout", type=float, default=5.0)
    ev.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.command == "eval":
        evaluate.run(args.tasks, args.solutions, args.timeout, args.json)
