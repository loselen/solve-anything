# solve-anything

**Agent skills that turn your AI assistant into a one-on-one problem-solving coach, built on Pólya's *How to Solve It*.**

Tell your agent *"I want to get better at solving X"*. Instead of solving problems for you, it acts like a good coach:

1. **Finds out which problems you actually want to solve.** Problem-solving skill is domain-specific, so "get better at problem solving" becomes a concrete class of problems, such as "counting problems in under 20 minutes". If the goal is too far away, it scopes it down to a first milestone.
2. **Checks where you are now.** You solve a few problems out loud. It watches where you get stuck in Pólya's four phases (understand, plan, carry out, look back), and whether the cause is missing knowledge, a missing strategy, sticking with a dead approach, or a belief like "if I don't see it fast I can't do it".
3. **Makes problems at the edge of your ability.** One at a time, with fresh details and without announcing the method. When you're stuck it asks Pólya's questions ("What is the unknown?", "Have you seen a related problem?", "Could you solve a simpler version?") instead of giving the answer. Every problem ends with a look-back: check it, find another route, name the key idea. The difficulty goes up or down based on how you do.

It all happens in normal chat. Your progress is saved in a small local SQLite database, so you can pick up later.

> **Status: 0.1.0, the first release.** Expect rough edges and fixes in upcoming versions. Feedback and issues are welcome.

## The skills

| Skill | What it does | Built on |
| --- | --- | --- |
| `clarify-me` | Turns "I want to get better at X" into one observable, reachable problem-solving goal; lowers it if it's too far | Backward design, goal-setting theory, proximal subgoals, domain-specificity of expertise |
| `check-me` | Diagnoses current ability by watching the learner solve a short adaptive set of problems | Pólya's four phases, Schoenfeld's resources/heuristics/control/beliefs, think-aloud protocols, adaptive testing |
| `make-problem` | Makes problems at the edge of ability, coaches with Pólya's questions as a hint ladder, records attempts, adjusts difficulty until the goal is reached | Pólya, Schoenfeld, deliberate practice, interleaving, hint ladders, expertise reversal |

Each `SKILL.md` lists the research it follows.

## Requirements

- An AI coding agent that supports [Agent Skills](https://agentskills.io), such as Claude Code, Codex or Cursor.
- `python3` with SQLite 3.37 or newer. Check with `python3 -c "import sqlite3; print(sqlite3.sqlite_version)"`. The database script uses only the Python standard library, so nothing else needs installing.

## Install

### 1. Add the skills

With the [`skills`](https://github.com/vercel-labs/skills) tool, from the project folder where you want to practise:

```bash
npx skills add loselen/solve-anything
```

Pick your agent when asked, or pass it directly, e.g. `npx skills add loselen/solve-anything -a claude-code`. Add `-g` to install for your user instead of one project. Install all three skills; they hand off to each other.

### 2. Add the flow to your agent instructions

The skills tool installs skills only, so you need to tell your agent when to use them. Paste this into your project's agent instruction file: `AGENTS.md` for most agents, `CLAUDE.md` for Claude Code.

```markdown
# Problem-solving flow

When the user says they want to get better at solving problems ("I want to get better at X problems", "help me solve X", "coach me on X"), act as their one-on-one problem-solving coach in a normal conversation and follow these steps in order. Use each skill by name.

1. **clarify-me**: find which class of problems they really want to solve and confirm one reachable goal. If the goal is too far, lower it to a first milestone.
2. **check-me**: diagnose their current level against that goal by having them solve problems.
3. **make-problem**: save the goal, then make problems one at a time at the edge of their ability, coach them through Pólya's four phases without giving answers, record every attempt, and adjust the level until the goal is reached.

Hand off between steps in the conversation without announcing skill names to the learner.

If the user comes back to keep practising, use **make-problem** to find their saved goal and continue where they left off.
```

### 3. Start practising

Open your agent in that folder and say:

```
I want to get better at solving X
```

## Where your progress is saved

Everything is stored in `.solve/solve.db`, a SQLite file in the folder where you run the agent. Add `.solve/` to your `.gitignore` if you don't want it committed.

What's saved:

- **goals**: your goal, where you started, your current level, and the date it was reached
- **problems**: each problem made for you, its level, what it trains, and a solution sketch
- **attempts**: your answer, the verdict, how many hints you needed, the phase where you got stuck, the type of mistake, and the key idea

The skill reads and writes the database through a bundled script, `scripts/db.py`. You can run it yourself too, e.g. `python3 .claude/skills/make-problem/scripts/db.py status` to list your goals. The exact path depends on your agent.

## Repository layout

```
skills/
  clarify-me/SKILL.md
  check-me/SKILL.md
  make-problem/SKILL.md   scripts/db.py
```

## License

[MIT](LICENSE)
