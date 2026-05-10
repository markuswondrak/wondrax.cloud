# Style Reference

Examples drawn from this author's existing articles.

---

## Opening: Start With a Problem, Not Background

**Good — drops the reader into a real situation:**
> I haven't written a line of code by hand in the last months. Agents coordinate across repositories, write migration scripts, doing work in large codebases. The question is no longer whether this can work. It's how to structure the workflow so the agents remain coherent as complexity scales.

**Bad — starts with context:**
> AI-assisted development has become increasingly common. Many developers now use tools like GitHub Copilot and Cursor. This article evaluates GitHub's Spec Kit framework.

The first version creates a concrete world; the second restates what the reader already knows.

---

## Section Structure: One Claim Per Section

Each section heading states the core problem or finding. The section then proves it.

**Good:**
> ## No State Machine
> Spec Kit describes a workflow, but does not enforce one.

Everything that follows supports that single claim. The heading is not a label ("State Machine") — it is a verdict.

**Bad:**
> ## The State Machine in Spec Kit
> In this section we will look at how Spec Kit handles state transitions...

---

## Sachlich Tone: No Hedging, No Inflation

**Good:**
> Determinism in an agent pipeline means one specific thing: given a valid workflow state and a valid input, only valid transitions are possible, and the runtime rejects everything else.

**Bad:**
> Determinism could potentially be considered important in agent pipelines, as it might help ensure more reliable behavior in certain cases.

State the thing. If it is uncertain, say it is uncertain — don't use vague language as a hedge.

---

## Narrative Tension: Name the Gap Before Offering the Answer

The article builds toward a conclusion. Gaps and problems are named explicitly before solutions appear.

Pattern used in the spec-kit article:
1. Here is what Spec Kit does well (phase-gated workflow, extension system)
2. Here is the gap (no state machine, no distribution layer, no spec lifecycle model)
3. Here is what that means for enterprise use
4. Conclusion: right direction, specific remaining work

The reader should feel the weight of the problem before the resolution arrives.

---

## Transitions Between Sections

Sections connect explicitly. The last sentence of a section often signals what comes next — not with "in the next section" but by naming the remaining tension.

**Example from the article:**
> The first two gaps are operational — addressable with tooling investment. The third is different. It goes to the question of what Spec Kit fundamentally believes a spec *is*.

This transition does three things: closes the prior topic, signals a gear shift, and creates anticipation.

---

## Claim-First Within Paragraphs

Lead with the point, then support it.

**Good:**
> There is a cost to the convention model beyond correctness. Without enforced state, every agent call must carry enough workflow context for the agent to orient itself...

**Bad:**
> Without enforced state, every agent call must carry enough workflow context for the agent to orient itself... This means there is a cost to the convention model beyond correctness.

---

## Footnotes and Citations

- Cite claims that are not common knowledge
- Use numbered footnotes, not inline URLs in the prose
- Sources go in a ## Sources section at the end
- Never cite a source for a claim the source does not actually support

---

## Terms to Use Consistently

Pick one term and use it throughout. Do not mix synonyms for the same concept.

Examples from the spec-kit article:
- "phase-gated workflow" — not "phased approach" or "staged process"
- "spec" — not "specification" (except in formal definitions)
- "state machine" — not "state diagram" or "FSM"
- "extension" — not "plugin" or "module"

---

## What Not to Do

- No bullet-point summaries at the end of sections ("Key takeaways: ...")
- No rhetorical questions used as transitions ("But what does this mean for teams?")
- No passive voice where active is possible
- No "it is worth noting that..." — just say the thing
- No section that repeats what the previous section already concluded
