# Rhetoric Review Protocol

Use this protocol for a rhetoric-only review of an existing article. The purpose is to evaluate how the prose develops and delivers the argument, not whether the argument is factually correct.

## Scope

Review these dimensions:

- **Paragraph purpose and movement.** Does each paragraph establish its purpose early enough, develop one coherent point, and end without merely repeating itself?
- **Sentence construction.** Are relationships between clauses clear? Is a sentence overloaded, choppy, ambiguously attached, or difficult to parse on the first reading?
- **Rhythm and pattern.** Do sentence lengths, openings, paragraph shapes, contrasts, lists, or section structures repeat mechanically?
- **Cohesion and transitions.** Does each sentence follow from the previous one? Do paragraphs and sections make their dependency, contrast, consequence, or change in direction clear without procedural announcements?
- **Emphasis and proportion.** Does the prose give weight to the points that carry the argument, or does it announce importance, overstate a minor detail, bury the main clause, or spend too much space on setup?
- **Voice and ownership.** Does the prose distinguish technical description from the author's observation, choice, inference, and recommendation? Is agency hidden where naming the actor would clarify the point?
- **Diction and abstraction.** Are nouns and verbs concrete enough for the argument? Do vague labels, generic connectives, nominalizations, unnecessary qualifiers, or stacked abstractions make the prose less direct?
- **Repetition and compression.** Does a passage add evidence, qualification, consequence, contrast, or synthesis, or only restate an earlier point?
- **Headings and section shape.** Does each heading orient the reader at the right level? Does the section prove what its heading promises, and is its length proportionate to its role?
- **Opening and conclusion.** Does the opening create a concrete reason to care and state the article's real problem? Does the conclusion land on a claim earned by the article rather than merely summarize it?
- **Visual pacing.** Would prose be easier to follow as prose, a list, a table, code, or a diagram? Judge this as rhetoric and reading flow, not decoration.

Apply the corresponding rules in [style.md](style.md), especially Narrative, Voice, Rhythm and structure, Sections and headings, Transitions, Paragraph movement, Visual structure, Consistent terminology, Repetition, and the rhetorical anti-patterns.

## Exclusions

Do not:

- Verify claims, links, citations, versions, numbers, product behavior, or technical correctness.
- Create a claim inventory or recommend sources.
- Treat lack of citation as a rhetorical defect.
- Replace a qualified claim with a stronger claim merely to make it sound decisive.
- Invent examples, experiences, technical details, motives, consequences, or certainty.
- Rewrite a clear sentence merely to make it different.

If a rhetorical judgment depends on whether a claim is true or supported, mark it `Out of scope: requires factual review` and leave the wording unchanged.

## Procedure

1. **Map the argument.** State the article's apparent central claim and give one sentence for the rhetorical job performed by each section. This describes the prose; it does not validate the claims.
2. **Inventory every prose paragraph.** Assign stable IDs such as `P01`, `P02`, and record its heading and line range. Treat list introductions, list items as a group, tables, code blocks, and the conclusion as review units when they affect reading flow.
3. **Run the rhetoric matrix.** Check every unit against every applicable dimension in Scope. Record issues as findings. Record `Clear` when a unit has no rhetorical defect; do not omit it.
4. **Run an article-level pass.** Check repetition across distant sections, recurring sentence patterns, section proportions, heading progression, opening-to-conclusion alignment, and visual pacing that cannot be judged paragraph by paragraph.
5. **Finish detection before rewriting.** Complete the paragraph inventory and article-level findings before proposing any replacement text.
6. **Propose the smallest effective treatment.** Prefer keep, delete, move, merge, split, or a local replacement over rewriting a whole paragraph. Preserve meaning, confidence, terminology, links, code, and citations.
7. **Adversarially validate each rewrite.** Compare the proposal with the original and its neighboring paragraphs. Reject or revise it if it changes the claim, adds unsupported detail, flattens a useful distinction, creates repetitive syntax, overexplains, introduces generic connective language, or violates ASCII punctuation.
8. **Prove coverage.** Include every inventoried unit in the coverage table. If any unit or rhetoric dimension was not checked, identify it precisely and do not call the review complete.

## Finding Format

Assign IDs such as `R01`, `R02`, and include:

| Field | Required content |
|---|---|
| Location | Paragraph ID, heading, and exact line range |
| Dimension | The rhetoric dimension and corresponding `style.md` rule |
| Symptom | The exact phrase or construction causing the problem |
| Effect | What it makes harder to understand, follow, or believe |
| Treatment | Keep, delete, move, merge, split, or replacement in context |
| Rewrite validation | Meaning, confidence, terminology, local transition, rhythm, repetition, and ASCII punctuation |

Do not use vague findings such as "wordy", "awkward", "improve flow", or "could be clearer" without identifying the construction and its effect.

## Required Output

1. **Rhetorical map:** central claim and each section's job.
2. **Findings:** ordered by effect on comprehension and argument, then by article position.
3. **Proposed treatments:** only after the complete findings list.
4. **Coverage table:** every paragraph or review unit with line range and `finding IDs` or `Clear`.
5. **Dimension summary:** all scope dimensions marked `Checked`, `Not applicable`, or `Unchecked` with a reason.
6. **Residual scope:** anything requiring factual, source, or technical review, without attempting that review.
