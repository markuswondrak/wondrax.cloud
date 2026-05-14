---
name: author
description: Write, edit, revise, or structure technical articles. Enforces consistent voice, narrative coherence, source-backed claims, and whole-article awareness across all edits. Use when the user asks to write, edit, revise, structure, critique, or improve an article, blog post, or long-form text.
---

Writes and iterates technical articles with whole-article awareness, source-backed claims, and a consistent authorial voice.

## Setup (non-optional)

Two steps before any article work. Both are required.

### 1. Read the full article

If an article file already exists, read it completely before making any change. Every section edit must be checked against:

- The opening hook and the promise it makes to the reader
- The conclusion and whether it still lands after the change
- Any sections that reference or depend on what changed
- The overall argument chain: does the logic still hold end-to-end?

Never edit in isolation. A changed section that is correct on its own but breaks the narrative is a bad edit.

If no article exists yet, read the style reference before starting.

### 2. Load style reference

Read [reference/style.md](reference/style.md) before any writing or editing task. If the output is already in this session's conversation history, don't re-read.

The style reference contains voice rules, anti-patterns, and examples from this author's existing work. Writing without it produces generic output that ignores the project's voice.

## Audience

Default: senior technical practitioners and engineering-adjacent business roles. They understand systems thinking; they do not need basic concepts explained. Adjust per article if specified.

## Commands

| Command | Category | Description | Reference |
|---|---|---|---|
| `draft [topic]` | Build | Full article from topic through research to final draft | [reference/workflow.md](reference/workflow.md) |
| `outline [topic]` | Build | Structure and claims before writing | [reference/workflow.md](reference/workflow.md) |
| `revise [target]` | Refine | Edit existing article against style rules | [reference/workflow.md](reference/workflow.md) |
| `source [claim]` | Verify | Verify or find sources for a claim | [reference/workflow.md](reference/workflow.md) |
| `critique [target]` | Evaluate | Evaluate article against structural checklist | [reference/workflow.md](reference/workflow.md) |

### Routing rules

1. **No argument** — render the command table above. Ask what they'd like to do.
2. **First word matches a command** — load the workflow reference and follow the relevant phase. Everything after the command name is the target or topic.
3. **First word doesn't match** — general writing invocation. Apply setup steps, style reference, and workflow, using the full argument as context.

Setup (full-article read, style reference) is loaded before any command executes; sub-commands don't re-invoke `$author`.

## Article structure

Each article lives in its own directory: `NN_slug-name/article.md`

Every `article.md` must include YAML frontmatter per the project's AGENTS.md convention:

```yaml
---
title: "Article Title"
author: "Markus Wondrak"
date: "2026-04-15"
excerpt: "One-liner for listings"
tags: ["Tag1", "Tag2"]
reading_time: "8 min read"
slug: "article-slug"
---
```

The `date` field uses ISO format (`YYYY-MM-DD`) for chronological sorting.

## Source discipline

All assumptions must be evaluated and proven by sources. This is a project rule from AGENTS.md, not a suggestion.

- Every factual claim that is not common knowledge gets a numbered footnote
- Sources go in a `## Sources` section at the end, not inline URLs in the prose
- Never cite a source that does not actually support the claim
- If no source can be found for a claim, mark it explicitly as an assertion, not a fact

## Draft-first rule

All changes must be drafted and presented to the user before being written to any file. No exceptions.

1. **Draft.** Produce the complete proposed change — full text, not a summary.
2. **Present.** Show the draft to the user for review.
3. **Wait for approval.** Do not write to disk until the user explicitly approves.
4. **Apply.** Only after approval, write the changes.

This applies to every command: `draft`, `revise`, `source`, `critique`. Even when the user asks for a quick fix, draft it first, show it, wait.