# Leaderboard

Regenerate with `python scripts/leaderboard.py`. Byte totals compare only within one task set and over the same solved tasks, so rank by solve rate across sets. Model entries note their decode configuration because it changes the result more than the model choice does.

## Generated task set, 31 tasks

| entry | solved | rate | bytes | notes |
| --- | --- | --- | --- | --- |
| examples baseline | 31/31 | 100% | 1755 | hand golfed reference solvers |
| qwen3-4b | 9/31 | 29% | 570 | Ollama, thinking on and hidden, best of 4 |
| qwen3.5-4b | 0/31 | 0% | 0 | Ollama, thinking off, best of 4 |
| qwen2.5-7b | 0/31 | 0% | 0 | Ollama, thinking on and hidden, best of 4 |

## ARC training set, 400 tasks

| entry | solved | rate | bytes | notes |
| --- | --- | --- | --- | --- |
| human par | 400/400 | 100% | 131663 | shortest verified 2025 comp solution per task |

Frontier API models are the main open row and need a key in the environment. Local sampling is closed at these numbers.
