import json
import os
import subprocess
import tempfile

from . import scorer

PROMPT = """\
You are playing Ars Brevis, a code golf benchmark over grid puzzles.
Write the shortest possible Python program that defines a function p.
The function p takes an input grid, a list of lists of ints, and returns the output grid.
Your program must reproduce every example below and generalize to unseen pairs drawn from the same rule.
The program runs with the standard library only.
Reply with the program alone, in one fenced code block or as bare code.

Examples
{pairs}
"""


def build_prompt(task):
    lines = []
    for pair in task["train"]:
        lines.append(json.dumps(pair["input"]) + " -> " + json.dumps(pair["output"]))
    return PROMPT.format(pairs="\n".join(lines))


def extract(text):
    if "```" not in text:
        return text.strip()
    block = text.split("```")[1]
    lines = block.splitlines()
    if lines and lines[0].strip() in ("python", "py", ""):
        lines = lines[1:]
    return "\n".join(lines).strip()


def run_model(cmd, prompt, timeout=120.0):
    try:
        proc = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            shell=isinstance(cmd, str),
        )
    except subprocess.TimeoutExpired:
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout


def best_of_k(cmd, task_path, k, out_path, cmd_timeout=120.0, timeout=5.0):
    with open(task_path, encoding="utf-8") as f:
        task = json.load(f)
    prompt = build_prompt(task)
    best = None
    passes = 0
    for _ in range(k):
        text = run_model(cmd, prompt, timeout=cmd_timeout)
        if not text:
            continue
        code = extract(text).encode()
        if not code:
            continue
        fd, tmp = tempfile.mkstemp(suffix=".py")
        with os.fdopen(fd, "wb") as f:
            f.write(code)
        try:
            passed = scorer.score_solution(tmp, task_path, timeout=timeout)["passed"]
        finally:
            os.unlink(tmp)
        if not passed:
            continue
        passes += 1
        if best is None or len(code) < len(best):
            best = code
    if best is not None:
        with open(out_path, "wb") as f:
            f.write(best)
    return {"solved": best is not None, "bytes": len(best) if best else 0, "passes": passes, "attempts": k}
