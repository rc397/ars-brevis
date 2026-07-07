import json
import os
import subprocess
import sys
import tempfile

RUNNER = """\
import contextlib, io, json, sys
src = open(sys.argv[1], encoding="utf-8").read()
pairs = json.load(sys.stdin)
ns = {}
out = []
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, ns)
    p = ns["p"]
    for g in pairs:
        try:
            out.append(p(g))
        except Exception:
            out.append(None)
sys.stdout.write(json.dumps(out))
"""


def run_solution(path, inputs, timeout=5.0):
    fd, runner = tempfile.mkstemp(suffix=".py")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(RUNNER)
    try:
        proc = subprocess.run(
            [sys.executable, "-I", runner, os.path.abspath(path)],
            input=json.dumps(inputs),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return None
    finally:
        os.unlink(runner)
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None
