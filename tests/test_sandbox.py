import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brevis import sandbox


def write(d, src):
    path = os.path.join(d, "sol.py")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(src)
    return path


def test_exception_becomes_none():
    with tempfile.TemporaryDirectory() as d:
        sol = write(d, "p=lambda g:[[1]] if g==[[0]] else 1//0")
        assert sandbox.run_solution(sol, [[[0]], [[5]]]) == [[[1]], None]


def test_bad_source_fails():
    with tempfile.TemporaryDirectory() as d:
        sol = write(d, "def p(")
        assert sandbox.run_solution(sol, [[[0]]]) is None


def test_missing_p_fails():
    with tempfile.TemporaryDirectory() as d:
        sol = write(d, "q=1")
        assert sandbox.run_solution(sol, [[[0]]]) is None


def test_timeout_kills():
    with tempfile.TemporaryDirectory() as d:
        sol = write(d, "while 1:pass")
        assert sandbox.run_solution(sol, [[[0]]], timeout=1.0) is None


def test_prints_are_swallowed():
    with tempfile.TemporaryDirectory() as d:
        sol = write(d, "print(9)\ndef p(g):\n    print(g)\n    return g")
        assert sandbox.run_solution(sol, [[[3, 1]]]) == [[[3, 1]]]


if __name__ == "__main__":
    test_exception_becomes_none()
    test_bad_source_fails()
    test_missing_p_fails()
    test_timeout_kills()
    test_prints_are_swallowed()
    print("sandbox pass")
