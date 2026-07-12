import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brevis import cli

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_find_task():
    dirs = [os.path.join(BASE, "tests", "fixtures", "tasks")]
    found = cli.find_task("anywhere/identity.py", dirs)
    assert found and found.endswith("identity.json")
    assert cli.find_task("anywhere/missing.py", dirs) is None


def test_score_shorthand():
    proc = subprocess.run(
        [sys.executable, "-m", "brevis", "examples/solutions/identity.py",
         "--task", "tests/fixtures/tasks/identity.json"],
        cwd=BASE,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == "pass 12 bytes"


def test_score_fail_exit():
    proc = subprocess.run(
        [sys.executable, "-m", "brevis", "score", "brevis/cli.py",
         "--task", "tests/fixtures/tasks/identity.json"],
        cwd=BASE,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 1
    assert proc.stdout.startswith("fail")


if __name__ == "__main__":
    test_find_task()
    test_score_shorthand()
    test_score_fail_exit()
    print("cli pass")
