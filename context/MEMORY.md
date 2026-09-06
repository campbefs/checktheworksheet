# Project memory — child-support-reform-public

**This file is project-scoped memory. It loads automatically into every session in this folder**
(imported by `CLAUDE.md`). It is the project's answer to `~/.claude/.../memory/` — same idea, but
scoped here, living in the repo, and travelling with it through git.

**It is not a session log.** Dated files in `context/` are session context, written by
`/save-context` and read by `/load-context`. They are a transcript of *what happened*. This file is
*what remains true afterwards*. When a session ends, durable facts get promoted up into this file;
the dated file stays where it is.

## What belongs here

- Decisions made and **why** — especially ones already settled, so they don't get re-litigated.
- Corrections Chris has made to how Claude works **in this project**.
- Conventions and gotchas that the code and git history do not reveal on their own.
- Load-bearing numbers, and where they were measured.
- What is still unverified, and what would verify it.
- Pointers to the canonical source of something that lives outside the repo.

## What does NOT belong here

- Anything cross-project or about Chris generally → that is global memory
  (`~/.claude/projects/<project>/memory/`) or `~/.claude/CLAUDE.md`.
- Anything the repo already records — file structure, past fixes, git history.
- Narration of a session. That is `context/`.
- Secrets, credentials, tokens.

## How to maintain it

At a task boundary — and always before `/clear` — do a **promote pass**: read what this session
established, and write anything durable into the sections below. Say plainly what was promoted.
Update an existing entry rather than appending a near-duplicate. Date entries that could go stale.
Nothing here is deleted without asking; a superseded entry is marked superseded, not removed.

---

## Decisions

_Settled calls and the reasoning. Do not re-raise these without new information._

<!-- - **YYYY-MM-DD — <decision>.** <why>. Superseded by: <none> -->

## Conventions

_How this project does things, where it differs from the default or is not obvious from the code._

## Corrections

_Where Claude got it wrong here and what the right approach is. The point is not repeating it._

## Verified facts

_Load-bearing values, each with its source. Where recollection and this section disagree, this
section governs._

## Open / unverified

_Known unknowns, and what would settle each one._

## External sources of truth

_Things this project depends on that do not live in this repo._
