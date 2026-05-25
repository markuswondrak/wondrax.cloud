---
title: "State of Agent Skills: Format Portability Achieved; Composability, Scoping, and Execution Semantics to Be Defined"
author: "Markus Wondrak"
date: "2026-05-24"
excerpt: "The SKILL.md standard gives agents portable instructions, but its static nature creates real friction: probabilistic loading, no variables, no composition, no scoping, no tests. The solution is not to bloat Markdown into a programming language but to build orchestrators that resolve these gaps deterministically."
tags: ["Agentic Coding", "Skills", "Developer Experience", "Architecture"]
slug: "agent-skills-devex-gaps"
---

I was adding a new feature to [BriefCheck](https://briefcheck.app): new users should get a month of premium access for free after onboarding. A feature like this touches subscription state, trial periods, upgrade paths, and billing edge cases. The domain language matters. Does "free month" mean a trial that expires, or a grant that converts? Is the user a "trial user" or a "premium user on a promotional period". What happens to quota resets? Getting the terminology wrong cascades into wrong code.

I had read about Matt Pocock's `grill-with-docs` skill and wanted to try it. The skill runs a focused interview session that stress-tests a plan against the project's domain model, sharpens terminology when it drifts, and updates documentation inline so the clarification survives the conversation.[^8] It is exactly the kind of workflow discipline that keeps a context layer honest as the codebase outpaces the docs -- the same friction arc42 is meant to solve, and the same reason I had already put it in place as the context layer for agents.[^9]

So I had a look at the skill and found the mismatch immediately. It hardcodes a specific layout: the agent looks for a `CONTEXT.md` file at the project root, checks for a `CONTEXT-MAP.md` if the repo has multiple bounded contexts, finds ADRs under `docs/adr/`, and keeps the glossary implementation-free. My files live in different directories, under different names, with different conventions. The path assumptions are interleaved with the interview logic throughout the Markdown body. I could not override just the layout part, compose it with my own conventions, or declare a dependency on a "project layout" skill that `grill-with-docs` would pick up.

I started digging. How do skills compose? Can one skill depend on another? Can I inject project-specific context into a shared skill? The answer to every question was the same: the specification does not say.

That experience made me look closer. The Agent Skills specification has achieved broad adoption, but it leaves five operational topics open where there is room for optimisation. Here is what I want to look at in detail:

- **Composition.** How do skills relate to each other? There is no standard mechanism for one skill to build on another.
- **Variables.** How can a skill adapt to runtime context? Paths and configurations are currently static, with no standard way to inject dynamic values.
- **Triggers.** When should a skill be loaded? The current approach relies on description matching, which leaves room for more deterministic mechanisms.
- **Scoping.** Which skills apply where? In larger repositories, the rules for when a skill is active remain unspecified.
- **Tests.** How do you verify a skill works? There is no standard way to validate that a skill produces the intended behaviour.

---

## What a Skill Is

A skill is a directory with a `SKILL.md` file at its root. The frontmatter declares a `name` and a `description`. The `name` is the skill's identifier. The `description` is what the orchestrator—the agentic loop process that manages tool calls, context, and skill loading—uses to decide whether the skill is relevant to the current task.[^1]

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
2. Mirror the package structure: `src/main/java/com/example/Foo.java` → `src/test/java/com/example/FooTest.java`
3. Name the test class `{ClassUnderTest}Test`
4. Use the `@DisplayName` annotation to describe intent in plain English
5. Use AssertJ for assertions: `assertThat(result).isEqualTo(expected)`
6. Mock external dependencies with Mockito. Do not mock value objects or internal helpers
7. Cover: null inputs, empty collections, boundary values, and the happy path
```

Optionally, the directory can contain additional files: scripts the skill can reference, image assets, Mermaid diagrams, or supplementary Markdown files. The skill may instruct the model to read these files, but the specification does not enforce how they are structured or when they are loaded.[^1]

Skills are discovered in two ways. Global skills sit in a platform-specific directory (for example, `~/.config/opencode/skills/` or `~/.claude/skills/`) and are available in every session. Project-local skills live inside the repository itself, typically under a hidden directory like `.opencode/skills/` or `.claude/skills/`.[^2] Project skills travel with the codebase, so a team can commit its conventions to version control and every developer gets the same agent behaviour.

Activation works through progressive disclosure. Skills are not part of the default context. At startup, the orchestrator scans all skill directories and reads only the `name` and `description` fields. The full body stays on disk. When the user submits a task, the orchestrator compares the task text against the skill descriptions and decides which ones to load. Only then are the full instructions read and injected into the model's context.[^1]

An agent with fifty installed skills does not carry fifty instruction sets into every prompt. It carries fifty short descriptions and the full text of the few skills that matched the current task.

Because the format is just Markdown frontmatter plus a body, any tool that implements the discovery and loading rules can run the same skill. The same `SKILL.md` works in Claude Code, Cursor, OpenCode, and any other compliant orchestrator.[^1] That portability comes from deliberate restraint. The standard defines only what a skill is, not how it behaves once loaded — a minimalism that made adoption possible. Now that the format has proven itself, the next step is to address what it left open.

---

## No Composition: DRY Violations as a Maintenance Tax

If a "deployment" skill requires knowledge from a "build" skill, the current standard offers no way to express that dependency. The context has to be duplicated. When the build process changes, every skill that depends on it needs a manual update.

This is what blocked me with `grill-with-docs`. The skill assumes a specific documentation layout: `CONTEXT.md` at the root, ADRs under `docs/adr/`. My project structures documentation differently. The skill's path assumptions are interleaved with its interview logic throughout the Markdown body. There is no way to override just the layout part. I would have to fork the entire skill and maintain my own copy, or rewrite it from scratch. Both options defeat the point of a shared, portable skill format.

In a small project with three skills, this is manageable. In an enterprise codebase with dozens of skills maintained by different teams, it becomes a maintenance nightmare. A change to a foundational concept forces developers to manually find and update every `SKILL.md` that references it.

Issue #100 asks how skills should depend on other skills.[^4] The open questions are how to define dependencies, whether dependent skills auto-install, and whether users install them separately. There are no answers yet.

Issue #110 proposes a more formal approach: a `requires` field in the frontmatter that declares dependencies with version validation.[^5] A deployment skill could declare:

```yaml
requires:
  - skill: build-conventions
    version: "1.2.0"
  - skill: logging-standards
```

The validation runs at the tooling level, not at the agent level. The orchestrator checks that required skills exist and meet the version constraint before the skill becomes available. Circular dependencies are rejected. The agent never sees the `requires` field.

That is the correct boundary. Dependency resolution is a deterministic problem that belongs in the orchestrator. Delegating it to the model would mean the model sometimes loads dependent skills, sometimes does not, and has no way to report a missing dependency as an error.

Issue #137 raises a related concern: whether a skill can instruct the agent to invoke another skill by name.[^6] The specification is silent. Some implementations support it. Some do not. The behavior is inconsistent, which is exactly the portability problem the standard was designed to solve.

---

## No Variables: The Static Straitjacket

A `SKILL.md` file is static text. Paths, configurations, tool outputs, environment variables: none of these can be resolved at runtime within the standard. If a skill needs to know the current git branch or the project's package manager, it has two options: hardcode the value, or instruct the model to figure it out.

Hardcoding breaks portability. A skill that references `/home/user/project` works on one machine. Instructing the model to discover the value breaks reliability: the model might use the wrong command, skip the step, or hallucinate a value. The result is the same probabilistic behavior.

Issue #124 on the agentskills repository proposes dynamic context injection: an inline syntax where shell commands execute before the skill content is sent to the model.[^3] The proposal uses `` !`command` `` placeholders that the orchestrator resolves at invocation time. The model receives only the rendered output, never the command itself.

```yaml
---
name: pr-review
description: Review the current pull request
---

## Context

Changed files:
!`gh pr diff --name-only`

Diff:
!`gh pr diff`

## Instructions

Review the changes above for correctness and security issues.
```

Claude Code already implements this exact mechanism.[^2] The `` !`command` `` syntax executes before the model sees the skill content. Command output replaces the placeholder. Failure is explicit: a non-zero exit produces `[command failed: exit code 1]` rather than silent omission.

The proposal has been open since February 2026 without resolution.[^3] The specification remains silent on dynamic context. Skills that need live data remain either non-portable or unreliable.

The orchestrator, not the model, should resolve dynamic values before the LLM call. This keeps the skill format simple while removing the most common source of context-gathering fragility.

---

## Probabilistic Triggers: Skills as Polite Suggestions

The frustration is immediate. An orchestrator decides which skills to load based on the current task. In practice, this decision is probabilistic: the agent reads the skill descriptions, compares them to the conversation context, and makes a judgment call about relevance.

Sometimes that judgment is wrong. A skill with a clear `description` field that matches the current task can still be skipped. The model weighs the skill description against everything else in its context and decides to proceed without it.

Claude Code addresses this with a `paths` field in the frontmatter: glob patterns that limit when a skill is activated.[^2] Set `paths: ["*.dart"]` and Claude Code loads the skill automatically when working with Dart files. This is a deterministic trigger: the file extension matches, so the skill is injected. The orchestrator, not the model, makes the decision.

The Agent Skills specification does not define this mechanism. Claude Code implements it as a client-specific extension, which means the same `paths` field is meaningless to Gemini CLI, OpenHands, or any other tool. Portability breaks where reliability matters most.

The community has not yet proposed a standardized trigger mechanism for the specification. The `paths` approach is a natural candidate, but it needs to be part of the standard, not a client extension, to preserve the cross-product promise.

---

## Scope Confusion: Implicit Inheritance or Explicit Structure?

In a monorepo, different areas have different conventions. The frontend team uses different naming patterns than the backend team. A `code-style` skill at the root cannot serve both. The question is where skills should live, and how the orchestrator knows which ones apply.

Issue #115 proposes path-based, recursive skill discovery.[^7] Skills placed in subdirectories apply only when the agent is working in that area. A skill at `src/frontend/.agents/skills/react-patterns/` applies to `src/frontend/**`. Skills at parent directories inherit downward. The deepest match wins on name conflicts.

Claude Code already implements a version of this: project skills load from `.claude/skills/` in the starting directory and in every parent directory up to the repository root. When working in subdirectories, Claude Code also discovers nested skill directories on demand.[^2]

Path-based inheritance extends the progressive disclosure principle: skill availability scopes to the current work area, not the entire repository. It solves the monorepo problem. It also introduces implicit behavior that is difficult to debug. A developer working in `src/frontend/components/` inherits skills from four levels: root, `src/`, `src/frontend/`, and `src/frontend/components/`. A skill defined at the root level two years ago, forgotten by everyone, still applies. When it conflicts with a skill defined at the component level, the "deepest wins" rule resolves the conflict, but the developer may not know either skill is active. Debugging which skill influenced an agent's behavior requires tracing the entire directory chain.

Explicit scoping provides a cleaner alternative. Instead of implicit path-based inheritance, a skill could declare its scope in the frontmatter:

```yaml
scope: "src/frontend/**"
```

The orchestrator matches the scope against the current working path. No inheritance chain. No hidden skills from parent directories. The developer can see exactly which skills apply by reading the frontmatter, not by tracing the file system.

This is an architectural choice, not a feature request. Implicit inheritance optimizes for convenience in small projects. Explicit scoping optimizes for debuggability in large ones. The specification needs to choose, because the current silence means every implementation makes its own choice, and portability breaks again.

---

## No Tests: The Unvalidated Assumption

Verifying that a skill change does not break the agent's behavior requires prompting the agent and checking the output. If the output is wrong, the developer tweaks the skill and tries again. This is manual trial-and-error applied to a document that is supposed to be an executable instruction.

Every other artifact in a software project has a validation mechanism. Code has unit tests. Configuration has linters. Infrastructure has compliance checks. Skills have nothing.

Issue #110 proposes a `test` field that declares test cases for skill validation.[^5] The test format is agent-agnostic: assertions check whether the output contains or excludes specific strings, matches a regex, or satisfies a semantic criterion evaluated by an LLM judge.

```yaml
test:
  cases: test/cases.yaml
```

```yaml
cases:
  - name: select_dev
    input: "Select DEV environment"
    assertions:
      output_contains:
        - "DEV"
      output_not_contains:
        - "PROD"
```

The distinction between `output_contains` (deterministic string matching) and `semantic_match` (probabilistic LLM evaluation) is honest about what can be tested deterministically and what cannot. Deterministic assertions catch regressions in the skill's core behavior. Semantic assertions catch subtler drift.

This gap gets more expensive as skills get more complex. As skills become more complex and more central to how teams work with agents, the cost of undetected breakage increases. A skill that silently stops influencing the agent is worse than no skill at all: it gives the developer false confidence that a rule is being applied.

---

## The Pattern Behind the Gaps

Five gaps, one pattern. Each gap exists because the specification treats the `SKILL.md` file as a static document that the model interprets. Each proposed solution moves the responsibility from the model to the orchestrator.

Dependency resolution belongs in the orchestrator because it is graph validation, not prompt engineering. Variable resolution belongs in the orchestrator because it is shell execution, not language understanding. Triggers belong in the orchestrator because they are file-pattern matching, not semantic inference. Scope belongs in the orchestrator because it is path matching, not context interpretation. Test execution belongs in the orchestrator because it is deterministic validation, not subjective evaluation.

Deterministic operations should happen before the probabilistic LLM call. The model receives resolved, validated, scoped instructions. It does not discover, resolve, or validate them.

This is not a call to bloat the Markdown format into a programming language. The `SKILL.md` body should stay as instructions the model reads. The frontmatter should declare what the orchestrator needs to resolve: dependencies, variables, triggers, scope, tests. The orchestrator does the work. The model reads the result.

The Agent Skills specification has achieved broad adoption by being minimal. That was the right first move. The second move is to define the orchestrator contract: the set of deterministic operations every compliant tool must support before handing context to the model. Without it, every tool extends the standard in its own direction, and the cross-product promise erodes.

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
