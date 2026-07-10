import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brevis import sampler

BASE = os.path.dirname(os.path.abspath(__file__))
IDENTITY = os.path.join(BASE, "fixtures", "tasks", "identity.json")

STUB_OK = 'print("```python\\np=lambda g:g\\n```")'
STUB_BAD = 'print("no code here at all")'
STUB_ALT = """\
import os
flag = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flag")
if os.path.exists(flag):
    print("p=lambda g:g")
else:
    open(flag, "w").close()
    print("p=lambda g:list(g)")
"""


def write_stub(d, src):
    path = os.path.join(d, "stub.py")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(src)
    return path


def test_extract():
    assert sampler.extract("p=lambda g:g") == "p=lambda g:g"
    assert sampler.extract("```python\np=1\n```") == "p=1"
    assert sampler.extract("```\np=1\n```") == "p=1"
    assert sampler.extract("here\n```py\np=1\n```\nthanks") == "p=1"


def test_prompt_shows_train_only():
    with open(IDENTITY, encoding="utf-8") as f:
        task = json.load(f)
    prompt = sampler.build_prompt(task)
    assert json.dumps(task["train"][0]["input"]) in prompt
    assert json.dumps(task["test"][0]["input"]) not in prompt
    assert "shortest" in prompt


def test_best_of_k_solves():
    with tempfile.TemporaryDirectory() as d:
        stub = write_stub(d, STUB_OK)
        out = os.path.join(d, "win.py")
        result = sampler.best_of_k([sys.executable, stub], IDENTITY, 2, out)
        assert result["solved"] and result["bytes"] == 12 and result["passes"] == 2
        with open(out, "rb") as f:
            assert f.read() == b"p=lambda g:g"


def test_best_of_k_rejects_garbage():
    with tempfile.TemporaryDirectory() as d:
        stub = write_stub(d, STUB_BAD)
        out = os.path.join(d, "win.py")
        result = sampler.best_of_k([sys.executable, stub], IDENTITY, 2, out)
        assert not result["solved"] and result["passes"] == 0
        assert not os.path.exists(out)


def test_string_cmd_spawns_without_shell():
    with tempfile.TemporaryDirectory() as d:
        stub = write_stub(d, STUB_OK)
        out = os.path.join(d, "win.py")
        cmd = f'"{sys.executable}" "{stub}"'
        result = sampler.best_of_k(cmd, IDENTITY, 1, out)
        assert result["solved"] and result["bytes"] == 12


def test_keep_writes_attempts():
    with tempfile.TemporaryDirectory() as d:
        stub = write_stub(d, STUB_OK)
        out = os.path.join(d, "win.py")
        keep = os.path.join(d, "atts")
        result = sampler.best_of_k([sys.executable, stub], IDENTITY, 2, out, keep_dir=keep)
        assert result["solved"]
        assert sorted(os.listdir(keep)) == ["identity-1.txt", "identity-2.txt"]


def test_best_of_k_keeps_shortest():
    with tempfile.TemporaryDirectory() as d:
        stub = write_stub(d, STUB_ALT)
        out = os.path.join(d, "win.py")
        result = sampler.best_of_k([sys.executable, stub], IDENTITY, 2, out)
        assert result["solved"] and result["bytes"] == 12 and result["passes"] == 2


if __name__ == "__main__":
    test_extract()
    test_prompt_shows_train_only()
    test_best_of_k_solves()
    test_best_of_k_rejects_garbage()
    test_string_cmd_spawns_without_shell()
    test_keep_writes_attempts()
    test_best_of_k_keeps_shortest()
    print("sampler pass")
