# Writing Workflow

Use the phases required by the selected workflow in their defined order. Complete a phase's gate before moving to the next required phase.

---

## Workflow selection

| Command | Phases |
|---|---|
| `draft` | Research, outline, draft, revise, polish |
| `outline` | Research, outline |
| `revise` | Revise, polish as needed |
| `source` | Research for the specified claim |
| `critique` | Complete coverage review without changing files |

---

## Phase 1: Research

Identify and verify the evidence the argument depends on before drafting the article.

### Steps

1. **Define the central argument.** State in one sentence what the article will establish, examine, or recommend.
2. **Create a claim inventory.** List the assumptions and externally verifiable claims the article relies on.
3. **Research those claims.** Follow the evidence, link, and citation rules in [style.md](style.md). Record the source, the exact claim it supports, and the relevant passage or result.
4. **Resolve evidence gaps.** Research, narrow, or remove unsupported factual claims. Keep an interpretation or hypothesis only when it is clearly identified as such.

### Output

Research notes that map each load-bearing claim to its evidence or documented treatment.

### Gate

Every assumption and externally verifiable claim that the argument depends on has evidence or has been handled according to the rules in [style.md](style.md).

---

## Phase 2: Outline

Define the article's argument and reading path before drafting prose.

### Steps

1. **Write the opening promise.** State what the reader should understand or be able to decide after reading.
2. **Map the argument.** List the sections in order, with each section's purpose, supporting evidence, and dependency on earlier sections.
3. **Test the sequence.** Check that each section is necessary and appears where the reader has enough context for it.
4. **Plan supporting elements.** Note where a list, table, code example, or visual would clarify the argument. Follow the visual guidance in [style.md](style.md).
5. **Define the landing point.** State what the conclusion should establish after the evidence has been presented.

### Output

An outline with section purposes, evidence mappings, structural dependencies, and proposed supporting elements.

### Gate

The outline has a coherent argument, no unsupported structural jumps, and enough evidence to begin drafting. Present it for approval when the user requested an outline, asked to review the structure first, or when unresolved structural choices require a decision.

---

## Phase 3: Draft

Turn the validated outline into a complete article.

### Steps

1. **Draft from the outline.** Write in manageable sections while keeping the full argument available as context.
2. **Apply the style reference.** Follow [style.md](style.md) without restating its rules here.
3. **Attach evidence while drafting.** Add citations and links when the supporting claim is written rather than reconstructing evidence afterward.
4. **Maintain article-level coherence.** Recheck dependencies when a drafted section changes the planned argument.
5. **Write or revise the opening after the body.** Make sure it introduces the article that was actually written rather than the article originally imagined.
6. **Add proposed visuals.** Include Mermaid directly where appropriate and provide production prompts for external visuals.

### Output

A complete Markdown draft with repository-required frontmatter, citations, sources, and any visual proposals.

### Gate

The article is complete enough to review end to end. It contains no placeholder sections, unresolved structural gaps, or untracked evidence dependencies.

---

## Phase 4: Revise

Review the complete draft as one argument rather than as isolated sections.

### Steps

1. **Check the argument.** Verify that the opening, section sequence, evidence, and conclusion still support the same central argument.
2. **Check dependencies.** Find references, assumptions, or transitions that no longer work after drafting changes.
3. **Apply the style reference.** Review the article against [style.md](style.md), including voice, rhythm, visual structure, repetition, terminology, links, citations, and anti-patterns.
4. **Verify evidence.** Confirm that each evidentiary source supports the exact claim and scope attached to it.
5. **Review visual proposals.** Confirm that each visual adds understanding, matches the article, and contains enough information to produce without inventing details.

### Output

A coherent revised draft with verified evidence and resolved structural issues.

### Gate

The opening matches what the article delivers, the argument holds end to end, and no edit has left broken references or unsupported dependencies.

### Critique protocol

For `critique`, do not stop after finding representative examples. Review the complete article with this protocol:

1. **Inventory the article.** Record every heading and the line range or paragraph range it covers. Include the opening and conclusion as separate review units.
2. **Review structure first.** Check the central claim, opening promise, section order, transitions, repetition across sections, terminology, conclusion, and visual structure. Record each finding before reviewing sentences.
3. **Review every unit locally.** For each review unit, check every paragraph against the applicable rules in [style.md](style.md). Record either its findings or `No local finding`. Do not use spot checks, sampling, or a fixed number of examples.
4. **Separate detection from rewriting.** Finish the complete finding inventory before drafting any replacement text. Do not silently edit the article during critique.
5. **Validate every proposed replacement.** Re-read the original passage, its surrounding paragraph, and the applicable style rules. Reject or revise a proposal if it introduces another violation, changes the claim or confidence level, removes evidence, changes terminology, or uses unsupported detail.
6. **Check coverage.** Account for every review unit and every applicable style category before declaring the critique complete. If context or tool limits prevent complete coverage, state exactly what remains unchecked instead of claiming completion.

Use this finding format:

| Field | Required content |
|---|---|
| Location | Heading and exact line or paragraph range |
| Severity | Hard failure, strong default, warning sign, or structural |
| Rule | The specific `style.md` rule, not a generic label such as "style" |
| Problem | Why the passage violates or weakens that rule in this context |
| Proposed treatment | Keep, delete, move, split, or a complete replacement in context |
| Validation | Confirm claim, evidence, terminology, transition, ASCII punctuation, and absence of newly introduced style violations |

The critique output must contain:

1. The article's central claim and argument outline.
2. Findings ordered by severity and then article position.
3. A coverage table listing every review unit, its range, and `finding IDs` or `No local finding`.
4. A style-category checklist covering claims and uncertainty, narrative and voice, rhythm and paragraphs, sections and transitions, visual structure, examples and evidence, links and citations, terminology, formatting, repetition, and anti-patterns.
5. Any residual uncertainty or unchecked scope.

`No local finding` means only that the unit has no paragraph-level defect. It does not exempt the unit from article-level structural findings.

---

## Phase 5: Polish

Perform the final publication check without reopening settled arguments unless a real defect appears.

### Steps

1. **Read for friction.** Read the article end to end and revise sentences that require a second pass to understand.
2. **Validate references.** Confirm that evidentiary links resolve and that internal links, footnotes, code blocks, tables, and diagrams render correctly.
3. **Check repository requirements.** Validate the article location and frontmatter against `AGENTS.md`.
4. **Confirm completeness.** Remove placeholders, temporary notes, and unresolved visual instructions that are not intended for publication.

### Output

A publication-ready article.

### Gate

The article renders correctly, satisfies repository conventions, and has no known editorial or evidentiary defects.

---

## Pre-delivery check

Before presenting or applying article text:

1. Read the changed text in its surrounding context.
2. Check the changed passages against [style.md](style.md) according to each rule's stated severity.
3. Confirm that the change does not introduce factual, structural, citation, or formatting regressions.

Scale the check to the change, but include the complete article when coherence or terminology may be affected.

---

## Approval gate

Before changing an article file, present the proposed text and wait for approval unless the user explicitly asked for immediate edits.

Show enough context to evaluate the change:

- For a new article, present the complete draft.
- For a section revision, present the complete revised section.
- For a local edit, present the affected passage.
- For research or critique without article changes, return the findings directly.

After approval, apply only the reviewed change. If the requested scope changes materially, present the revised proposal again.
