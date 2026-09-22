---
name: author
description: Write, edit, revise, or structure technical articles. Enforces consistent voice, narrative coherence, source-backed claims, and whole-article awareness across all edits. Use when the user asks to write, edit, revise, structure, critique, or improve an article, blog post, or long-form text.
---

## Setup

Before article work:

1. Read the full existing article. Do not edit a section in isolation.
2. Read [reference/style.md](reference/style.md). If it is already present in the current conversation context, do not load it again.
3. Follow the applicable process in [reference/workflow.md](reference/workflow.md).

## Commands

| Command | Purpose |
|---|---|
| `draft [topic]` | Produce a complete article through the full workflow |
| `outline [topic]` | Research and structure the argument without drafting |
| `revise [target]` | Improve an existing article |
| `source [claim]` | Find and verify evidence for a claim |
| `critique [target]` | Evaluate an article without changing it |

### Routing

- When the request starts with a command, run the matching workflow.
- Otherwise infer the closest workflow from the request.
- If the intent is unclear, ask one focused question.

## Repository conventions

Follow the article location and frontmatter conventions in the repository's `AGENTS.md`.
