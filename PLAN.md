# PLAN

## Phase 0, decisions and raw materials

- [x] Create the repo and the MIT license under Ryan Chen
- [x] Fix the scoring rules. One Python file per task defining `p`, exact match on all pairs, score is file bytes.
- [x] Vendor the 400 ARC-AGI-1 training tasks from fchollet/ARC-AGI with their Apache 2.0 license
- [x] Import the 2025 comp solution archive into `gold/`
- [ ] Claim PyPI `brevis`, a HuggingFace org and arsbrevis.dev

## Phase 1, harness and the human par line

- [x] Sandbox runner with a timeout and print capture
- [x] Byte scorer over train and test pairs
- [x] Eval CLI with a fixture smoke test, identity at 12 bytes
- [x] Generated task families with property-based tests, covering string ops, grid ops and number theory
- [x] Hidden-test guard so hardcoded outputs cannot pass
- [x] Human par run over the gold solutions

The phase is done when the harness scores an arbitrary solutions directory reproducibly and the par line is recorded.

## Phase 2, eval the field

- [ ] Fixed prompt template and best-of-k sampling for the API models, GPT, Claude and Gemini
- [x] Local models through llama.cpp, Qwen3-4B first
- [ ] Pre-flight the API spend with calcis
- [ ] Collect solve rate, mean bytes against par and a per-task table
- [ ] Failure analysis covering byte-blindness and the verbosity prior
- [ ] Writeup 1 and the public leaderboard page

The phase is done when the leaderboard is live with the human par and five or six models.

## Phase 3, train the golfer

- [x] Long-to-short pairs distilled from Ryan's own golf transforms
- [ ] Expert iteration. Sample hot via llama.cpp, verify in the sandbox, keep the shortest passing, LoRA SFT on the winners, repeat.
- [x] Benchmark decode speed before any long sampling run
- [ ] Run two to four rounds tracking solve rate and mean bytes per round
- [ ] Reward-hacking audit by reading the shortest solutions and checking hidden-test pass rates
- [ ] Ablation notes as work proceeds, base against long-to-short against expert iteration
- [ ] GRPO only if expert iteration plateaus

The phase is done when Brevis-4B beats every open model on the leaderboard.

## Phase 4, ship

- [ ] The model on HuggingFace with a full model card, Apache 2.0
- [ ] Public submission instructions so others can enter the leaderboard
- [x] The `brevis file.py` CLI
- [ ] Writeup 2
- [ ] Cross-post and claim the project on the personal site under Ryan's name

The phase is done when a stranger submits a leaderboard entry or files an issue.
