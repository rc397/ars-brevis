# CLAUDE.md

Ars Brevis is a code golf benchmark and model project. For each ARC-AGI task the goal is the shortest Python program that performs the transformation. A solution is one file defining `p`, a function from an input grid to the output grid, and it scores by file size in bytes after passing every train and test pair. The build plan lives in PLAN.md and the running record lives in DEVLOG.md. Append a DEVLOG entry for every working session.

## Hard style rules

These are Ryan's rules and they apply to every kind of output, including docs, commit messages, code and chat. No em-dashes anywhere. No emojis. In prose never use colons or semicolons, not even as list or label markers. Rewrite those into sentences. Avoid if-then constructions and comma splices. Write separate well-formed sentences that each carry one idea. Code must read as human-written, with minimal to no comments and no docstring boilerplate.

## Git

Commit and push as rc397 with user.email rchen7530@gmail.com. The local repo config is already set. Commit messages are short imperative sentences. Never add Co-Authored-By or any other AI trailer.

## Privacy

Nothing in `gold/` is ever committed or published. The public leaderboard reports byte counts only. The `.gitattributes` keeps solution and data files byte-exact because bytes are the metric. Do not weaken it.

## Context

Ryan also runs the ARC Prize 2026 paper project in `D:\ARC_AGI-2,3` and that work has priority. This project is designed to pause cleanly at phase boundaries.
