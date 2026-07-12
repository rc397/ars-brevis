import json
import os
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f)


def test_table_includes_par_and_sorts():
    with tempfile.TemporaryDirectory() as d:
        write_json(os.path.join(d, "runs", "modelx", "results.json"),
                   {"summary": {"tasks": 10, "solved": 4, "bytes": 900}})
        write_json(os.path.join(d, "runs", "modely", "results.json"),
                   {"summary": {"tasks": 10, "solved": 4, "bytes": 700}})
        write_json(os.path.join(d, "par.json"),
                   {"tasks": {}, "summary": {"tasks": 10, "solved": 9, "bytes": 500}})
        proc = subprocess.run(
            [sys.executable, os.path.join(BASE, "scripts", "leaderboard.py"),
             "--runs", os.path.join(d, "runs"), "--par", os.path.join(d, "par.json")],
            capture_output=True, text=True,
        )
        assert proc.returncode == 0, proc.stderr
        lines = proc.stdout.strip().splitlines()
        assert lines[2] == "| human par | 9/10 | 90% | 500 |"
        assert lines[3] == "| modely | 4/10 | 40% | 700 |"
        assert lines[4] == "| modelx | 4/10 | 40% | 900 |"


def test_missing_par_is_fine():
    with tempfile.TemporaryDirectory() as d:
        write_json(os.path.join(d, "runs", "modelx", "results.json"),
                   {"summary": {"tasks": 10, "solved": 1, "bytes": 100}})
        proc = subprocess.run(
            [sys.executable, os.path.join(BASE, "scripts", "leaderboard.py"),
             "--runs", os.path.join(d, "runs"), "--par", os.path.join(d, "nope.json")],
            capture_output=True, text=True,
        )
        assert proc.returncode == 0, proc.stderr
        assert "modelx" in proc.stdout and "human par" not in proc.stdout


if __name__ == "__main__":
    test_table_includes_par_and_sorts()
    test_missing_par_is_fine()
    print("leaderboard pass")
