---
title: "When Orchestrators Drift: Why Deterministic Pipelines Must Live Outside the Agent"
author: "Markus Wondrak"
date: "2026-05-10"
excerpt: "Agents are probabilistic by design. Hard workflow guarantees — phase gates, enforced sequencing, human checkpoints — cannot be achieved by giving an agent better instructions. They require a runtime that the agent cannot override."
tags: ["Agentic Coding", "Spec Kit", "Architecture", "Workflows"]
reading_time: "13 min read"
slug: "deterministic-pipelines"
---

The agent had been running for forty minutes. The task was clear: refactor the authentication module, write tests, open a PR. No surprises.

By minute twelve, it had drifted. Not dramatically — it still produced code, still ran the test suite, still committed incrementally. But the spec it had been given called for an architecture review before touching the token validation logic. The agent skipped it. Not because it decided to — it never decided anything. It moved to the next plausible step, because "next plausible step" is what the model does.

By minute forty, the test suite was passing. The authentication module had been refactored in a way that was syntactically correct, functionally coherent, and architecturally incompatible with the planned microservices migration. The agent had been consistent. Just not right. And because it had been consistent, the errors compounded quietly across every commit.

This is agentic drift. It is not a model quality problem. It is a structural consequence of asking a probabilistic system to manage its own workflow — and it gets worse the longer the session runs.

When you ask your agent how to mitigate that risk, it will suggest writing better instructions. Add emphasis. Make the constraint louder. I have done this. The system prompt began accumulating things like `IMPORTANT: DO NOT proceed to implementation before the architecture review is complete. YOU MUST ASK THE USER TO CONFIRM FIRST.` All caps. Exclamation marks. The model read those instructions with the same probabilistic attention it applied to everything else in the context window. Sometimes it complied. Under a long context with competing signals, it did not. The instructions had weight — not authority.

---

## Why Agents Drift

The underlying mechanism is how attention works. Models do not process context uniformly — tokens at the beginning and end of the context window receive systematically more weight than those in the middle.[^1] Recency is a further pull: the closer a token is to the current generation point, the stronger its influence on the next prediction. This means a constraint written in the system prompt does not get read once and retained. It competes continuously against everything that has accumulated between it and the current step — and that competition is structural, not a failure of model quality.

Session length is the practical consequence. The longer the session, the more tool outputs, intermediate results, and generated content accumulate between early instructions and the current generation point. A constraint established in the first ten minutes may have no practical weight by minute sixty — not because the agent decided to ignore it, but because it has been progressively outweighed by more recent material.

Phase discipline is the next casualty. A workflow that requires design before planning before implementation is a sequence of commitments. In a human workflow, something enforces those commitments: a ticket system, a review gate, a process that withholds the next step until the previous one is signed off. In an agent workflow that exists only as instructions in a prompt, the mechanism is the model's compliance with those instructions. Compliance is probabilistic. Under pressure — a long context, a complex task, conflicting signals — it degrades.

The third factor is stochastic divergence. Run the same agentic workflow twice with identical inputs and you will not get identical outputs. This is expected — it is not a defect. But it means that any workflow property you rely on is a statistical tendency, not a guarantee. The agent will usually check architecture constraints. It will usually run linting before committing. Under the load of a long context or an unlucky sampling path, it won't.

And the compounding dynamic in long sessions makes this worse: a small drift in step three becomes a larger constraint violation in step seven, because subsequent steps optimize for the current state — however that state was arrived at. By the end of a multi-hour session, the distance between what was intended and what was produced can be substantial, even though every individual step looked plausible.[^2]

---

## The Architecture That Should Work

The obvious engineering response follows directly from the drift diagnosis: if an agent drifts because it carries too much — too many phases, too many concerns, too long a session — the fix is to narrow its scope. Give each agent exactly one job. A researcher that only retrieves and summarizes. A coder that only implements a bounded task against a given spec. A reviewer that only evaluates output against defined criteria. Each worker has a short context, a single responsibility, and only the tools that responsibility requires.

This is the specialist-worker architecture. The researcher receives a question and returns structured findings. The coder receives a spec and a file list and returns a diff. The reviewer receives code and acceptance criteria and returns a pass/fail with notes. The context window for each call stays narrow. The drift surface shrinks proportionally. Each invocation is short enough that recency effects and the "lost in the middle" problem don't dominate. On paper, the architecture solves the problem that the single-agent approach could not.

But the workers don't coordinate themselves. Something has to decide which worker runs next, what output gets passed as input to the following step, whether the reviewer's rejection means retry or abort. The natural answer — the answer most teams reach — is to handle coordination with another agent. An orchestrator that receives the original goal, maintains the overall plan, dispatches workers in sequence, and synthesizes their outputs into a coherent result. It is a reasonable design. It is also the point where the original problem re-enters the system.

The orchestrator is an agent. It is subject to exactly the same attention mechanics established above. Its context window accumulates the outputs of every worker it has dispatched — research summaries, generated diffs, reviewer notes. Early decisions recede into the middle of a growing context: the architectural constraints agreed on at the start of the session, the scope boundaries defined before any code was written. The orchestrator's judgment about what the reviewer's output means, whether a failed test warrants a retry or a replanning, which worker should handle an unexpected edge case — all of that is probabilistic inference against a context that degrades over time. The specialist workers reduced drift at the leaf level. The orchestrator reintroduces it at the root.

The underlying assumption is that the orchestrator manages state coherently across the full session. In a short session with a tightly scoped task, this holds. Scale either dimension — session length or task complexity — and the assumption breaks for the same reasons it broke with the single agent.

---

## Structure Cannot Live Inside the Agent

This is the core problem, stated precisely: a deterministic property cannot be achieved through a probabilistic mechanism.

Software engineering requires determinism in specific places. A function call either succeeds or raises an exception. An API contract is met or it is not. A test passes or it fails. These are not approximations. They are boolean facts on which the rest of the system depends. When an agent is asked to *guarantee* that planning was completed before implementation began, the guarantee is only as strong as the model's disposition to comply.

The Dual-State Agent Process framework formalizes this as a separation between two state spaces.[^3] The first is $S_{workflow}$: the deterministic control flow — what states are legal, what transitions are permitted, what happens when a guard condition fails. The second is $S_{env}$: the stochastic environment where content is generated. These are fundamentally different concerns. $S_{env}$ is where the agent operates, and probabilistic behavior is appropriate there — that is the space where language model capabilities are relevant. $S_{workflow}$ must be engineered, not modeled.

Post-condition guards follow from this separation. Instead of trusting the agent to self-certify that a phase is complete, a deterministic guard function evaluates the output against defined criteria before the workflow advances. The agent produces content; the runtime decides what happens next. The agent can be wrong. The guard is not.

There is a cost beyond correctness when this separation is absent. Without enforced state, every agent call must carry enough workflow context for the model to orient itself: current phase, completed phases, applicable rules, transition criteria. It all goes into the system prompt. With a workflow state machine managing transitions externally, each call receives only the instructions scoped to the current state. The context is narrower, cheaper, and less susceptible to instruction decay toward the end of a long window.

The conclusion is uncomfortable but unavoidable. You cannot make an agent more deterministic by giving it better instructions. Instructions are processed by the same probabilistic mechanism that causes drift in the first place. The only way to enforce workflow structure is to move it outside the agent entirely — into an execution environment the agent cannot override.

---

## Engineering Already Has a Framework for This

The software development lifecycle is not a convention. It is a structure for managing context contamination and error accumulation across phases.

Hard phase separation exists because state bleeds. A developer who has been deep in implementation details for three days will make different architectural decisions than the same developer in a fresh design session. Phases enforce cognitive distance. They also enforce verification: you do not move from design to implementation until the design has been reviewed. Not reviewed by the person who produced it — reviewed by someone whose job is to evaluate it.

Quality gates are deterministic checkpoints. A pull request does not ask the developer whether the code is correct. The CI pipeline runs the tests, evaluates the result, and either gates the merge or lets it through. The developer's intent is not a factor. The outcome is a fact.

The parallel for agentic orchestration is exact. The agent should be a worker in a pipeline — skilled, generative, capable of producing output that no deterministic system could produce. But it should not be the pipeline. It should not decide when phases transition, whether its own output met the required criteria, or how many iterations a loop is allowed to run. Those are runtime properties. They belong in the execution environment.

The agentic workflow engine is the piece that most implementations are missing. It is what makes the rest of the architecture coherent.

---

## Spec-Kit's Workflow Engine

When I re-evaluated GitHub's Spec-Kit in April 2026, the primary structural gap I identified was the absence of an enforced state machine.[^4] The phase-gated workflow was well-designed and well-documented. But the mechanism that enforced phase transitions was the model's compliance with documentation — convention, not constraint. An agent could read the spec phase, declare itself done, and proceed directly to implementation. Nothing in the tooling prevented it.

The April 2026 release of the workflow engine is the direct answer to that gap.[^5] The architecture is clean: a workflow is a YAML file with a defined schema. The runtime is a deterministic orchestrator that reads the YAML, executes steps in sequence, and dispatches AI integrations as needed. The AI calls are one step type among several. The orchestrator does not delegate control to the model — it delegates a bounded task, collects the output, and decides what happens next.

**Step types** define the vocabulary:

| Type | Purpose |
|---|---|
| `command` | Invokes a Spec-Kit command (e.g., `speckit.plan`) |
| `gate` | Pauses for human review; `on_reject: abort` halts the workflow |
| `shell` | Executes shell commands without involving an agent |
| `prompt` | Sends a free-form prompt to the configured AI integration |
| `if` / `switch` | Conditional branching based on step outputs |
| `while` / `do-while` | Loops with a `max_iterations` safety limit |
| `fan-out` | Dispatches a collection in parallel with `max_concurrency` |
| `fan-in` | Collects all fan-out branches before proceeding |

The gate step is where the human-in-the-loop guarantee is actually implemented:

```yaml
- id: review-spec
  type: gate
  message: "Review the generated spec before planning."
  options: [approve, reject]
  on_reject: abort
```

The workflow stops here. Not "pauses and might continue" — stops. The agent has no mechanism to resume this run. Only `specify workflow resume <run-id>` after a human approval does that. The model cannot bypass a gate because the gate is enforced by the runtime, not requested of the model. The control surface is unambiguous: human approval is not a convention, it is a hard dependency.

Fan-out applies the same principle to parallelism. Instead of asking an agent to coordinate parallel tasks — which requires the model to manage concurrency, track completion, and decide when to collect results — the runtime handles all of it:

```yaml
- id: implement-parallel
  type: fan-out
  items: "{{ steps.tasks.output.task_list }}"
  max_concurrency: 3
  step:
    id: implement-task
    command: speckit.implement
    integration: "{{ item.preferred_integration | default('claude') }}"
    input:
      args: "{{ item.file }}"
```

Each task runs in a bounded parallel branch. `max_concurrency: 3` is enforced by the runtime — no agent decides how many tasks run at once. The agent implementing each task has no awareness of the other branches, which is correct: it should not.

The while loop shows the same constraint applied to iteration:

```yaml
- id: test-loop
  type: while
  condition: "{{ steps.run-tests.output.exit_code != 0 }}"
  max_iterations: 5
  steps:
    - id: fix
      command: speckit.implement
      input:
        args: "--fix {{ steps.run-tests.output.failures }}"
    - id: run-tests
      type: shell
      run: "npm test"
```

The agent iterates. `max_iterations: 5` means the loop cannot run indefinitely — not because the agent was instructed to stop, but because the runtime enforces the bound. The exit condition is evaluated deterministically on the shell step's output, not on the model's assessment of whether the tests are passing.

**Expressions** pass typed data between steps. `{{ steps.specify.output.file }}` routes a previous step's output as the next step's input. Branching conditions like `{{ steps.plan.output.task_count > 5 }}` are evaluated against concrete step outputs — not against the model's judgment. The expression language is a sandboxed Jinja2 subset with no file I/O, no imports, and no code injection surface.

**Multi-integration dispatch** allows different AI models per step. A planning step that requires sustained reasoning can specify Gemini 2.5 Pro with a thinking budget. An implementation step that benefits from code quality can use Claude Opus. The workflow declares this; each model at its step has no knowledge of what model ran before or will run after. The cognitive specialization is explicit in the configuration, not emergent from agent coordination.

**State persistence** ties the whole design together. Every workflow run stores its state under `.specify/workflows/runs/<run-id>/`: a `state.json` with the current step index and all step outputs, an `inputs.json` with resolved input values, and a `log.jsonl` append-only execution log. A paused run — whether paused at a gate or failed mid-execution — can be resumed exactly at the last completed step. Nothing is reconstructed from agent memory. The run state is a first-class artifact, independent of any model's context window.[^6]

This is what the Dual-State separation looks like in practice. $S_{workflow}$ is the YAML definition plus the runtime's execution state. $S_{env}$ is what happens inside each AI step. The two spaces are explicitly bounded, with no leakage in either direction.

---

## Getting Started

A workflow run starts with a single command:

```bash
specify workflow run speckit -i spec="Build a kanban board with drag-and-drop"
```

Three built-in variants ship with Spec-Kit. `speckit` runs the full SDD cycle: specify → gate → plan → gate → tasks → implement, with two human review checkpoints before any code is written. `speckit-quick` collapses to specify → implement for fast iteration on low-stakes changes. `speckit-review` runs specify → plan → gate → tasks without auto-implementation — useful when the intent is to produce a plan for human-driven execution.

A paused workflow resumes with `specify workflow resume <run-id>`. The catalog system distributes additional workflows via environment variable, project config, or user config, with a resolution order that makes org-wide overrides possible without touching individual project files. Custom workflows and extensions follow the same distribution path.

Presets standardize across teams. A preset packages template overrides for specs, plans, tasks, and agent instructions, and applies across every project that installs it. An organization can ship compliance constraints or domain-specific architectural standards once as a preset and apply them without forking anything.

---

## Conclusion

The phrase "intention as the new source of truth" captures something real. The shift from asking agents to produce code toward asking them to first produce, and then execute, a formal specification is a structural improvement. Intention stated explicitly before implementation begins is more auditable, more consistent, and more aligned with how engineering teams actually want to work.

But intention without enforcement is documentation. Teams have always documented their intentions. Documentation does not stop an agent from skipping the planning phase. It does not terminate a loop that runs to infinity. It does not create a human review checkpoint the model cannot bypass.

What the workflow engine provides is something different: intention that the execution environment enforces. The spec is reviewed before planning begins because the gate step blocks the runtime. The test loop terminates because `max_iterations: 5` is evaluated by the orchestrator. The AI call at each step receives a bounded task and no control over what comes next.

This is the correct architecture for agentic software development. Use agents for the generative work — the work where probabilistic behavior is the feature, not the defect. Own the structure through workflow design. The agent does not orchestrate the workflow. The workflow dispatches the agent.

[^1]: Nelson F. Liu et al., "Lost in the Middle: How Language Models Use Long Contexts," arXiv:2307.03172, 2023. <https://arxiv.org/abs/2307.03172>
[^2]: Matthew Thompson, "Managing the Stochastic: A Dual-State Agent Process Framework," arXiv:2512.20660, 2024. <https://arxiv.org/abs/2512.20660>
[^3]: Ibid. The paper formalizes the separation as $S_{workflow} \times S_{env}$, with guard functions $g: S_{workflow} \times Output \to \{pass, fail\}$ evaluated deterministically before any state transition.
[^4]: Markus Wondrak, "Re-evaluating GitHub's Spec Kit: Structured SDLC Automation," wondrax.cloud, April 2026. <https://markus.wondrax.cloud/articles/spec-kit-reevaluation.html>
[^5]: GitHub, "Workflow Engine — spec-kit Issue #2142," github.com, April 2026. <https://github.com/github/spec-kit/issues/2142>
[^6]: GitHub, "Workflow Reference — github/spec-kit," github.com. <https://github.com/github/spec-kit/blob/main/docs/reference/workflows.md>
