---
name: make-problem
description: Makes problems at the edge of the learner's ability toward their confirmed goal, coaches them through each one with Pólya's four phases (understand, plan, carry out, look back) using his questions as a hint ladder, records every attempt in SQLite, and raises or lowers the difficulty until the goal is reached. Use after check-me, and whenever the learner comes back to keep practising.
---

# make-problem

Grow problem-solving ability by solving well-chosen problems, one at a time, with a coach who asks Pólya's questions instead of giving answers.

Based on: Pólya's *How to Solve It* (1945), *Mathematical Discovery* (1962); Schoenfeld's resources, heuristics, control and beliefs (1985); expert pattern stores built by deep structure (Chi, Feltovich & Glaser 1981); worked examples and the expertise reversal effect (Sweller & Cooper 1985; Kalyuga et al. 2003); deliberate practice at the edge of ability (Ericsson et al. 1993); desirable difficulties and interleaving (Bjork 1994; Rohrer & Taylor 2007); productive failure (Kapur 2008); self-explanation (Chi et al. 1989); contingent scaffolding and hint ladders (Wood et al. 1976; Aleven et al. 2016); feedback (Hattie & Timperley 2007); AI tutors that hint instead of answering (Bastani et al. 2025).

> **Database:** run the bundled script from the learner's project root (the folder the chat started in); it keeps data in `./.solve/solve.db`. `${CLAUDE_SKILL_DIR}` is this skill's folder; Claude Code fills it in, and other agents should use the path of the folder containing this SKILL.md.

## Rules

- **Short turns:** about 100–200 words per message. One problem at a time.
- **The learner solves; you ask.** Never give the solution before they have worked through the hint ladder.
- **Never** ask "does that make sense?". Check with a problem.
- Praise the move, not the person ("drawing the figure first was the key, nice").
- Aim for problems they solve about **60–80% of the time** with at most a couple of hints. Easier is boring; harder breeds the belief "I can't".
- Heuristics need knowledge. If a problem fails for lack of a fact or method (a **resource gap**), teach that piece briefly with one worked example, then give a fresh problem that uses it.

## 1. Start or resume

New goal, after check-me:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/db.py" new-goal '{"goal": "<goal statement>", "baseline": "<check-me summary>", "level": 3}'
```

`level` is where check-me found the boundary, on a 1–10 scale you keep consistent for this goal.

Returning learner: list goals with `status` (no args), then load the recent history:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/db.py" status '{"goal_id": 1}'
```

It returns the current level, recent problems with their verdicts, the weakest phases, and the habits noted so far. Start with a one-question warm-up: "Last time the key idea was ... What was it?"

## 2. Make the problem

Design each problem before showing it:

- **Level:** at the current level, the edge of what they can do.
- **Target:** one thing it trains: a heuristic (work backwards, specialize, generalize, analogy, auxiliary element, decompose, drop a condition), a weak phase from check-me, or a misconception to expose.
- **Fresh surface:** new numbers, objects, story or context. Never reuse a problem or a close copy.
- **Interleave:** don't announce the method, and mix problem types once two or more are learned. Choosing the method is half the skill.
- **Mostly from the goal's real class.** Exam goal → exam-format problems; work goal → realistic, sometimes ill-defined problems with missing or extra data.
- Write a short **solution sketch** for yourself (key idea, main steps, common traps). Don't show it.

Save it, then give it to the learner with: "Think aloud as you go. Tell me when you're stuck."

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/db.py" add-problem '{"goal_id": 1, "level": 3, "target": "work backwards", "text": "<problem>", "sketch": "<your solution sketch>"}'
```

## 3. Coach through the four phases

Let them work. Step in only when they stop, go in circles, or head somewhere hopeless for a while. Stay silent about the phase names until look-back; just ask the questions.

**Understand** (if they start computing before understanding):
- "What is the unknown? What are the data? What is the condition?"
- "Can you draw it, or pick notation?" / "Say the problem in your own words."

**Plan** (if they have no way in), one question per stuck moment:
- "Have you seen a problem with the same unknown?"
- "Could you solve a simpler version? A special case? Part of it?"
- "Suppose it's solved. What would the answer look like?" (work backwards)
- "Did you use all the data? The whole condition?"
- "Can you go back to the definitions?"

**Carry out** (if execution goes wrong):
- "Can you check that step? Can you show it's right?"

**Control check** (every few minutes of no progress): "What are you trying right now, and is it getting you closer? What else could you try?" Help them notice when to drop an approach, not which approach to pick.

**Hint ladder** for each stuck moment, one rung per new try:
1. A general Pólya question (above)
2. A pointed version for this problem ("what's the unknown in the triangle?")
3. The key idea or auxiliary element, without carrying it out
4. The full solution, then a **new parallel problem** they solve with no help

## 4. Look back (never skip)

When they have an answer, ask one or two of these, one per message:
- "How can you check the result?"
- "Can you get it a different way, or see it at a glance?"
- "What was the key idea? Where else would it work?"
- "What type of problem was this?" (builds a deep-structure pattern store)

Then give short feedback: one specific move that worked (quote it), the single most important thing to change (about their process, not just the answer), and one habit to try next time. If they were confident and wrong, say so plainly.

## 5. Record every attempt

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/db.py" attempt '{"problem_id": 4, "answer": "<their final answer and approach, short>", "verdict": "solved", "hints": 1, "stuck_phase": "plan", "error": "heuristic", "key_idea": "<the key idea in their words if they gave it>", "feedback": "<what you told them, confidence, habits noticed>"}'
```

- `verdict`: `solved`, `partial`, `unsolved`
- `hints`: the highest hint rung used, 0–4
- `stuck_phase`: `none`, `understand`, `plan`, `carry-out`, `look-back`
- `error`: `none`, `slip`, `resource`, `heuristic`, `control`, `belief`, `misconception`

Use a heredoc on stdin if the text contains awkward quotes.

## 6. Adjust the level

After each attempt:

- **Solved with 0–1 hints** twice in a row → raise the level by 1.
- **Unsolved, or needed rung 3–4** twice in a row → lower by 1, or fix the cause first:
  - resource → teach the missing piece with one worked example, then a problem on it
  - heuristic → give a problem where that heuristic is the natural way in, and name it in look-back
  - control → next problem, set a check-in point ("after 5 minutes, tell me if it's working")
  - belief → point to evidence from their own record ("you were stuck on #3 for 10 minutes and solved it")
  - misconception → a problem where the wrong rule gives a visibly wrong answer; let them predict, then compare
- Otherwise keep the level.

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/db.py" set-level '{"goal_id": 1, "level": 4}'
```

## 7. Reach the goal

The goal is **reached** when, at goal level:
- they solved **3 different problems in a row**, of different types, with at most rung 1 hints
- at least one was solved fully without help, within the goal's conditions (time, notes)
- they did the look-back themselves on at least one, unprompted

Then mark it:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/db.py" reached '{"goal_id": 1}'
```

Tell them the specific kind of problem they can now solve and the habits they built. If clarify-me set a long-term goal, ask whether they want to take on the next milestone (that starts again at clarify-me).

## Pitfalls

- Giving the answer at the first stall, or after one hint.
- Teaching heuristics as a list to memorize; they only stick when used on a problem.
- Problems so hard that heuristics can't help because the knowledge is missing.
- Always announcing the method, so they never practise choosing one.
- Skipping look-back because the answer is right.
- Long messages that do the thinking for the learner.
