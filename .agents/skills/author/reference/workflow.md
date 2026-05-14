# Writing Workflow

Multi-pass workflow for producing technical articles. Each phase has an explicit gate — no skipping phases. The outline must be validated before drafting. The draft must be complete before revising.

---

## Phase 1: Research

Before writing a single word, gather and verify sources.

### Steps

1. **Identify the central claim.** What is the one thing this article argues? Write it in one sentence. If you cannot, the topic is not ready.

2. **Collect sources.** For every factual claim the article will make, find a source that supports it. Use web search, academic papers, documentation, primary sources. Record each source with:
   - Full URL
   - Author and publication
   - The specific claim it supports
   - A direct quote if relevant

3. **Mark assertions.** If no source can be found for a claim, mark it explicitly as an assertion, not a fact. The article can still make the claim — but it must be framed as the author's position, not as established truth.

4. **Identify gaps.** Claims that need sources but don't have them yet are research gaps. Either fill them or restructure the argument to avoid relying on unsupported claims.

### Output

A structured source list:

```
[^1]: Author, "Title," Publication, Date. <URL>
Claim supported: [specific claim]
Quote: "[relevant excerpt]"
```

### Gate

All claims have either a verified source or are explicitly marked as assertions. No claim presents an assertion as sourced fact.

---

## Phase 2: Outline

Structure the argument before writing any prose.

### Steps

1. **Write the opening promise.** One sentence: what will the reader get from this article? This becomes the hook.

2. **Map the argument chain.** Each section makes one claim. List them in order:
   - Section heading (stating the claim, not labeling the topic)
   - Key claim the section proves
   - Sources it draws on
   - How it connects to the next section

3. **Identify tension points.** Where does the article build pressure before releasing it? Mark these explicitly. An article without tension is a reference document, not an argument.

4. **Write the conclusion claim.** One sentence: what does the article land on? If the conclusion is a vague summary ("in conclusion, there are many considerations"), the argument is not finished.

5. **Check the structural checklist:**
   - [ ] Opening: concrete observation or problem, not context
   - [ ] Promise: clear what the article delivers
   - [ ] Flow: each section follows logically from the previous one
   - [ ] Tension: a clear problem/gap/question that the article resolves
   - [ ] Conclusion: specific claim, not vague summary
   - [ ] Consistency: terms used the same way throughout
   - [ ] Audience fit: depth is right — not over-explained, not assumed

### Output

A structured outline with section headings, claims, source mappings, and transition notes.

### Gate

The outline passes the structural checklist. The author (user) reviews and approves before drafting begins.

---

## Phase 3: Draft

Write the article section by section. No single-prompt full-article generation.

### Steps

1. **Write one section at a time.** Provide the full outline and style reference as context for each section. Each section makes exactly one claim. The heading states the claim.

2. **Follow the style rules.** Load and apply [style.md](style.md) for every section:
   - Sachlich tone — factual, direct, no hedging
   - Claim-first paragraphs
   - Short to medium sentences, one idea per sentence
   - 2–4 sentence paragraphs
   - No anti-patterns (see style.md for the full list)

3. **Cite as you write.** Every factual claim that is not common knowledge gets a numbered footnote inline. Do not add footnotes after the fact — cite in the moment.

4. **Connect sections explicitly.** The last sentence of each section should signal what comes next, not by saying "in the next section" but by naming the remaining tension or the next claim.

5. **Write the opening last.** The opening makes a promise to the reader. You cannot make that promise precisely until you know what the article delivers. Write the body first, then write the opening that hooks the reader into the argument you actually built.

### Output

A complete draft in Markdown with frontmatter, footnotes, and sources section.

### Gate

The draft is complete — all sections written, all footnotes in place, frontmatter filled per AGENTS.md convention. No placeholder sections.

---

## Phase 4: Revise

Evaluate the complete draft against explicit criteria.

### Steps

1. **Voice consistency check.** Does every section sound like the same author? Compare against the voice examples in [style.md](style.md). Flag any section that drifts into generic AI prose.

2. **Anti-pattern sweep.** Search the full draft for every item on the anti-pattern list in [style.md](style.md). Flag and rewrite each instance:
   - Typographic/smart characters (curly quotes, em dashes, en dashes, ellipsis)
   - Generic transitions ("Furthermore", "Moreover", "Additionally")
   - Excessive hedging
   - Passive voice where active works
   - Bullet summaries at section ends
   - Rhetorical questions as transitions
   - Unearned summary paragraphs
   - Listification where prose is better
   - "It is worth noting that..."
   - False specificity without sources

3. **Factual accuracy check.** Verify every footnote references a real source that actually supports the claim it is attached to. Remove or reframe any claim where the source does not directly support it.

4. **Structural checklist.** Re-run the checklist from Phase 2:
   - [ ] Opening: concrete observation or problem, not context
   - [ ] Promise: clear what the article delivers
   - [ ] Flow: each section follows logically
   - [ ] Tension: a clear problem/gap/question that resolves
   - [ ] Conclusion: specific claim, not vague summary
   - [ ] Consistency: terms used the same way throughout
   - [ ] Audience fit: depth is right

5. **Cross-reference check.** After any edit, verify that:
   - The opening hook still matches what the article delivers
   - The conclusion still lands after the change
   - No section references something that was removed or changed
   - The argument chain holds end-to-end

### Output

A revised draft with all anti-patterns removed, all sources verified, and the structural checklist passing.

---

## Phase 5: Polish

Final pass before the article is considered complete.

### Steps

1. **Source verification.** Independently verify that every URL in the sources section resolves and contains the claimed information. Remove or replace any dead links.

2. **Read-aloud rhythm check.** Read the article aloud (or simulate this). Flag any sentence that requires re-reading to parse. Rewrite for clarity.

3. **Frontmatter generation.** Ensure the YAML frontmatter follows the AGENTS.md convention:
   ```yaml
   ---
   title: "Article Title"
   author: "Markus Wondrak"
   date: "YYYY-MM-DD"
   excerpt: "One-liner for listings"
   tags: ["Tag1", "Tag2"]
   reading_time: "N min read"
   slug: "article-slug"
   ---
   ```

4. **Final anti-pattern pass.** One last sweep for any remaining anti-patterns from [style.md](style.md).

5. **Consistency check.** Verify terminology is used consistently throughout. No synonym-switching for the same concept.

### Output

A publication-ready article.

---

## Draft Approval Gate

Before any change is written to disk, the author must present the complete draft to the user and receive explicit approval.

This gate applies to all commands, not just `draft`. Whether revising an existing article, adding a source, or polishing a final version: draft first, present, wait for approval, then apply.

The draft must include:
- The full text of the proposed change (not a summary or diff description)
- Frontmatter if the article has it
- All footnotes and sources

Partial drafts are acceptable only if the user explicitly requests incremental delivery.

---

## Command-specific workflows

### `draft [topic]`

Runs all five phases sequentially. Start with research, end with polish. Each phase gate must pass before proceeding.

### `outline [topic]`

Runs Phase 1 (Research) and Phase 2 (Outline). Stops before drafting. Returns the structured outline for review.

### `revise [target]`

Skips to Phase 4 (Revise). Reads the full article first (Setup step 1), then applies the revision criteria. Presents the revised draft to the user for approval before writing any changes to disk. Use when an article exists but needs improvement.

### `source [claim]`

Runs the source-gathering portion of Phase 1 for a specific claim. Finds and verifies sources, or marks the claim as an assertion if no source exists.

### `critique [target]`

Runs the structural checklist and anti-pattern sweep without making changes. Returns a report of issues found, organized by category (structural, prose, sourcing, consistency). Use when you want feedback before revising. If the user asks for edits based on the critique, the draft-first rule applies: draft the changes, present them, wait for approval.