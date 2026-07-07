# DEVLOG

## 2026-07-07

Scaffolded the repository. The harness lives in `brevis/` with a subprocess sandbox, a byte-count scorer, and an eval entrypoint. A solution is one Python file defining `p(grid)` and scores by file size in bytes. Vendored the 400 public ARC-AGI-1 training tasks from fchollet/ARC-AGI through `scripts/fetch_arc.py` and kept their Apache 2.0 license next to the data. Added an identity fixture task and a 12 byte example solution. The smoke test and the eval CLI both pass end to end. The gold directory is gitignored apart from its README and will hold the private 2025 comp solutions. Next up is importing those for the human par line, then a hidden-test generator so hardcoded outputs cannot pass.

Added CLAUDE.md and PLAN.md so any session rooted in this repo carries the full plan, the style rules and the git identity without depending on another project's memory.
