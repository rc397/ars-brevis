# Submitting

A submission is a directory of Python files with one file per task. Each file is named `<task_id>.py` and defines a function `p` that maps the input grid to the output grid. Grids are lists of lists of ints. A file passes its task when `p` reproduces every train and test pair exactly. The score of a passing file is its size in bytes and lower is better. Unattempted tasks score nothing.

## Check your solutions locally

```
python -m brevis eval --tasks data/arc/training --solutions path/to/yours
python -m brevis eval --tasks data/generated/tasks --solutions path/to/yours
python -m brevis path/to/yours/007bbfb7.py
```

## Rules

Solutions run in an isolated subprocess with a five second timeout per task. The standard library is the whole toolbox. The file is executed once and `p` is called once per pair inside the same process. Output must equal the expected grid after a JSON round trip. Generated tasks are rendered again from a private seed for leaderboard runs, so hardcoded outputs fail there. The leaderboard publishes byte counts only and never publishes solution files.

## Entering the leaderboard

The public leaderboard is not live yet. Watch the repository for the submission address once it ships.
