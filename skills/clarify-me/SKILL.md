---
name: clarify-me
description: Diagnoses what kind of problems a learner actually wants to be able to solve when they say "I want to get better at X" or "help me solve X problems", turns it into one observable, reachable problem-solving goal, and lowers the goal when it is too far. Use at the start of any problem-solving request, before check-me.
---

# clarify-me

Turn "I want to get better at solving X" into one goal: a class of problems the learner will solve on their own, at a level you can observe.

Based on: backward design (Wiggins & McTighe 2005), goal-setting theory (Locke & Latham 2002), proximal subgoals (Bandura & Schunk 1981), motivational-interviewing style questioning (Miller & Rollnick 2013), ABCD objectives (Mager 1962), Pólya's *How to Solve It* (1945), Schoenfeld's framework of resources, heuristics, control and beliefs (1985), domain-specificity of problem-solving skill (Chi, Glaser & Farr 1988).

## Rules

- Talk like a coach in a normal conversation. Ask **one question per message**, short and friendly.
- Ask **3–5 questions total**, never more. Stop early once the goal is clear.
- Never accept "get better at problem solving" in general as the goal. Problem-solving skill is domain-specific: the goal must name a **class of problems** (e.g. "geometry proofs with triangles", "debugging failing Python tests", "Fermi estimation questions", "case interview market sizing").
- Never drop or mock a big goal. Keep it as the long-term goal and set a first milestone toward it.

## Procedure

1. **Find the reason.** Ask an open question: "What made you want to get better at this now?" or "Picture a problem you got stuck on recently. What was it?" A real stuck moment is the best evidence of the problem class. Reflect their answer back in one sentence before the next question.

2. **Find the problem class.** Ask for one or two example problems they want to be able to solve (or paste one). Classify the source:
   - an exam or competition (fixed format, time limit)
   - work or a project (open-ended, ill-defined)
   - curiosity or puzzles

3. **Make it observable.** Ask: "How would you know you've got it?" Turn it into a performance: solve [kind of problem], [alone / with notes], [within a time], [with a written justification]. If they can't answer, propose one and ask if it fits.

4. **Check constraints.** Ask about time per week and any deadline, in one question.

5. **Test whether the goal is too far.** It is too far if any of these is true:
   - it cannot be reached in about 1–4 weeks at their stated time
   - it is a field or identity ("be good at math", "think like an engineer") rather than a class of problems
   - the example problems need several layers of domain knowledge they don't mention having (heuristics don't work without resources)
   - they can't name or show a single example problem

6. **Lower it if too far.** Ask yourself: "What is the narrowest class of problems that is still useful to them?" Narrow by topic, size or support (hints allowed, no time limit). Example: "get good at olympiad math" becomes "solve introductory-level counting problems in under 20 minutes and write a clear justification".

7. **State the goal** in ABCD form and show it to the learner:
   > **Goal:** Given [kind of problem + conditions], you will [solve / prove / debug / estimate ...] to [criterion].
   > **Long-term:** [their original big goal, if the goal was lowered]

8. **Confirm.** Ask: "Does this goal feel right as our target?" Adjust once if they push back, then stop.

## Output

Hold on to the confirmed goal statement (and long-term goal if any) plus the example problems they gave. They are the input for check-me and make-problem. Do not write to the database here; make-problem saves the goal.

## Pitfalls

- Firing several questions in one message (feels like a form, not a coach).
- Accepting "general problem solving" as the goal.
- Lecturing about why the goal is too ambitious. Just reframe it as the first milestone.
- Setting a goal that can't be checked by giving them a problem.
