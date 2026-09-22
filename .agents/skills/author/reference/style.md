# Style Reference

Voice, tone, structural rules, and anti-patterns for this author's technical articles.

---

## Tone

Sachlich: factual, direct, and technically grounded. Avoid academic distance, corporate polish, and chatty filler. The prose may be conversational when that makes an observation or decision sound natural, but it should not become flippant.

---

## Claims and uncertainty

Distinguish between externally verifiable facts, personal observations, inferences, and recommendations. State each with the level of confidence its evidence supports.

Take a position when the available evidence supports one, but do not present an interpretation as established fact.

When evidence is incomplete, identify the exact boundary of what is known. Remove anonymous or stacked hedges such as "It could potentially be argued that" and "Some might say." Do not turn uncertainty into apparent consensus or false confidence.

The following examples show different kinds of uncertainty. They are not sentence templates to repeat:

- "The documentation defines the resolution order but does not cover equal priorities."
- "This worked in the repositories I tested. I do not know whether the result holds for larger monorepos."
- "The mechanism is documented, but its effect on long-running workflows has not been measured."
- "My conclusion follows from the implementation and two issue reports rather than a controlled comparison."
- "Version 0.16.0 behaves this way. A later release may change the default."

---

## Narrative

Open with a concrete problem, observation, decision, or incident that gives the reader a reason to care about the technical argument. A short story can work well when it comes from a real experience and shows how the problem surfaced. Do not invent or dramatize an anecdote to create a hook.

Move from the opening to the technical point without unnecessary scene-setting. Background belongs where the argument requires it, not automatically at the beginning.

Tension may emerge from a real constraint, contradiction, failed assumption, or unresolved decision. Do not manufacture suspense when the technical problem is already interesting enough.

**Effective opening:**
> I haven't written a line of code by hand in the past few months. Agents coordinate across repositories, write migration scripts, and work in large codebases. The question is no longer whether this can work. It's how to structure the workflow so the agents remain coherent as complexity scales.

**Generic opening:**
> AI-assisted development has become increasingly common. Many developers now use tools like GitHub Copilot and Cursor. This article evaluates GitHub's Spec Kit framework.

The first opening shows the problem through a concrete situation. The second delays the article's actual subject with broad context. Background is useful when the reader needs it, but it should not replace the opening point.

---

## Voice

Use first person when the author's experience, judgment, decision, or uncertainty is part of the argument. It should establish ownership, not add personality for its own sake.

Name the artifact or system directly when describing verifiable behavior. Use "I" when explaining why you chose, changed, tested, or rejected something. Do not describe a personal decision as though the project made it by itself, and do not rewrite neutral technical facts into first person merely to sound human.

**Technical fact:**
> The preset prepends the same runtime file to multiple commands.

**Owned decision:**
> I moved the shared instruction into one runtime file so the commands no longer maintain separate copies.

---

## Audience

Assume technical competence. Explain concepts that are necessary for the argument, especially when terminology is ambiguous or domain-specific. Do not explain standard engineering concepts merely to make the article appear comprehensive. Audience knowledge depends on the article; do not mistake concision for clarity.

---

## Rhythm and structure

Write for clarity, but let the argument determine the rhythm. Mix short statements with longer sentences when several details belong together. Split a sentence when its relationships become difficult to follow, not merely because it contains more than one idea.

Most paragraphs should have one dominant purpose, but they do not need a fixed length. A one-sentence paragraph can add emphasis. A longer paragraph is appropriate when splitting it would interrupt a connected line of reasoning.

Watch for repeated sentence openings, contrasts, paragraph patterns, section lengths, and identical numbers of points. Repetition becomes a problem when the reader can anticipate the form before reaching the content. Symmetry is useful for genuinely parallel material, and clear sentences should not be rewritten merely to create artificial variety.

---

## Sections and headings

Each section should have a clear purpose in the article's argument. Closely related claims may share a section when separating them would fragment the reasoning.

Headings should name the section's topic, decision, or conclusion at the level needed for orientation. Argumentative sections often benefit from a heading that states the claim. Explanatory sections may use a clear topic label.

State the shape of the point in the heading and prove it in the body. Numbers, filenames, and other supporting details usually belong where the evidence is explained. Include them in the heading only when they are themselves the subject of the section.

**Too vague:**
> ### Runtime configuration

**Too specific:**
> ### One runtime preamble beats fourteen copies

**Better:**
> ### One runtime preamble instead of multiple copies

---

## Transitions

Sections must follow each other logically. Add an explicit transition only when it clarifies a change in direction, a dependency, or an unresolved tension. If the connection is already clear, let the section break do the work.

Avoid procedural announcements such as "in the next section" and questions that manufacture momentum without adding information. A concrete technical question is acceptable when it expresses a real problem that the following text answers.

Do not open a section by restating the previous section's conclusion. Refer back only when the new section adds a dependency, distinction, or consequence.

---

## Paragraph movement

Make each paragraph's purpose clear early enough that the reader does not have to reconstruct it. Often the clearest structure is to state the claim first and then support it.

Evidence, an example, or an observed contradiction may come first when it makes the point easier to understand or the conclusion more convincing. Choose the order that best serves the reasoning rather than applying the same pattern to every paragraph.

---

## Visual structure

Avoid long stretches of visually uniform prose. When the content supports it, alternate between paragraphs and other elements such as bullet lists, tables, code blocks, diagrams, quotations, or restrained inline emphasis. The purpose is to give the reader visual anchors, not to decorate the article.

Choose the format that matches the information:

- Use bullets for parallel items, alternatives, findings, or steps that benefit from scanning.
- Use tables for structured comparisons across consistent dimensions.
- Use code blocks when syntax, configuration, commands, or file structure are part of the explanation.
- Use diagrams for architecture, sequence, state, ownership, boundaries, or information flow.
- Use inline code for identifiers, paths, commands, and literal values.
- Use bold or italics sparingly when emphasis helps the reader locate an important distinction.

Preview a longer sequence when the reader needs the full map before following its individual parts. Skip the preview when the sequence is short, intuitive, or clearer when revealed through the argument. Do not repeat the same information in both the preview and the sections that follow.

Keep an enumeration in prose when order, causality, or the relationship between the items matters more than scanability. Do not force content into a list, table, diagram, or code block solely to create visual variety.

A summary list is useful when it consolidates decisions, requirements, or actions the reader needs as a reference. Do not append "Key takeaways" that merely repeat the preceding section.

Review the article as a whole. If several consecutive sections consist only of similarly sized paragraphs, look for information that would be clearer in another form. If the article already contains frequent lists, tables, diagrams, or emphasis, do not add more.

## Visual proposals

Propose a visual when spatial structure, sequence, ownership, state, or comparison would be harder to understand in prose alone.

Prefer a Mermaid diagram when the visual represents technical relationships that can be expressed accurately in text. Suggest an externally produced diagram or illustration only when Mermaid would be too limited for the intended result.

Every proposed visual must include:

- The section and exact position where it belongs
- The question it helps the reader answer
- The appropriate format, such as Mermaid, SVG, annotated screenshot, or illustration
- Every component, label, boundary, and relationship that must appear
- The direction of flows or sequence of steps
- The distinction the reader should notice first
- Details that must not appear because they would be inaccurate, distracting, or unsupported
- A concise caption that connects the visual to the article's argument

For an externally generated visual, provide a complete production prompt rather than a vague concept. The prompt must specify the composition, hierarchy, labels, relationships, visual style, aspect ratio, color constraints, and exclusions. It should be possible to create the visual from the prompt without reading the full article.

Do not invent architecture, data flows, interfaces, measurements, or product behavior to make a visual more complete. Mark unresolved details explicitly or omit them.

---

## Examples and evidence

Use a concrete example when it makes a mechanism, trade-off, or failure mode easier to understand or verify. Prefer details that carry argumentative weight: the relevant configuration, command, file boundary, behavior, or observed result.

Specificity is useful only when the detail changes the reader's understanding or lets them verify the claim. Do not add exact counts, filenames, versions, or implementation details merely to make the prose sound concrete.

Keep exposition when the concept is already clear and an example would only repeat it. When an explanation remains abstract or difficult to test, replace part of it with the smallest example that exposes the mechanism.

**Concrete and relevant:**
> The preset prepends `commands/workflow-runtime.md` to each automated command, so the shared instruction has one maintained source.

**Specific but unfocused:**
> The preset declares fourteen `type: command` entries in a 73-line manifest last updated in version 0.16.0.

---

## Links and citations

Use sources where verification matters to the argument. Cite claims about measured results, documented product behavior, specification requirements, dates, versions, quotations, disputed facts, or statements attributed to another person or organization.

Do not cite every technical sentence. Stable background knowledge, definitions introduced by the article, the author's reasoning, and clearly identified personal observations usually do not need external support. Add a source when removing it would leave the reader with a relevant reason to doubt or verify the claim.

Use numbered footnotes when a source serves as evidence. Place the footnote next to the claim it supports, and include the full reference in the `## Sources` section. One citation may support several nearby claims only when the source actually covers all of them.

Use a direct inline link when its main purpose is navigation rather than evidence. This is appropriate for a named tool, repository, specification, issue, discussion, or documentation page that the reader may reasonably want to open. Do not duplicate a navigational link in the Sources section unless the article also relies on it as evidence.

A link does not prove the surrounding sentence merely because it points to the right project or topic. Check that evidentiary sources support the exact wording and scope of the claim. If an important factual claim cannot be verified, narrow it to what the evidence supports or remove it. An interpretation or hypothesis may remain when it is clearly identified and does not stand in for missing evidence.

---

## Consistent terminology

Keep terminology stable within an article. Do not switch synonyms merely for stylistic variety when they refer to the same concept.

Preserve different terms when they represent different technical concepts, even if they appear similar in ordinary language. Define the distinction when a reader could reasonably confuse them.

Establish article-specific terminology during outlining or revision. Prefer the term used by the relevant specification, product, or source unless the article explicitly argues for a different definition.

---

## Formatting constraints

Use ASCII punctuation in article prose for consistent source files and predictable diffs:

- Straight double quotes (`"`), not curly quotes
- Straight apostrophes (`'`), not curly apostrophes
- Hyphen-minus (`-`) instead of en or em dashes
- Three periods (`...`) instead of the ellipsis character
- Regular spaces instead of non-breaking spaces

This is a repository formatting convention, not part of the author's voice. Do not alter code, commands, URLs, identifiers, product names, or direct quotations merely to enforce it.

---

## Repetition

Remove a sentence or paragraph when it only paraphrases an earlier claim. Repetition is justified when it adds evidence, qualification, consequence, contrast, or synthesis. A conclusion may return to the central claim when the intervening argument has changed what the reader understands about it.

---

## Anti-patterns

Treat the items below according to their type:

- **Hard failure:** Factual or editorial problems that must be corrected, such as unsupported claims that carry the argument, false precision, invented details, misleading citations, or copied chat language.
- **Strong default:** Prefer the stated alternative unless the context gives a clear reason not to.
- **Warning sign:** Review the passage when a pattern repeats, adds no information, or makes the prose feel mechanical. A single justified use is not automatically a problem.

Each rule below should make its severity clear. Do not rewrite a sentence merely because it resembles a warning sign; confirm that the pattern is actually harming clarity, accuracy, rhythm, or voice.

- **Warning sign: Generic connective words.** Repeated use of "Furthermore," "Moreover," "Additionally," or "In addition" can make prose sound assembled rather than argued. Prefer to state the actual relationship between the ideas, such as contrast, consequence, dependency, or exception. Start the next claim directly when no transition is needed. A connective word is acceptable when it is the clearest and most natural option; do not replace it solely because it appears on this list.
- **Strong default: Name the actor when it matters.** Prefer active voice when it clarifies who made a decision, performs an action, owns a constraint, or caused a result. Passive voice is appropriate when the actor is unknown, irrelevant, already obvious, or less important than the operation or affected system. Do not use passive constructions to hide responsibility or uncertainty.

  **Unclear ownership:**
  > It was decided that installed packages should not be committed.

  **Clear ownership:**
  > I decided not to commit installed packages.

  **Useful passive:**
  > The generated files are removed after each run.
- **Hard failure: Unsupported precision.** Do not use exact numbers, dates, versions, measurements, rankings, or causal claims unless a source or reproducible observation supports that level of precision. Match the wording to the evidence. If the source says "roughly one third," do not rewrite it as `33.3%`.
- **Hard failure: Unsupported absolutes.** Words such as "none," "nothing," "always," "never," "every," and "all" make categorical claims. Use them only when the relevant scope is defined and the evidence covers it. Otherwise state the verified boundary, exception, or observed sample.
- **Warning sign: Unearned emphasis.** Do not announce that a point is important, obvious, fundamental, or profound when the following content can establish its weight directly. This includes empty lead-ins such as "It is worth noting that," "The pattern is clear:" and "The real issue is:" as well as language that turns a small implementation detail into a paradigm shift or deeper truth. Keep framing when it contributes scope, classification, or a necessary connection. Strong language is appropriate when the demonstrated consequence warrants it.
- **Hard failure: Chat artifacts.** Remove phrases addressed to the user or inherited from assistant conversation, such as "Great question," "That is an insightful point," "I hope this helps," or "Let me know if you want more." Article prose should address the subject, not simulate a chat response.
- **Warning sign: Announcing visible content.** Do not introduce a table, list, code block, or example with a sentence that only says it follows. Use an introduction when it establishes what the reader should compare, verify, or notice. Do not restate the content immediately afterward.
