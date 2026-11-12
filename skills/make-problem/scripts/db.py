#!/usr/bin/env python3
"""solve-anything SQLite helper. Stdlib only. All output is JSON.

Usage (run from the learner's project root; the database is created at ./.solve/solve.db):
  python3 scripts/db.py new-goal    '{"goal": "...", "baseline": "...", "level": 3}'
  python3 scripts/db.py add-problem '{"goal_id": 1, "level": 3, "target": "...", "text": "...", "sketch": "..."}'
  python3 scripts/db.py attempt     '{"problem_id": 4, "answer": "...", "verdict": "solved|partial|unsolved",
                                     "hints": 0, "stuck_phase": "none|understand|plan|carry-out|look-back",
                                     "error": "none|slip|resource|heuristic|control|belief|misconception",
                                     "key_idea": "...", "feedback": "..."}'
  python3 scripts/db.py set-level   '{"goal_id": 1, "level": 4}'
  python3 scripts/db.py reached     '{"goal_id": 1}'
  python3 scripts/db.py status      '{"goal_id": 1, "recent": 10}'   (omit goal_id to list all goals)

The JSON argument may also be piped on stdin instead of passed as an argument.
"""
import json
import os
import sqlite3
import sys
import time
from contextlib import closing

DB_PATH = os.environ.get("SOLVE_DB", os.path.join(os.getcwd(), ".solve", "solve.db"))
SCHEMA_VERSION = 1

SCHEMA = """
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS goals (
  id         INTEGER PRIMARY KEY,
  goal       TEXT NOT NULL,
  baseline   TEXT NOT NULL,
  level      INTEGER NOT NULL DEFAULT 1,
  created_at INTEGER NOT NULL,
  reached_at INTEGER
) STRICT;

CREATE TABLE IF NOT EXISTS problems (
  id         INTEGER PRIMARY KEY,
  goal_id    INTEGER NOT NULL REFERENCES goals(id) ON DELETE CASCADE,
  level      INTEGER NOT NULL,
  target     TEXT NOT NULL DEFAULT '',
  text       TEXT NOT NULL,
  sketch     TEXT NOT NULL DEFAULT '',
  created_at INTEGER NOT NULL
) STRICT;
CREATE INDEX IF NOT EXISTS problems_goal ON problems(goal_id);

CREATE TABLE IF NOT EXISTS attempts (
  id          INTEGER PRIMARY KEY,
  problem_id  INTEGER NOT NULL REFERENCES problems(id) ON DELETE CASCADE,
  answer      TEXT NOT NULL,
  verdict     TEXT NOT NULL CHECK (verdict IN ('solved', 'partial', 'unsolved')),
  hints       INTEGER NOT NULL DEFAULT 0 CHECK (hints BETWEEN 0 AND 4),
  stuck_phase TEXT NOT NULL DEFAULT 'none'
              CHECK (stuck_phase IN ('none', 'understand', 'plan', 'carry-out', 'look-back')),
  error       TEXT NOT NULL DEFAULT 'none'
              CHECK (error IN ('none', 'slip', 'resource', 'heuristic', 'control', 'belief', 'misconception')),
  key_idea    TEXT NOT NULL DEFAULT '',
  feedback    TEXT NOT NULL DEFAULT '',
  created_at  INTEGER NOT NULL
) STRICT;
CREATE INDEX IF NOT EXISTS attempts_problem ON attempts(problem_id);
"""


def connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con = sqlite3.connect(DB_PATH, timeout=5.0, isolation_level=None)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA synchronous = NORMAL")
    con.execute("PRAGMA foreign_keys = ON")
    con.execute("PRAGMA temp_store = MEMORY")
    if con.execute("PRAGMA user_version").fetchone()[0] < SCHEMA_VERSION:
        con.executescript(SCHEMA + f"PRAGMA user_version = {SCHEMA_VERSION};")
    return con


class tx:
    """BEGIN IMMEDIATE ... COMMIT / ROLLBACK."""

    def __init__(self, con):
        self.con = con

    def __enter__(self):
        self.con.execute("BEGIN IMMEDIATE")
        return self.con

    def __exit__(self, exc_type, *_):
        self.con.execute("ROLLBACK" if exc_type else "COMMIT")
        return False


def need(args, *keys):
    missing = [k for k in keys if args.get(k) in (None, "")]
    if missing:
        raise ValueError(f"missing field(s): {', '.join(missing)}")


def iso(ts):
    return None if ts is None else time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


def goal_exists(con, goal_id):
    if not con.execute("SELECT 1 FROM goals WHERE id = ?", (goal_id,)).fetchone():
        raise ValueError(f"goal {goal_id} not found")


def cmd_new_goal(con, a):
    need(a, "goal", "baseline")
    with tx(con):
        cur = con.execute(
            "INSERT INTO goals (goal, baseline, level, created_at) VALUES (?, ?, ?, ?)",
            (a["goal"], a["baseline"], int(a.get("level", 1)), int(time.time())),
        )
    return {"goal_id": cur.lastrowid}


def cmd_add_problem(con, a):
    need(a, "goal_id", "text")
    with tx(con):
        row = con.execute("SELECT level FROM goals WHERE id = ?", (a["goal_id"],)).fetchone()
        if not row:
            raise ValueError(f"goal {a['goal_id']} not found")
        cur = con.execute(
            "INSERT INTO problems (goal_id, level, target, text, sketch, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (a["goal_id"], int(a.get("level", row["level"])), a.get("target", ""), a["text"],
             a.get("sketch", ""), int(time.time())),
        )
    return {"problem_id": cur.lastrowid}


def cmd_attempt(con, a):
    need(a, "problem_id", "answer", "verdict")
    with tx(con):
        if not con.execute("SELECT 1 FROM problems WHERE id = ?", (a["problem_id"],)).fetchone():
            raise ValueError(f"problem {a['problem_id']} not found")
        cur = con.execute(
            """INSERT INTO attempts (problem_id, answer, verdict, hints, stuck_phase, error, key_idea, feedback, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (a["problem_id"], a["answer"], a["verdict"], int(a.get("hints", 0)), a.get("stuck_phase", "none"),
             a.get("error", "none"), a.get("key_idea", ""), a.get("feedback", ""), int(time.time())),
        )
    return {"attempt_id": cur.lastrowid}


def cmd_set_level(con, a):
    need(a, "goal_id", "level")
    with tx(con):
        goal_exists(con, a["goal_id"])
        con.execute("UPDATE goals SET level = ? WHERE id = ?", (int(a["level"]), a["goal_id"]))
    return {"goal_id": a["goal_id"], "level": int(a["level"])}


def cmd_reached(con, a):
    need(a, "goal_id")
    with tx(con):
        goal_exists(con, a["goal_id"])
        con.execute(
            "UPDATE goals SET reached_at = ? WHERE id = ? AND reached_at IS NULL", (int(time.time()), a["goal_id"])
        )
    return {"goal_id": a["goal_id"], "reached": True}


def cmd_status(con, a):
    if not a.get("goal_id"):
        return {"goals": [
            {**dict(r), "reached_at": iso(r["reached_at"])}
            for r in con.execute("SELECT id, goal, level, reached_at FROM goals ORDER BY id")
        ]}
    g = con.execute("SELECT * FROM goals WHERE id = ?", (a["goal_id"],)).fetchone()
    if not g:
        raise ValueError(f"goal {a['goal_id']} not found")
    recent = []
    for r in con.execute(
        """SELECT p.id AS problem_id, p.level, p.target, p.text, a.verdict, a.hints, a.stuck_phase, a.error,
                  a.key_idea, a.feedback, a.created_at
           FROM attempts a JOIN problems p ON p.id = a.problem_id
           WHERE p.goal_id = ? ORDER BY a.id DESC LIMIT ?""",
        (a["goal_id"], int(a.get("recent", 10))),
    ):
        d = dict(r)
        d["created_at"] = iso(d["created_at"])
        recent.append(d)

    def counts(col):
        return {
            r[0]: r[1]
            for r in con.execute(
                f"""SELECT a.{col}, COUNT(*) FROM attempts a JOIN problems p ON p.id = a.problem_id
                    WHERE p.goal_id = ? AND a.{col} != 'none' GROUP BY a.{col} ORDER BY COUNT(*) DESC""",
                (a["goal_id"],),
            )
        }

    unattempted = [
        dict(r) for r in con.execute(
            """SELECT id AS problem_id, level, target, text FROM problems p
               WHERE goal_id = ? AND NOT EXISTS (SELECT 1 FROM attempts a WHERE a.problem_id = p.id)
               ORDER BY id""",
            (a["goal_id"],),
        )
    ]
    return {
        "goal_id": g["id"], "goal": g["goal"], "baseline": g["baseline"], "level": g["level"],
        "created_at": iso(g["created_at"]), "reached_at": iso(g["reached_at"]),
        "problems": con.execute("SELECT COUNT(*) FROM problems WHERE goal_id = ?", (a["goal_id"],)).fetchone()[0],
        "stuck_phases": counts("stuck_phase"), "errors": counts("error"),
        "unattempted": unattempted, "recent_attempts": recent,
    }


COMMANDS = {
    "new-goal": cmd_new_goal,
    "add-problem": cmd_add_problem,
    "attempt": cmd_attempt,
    "set-level": cmd_set_level,
    "reached": cmd_reached,
    "status": cmd_status,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(2)
    raw = sys.argv[2] if len(sys.argv) > 2 else (sys.stdin.read() if not sys.stdin.isatty() else "")
    try:
        args = json.loads(raw) if raw.strip() else {}
        with closing(connect()) as con:
            out = COMMANDS[sys.argv[1]](con, args)
            con.execute("PRAGMA optimize")
        print(json.dumps(out, ensure_ascii=False))
    except (ValueError, sqlite3.Error, json.JSONDecodeError) as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
