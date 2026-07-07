import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brevis import scorer

BASE = os.path.dirname(os.path.abspath(__file__))
IDENTITY = os.path.join(BASE, "fixtures", "tasks", "identity.json")


def test_wrong_output_fails():
    with tempfile.TemporaryDirectory() as d:
        sol = os.path.join(d, "sol.py")
        with open(sol, "w", encoding="utf-8", newline="\n") as f:
            f.write("p=lambda g:[[7]]")
        result = scorer.score_solution(sol, IDENTITY)
        assert not result["passed"]
        assert result["bytes"] == os.path.getsize(sol)


def test_partial_match_fails():
    with tempfile.TemporaryDirectory() as d:
        sol = os.path.join(d, "sol.py")
        with open(sol, "w", encoding="utf-8", newline="\n") as f:
            f.write("p=lambda g:g if len(g)>1 else [[7]]")
        assert not scorer.score_solution(sol, IDENTITY)["passed"]


if __name__ == "__main__":
    test_wrong_output_fails()
    test_partial_match_fails()
    print("scorer pass")
