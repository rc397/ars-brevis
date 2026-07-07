import argparse
import sys

import anthropic


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="claude-opus-4-8")
    ap.add_argument("--max-tokens", type=int, default=16000)
    ap.add_argument("--effort")
    args = ap.parse_args()
    prompt = sys.stdin.read()
    extra = {}
    if args.effort:
        extra["output_config"] = {"effort": args.effort}
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=args.model,
        max_tokens=args.max_tokens,
        thinking={"type": "adaptive"},
        messages=[{"role": "user", "content": prompt}],
        **extra,
    )
    if response.stop_reason == "refusal":
        sys.exit(1)
    for block in response.content:
        if block.type == "text":
            print(block.text)


if __name__ == "__main__":
    main()
