# Transition Analysis: "From Wiki to Source: How arc42 Becomes the Context Layer for AI Agents"

**File analyzed:** `02_documentation-agentic-coding/article.md`  
**Date:** 2026-05-01  
**Role:** Narrative Flow & Transition Enforcer

---

## Article Premise (Context)

The article argues:

1. Code is the source of truth for what a system *does*, but it cannot express what the system *should* do or *must not* do.
2. SDD wrongly tries to make specs the primary artifact.
3. The real answer is documentation-as-context-layer, living in-repo as Markdown, structured via arc42, loaded progressively.
4. The only genuine gap is AI-specific vocabulary, which RAD-AI fills.

**Narrative arc:** problem → wrong answer (SDD) → right framing (code = truth of state, docs = truth of intent) → what docs must do → what breaks without them → how to resolve conflicts → what good docs look like → arc42 already solves this → concrete implementation → conclusion.

---

## Identified Hard Jumps

### JUMP 1 — Lines 16 → 18 → 20

**Quote the Jump:**

> Line 16: *"Agents optimize for what is explicit, not what is intended."*
>
> Line 18: *"The instinctive industry response is Spec-Driven Development — shifting the source of truth away from code into natural-language specifications, and letting agents generate the implementation."*
>
> Line 20: *"The distinction that matters is between Code as Truth of State — what the system actually does — and Documentation as Truth of Intent — what it is allowed to do. The agent in this scenario had perfect knowledge of the first and none of the second."*

**Explain the Gap:**

The article establishes that agents lack intent context (line 16), then names SDD as the industry's response (line 18), then immediately introduces a two-part conceptual distinction (line 20) — all in three short paragraphs. The problem: the reader doesn't yet understand *why* SDD is the wrong response to the intent gap, so the distinction in line 20 lands without its motivating contrast. The article is about to spend an entire section arguing that SDD conflates these two truths, but the introduction previews the distinction before the reader understands what SDD claims and why that claim is wrong. The conceptual framework arrives before the argument that requires it.

**Bridge Options:**

1. **Explicit/Logical:** After line 18, add: "The appeal is understandable: if agents lack intent, give them a document that captures intent and make that document the source of truth. The problem is that this conflates two different things."

2. **Analogy-based:** After line 18, add: "It's a reasonable instinct — like handing someone a map when they keep getting lost. But the map is not the territory, and making the map authoritative over the territory creates a different kind of disorientation."

3. **Punchy:** After line 18, add: "SDD's answer to the intent gap is to promote the document above the code. That answer works only if the document stays synchronized with the code. It never does."

---

### JUMP 2 — Lines 32 → 34 ⚠️ CRITICAL

**Quote the Jump:**

> Line 32: *"The result is reactive engineering — significant development capacity spent on features whose value was never validated."*
>
> Line 34: *"Recognizing code as the source of truth is not the same as claiming code is self-explanatory. Code tells you what the system does. It does not tell you why decisions were made, what constraints apply, or what the architecture forbids. Those are distinct claims — and conflating them is what SDD exploits."*

**Explain the Gap:**

This is the article's most important pivot — and its hardest jump. For two sections, the article has been arguing *against* SDD and *for* code as the source of truth. The reader has been led to the position that specs are unreliable and code is authoritative. Now the article needs to pivot: "But code alone isn't enough either." The transition at line 34 makes this pivot, but it does so *without signaling that a pivot is happening*. The sentence "Recognizing code as the source of truth is not the same as claiming code is self-explanatory" introduces a new distinction (truth ≠ legibility) that fundamentally reframes the argument — but the reader hasn't been prepared for this reframing. The previous paragraph ended on SDD's structural failure (specs describe *what*, not *why*); the new paragraph introduces a distinction between two claims about code that the reader hasn't been asked to separate yet. The hidden assumption is: "We've established code is the truth; now I need to show you that truth and legibility are different properties of that truth." That assumption is never made explicit.

**Bridge Options:**

1. **Explicit/Logical:** Between lines 32 and 34, add: "This is the point where the argument could stop — and where most of the SDD debate does stop, with one side insisting code is all that matters and the other insisting specs must govern. Both positions miss the same thing. Code is authoritative about what the system does. That authority does not extend to explaining why it does it, what it is forbidden from doing, or what constraints shaped it."

2. **Analogy-based:** Between lines 32 and 34, add: "A circuit diagram is the authoritative description of what a board does. It is not a guide to why a particular resistor was chosen, or which traces must never be rerouted. The diagram is true. It is also incomplete — and the incompleteness is structural, not accidental."

3. **Punchy:** Between lines 32 and 34, add: "So far this reads like an argument for code supremacy. It isn't. Code is the truth of state. Documentation is the truth of intent. The next several sections are about the second — and about why conflating the two is exactly the mistake SDD makes, in the opposite direction."

---

### JUMP 3 — Lines 68 → 74

**Quote the Jump:**

> Line 68: *"For organizations operating under regulatory scrutiny, absent documentation is not a technical debt problem — it is a legal one."*
>
> Line 74: *"Treating documentation as essential context while maintaining that code is the source of truth creates a tension we cannot ignore: when the two disagree, which does the agent follow?"*

**Explain the Gap:**

The previous section ("What Breaks When Documentation Is Absent") ends on a regulatory/legal argument — absent documentation is a legal liability under the EU AI Act. The next section ("When Code and Documentation Conflict") opens with a philosophical tension about conflicting sources of truth. The reader has to make an unprepared leap from "documentation absence has legal consequences" to "documentation and code can contradict each other." The section that just concluded was about *absence* of documentation; the new section is about *conflict between* documentation and code. These are related but distinct problems, and the transition doesn't acknowledge the shift from "no docs" to "docs that disagree with code."

**Bridge Options:**

1. **Explicit/Logical:** Between lines 68 and 74, add: "Absence is one failure mode. Presence creates another. Documentation that exists but contradicts the code introduces a different kind of risk — and it is the one that surfaces when you take the previous sections seriously and actually add documentation to the repository."

2. **Analogy-based:** Between lines 68 and 74, add: "So far the argument has been about the damage caused by a map that doesn't exist. But a map that contradicts the terrain is a different kind of hazard — and it is the one that appears the moment you take the advice in this article and start writing things down."

3. **Punchy:** Between lines 68 and 74, add: "The case for documentation is established. The case against it is the next question: what happens when the documentation and the code say different things?"

---

### JUMP 4 — Lines 82 → 88

**Quote the Jump:**

> Line 82: *"The residual cases require human judgment, and that is a feature of the approach, not a gap in it."*
>
> Line 88: *"The obvious fix is to add documentation. But adding the wrong kind compounds the problem."*

**Explain the Gap:**

The previous section concluded a thorough argument about how code/documentation conflicts resolve (human-in-the-loop, PR-based synchronization). The new section opens with "The obvious fix is to add documentation" — but the article has been arguing *for* documentation for four consecutive sections already. The reader has been told documentation is essential (lines 38–56), that its absence causes drift and legal risk (lines 60–68), and that it should be treated as authoritative for intent (lines 72–82). Presenting "add documentation" as an "obvious fix" at this point reads as if the article is starting the argument over, rather than transitioning from *why* documentation matters to *what form* it should take.

**Bridge Options:**

1. **Explicit/Logical:** Replace line 88's opening with: "The previous sections established that documentation is not optional — it is the mechanism that makes code legible, prevents drift, and carries intent. The question is not whether to add it, but what form it should take. And here the wrong choice compounds the problem it is meant to solve."

2. **Analogy-based:** Replace line 88's opening with: "A map is only useful if it is drawn for the terrain and the traveler. Documentation is the same: the right structure makes agents faster and more accurate; the wrong structure makes them slower and more confused."

3. **Punchy:** Replace line 88's opening with: "More documentation is not better documentation. The wrong format, the wrong granularity, the wrong location — each of these can make the problem worse than no documentation at all."

---

### JUMP 5 — Lines 107–109 → 115

**Quote the Jump:**

> Line 107: *"Rules constrain. Examples teach. A documentation system needs both."*
>
> Line 109: *"A well-structured documentation set also includes a Gold Standard File: a single, perfectly formatted source file that serves as the absolute reference for all generation."*
>
> (Section break)
>
> Line 115: *"The properties described above — machine-readable, layered, living, concise — do not require a new framework to fulfill them."*

**Explain the Gap:**

The section "What Good Documentation Looks Like for Agents" has been listing properties: machine-readable, concise, living, layered, bad-faith test, gold standard file. The next section ("Architecture Documentation Must Evolve — and arc42 Already Shows You How") opens by referring back to "the properties described above" and asking whether a new framework is needed. The transition from specific implementation advice (Gold Standard Files, correct-vs-incorrect comparisons) to a meta-question about frameworks is abrupt. The reader is in the middle of concrete guidance and is suddenly asked to zoom out to a strategic question. The section also doesn't explicitly close the "what good docs look like" argument before shifting to "arc42 already does this."

**Bridge Options:**

1. **Explicit/Logical:** Before line 115, add a closing sentence to the previous section: "These six properties — machine-readable, concise, living, layered, bad-faith-tested, and example-grounded — define what agent documentation must be. The question is whether they require a new framework to achieve."

2. **Analogy-based:** Before line 115, add: "The blueprint for agent documentation is now clear. The question is whether it needs a new architect — or whether an existing one, with a few adjustments, already draws these plans."

3. **Punchy:** Before line 115, add: "Six properties. No new framework required — which is convenient, because one already exists."

---

### JUMP 6 — Lines 162 → 168

**Quote the Jump:**

> Line 162: *"§11 — Risks & Technical Debt is the exception that proves the rule. Standard arc42 has no machine-readable format for this section — it is prose, and prose technical debt registers produce no operational signal. The correct approach here is an AI Debt Register: a structured list of patterns present in the codebase that are known debt and must not be replicated by the next agent session. A pointer to this register belongs in Tier 1. The full content is Tier 3."*
>
> Line 168: *"A constraint that applies to the backend service is not a constraint that should consume context in a frontend session."*

**Explain the Gap:**

The three-tier model (just described in detail) addresses *what* to load and *when*. The nested inheritance model (introduced at line 168) addresses *where* to scope constraints. These are orthogonal concerns — loading tier vs. scoping location — but the transition doesn't acknowledge that the article is shifting from a loading strategy to a scoping strategy. The reader is still processing the tier model when a new concept (constraint scoping by directory) appears without being framed as a separate dimension of the same problem.

**Bridge Options:**

1. **Explicit/Logical:** Before line 168, add: "The three-tier model answers *what* to load. A second question — equally important — is *where* constraints apply. Not every rule is universal."

2. **Analogy-based:** Before line 168, add: "Tiering solves the depth problem: how much context to load. Scoping solves the breadth problem: which context applies where. A global constraint is a speed limit — it applies everywhere. A backend constraint is a weight restriction on a specific bridge — it applies only to the road that crosses it."

3. **Punchy:** Before line 168, add: "What to load is half the problem. The other half is where it applies."

---

### JUMP 7 — Lines 326 → 332

**Quote the Jump:**

> Line 326: *"These are not niche concerns — they are operational requirements for any system that relies on non-deterministic components, and any team operating without them is accruing decision debt at the same rate they are accruing code."*
>
> Line 332: *"The scenario from the opening section has a different outcome if this structure is in place."*

**Explain the Gap:**

The subsection "The Genuine Gap" (lines 318–326) introduced RAD-AI, AI Debt Registers, and extended ADR fields — all about vocabulary gaps in arc42 for AI-specific decisions. The next subsection ("What This Changes in Practice") jumps back to the opening banking scenario. The reader has to connect that the three-tier loading model (from much earlier) plus the RAD-AI vocabulary extension (just described) together resolve the opening scenario. But the article doesn't signal this synthesis — it just drops the reader back into the banking example.

**Bridge Options:**

1. **Explicit/Logical:** Before line 332, add: "The vocabulary gap is the last piece. With arc42's structure providing the framework, the three-tier model providing the loading strategy, nested inheritance providing the scoping, and RAD-AI providing the AI-specific vocabulary, the full picture is now in place. The question is whether it works."

2. **Analogy-based:** Before line 332, add: "The foundation, the floors, the wiring, and the signage are all specified. The only way to know if the building works is to walk through it."

3. **Punchy:** Before line 332, add: "Structure, loading, scoping, vocabulary. Four moves, one system. Time to replay the opening hand."

---

## Summary Table

| # | Location | Severity | Type |
|---|----------|----------|------|
| 1 | Lines 16→18→20 | Moderate-Hard | Conceptual distinction introduced before its motivating contrast |
| 2 | Lines 32→34 | **CRITICAL** | Pivot from "code is truth" to "code isn't enough" unprepared |
| 3 | Lines 68→74 | Hard | Leap from absence-as-legal-risk to presence-as-contradiction |
| 4 | Lines 82→88 | Moderate | "Add documentation" presented as new idea after 4 sections arguing for it |
| 5 | Lines 107→115 | Moderate | Concrete implementation advice → meta-question about frameworks |
| 6 | Lines 162→168 | Moderate-Hard | Loading strategy → scoping strategy without signaling orthogonal dimension |
| 7 | Lines 326→332 | Moderate | RAD-AI vocabulary → opening scenario replay without synthesis signal |

---

## Priority Recommendation

**Jump #2 (lines 32→34) requires immediate attention.** This is where the article's central argument pivots from "SDD is wrong because code is truth" to "but code alone can't give you what you need." If this transition fails, the reader either thinks the article is contradicting itself or loses the thread of why documentation matters. The article's entire thesis depends on the reader holding both positions simultaneously — code is the truth of state, documentation is the truth of intent — and this is the exact point where that dual position is introduced.
