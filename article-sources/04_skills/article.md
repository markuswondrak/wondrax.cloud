---
title: "Keep Skills Dumb: The Orchestrator Contract for Portable Agent Context"
author: "Markus Wondrak"
date: "2026-05-25"
excerpt: "The SKILL.md standard succeeds because it is minimal. The gaps around variables, composition, scoping, and triggers are real, but the wrong response is to turn Markdown into a scripting language. The right response is a sharp architectural split: skills stay declarative, and the orchestrator grows up."
tags: ["Agentic Coding", "Skills", "Developer Experience", "Architecture"]
slug: "agent-skills-devex-gaps"
---

I was adding a new feature to [BriefCheck](https://briefcheck.app): new users should get a month of premium access for free after onboarding. The change touches subscription state, trial periods, upgrade paths, and billing edge cases. The domain language matters. Does "free month" mean a trial that expires, or a grant that converts? Is the user a "trial user" or a "premium user on a promotional period"? Getting the terminology wrong cascades into wrong code. I needed a way to keep the domain model in front of the agent while we worked through the implementation.

I had read about Matt Pocock's `grill-with-docs` skill and wanted to try it for exactly this kind of problem. The skill runs a focused interview session that stress-tests a plan against the project's domain model, sharpens terminology when it drifts, and updates documentation inline so the clarification survives the conversation.[^8] It is exactly the kind of workflow discipline that keeps a context layer honest as the codebase outpaces the docs, the same friction arc42 is meant to solve, and the same reason I had already put it in place as the context layer for agents.[^9]

This is exactly what a skill does well. It is pure context: terminology, constraints, and rules that the model reads before it writes code. No ambiguity about state transitions, no drift in naming.[^8]

So I had a look at the skill and found the wall immediately. It hardcodes a specific layout: the agent looks for a `CONTEXT.md` file at the project root, checks for a `CONTEXT-MAP.md` if the repo has multiple bounded contexts, finds ADRs under `docs/adr/`, and keeps the glossary implementation-free. My files live in different directories, under different names, with different conventions. The path assumptions are interleaved with the interview logic throughout the Markdown body.

The skill is not wrong. It is a perfectly good piece of declarative context. The problem is that static text cannot adapt to different project layouts. A skill that assumes `docs/adr/` breaks in a repository that uses `architecture/decisions/`. This is a portability problem, not a missing language feature. The solution is not to make the skill smarter. It is to make the orchestrator responsible for bridging the gap between the skill's abstract intent and the project's concrete reality.

That experience made me look closer. The Agent Skills specification has achieved broad adoption by staying minimal.[^1] It defines what a skill is: a Markdown file with frontmatter that an orchestrator loads into context. It deliberately does not define how the orchestrator resolves, scopes, or adapts that context. That restraint made portability possible. Now the same restraint creates friction in five areas where the orchestrator contract is undefined.

---

## What a Skill Is, and What It Is Not

A skill has one job: give the model the right context for a specific kind of task. It is the mechanism behind `grill-with-docs` running a focused interview, a Java test skill enforcing JUnit 5 conventions, or a deployment skill knowing to verify rollback procedures.

On disk, it is a directory with a `SKILL.md` file at its root. The frontmatter declares a `name` and a `description`. The `name` is the skill's identifier. The `description` is what the orchestrator uses to decide whether the skill is relevant to the current task.[^1]

The body of `SKILL.md` contains instructions written for the model: constraints, workflow steps, style rules, or domain context. The format is Markdown. There is no special syntax for variables, conditionals, or includes. Everything the model sees is plain text that the author wrote in advance.[^1]

A minimal skill looks like this:

```markdown
---
name: java-tests
description: Generate JUnit 5 unit tests for Java classes
---

## Instructions

When asked to write tests for a Java class:

1. Use JUnit 5. Prefer `@ParameterizedTest` over duplicated test cases
2. Mirror the package structure: `src/main/java/com/example/Foo.java` -> `src/test/java/com/example/FooTest.java`
3. Name the test class `{ClassUnderTest}Test`
4. Use the `@DisplayName` annotation to describe intent in plain English
5. Use AssertJ for assertions: `assertThat(result).isEqualTo(expected)`
6. Mock external dependencies with Mockito. Do not mock value objects or internal helpers
7. Cover: null inputs, empty collections, boundary values, and the happy path
```

Optionally, the directory can contain additional files: image assets, Mermaid diagrams, or supplementary Markdown files. The skill may instruct the model to read these files, but the specification does not enforce how they are structured or when they are loaded.[^1]

Skills are discovered in two ways. Global skills sit in a platform-specific directory and are available in every session. Project-local skills live inside the repository itself, typically under a hidden directory like `.opencode/skills/` or `.claude/skills/`.[^2] Project skills travel with the codebase, so a team can commit its conventions to version control and every developer gets the same agent behaviour.

Activation works through progressive disclosure. At startup, the orchestrator scans all skill directories and reads only the `name` and `description` fields. The full body stays on disk. When the user submits a task, the orchestrator compares the task text against the skill descriptions and decides which ones to load. Only then are the full instructions read and injected into the model's context.[^1]

When the model gets this wrong, a skill is silently skipped.

This is the critical boundary. A skill does not execute. It does not call tools, run shell commands, or make decisions about when it applies. It is context that the model reads. Any behaviour beyond that belongs in the orchestrator. The current friction comes from a blurry line where the community asks the skill format to do orchestration work because the orchestrator contract is undefined.

The first of these five gaps appears in the simplest place: variable resolution. Because a `SKILL.md` file is static text, every path and configuration value must be baked directly into the document.

---

## Variables: Template Placeholders, Not Runtime State

A `SKILL.md` file is static text. Paths, configurations, and conventions are baked into the document. If a skill needs to know where architectural decisions are recorded, it has two bad options: hardcode the path, or instruct the model to discover it.

Hardcoding breaks portability. A skill that references `docs/adr/` fails in any project that uses a different layout. Instructing the model to discover the value breaks reliability. The model might search the wrong directory, skip the step, or hallucinate a path. Both options undermine the cross-product promise.

Issue #124 proposes dynamic context injection: an inline syntax where shell commands execute before the skill content is sent to the model.[^3] The proposal uses `` !`command` `` placeholders that the orchestrator resolves at invocation time. Claude Code already implements this exact mechanism.[^2]

This is the wrong direction. Embedding shell commands inside a skill turns declarative context into an executable script. The skill now holds runtime state and side effects. It is no longer a portable document that any orchestrator can load. It is a program that requires a specific runtime.

The correct mechanism is simpler. A skill should declare template placeholders that the orchestrator resolves from project metadata before the model sees the text.

```yaml
---
name: grill-with-docs
description: Stress-test plans against the domain model
variables:
  ADR_PATH: "docs/adr/"
  CONTEXT_FILE: "CONTEXT.md"
---

## Instructions

Read the architectural decisions from {{ ADR_PATH }} and the domain glossary from {{ CONTEXT_FILE }}. Conduct an interview...
```

The orchestrator replaces `{{ ADR_PATH }}` with the actual path, resolved from project configuration. That resolution must be deterministic: the same project state always produces the same rendered text. The model receives only the rendered text. The skill itself remains stateless, side-effect free, and executable on any compliant orchestrator. The variable is not a command to run. It is a contract that says: this skill needs this piece of context, and the orchestrator must provide it.

The distinction is architectural. Dynamic context injection asks the skill to gather its own dependencies. Template resolution asks the orchestrator to prepare the context. Gathering belongs in the pipeline. The skill should only describe what it needs. Template placeholders solve portability. They do not solve the question of when a skill should be loaded at all.

---

## Triggers and Scoping: The Orchestrator Decides, Not the Model

The current activation mechanism is probabilistic. The orchestrator presents skill descriptions to the model, and the model decides which ones are relevant. Sometimes it gets this wrong. A skill with a clear `description` that matches the current task can still be skipped because the model weighs it against everything else in the prompt and decides to proceed without it.[^1]

This is backwards. The model should not guess which context it needs. The orchestrator should know.

Claude Code addresses this with a `paths` field in the frontmatter: glob patterns that limit when a skill is activated.[^2] Set `paths: ["*.dart"]` and Claude Code loads the skill automatically when working with Dart files. This is a deterministic trigger. The orchestrator matches the file pattern and injects the skill. The model does not get a vote.

The Agent Skills specification does not define this mechanism. Claude Code implements it as a client-specific extension, which means the same `paths` field is meaningless to Gemini CLI, OpenHands, or any other tool. Portability breaks where reliability matters most.

Portability across tools is only one dimension of the activation problem. Inside a single repository, the same lack of deterministic rules produces a different but equally painful symptom. In a monorepo, different areas have different conventions. The frontend team uses different patterns than the backend team. A `code-style` skill at the root cannot serve both.

Issue #115 proposes path-based, recursive skill discovery.[^7] Skills placed in subdirectories apply only when the agent is working in that area. Claude Code already implements a version of this: project skills load from `.claude/skills/` in the starting directory and in every parent directory up to the repository root.[^2]

Path-based inheritance solves the monorepo problem, but it introduces implicit behaviour that is difficult to debug. A developer working in `src/frontend/components/` inherits skills from four levels. A skill defined at the root two years ago, forgotten by everyone, still applies. When it conflicts with a skill at the component level, the "deepest wins" rule resolves the conflict, but the developer may not know either skill is active.

Explicit scoping in the frontmatter is the cleaner alternative:

```yaml
scope: "src/frontend/**"
```

The orchestrator matches the scope against the current working path. No inheritance chain. No hidden skills from parent directories. The developer can see exactly which skills apply by reading the frontmatter, not by tracing the file system.

Trigger and scope are not suggestions for the model to consider. They are hard rules for the orchestrator to enforce. The model receives only the context that the orchestrator has determined is relevant. It does not select, filter, or override. Deterministic scoping tells the orchestrator which context to load. It does not say how multiple contexts should be combined.

---

## Composition: Context Merging, Not Dependency Chains

Consider two skills: one that defines deployment conventions, one that defines build verification. Both need to know where build artifacts are placed. Currently each skill must hardcode that path. Change the output directory once, and you hunt through every `SKILL.md` that references it.

This is what blocked me with `grill-with-docs`. The skill assumes a specific documentation layout. My project structures documentation differently. There is no way to override just the layout part. I would have to fork the entire skill and maintain my own copy. Both options defeat the point of a shared, portable format.

The obvious response to this duplication and override problem is to let skills share values by referencing one another. The community has followed that instinct, but the resulting proposals drift toward imperative dependency management. Issue #100 asks how skills should depend on other skills.[^4] Issue #110 proposes a `requires` field in the frontmatter that declares dependencies with version validation.[^5] Discussion #210 takes this further with a full `skills.json` manifest and lockfile, modeled on `package.json` and `go.mod`.[^11]

These proposals treat skills like software packages that call each other. A deployment skill `requires` a build-conventions skill, which implies an execution chain: load A, then load B, pipe output from A into B. That is not what skills are. Skills do not execute. They do not have outputs to pipe. They are text that the model reads.

The correct model for composition is context merging. If a development task needs domain vocabulary, API conventions, and testing standards, the orchestrator loads all three skill documents and presents them as a unified context block. The model reads the merged text and acts on the combined constraints. There is no "calling" of one skill by another. There is no sequencing or state passing. There is only the orchestrator's responsibility to assemble the right documents before the LLM call.

The shared-value problem is already solved by template variables. Each skill declares the paths it needs as variables in its frontmatter. The orchestrator resolves them from the same project configuration before injecting any skill into context. Two skills that reference `{{ ARTIFACT_PATH }}` get the same value without knowing about each other. Activation handles the rest: when multiple skills have matching scopes for the current task, the orchestrator loads them all and presents the concatenated text as a single instruction set. The model does not see boundaries between skills. It sees one coherent document.

This preserves the deterministic separation between pipeline and agent. The orchestrator handles graph validation and text assembly. The model handles generative work. That separation is the central argument of the Spec-Kit workflow engine analysis, and it applies directly to skills.[^10] The same separation governs how we validate skills. A skill is not code to execute, so its test is not a unit test for behaviour.

---

## Tests: Semantic Validation, Not Code Verification

Verifying that a skill change does not break the agent's behaviour requires prompting the agent and checking the output. If the output is wrong, the developer tweaks the skill and tries again. This is manual trial-and-error applied to a document that is supposed to govern behaviour.

Every other artifact in a software project has a validation mechanism. Code has unit tests. Configuration has linters. Infrastructure has compliance checks. Skills have nothing.

Issue #110 proposes a `test` field that declares test cases for skill validation.[^5] The test format checks whether the output contains or excludes specific strings, matches a regex, or satisfies a semantic criterion evaluated by an LLM judge.

The intuition behind testing is correct. The implementation must respect what a skill actually is. A skill test is not a unit test for code execution. It is a semantic validation of context quality.

Does the model still understand that "promotional period" and "trial" are different states after the skill text was refactored? Does it still respect the rule that ADRs must not reference implementation details when the skill document was shortened to fit a smaller context window? These are the questions a skill test must answer.

```yaml
test:
  cases:
    - name: promotional_period_is_not_trial
      input: "A user is in a promotional period. What happens to their quota?"
      assertions:
        semantic_match: "The response must distinguish a promotional period from a trial and describe the quota reset policy for promotional users."
```

The assertion checks whether the model's output reflects the domain rule as stated in the skill. It does not check whether the model wrote correct code. It checks whether the context was transmitted intact.

Deterministic assertions catch regressions in the skill's core behaviour. Semantic assertions catch subtler drift in how the model interprets the text. Both belong in the orchestrator, which runs the validation loop before the skill is accepted into the project's trusted context set.

---

## The Orchestrator Contract: Let Skills Stay Dumb

Five gaps, one cause. Each gap exists because the specification treats the `SKILL.md` file as a document that must do everything itself. The community responds by asking for more features in the format: variables, conditionals, dependencies, execution hooks. That response turns skills into a scripting language and destroys the portability that made them valuable.

The correct response is the opposite. The `SKILL.md` format should stay as minimal as possible. It should declare what it is, what it needs, and where it applies. The orchestrator should do everything else.

Template resolution belongs in the orchestrator because it is metadata substitution, not language generation. Trigger and scope belong in the orchestrator because they are pattern matching, not semantic inference. Composition belongs in the orchestrator because it is document assembly, not reasoning. Test execution belongs in the orchestrator because it is deterministic validation, not subjective evaluation.

The community is not really asking for a richer skill format. It is asking for a standardised pipeline specification that lives parallel to the skills and defines how an orchestrator resolves, scopes, merges, and validates them. That specification does not exist yet. The Agent Skills specification defines the document. It does not define the runtime.

The first specification made the right call. Minimalism enabled adoption. The second specification must define the orchestrator contract: the set of deterministic operations every compliant tool must perform before handing context to the model. Without that contract, every tool extends the standard in its own direction, and the cross-product promise erodes.

Skills are context. The orchestrator is the pipeline. Keep them separate, and both can stay honest.

---

## Sources

[^1]: Agent Skills Specification, agentskills.io. <https://agentskills.io/specification>
[^2]: Anthropic, "Extend Claude with skills," Claude Code Documentation. <https://docs.anthropic.com/en/docs/claude-code/skills>
[^3]: digitarald, "Proposal: Dynamic context injection in SKILL.md," agentskills/agentskills Issue #124, February 6, 2026. <https://github.com/agentskills/agentskills/issues/124>
[^4]: marcofranssen, "Best practice on having a skill use/depend on other skills," agentskills/agentskills Issue #100, January 22, 2026. <https://github.com/agentskills/agentskills/issues/100>
[^5]: AndoSan84, "Adding Skill Dependencies with Version Validation + Testing Specification," agentskills/agentskills Issue #110, January 28, 2026. <https://github.com/agentskills/agentskills/issues/110>
[^6]: PaulRBerg, "Clarify whether nested skills are allowed," agentskills/agentskills Issue #137, February 12, 2026. <https://github.com/agentskills/agentskills/issues/137>
[^7]: lcs-bdr, "Proposal: add path-based, recursive skill discovery," agentskills/agentskills Issue #115, February 2, 2026. <https://github.com/agentskills/agentskills/issues/115>
[^8]: Matt Pocock, "grill-with-docs" skill, mattpocock/skills repository. <https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md>
[^9]: Markus Wondrak, "From Wiki to Source: How arc42 Becomes the Context Layer for AI Agents," 2026. <https://wondrax.cloud/articles/documentation-agentic-coding>
[^10]: Markus Wondrak, "The Agent is not the Pipeline: Spec-Kit Workflows and the Enforcement Layer," 2026. <https://wondrax.cloud/articles/deterministic-pipelines>
[^11]: erdemtuna, "Proposal: Skill Package Manifest for Dependency Resolution and Distribution for Agent Skills," agentskills/agentskills Discussion #210, March 5, 2026. <https://github.com/agentskills/agentskills/discussions/210>
