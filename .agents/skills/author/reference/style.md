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
- **No unearned summary paragraphs.** A conclusion should make a specific claim, not restate what was said.
- **No redundant section transitions.** Do not open a section by restating what the previous section already concluded. Do not close with "in the next section we will..." An opening sentence that frames the section's scope or connects to the prior argument is legitimate — it earns its place when it adds information or direction, not when it repeats.
- **No listification without purpose.** Lists are appropriate when items are parallel, scannable, or structurally independent. Prose is appropriate when the relationship between ideas matters more than the individual items. Do not default to either — choose deliberately.

### Prose anti-patterns

- **No typographic/smart characters.** Use standard ASCII characters only. Straight double quotes (`"`), not curly quotes (`"` `"`). Straight apostrophes (`'`), not curly ones (`'` `'`). No em dashes (`—`) or en dashes (`–`) — use commas, colons, semicolons, periods, or parentheses instead. No `--` either. No ellipsis character (`…`) — use three periods (`...`). No non-breaking spaces where regular spaces work. If the keyboard has a direct key for it, use it; if it requires a compose sequence or special input, don't.
- **No generic transitions.** "Furthermore," "Moreover," "Additionally," "In addition" — these are statistically overrepresented in AI output. Use structural transitions instead: name the remaining tension, state the next claim directly, or let the section break do the work.
- **No excessive hedging.** "It could potentially be argued that..." "Some might say..." "While there are many perspectives..." — state the thing. If it is uncertain, say it is uncertain directly.
- **No passive voice where active works.** "It was decided that..." → "The team decided..."
- **No "it is worth noting that..."** — just say the thing.
- **No false specificity.** Do not claim precise statistics ("increased by 23.4%") without a source that confirms that exact number.
- **No colonated framing.** Sentences like "The pattern is consistent: ...", "The common principle: ...", or "The solution is straightforward: ..." use a subject+colon structure as a throat-clearing device. They delay the claim and sound like a slide deck. State the thing directly without the framing prefix.
- **No AI-validation phrases.** "Great question!", "That's an insightful point", "It's important to consider..." — these are chat artifacts, not article prose.

### Voice anti-patterns

- **No symmetrical structure disease.** Real writing has asymmetry. Not every section needs exactly three points. Not every paragraph needs the same structure.
- **No hedging to avoid commitment.** If the author has a position, state it. Articles that present every side equally without taking a stance are not balanced — they are evasive.
- **No over-explaining basics.** The audience understands systems thinking. Trust them.

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