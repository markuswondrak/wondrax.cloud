## Title Ideas

* Agent Skills in the Crucible: Where the SKILL.md Format (Still) Fails
* Why Agent Skills Need More Software Engineering: DevEx Gaps in the Markdown Standard
* Static Markdowns, Dynamic Problems: The Missing Glue for Agentic Coding

---

## Outline: The Missing Pieces in Agent Skills

### 1. Introduction: The Ceiling of Static Instructions

* **The Hook:** AI coding agents are rapidly evolving from simple chat assistants into deeply integrated development partners. To give them context and project-specific rules, the ecosystem relies on standardized instruction files—but these static formats are currently hitting a hard ceiling.
* **The Thesis:** While the `SKILL.md` paradigm is a great starting point for portability, its rigid, static nature causes major Developer Experience (DevEx) friction in real-world projects. For agents to scale reliably in complex codebases, their skills need to become dynamic, predictable, and maintainable.
* **Goal of the Article:** Taking inventory of the biggest architectural gaps in current agent skill formats and examining the solutions currently debated within the open-source community.

### 2. The Trigger Problem: When Skills are Just "Polite Suggestions"

* **The Problem:** Orchestrators often load skills probabilistically (e.g., via vector search on the current task). Despite highly detailed documentation, the agent might simply decide to ignore the provided context and hallucinate a generic solution based on its training data.
* **DevEx Impact:** Pure frustration caused by black-box behavior. Developers spend time crafting precise rules that are only applied "with a bit of luck."
* **The Solution:** The need for "Hard Enforcement" mechanisms (e.g., file-pattern matching in the YAML frontmatter like `trigger_on_files: ["*.dart"]`), where the orchestrator *must* inject the skill into the context as an absolute system rule.

### 3. Static Straitjackets: The Missing Context Injection

* **The Problem:** Markdown files lack variables. Paths, configurations, or the outputs of local tools currently have to be hardcoded, which completely breaks the portability of skills across different environments or projects.
* **The Community Discussion:** The orchestrator engine needs to become smarter and resolve templates or shell commands right before the LLM call, rather than turning Markdown itself into a complex programming language.
* **Sources & References:**
* *[Issue #124] Proposal: Dynamic context injection in SKILL.md* ([github.com/agentskills/agentskills/issues/124]()) – The central debate on resolving environment variables (like `{{WORKSPACE_ROOT}}`) and dynamic context at runtime.



### 4. The DRY Problem: Composition and "Skill Technical Debt"

* **The Problem:** There is no standardized way for one skill to build upon another. If a "Deployment" skill requires knowledge from a "Build" skill, the context usually has to be duplicated.
* **DevEx Impact:** A maintenance nightmare. Changes to foundational concepts force developers to manually update dozens of different `SKILL.md` files (violating the DRY principle).
* **The Community Discussion:** Approaches for formal skill dependencies and dependency resolution by the orchestrator prior to sending the prompt to the model.
* **Sources & References:**
* *[Issue #100] Best practice on having a skill use/depend on other skills* ([github.com/agentskills/agentskills/issues/100]()) – Discussion on avoiding redundancy.
* *[Issue #110] Adding Skill Dependencies with Version Validation* ([github.com/agentskills/agentskills/issues/110]()) – Enterprise-focused proposal with hard declarations of "Base Skills."



### 5. The Scope Conflict: Magic Inheritance vs. Deterministic Structure

* **The Problem:** Determining the boundaries of a skill. How does the agent know if a skill applies globally to the entire repository or only locally to a specific subdirectory?
* **The Architectural Debate:** Parts of the community lean toward implicit, path-based inheritance (child folders inherit skills from parent folders). From a systems architecture perspective, relying on "magic" implicit inheritance is dangerous and leads to side effects that are incredibly hard to debug. Explicit scoping and imports provide a much cleaner, deterministic alternative.
* **Sources & References:**
* *[Issue #115] Proposal: add path-based, recursive skill discovery* ([github.com/agentskills/agentskills/issues/115]()) – The push for context inheritance via the file system.
* *[Issue #137] Clarify whether nested skills are allowed* ([github.com/agentskills/agentskills/issues/137]()) – Legitimation of nested skill hierarchies.



### 6. Outlook: Testability for the "Agent OS"

* **The Blind Spot:** How do you validate a refactoring within a `SKILL.md`? Currently, the only way is through manual trial-and-error prompting in the chat.
* **The Vision:** The necessity of "Skill Test Suites"—small, deterministic assertions (Mocks) that ensure changes to the documentation do not break the agent's fundamental understanding of the codebase.

### 7. Conclusion

* **Summary:** The Markdown standard itself shouldn't be bloated into a programming language. The solution lies in more capable orchestrators that deterministically resolve injection, composition, and triggers *before* handing over control to the probabilistic LLM.
