# Style Reference

Voice, tone, structural rules, and anti-patterns for this author's technical articles.

---

## Tone

Sachlich — factual, direct. Not academic, not casual. No filler phrases, no hedging. Say what is true.

If something is uncertain, say it is uncertain. Do not use vague language as a hedge.

**Good:**
> Determinism in an agent pipeline means one specific thing: given a valid workflow state and a valid input, only valid transitions are possible, and the runtime rejects everything else.

**Bad:**
> Determinism could potentially be considered important in agent pipelines, as it might help ensure more reliable behavior in certain cases.

Technical honesty carries a human signature: admit uncertainty, limits, or a wrong turn in first person, without corporate hedging. "I don't have a source for this, so I'm marking it as an assertion" is honest. "It is generally understood that..." is not; it launders uncertainty into false authority.

---

## Narrative

Story-first. The reader needs a reason to keep reading. Open with a real problem or observation, not with background. Build tension before releasing it.

**Good — drops the reader into a concrete situation:**
> I haven't written a line of code by hand in the last months. Agents coordinate across repositories, write migration scripts, doing work in large codebases. The question is no longer whether this can work. It's how to structure the workflow so the agents remain coherent as complexity scales.

**Bad — starts with context the reader already knows:**
> AI-assisted development has become increasingly common. Many developers now use tools like GitHub Copilot and Cursor. This article evaluates GitHub's Spec Kit framework.

The first version creates a concrete world; the second restates what the reader already knows.

---

## Voice

First person where appropriate. The author has a perspective; use it.

**Own your decisions in first person.** If you built, configured, or decided something, say so directly. Describing your own project in third person, as if reporting on someone else's system, creates false distance between you and the work.

**Bad:**
> Extended Flow's preset declares fourteen `type: command` entries, all pointing at the same file...

**Good:**
> Spec Kit lets one preset entry compose onto many commands, so I pointed fourteen `type: command` entries at the same file...

The good version does two things: names the general capability the tool provides, then states the specific action taken with it. Lead with the mechanism, follow with the decision - not with the project's name standing in for "I."

---

## Sentences

Short to medium. No compound sentences stacked on each other. One idea per sentence where possible.

---

## Paragraphs

2–4 sentences. White space is structure.

---

## Sections

Each section makes exactly one point. The heading states the point. The section proves it.

**Good:**
> ## No State Machine
> Spec Kit describes a workflow, but does not enforce one.

Everything that follows supports that single claim. The heading is not a label ("State Machine") — it is a verdict.

**Bad:**
> ## The State Machine in Spec Kit
> In this section we will look at how Spec Kit handles state transitions...

---

## Transitions

Sections connect explicitly. The last sentence of a section often signals what comes next — not with "in the next section" but by naming the remaining tension.

**Example:**
> The first two gaps are operational — addressable with tooling investment. The third is different. It goes to the question of what Spec Kit fundamentally believes a spec *is*.

This transition does three things: closes the prior topic, signals a gear shift, and creates anticipation.

---

## Claim-first paragraphs

Lead with the point, then support it.

**Good:**
> There is a cost to the convention model beyond correctness. Without enforced state, every agent call must carry enough workflow context for the agent to orient itself...

**Bad:**
> Without enforced state, every agent call must carry enough workflow context for the agent to orient itself... This means there is a cost to the convention model beyond correctness.

---

## Preview bullets before detail

When an article discusses multiple discrete items in sequence, preview them as a list before diving into the first one. Give the reader a map before the tour.

**Good:**
> The friction shows up in five areas:
>
> - **Variable resolution.** Static text cannot adapt to different project layouts.
> - **Deterministic triggers.** The model decides relevance instead of the orchestrator.
> - **Scope boundaries.** No rule for which skills apply in which parts of a repository.
>
> Each is a question the specification leaves unanswered...

**Bad:**
> The first of these five gaps appears in the simplest place: variable resolution. Because a `SKILL.md` file is static text...

The reader has no idea what the other four gaps are, and no mental model for how they relate.

## Lists for parallel items

When a sentence enumerates multiple discrete items, convert it to a bullet-point list. Inline enumeration forces the reader to parse boundaries and obscures parallelism.

**Good:**
> The community has followed that instinct, but every proposal treats it as a dependency management problem:
>
> - Issue #100 asks how skills should depend on other skills.
> - Issue #110 proposes a `requires` field with version validation.
> - Discussion #210 offers a full `skills.json` manifest and lockfile.

**Bad:**
> The community has followed that instinct, but every proposal treats it as a dependency management problem. Issue #100 asks how skills should depend on other skills. Issue #110 proposes a `requires` field with version validation. Discussion #210 offers a full `skills.json` manifest and lockfile.

The first version lets the reader scan the structure. The second buries it in prose.

---

## Examples over exposition

Concrete beats abstract. If a paragraph explains a mechanism for more than three or four sentences without naming a real file, config, number, or snippet, cut the prose and replace it with the example.

**Good:**
> Extended Flow's preset declares fourteen `type: command` entries, all pointing at the same file - `commands/workflow-runtime.md` - each with `strategy: prepend`.

**Bad:**
> The preset applies its central instruction across a broad set of relevant commands, ensuring the behavior is consistently distributed without duplicating the underlying logic in each individual file.

The first sentence names the file, the count, and the strategy; a reader can go check it. The second describes the same idea in the abstract and gives the reader nothing to verify.

---

## Footnotes and citations

- Cite claims that are not common knowledge
- Use numbered footnotes, not inline URLs in the prose
- Sources go in a `## Sources` section at the end
- Never cite a source that does not actually support the claim

---

## Consistent terminology

Pick one term and use it throughout. Do not mix synonyms for the same concept.

Examples from existing articles:
- "phase-gated workflow" — not "phased approach" or "staged process"
- "spec" — not "specification" (except in formal definitions)
- "state machine" — not "state diagram" or "FSM"
- "extension" — not "plugin" or "module"

---

## Character discipline

Use standard ASCII characters throughout. No typographic substitutions:

- Straight double quotes (`"`), not curly (`"` `"`)
- Straight apostrophes (`'`), not curly (`'` `'`)
- Hyphen-minus (`-`), not en dash (`–`) or em dash (`—`)
- Three periods (`...`), not the ellipsis character (`…`)
- Regular spaces, not non-breaking spaces

This is a hard rule, not a style preference. Markdown renderers and tooling handle ASCII reliably. Typographic characters introduce encoding inconsistencies and diff noise.

---

## Anti-patterns

These are hard bans. If you are about to write any of these, rewrite.

### Structural anti-patterns

- **No bullet-point summaries at the end of sections.** ("Key takeaways: ...")
- **No rhetorical questions as transitions.** ("But what does this mean for teams?")
- **No sections that repeat what the previous section already concluded.**
- **No unearned summary paragraphs.** A conclusion should make a specific claim, not restate what was said. This holds at sentence level too: if a new sentence paraphrases a claim already made earlier in the article, it is repetition even when the wording differs. Example: if an earlier section already states "you still need to decide which files are the declaration of a dependency and which files are only the materialized result," a closing sentence that says "it does not tell you which files are a dependency and which are project intent" is the same claim in different words, not a new one. Check paraphrases against earlier claims, not just exact-string matches.
- **No redundant section transitions.** Do not open a section by restating what the previous section already concluded. Do not close with "in the next section we will..." An opening sentence that frames the section's scope or connects to the prior argument is legitimate — it earns its place when it adds information or direction, not when it repeats.
- **No listification without purpose.** Lists are appropriate when items are parallel, scannable, or structurally independent. Prose is appropriate when the relationship between ideas matters more than the individual items. Do not default to either — choose deliberately.

### Prose anti-patterns

- **No typographic/smart characters.** Use standard ASCII characters only. Straight double quotes (`"`), not curly quotes (`"` `"`). Straight apostrophes (`'`), not curly ones (`'` `'`). No em dashes (`—`) or en dashes (`–`) — use commas, colons, semicolons, periods, or parentheses instead. No `--` either. No ellipsis character (`…`) — use three periods (`...`). No non-breaking spaces where regular spaces work. If the keyboard has a direct key for it, use it; if it requires a compose sequence or special input, don't.
- **No generic transitions.** "Furthermore," "Moreover," "Additionally," "In addition" — these are statistically overrepresented in AI output. Use structural transitions instead: name the remaining tension, state the next claim directly, or let the section break do the work.
- **No repeated rhetorical crutch constructions.** If the same sentence shape becomes the default way to state nearly every claim (e.g., "X is/is not enforced by Y" used five separate times across one article), it has become a tic, not a technique. Vary how a claim lands: name the mechanism once, the consequence another time, the exception a third time.
- **No excessive hedging.** "It could potentially be argued that..." "Some might say..." "While there are many perspectives..." — state the thing. If it is uncertain, say it is uncertain directly.
- **No passive voice where active works.** "It was decided that..." → "The team decided..."
- **No "it is worth noting that..."** — just say the thing.
- **No false specificity.** Do not claim precise statistics ("increased by 23.4%") without a source that confirms that exact number.
- **No overclaimed absolutes.** Words like "none," "nothing," "always," "never," "every," "all" read as confident, but they are categorical claims that must hold without exception. Verify the claim is true everywhere before using an absolute, and check it doesn't contradict something already established elsewhere in the article. If only part of the claim holds, scope it precisely instead of reaching for the absolute because it sounds more decisive.

  **Bad:**
  > None of this is enforced by Spec Kit.

  **Good:**
  > Spec Kit enforces version pins during bundle validation, but nothing stops a team from leaving every preset at the default priority, committing installed extension copies, or even changing commands in place that get overridden after the next update.
- **No colonated framing.** Any sentence shaped as [claim] + colon + [the actual content] is a throat-clearing device, no matter the exact wording. "The pattern is consistent: ...", "The test is simple: ...", "This is the X point in miniature: ...", and "That is the X to avoid: ..." are all the same shape. Mechanical check: delete everything before the colon. If the remainder stands on its own, the part before it was filler - cut it.
- **No AI-validation phrases.** "Great question!", "That's an insightful point", "It's important to consider..." — these are chat artifacts, not article prose.
- **No stating the obvious.** Do not narrate that a table, list, or example is about to appear, or restate what it already shows. "Extended Flow applies that rule directly:" tells the reader nothing the table below doesn't already show. Cut the announcement; let the table, list, or code speak for itself.

### Voice anti-patterns

- **No symmetrical structure disease.** Real writing has asymmetry. Not every section needs exactly three points. Not every paragraph needs the same structure.
- **No hedging to avoid commitment.** If the author has a position, state it. Articles that present every side equally without taking a stance are not balanced — they are evasive.
- **No over-explaining basics.** The audience understands systems thinking. Trust them.
- **No pseudo-philosophical inflation.** Do not dress up a small technical or organizational decision as a profound insight. "The case study only makes sense after the ownership rule is clear" inflates a file-split decision into something with stakes it doesn't have. State the technical fact plainly and let the reader judge its weight.

---

## Voice examples

These excerpts demonstrate the author's established voice. Match this register, rhythm, and directness.

### Example 1: Opening with a concrete scenario

> An agent gets a straightforward ticket: "Display the available overdraft limit on the mobile banking dashboard." It does what any good engineer would — it looks for existing patterns. It explores the AccountOrchestration API, spots dozens of existing synchronous REST calls to the CoreBanking_Legacy endpoint, and replicates the pattern to fetch the overdraft data. The code is clean, the unit tests pass, and the agent opens a Pull Request.
>
> Twenty minutes later, a senior engineer rejects it.

### Example 2: Making a precise technical claim

> The underlying mechanism is how attention works. Models do not process context uniformly — tokens at the beginning and end of the context window receive systematically more weight than those in the middle. Recency is a further pull: the closer a token is to the current generation point, the stronger its influence on the next prediction.

### Example 3: Naming a gap before offering the answer

> The first two gaps are structural — each has a clear engineering answer. The third is different. It goes to the question of what Spec Kit fundamentally believes a spec *is*.

### Example 4: Direct conclusion with a specific claim

> The wheel does not need reinventing. It needs moving.

### Example 5: First-person perspective used deliberately

> In my view, determinism in an agent pipeline means one specific thing: given a valid workflow state and a valid input, only valid transitions are possible, and the runtime rejects everything else.