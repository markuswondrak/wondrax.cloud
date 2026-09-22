---
description: Exhaustively review an article's rhetoric and prose without fact-checking it.
agent: rhetoric-reviewer
model: opencode-go/kimi-k2.6
subtask: true
---

Perform a rhetoric-only review of the complete article at `$ARGUMENTS`.

Follow `.agents/skills/author/reference/rhetoric-review.md` exactly and apply the relevant rules from `.agents/skills/author/reference/style.md`. Review every prose paragraph and the article-level rhetorical structure. Include the required coverage table and dimension summary, then propose validated treatments for all findings.

Do not fact-check claims, inspect sources, assess citation coverage, or edit the article.
