import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brevis import scorer


def test_identity():
    base = os.path.dirname(os.path.abspath(__file__))
    result = scorer.score_solution(
        os.path.join(base, "..", "examples", "solutions", "identity.py"),
        os.path.join(base, "fixtures", "tasks", "identity.json"),
    )
    assert result["passed"], result
    print(f"identity pass, {result['bytes']} bytes")


if __name__ == "__main__":
    test_identity()
