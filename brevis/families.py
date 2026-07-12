COLORS = list(range(1, 10))


def rand_grid(rng, lo=2, hi=8, density=None):
    h = rng.randint(lo, hi)
    w = rng.randint(lo, hi)
    d = rng.uniform(0.4, 0.9) if density is None else density
    g = [[rng.choice(COLORS) if rng.random() < d else 0 for _ in range(w)] for _ in range(h)]
    if not any(c for r in g for c in r):
        g[rng.randrange(h)][rng.randrange(w)] = rng.choice(COLORS)
    return g


def mirror_apply(params, g):
    if params["axis"] == "h":
        return [r[::-1] for r in g]
    return [list(r) for r in g[::-1]]


def rot_apply(params, g):
    for _ in range(params["k"]):
        g = [list(r) for r in zip(*g[::-1])]
    return g


def transpose_apply(params, g):
    return [list(r) for r in zip(*g)]


def scale_apply(params, g):
    k = params["k"]
    return [[c for c in r for _ in range(k)] for r in g for _ in range(k)]


def tile_apply(params, g):
    return [list(r) * params["tx"] for r in g] * params["ty"]


def recolor_apply(params, g):
    m = params["map"]
    return [[m[c] for c in r] for r in g]


def gravity_apply(params, g):
    if params["d"] == "right":
        out = []
        for r in g:
            nz = [c for c in r if c]
            out.append([0] * (len(r) - len(nz)) + nz)
        return out
    h, w = len(g), len(g[0])
    out = [[0] * w for _ in range(h)]
    for j in range(w):
        col = [g[i][j] for i in range(h) if g[i][j]]
        for i, c in enumerate(col):
            out[h - len(col) + i][j] = c
    return out


def border_apply(params, g):
    c = params["c"]
    w = len(g[0]) + 2
    return [[c] * w] + [[c] + list(r) + [c] for r in g] + [[c] * w]


def crop_apply(params, g):
    rows = [i for i, r in enumerate(g) if any(r)]
    cols = [j for j in range(len(g[0])) if any(r[j] for r in g)]
    return [r[cols[0]:cols[-1] + 1] for r in g[rows[0]:rows[-1] + 1]]


def count_apply(params, g):
    flat = [c for r in g for c in r if c]
    return [[max(sorted(set(flat)), key=flat.count)]]


def modsum_apply(params, g):
    return [[sum(c for r in g for c in r) % 10]]


def cycle_apply(params, g):
    k = params["k"]
    return [r[-k:] + r[:-k] for r in g]


def sortrow_apply(params, g):
    out = []
    for r in g:
        nz = sorted((c for c in r if c), reverse=params["order"] == "desc")
        out.append(nz + [0] * (len(r) - len(nz)))
    return out


def dedupe_apply(params, g):
    w = len(g[0])
    out = []
    for r in g:
        row = []
        prev = 0
        for c in r:
            if c and c != prev:
                row.append(c)
            prev = c
        out.append(row + [0] * (w - len(row)))
    return out


def inc_apply(params, g):
    return [[c % 9 + 1 if c else 0 for c in r] for r in g]


def parity_apply(params, g):
    a, b = params["a"], params["b"]
    return [[(b if c % 2 else a) if c else 0 for c in r] for r in g]


def prime_apply(params, g):
    a, b = params["a"], params["b"]
    return [[(a if c in (2, 3, 5, 7) else b) if c else 0 for c in r] for r in g]


def default_input(rng, params):
    return rand_grid(rng)


def wide_input(rng, params):
    return rand_grid(rng, 3, 8)


def sparse_input(rng, params):
    while True:
        g = rand_grid(rng, 4, 9, 0.2)
        if crop_apply(params, g) != g:
            return g


def mode_input(rng, params):
    while True:
        g = rand_grid(rng, 3, 8, 0.7)
        flat = [c for r in g for c in r if c]
        counts = sorted(flat.count(c) for c in set(flat))
        if len(counts) == 1 or counts[-1] > counts[-2]:
            return g


def runs_input(rng, params):
    h = rng.randint(3, 7)
    w = rng.randint(5, 9)
    g = []
    for _ in range(h):
        row = []
        while len(row) < w:
            row += [rng.choice([0] + COLORS)] * rng.randint(1, 3)
        g.append(row[:w])
    return g


def color_pairs(rng, n):
    out = []
    while len(out) < n:
        a, b = rng.sample(COLORS, 2)
        if {"a": a, "b": b} not in out:
            out.append({"a": a, "b": b})
    return out


def perms(rng, n):
    out = []
    while len(out) < n:
        m = COLORS[:]
        rng.shuffle(m)
        if [0] + m not in [v["map"] for v in out]:
            out.append({"map": [0] + m})
    return out


FAMILIES = {
    "mirror": {"variants": lambda rng: [{"axis": "h"}, {"axis": "v"}], "apply": mirror_apply},
    "rot": {"variants": lambda rng: [{"k": 1}, {"k": 2}, {"k": 3}], "apply": rot_apply},
    "transpose": {"variants": lambda rng: [{}], "apply": transpose_apply},
    "scale": {"variants": lambda rng: [{"k": 2}, {"k": 3}], "apply": scale_apply},
    "tile": {"variants": lambda rng: [{"ty": 2, "tx": 1}, {"ty": 1, "tx": 2}, {"ty": 2, "tx": 2}], "apply": tile_apply},
    "recolor": {"variants": lambda rng: perms(rng, 3), "apply": recolor_apply},
    "gravity": {"variants": lambda rng: [{"d": "down"}, {"d": "right"}], "apply": gravity_apply},
    "border": {"variants": lambda rng: [{"c": c} for c in rng.sample(COLORS, 2)], "apply": border_apply},
    "crop": {"variants": lambda rng: [{}], "apply": crop_apply, "input": sparse_input},
    "count": {"variants": lambda rng: [{}], "apply": count_apply, "input": mode_input},
    "modsum": {"variants": lambda rng: [{}], "apply": modsum_apply},
    "cycle": {"variants": lambda rng: [{"k": 1}, {"k": 2}], "apply": cycle_apply, "input": wide_input},
    "sortrow": {"variants": lambda rng: [{"order": "asc"}, {"order": "desc"}], "apply": sortrow_apply},
    "dedupe": {"variants": lambda rng: [{}], "apply": dedupe_apply, "input": runs_input},
    "inc": {"variants": lambda rng: [{}], "apply": inc_apply},
    "parity": {"variants": lambda rng: color_pairs(rng, 2), "apply": parity_apply},
    "prime": {"variants": lambda rng: color_pairs(rng, 2), "apply": prime_apply},
}
