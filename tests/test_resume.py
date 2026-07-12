import json
import os
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDENTITY = os.path.join(BASE, "tests", "fixtures", "tasks", "identity.json")

STUB = """\
import os
c = os.path.join(os.path.dirname(os.path.abspath(__file__)), "count")
n = int(open(c).read()) if os.path.exists(c) else 0
open(c, "w").write(str(n + 1))
print("p=lambda g:g")
"""


def run(args, cwd):
    return subprocess.run(
        [sys.executable, os.path.join(BASE, "scripts", "eval_model.py")] + args,
        capture_output=True, text=True, cwd=cwd,
    )


def test_resume_skips_finished_tasks():
    with tempfile.TemporaryDirectory() as d:
        tasks = os.path.join(d, "tasks")
        os.makedirs(tasks)
        for name in ("a.json", "b.json"):
            with open(IDENTITY, "rb") as src, open(os.path.join(tasks, name), "wb") as dst:
                dst.write(src.read())
        stub = os.path.join(d, "stub.py")
        with open(stub, "w", encoding="utf-8", newline="\n") as f:
            f.write(STUB)
        counter = os.path.join(d, "count")
        out = os.path.join(d, "out")
        cmd = f'{sys.executable} "{stub}"'

        first = run(["--cmd", cmd, "--tasks", tasks, "--out", out, "--k", "1"], d)
        assert first.returncode == 0, first.stderr
        assert open(counter).read() == "2"

        second = run(["--cmd", cmd, "--tasks", tasks, "--out", out, "--k", "1", "--resume"], d)
        assert second.returncode == 0, second.stderr
        assert open(counter).read() == "2"
        with open(os.path.join(out, "results.json"), encoding="utf-8") as f:
            assert json.load(f)["summary"]["solved"] == 2

        third = run(["--cmd", cmd, "--tasks", tasks, "--out", out, "--k", "2", "--resume"], d)
        assert third.returncode == 0, third.stderr
        assert open(counter).read() == "6"


if __name__ == "__main__":
    test_resume_skips_finished_tasks()
    print("resume pass")
