# Ars Brevis

y long when short?

In 1308 Ramon Llull published Ars Brevis, the golfed edition of his own Ars Magna. This benchmark is in the same spirit. For each ARC-AGI task, write the shortest Python program that performs the transformation.

## How it works

A solution is a single Python file that defines a function `p` mapping an input grid, a list of lists of ints, to the output grid. A solution passes a task when `p` reproduces every train and test pair exactly. The score of a passing solution is the byte count of the file. Lower is better.

Solutions run in an isolated subprocess with a per-task timeout. The subprocess runs Python in isolated mode, so the standard library is the whole toolbox. The harness is not a security boundary, so run untrusted submissions in a container. SUBMITTING.md walks through the format and the local checks.

## Quickstart

```
python scripts/fetch_arc.py
python scripts/gen_tasks.py
python -m brevis.eval --tasks data/arc/training --solutions examples/solutions
python -m brevis examples/solutions/identity.py --task tests/fixtures/tasks/identity.json
```

The first command vendors the 400 public ARC-AGI-1 training tasks into `data/arc/training`. The second renders the generated tasks from the public seed. The third scores the example solutions against the training tasks. The fourth scores a single file. The task flag is optional when the filename matches a task id under the data directories.

## Layout

| Path | Contents |
| --- | --- |
| `brevis/` | the harness, with sandbox, scorer, eval, cli and task generators |
| `data/arc/` | ARC-AGI tasks, Apache 2.0, pulled from fchollet/ARC-AGI |
| `data/generated/` | original task families, CC BY 4.0 |
| `examples/solutions/` | sample solutions |
| `gold/` | private reference solutions, never committed |

## Generated tasks

The families in `brevis/families.py` produce original tasks in the ARC format, covering grid ops, row ops and a little number theory. `scripts/gen_tasks.py` samples each family's parameters once into `data/generated/manifest.json` and then renders one JSON file per task from a seed. A leaderboard run renders the same manifest with a private seed. The transformation behind each task id stays fixed while the pairs change, so a solution that hardcodes the public outputs fails the hidden ones.

## Model evaluation

`scripts/eval_model.py` drives any model behind a shell command that reads a prompt on stdin and prints one completion. It samples each task k times, keeps the shortest passing program and writes the winners plus `results.json` under a run directory. Runs stream `results.jsonl` as they go and `--resume` skips finished tasks after an interruption. `scripts/claude_cmd.py` is the reference wrapper for the Claude API and needs the `anthropic` package plus credentials in the environment. A llama.cpp invocation slots into the same interface. `scripts/leaderboard.py` renders every `runs/*/results.json` as a markdown table.

## Roadmap

1. Harness and the human par line
2. Frontier and open model evaluation with a public leaderboard
3. Brevis-4B, a fine-tuned golfer
4. A `brevis file.py` CLI

## Licensing

The code is MIT. ARC task data keeps its upstream Apache 2.0 license. Generated task data is CC BY 4.0. Model weights will ship under Apache 2.0.
