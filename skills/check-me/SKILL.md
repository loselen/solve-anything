---
name: check-me
description: Diagnoses a learner's current problem-solving ability toward a confirmed goal by having them solve a short adaptive set of problems, watching where in Pólya's four phases they get stuck, and summarizing their level, resources, heuristics, control and beliefs. Use after clarify-me and before make-problem.
---

# check-me

Find where the learner actually is, fast, by watching them solve problems, not by asking what they know.

Based on: prior knowledge as the strongest predictor of learning (Ausubel 1968), unreliability of self-assessment (Sitzmann et al. 2010; Kruger & Dunning 1999), adaptive testing (Wainer 2000), Pólya's four phases (1945), Schoenfeld's resources, heuristics, control and beliefs (1985), expert vs. novice problem categorization by deep structure (Chi, Feltovich & Glaser 1981), think-aloud protocols (Ericsson & Simon 1993), certainty-based marking and the hypercorrection effect (Gardner-Medwin 2006; Butterfield & Metcalfe 2001), the pretesting effect (Richland et al. 2009).

## Rules

- Frame it as "let's find where to start", never as an exam.
- **One question per message.** Wait for the answer.
- Use **real problems** from the goal's class, plus short probes. Never recognition questions ("have you heard of X?").
- Self-report only picks the starting point. It is never evidence.
- **Don't teach during the check.** If they get something wrong, note it and move on. A short "no worries, that tells me where to start" is enough.
- Ask them to **think aloud**: "Write your thoughts as you go, even half-ideas and dead ends." The process matters more than the answer here.
- Stop after **4–8 problems or probes** at most. Problems are longer than quiz questions; respect their energy.

## Procedure

1. **Background.** Ask for one or two lines: what have they studied or done that relates to the goal, and how do they usually go about a problem they can't immediately solve?

2. **Build a ladder (in your head, not shown).** List 5–7 levels of problems in the goal's class, from routine (one known method applies directly) to the goal level (needs choosing between methods, an auxiliary element, or a reformulation).

3. **Start in the middle** of the ladder (lower if the background is thin). Give one problem at that level. Ask them to think aloud.

4. **Ask confidence** right after their answer: "How sure are you: 1 guess, 2 fairly sure, 3 certain?"

5. **Observe the four phases** in what they write:
   - **Understand:** did they identify the unknown, the data, the condition? Restate it? Draw or set notation?
   - **Plan:** did they connect it to a related problem or method? Or start computing blindly?
   - **Carry out:** did they execute correctly and check steps?
   - **Look back:** did they check the result or stop at the first answer?

6. **Probe once if stuck**, without teaching: "What is the unknown here?" or "Have you seen a problem like this before?" If a single Pólya question unlocks them, they have the **resources** but lack the **heuristic** or **control**. If it doesn't, it's a **resource gap** (missing domain knowledge).

7. **One sorting probe** (optional, quick): show 3–4 short problem statements and ask "which two would you solve the same way, and why?" Grouping by surface features (same objects, same words) instead of deep structure (same method) signals a novice pattern store.

8. **Branch:**
   - solved, confident, with a sound plan → jump up about half the remaining distance
   - wrong, unsure, or solved by luck → go down a level
   - a level counts as **solid** after 2 solved problems, or 1 solved with a clearly reasoned plan

9. **Classify what went wrong:**
   - **slip:** right plan, careless execution
   - **resource gap:** missing fact, definition or method
   - **heuristic gap:** had the knowledge, didn't know how to find a way in
   - **control problem:** stuck to one dead approach too long, or jumped between approaches without checking
   - **belief:** "if I don't see it in 2 minutes I can't do it", "there's one trick", giving up fast
   - **misconception:** a consistent wrong rule, often said with confidence

10. **Stop** when you find the boundary: the highest level that is solid and the next one that fails.

11. **Summarize to the learner** in a short, encouraging message:
    - **Level:** solid up to ..., not yet at ...
    - **Strong phases:** ... / **Weak phases:** ... (e.g. "you plan well but rarely look back")
    - **Knowledge to fill:** ...
    - **Habits to build:** ... (heuristics, control, beliefs)
    - **Misconceptions to fix:** ... (flag confident wrong answers first)

## Output

Keep the summary. It becomes the `baseline` for make-problem. Do not write to the database here.

## Pitfalls

- Trusting "I'm good at this kind of problem".
- Judging only the final answer and ignoring the process.
- Teaching or hinting more than one probe question during the check.
- Mistaking a resource gap for a heuristic gap (no strategy helps without the knowledge).
- Testing so long the learner is tired before practice starts.
