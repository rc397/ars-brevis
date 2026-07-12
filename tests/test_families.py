import json
import os
import random
import sys
import tempfile
from itertools import groupby

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brevis import families, gen, scorer


def check_grid(g):
    assert g and g[0]
    w = len(g[0])
    for r in g:
        assert len(r) == w
        for c in r:
            assert isinstance(c, int) and 0 <= c <= 9
    assert len(g) <= 30 and w <= 30


def test_tasks_are_valid():
    manifest = gen.init_manifest("proptest")
    assert len(manifest["tasks"]) >= 25
    for tid, spec in manifest["tasks"].items():
        task = gen.make_task(random.Random(f"x/{tid}"), spec)
        assert len(task["train"]) >= 3 and len(task["test"]) == 2
        apply = families.FAMILIES[spec["family"]]["apply"]
        for pair in task["train"] + task["test"]:
            check_grid(pair["input"])
            check_grid(pair["output"])
            assert apply(spec["params"], pair["input"]) == pair["output"]


def test_transform_properties():
    rng = random.Random("props")
    for _ in range(100):
        g = families.rand_grid(rng)
        h, w = len(g), len(g[0])

        assert families.mirror_apply({"axis": "h"}, families.mirror_apply({"axis": "h"}, g)) == g
        assert families.mirror_apply({"axis": "v"}, families.mirror_apply({"axis": "v"}, g)) == g
        assert families.rot_apply({"k": 3}, families.rot_apply({"k": 1}, g)) == g
        assert families.transpose_apply({}, families.transpose_apply({}, g)) == g

        s = families.scale_apply({"k": 2}, g)
        assert len(s) == 2 * h and len(s[0]) == 2 * w
        assert all(s[2 * i][2 * j] == g[i][j] for i in range(h) for j in range(w))

        t = families.tile_apply({"ty": 2, "tx": 2}, g)
        assert len(t) == 2 * h and len(t[0]) == 2 * w
        assert all(t[i][j] == g[i % h][j % w] for i in range(2 * h) for j in range(2 * w))

        m = [0] + families.COLORS[1:] + [families.COLORS[0]]
        inv = [0] * 10
        for c in range(1, 10):
            inv[m[c]] = c
        assert families.recolor_apply({"map": inv}, families.recolor_apply({"map": m}, g)) == g

        gd = families.gravity_apply({"d": "down"}, g)
        for j in range(w):
            col = [gd[i][j] for i in range(h)]
            nz = [c for c in col if c]
            assert col == [0] * (h - len(nz)) + nz
            assert sorted(nz) == sorted(c for c in (g[i][j] for i in range(h)) if c)
        gr = families.gravity_apply({"d": "right"}, g)
        for orig, row in zip(g, gr):
            nz = [c for c in row if c]
            assert row == [0] * (w - len(nz)) + nz
            assert nz == [c for c in orig if c]

        b = families.border_apply({"c": 4}, g)
        assert b[0] == [4] * (w + 2) and b[-1] == [4] * (w + 2)
        assert all(r[0] == 4 and r[-1] == 4 for r in b)
        assert [r[1:-1] for r in b[1:-1]] == g

        cyc = families.cycle_apply({"k": 1}, g)
        assert sorted(cyc[0]) == sorted(g[0])
        assert families.cycle_apply({"k": w - 1}, cyc) == g if w > 1 else True

        sr = families.sortrow_apply({"order": "asc"}, g)
        for orig, row in zip(g, sr):
            nz = [c for c in row if c]
            assert nz == sorted(nz)
            assert row[len(nz):] == [0] * (w - len(nz))
            assert sorted(row) == sorted(orig)

        d = families.dedupe_apply({}, g)
        for orig, row in zip(g, d):
            nz = [c for c in row if c]
            assert row == nz + [0] * (w - len(nz))
            assert nz == [k for k, _ in groupby(orig) if k]

        x = g
        for _ in range(9):
            x = families.inc_apply({}, x)
        assert x == g

        pa = families.parity_apply({"a": 1, "b": 2}, g)
        assert all(c in (0, 1, 2) for r in pa for c in r)
        for orig, row in zip(g, pa):
            for oc, c in zip(orig, row):
                assert c == (0 if not oc else 2 if oc % 2 else 1)

        pr = families.prime_apply({"a": 3, "b": 4}, g)
        for orig, row in zip(g, pr):
            for oc, c in zip(orig, row):
                assert c == (0 if not oc else 3 if oc in (2, 3, 5, 7) else 4)

        assert families.modsum_apply({}, g) == [[sum(c for r in g for c in r) % 10]]

        sg = families.sparse_input(rng, {})
        cr = families.crop_apply({}, sg)
        assert any(cr[0]) and any(cr[-1])
        assert any(r[0] for r in cr) and any(r[-1] for r in cr)

        mg = families.mode_input(rng, {})
        mode = families.count_apply({}, mg)[0][0]
        flat = [c for r in mg for c in r if c]
        top = max(flat.count(c) for c in set(flat))
        assert flat.count(mode) == top
        assert sum(1 for c in set(flat) if flat.count(c) == top) == 1


def test_seeds_pin_params_not_pairs():
    manifest = gen.init_manifest("seedtest")
    assert manifest == gen.init_manifest("seedtest")
    for tid, spec in manifest["tasks"].items():
        a = gen.make_task(random.Random(f"s1/{tid}"), spec)
        b = gen.make_task(random.Random(f"s1/{tid}"), spec)
        c = gen.make_task(random.Random(f"s2/{tid}"), spec)
        assert a == b
        assert a != c


def test_hardcode_fails_hidden():
    manifest = gen.init_manifest("guard")
    tid = "mirror-1"
    spec = manifest["tasks"][tid]
    with tempfile.TemporaryDirectory() as d:
        pub = os.path.join(d, "pub")
        hid = os.path.join(d, "hid")
        gen.build({"tasks": {tid: spec}}, "public", pub)
        gen.build({"tasks": {tid: spec}}, "private", hid)
        with open(os.path.join(pub, tid + ".json"), encoding="utf-8") as f:
            task = json.load(f)
        table = {json.dumps(p["input"]): p["output"] for p in task["train"] + task["test"]}
        sol = os.path.join(d, tid + ".py")
        with open(sol, "w", encoding="utf-8", newline="\n") as f:
            f.write("import json\nT=" + repr(table) + "\np=lambda g:T[json.dumps(g)]")
        assert scorer.score_solution(sol, os.path.join(pub, tid + ".json"))["passed"]
        assert not scorer.score_solution(sol, os.path.join(hid, tid + ".json"))["passed"]


if __name__ == "__main__":
    test_tasks_are_valid()
    test_transform_properties()
    test_seeds_pin_params_not_pairs()
    test_hardcode_fails_hidden()
    print("families pass")
