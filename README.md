# Ars Brevis

y long when short?

In 1308 Ramon Llull published Ars Brevis, the golfed edition of his own Ars Magna. This benchmark is in the same spirit. For each ARC-AGI task, write the shortest Python program that performs the transformation.

## How it works

A solution is a single Python file that defines a function `p` mapping an input grid, a list of lists of ints, to the output grid. A solution passes a task when `p` reproduces every train and test pair exactly. The score of a passing solution is the byte count of the file. Lower is better.

Solutions run in an isolated subprocess with a per-task timeout. The harness is not a security boundary, so run untrusted submissions in a container.

## Quickstart

```
python scripts/fetch_arc.py
python -m brevis.eval --tasks tests/fixtures/tasks --solutions examples/solutions
```

The first command vendors the 400 public ARC-AGI-1 training tasks into `data/arc/training`. The second runs the fixture smoke test end to end.

## Layout

| Path | Contents |
| --- | --- |
| `brevis/` | the harness, with sandbox, scorer, eval and cli |
| `data/arc/` | ARC-AGI tasks, Apache 2.0, pulled from fchollet/ARC-AGI |
| `data/generated/` | original task families, CC BY 4.0 |
| `examples/solutions/` | sample solutions |
| `gold/` | private reference solutions, never committed |

## Roadmap

1. Harness and the human par line
2. Frontier and open model evaluation with a public leaderboard
3. Brevis-4B, a fine-tuned golfer
4. A `brevis file.py` CLI

## Licensing

The code is MIT. ARC task data keeps its upstream Apache 2.0 license. Generated task data is CC BY 4.0. Model weights will ship under Apache 2.0.
