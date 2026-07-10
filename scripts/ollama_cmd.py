import argparse
import json
import sys
import urllib.request


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--url", default="http://localhost:11434")
    ap.add_argument("--num-predict", type=int, default=2000)
    ap.add_argument("--think", action="store_true")
    args = ap.parse_args()
    prompt = sys.stdin.read()
    body = json.dumps({
        "model": args.model,
        "prompt": prompt,
        "stream": False,
        "think": args.think,
        "options": {"num_predict": args.num_predict},
    }).encode()
    req = urllib.request.Request(
        args.url + "/api/generate", body, {"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)
    sys.stdout.write(data.get("response", ""))


if __name__ == "__main__":
    main()
