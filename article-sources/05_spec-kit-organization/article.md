---
title: "How to Organize Your Spec-Kit Extensions, Presets, Workflows and Bundles"
author: "Markus Wondrak"
date: "2026-09-21"
excerpt: "The Spec-Kit docs explain each primitive. They do not tell you where a change belongs, what to version-control, or how a teammate reconstructs your setup from a clone. Field notes from running the Extended Flow bundle."
tags: ["Spec Kit", "Agentic Coding", "Workflow", "Best Practices"]
reading_time: "9 min read"
slug: "spec-kit-organization"
---

The Spec-Kit documentation describes extensions, presets, workflows, and bundles thoroughly — what each one is, how catalog resolution works, which CLI flags exist. What it does not answer are the operational questions that appear after the first month: where a specific change belongs, what should be committed, and how a teammate reconstructs your setup from a fresh clone.

These are field notes from building and running the [Spec-Kit Extended Flow](https://github.com/markuswondrak/spec-kit-extended-flow) bundle. Every claim below is tied to a concrete decision in that project.

## The extension/preset boundary is structural

The taxonomy is correct but easy to apply incorrectly. The rule that holds:

**A new command name requires an extension. A change to existing command or template content belongs in a preset.**

This is not a convention — it is enforced. Command names follow `speckit.<ext-id>.<cmd-name>`. When a preset registers a command with three or more dot segments, Spec Kit checks whether `.specify/extensions/<ext-id>/` exists. If it does not, the command is skipped.[^1] No error, no warning. The agent simply lacks the command. A preset can override a command that an installed extension or the core already provides; it cannot bring a new command into existence on its own.

Extended Flow is split along exactly this line:[^2]

| Component | Kind | Contents |
|---|---|---|
| Seven commands | Extension | `documentation`, `documentation-init`, `finish`, `project-init`, `quick-implement`, `quick-review`, `doc-check` |
| Templates + 14 overrides | Preset | `review-findings.md`, `documentation.md`, and a runtime preamble prepended to existing commands |

The split is functional. The extension can be versioned and reviewed as behavior; the preset can be replaced without removing commands.

## The runtime preamble pattern

The most useful preset pattern I have used: **one file composed onto many commands.**

Extended Flow's preset declares fourteen `type: command` entries, all pointing at the same file — `commands/workflow-runtime.md` — each with `strategy: prepend`.[^3] The file holds an unattended-runtime preamble: it tells the agent to stay inside the project and not block on a question.

Three decisions make this work:

1. **The preamble is declared once and composed at install time.** The single file is prepended to each target command, so the context is not duplicated fourteen times in the preset source.
2. **It is a preset, not an extension.** It changes the content of existing commands. It introduces nothing.
3. **Interactive commands are excluded deliberately.** `project-init` and `documentation-init` are bootstrap commands run by a human before the flows start. They must be allowed to ask questions, so they do not receive the preamble.[^3]

The pattern generalizes: any cross-cutting instruction that every automated command must carry — house style, guardrails, output conventions — belongs in a prepended preset file, not copy-pasted into each command.

## Pick priorities that leave room

Every preset defaults to priority `10`, and ties break alphabetically by preset id.[^4] Install everything at the default and your effective stack is arbitrary. Assign bands instead:

| Band | Priority | Contents |
|---|---|---|
| Base | 20 | Organizational standards, compliance |
| Methodology | 10 | Team process. Extended Flow pins its preset here.[^5] |
| Project | 5 | Localization, project-specific terminology |

Lower wins. When two presets both `replace` the same template, only the lower number is used — the other is ignored entirely, not merged. If two layers should compose, the lower-priority preset must declare `append`, `prepend`, or `wrap` for that file.

Extended Flow's bundle pins its preset at priority `10` with `strategy: append`.[^5] That reserves 1–9 for project-level overrides and 11+ for organizational layers, without touching the bundle.

## What to commit, what to ignore

`specify init` scaffolds a managed `.specify/.gitignore` that contains exactly two patterns:[^6]

```gitignore
feature.json
extensions/*/local-config.yml
```

That covers machine-local state only: the current-feature pointer and per-machine extension config overrides. It deliberately leaves the rest of `.specify/` shareable.

It does not answer the question that matters for a team: **should installed components be versioned?** The answer is no. Anything pulled from a catalog and not meant to be edited locally should not be committed. Its version is pinned in the catalog and in the bundle manifest — that is the source of truth, not a copy checked into git.

Add these rules to the managed file (your edits are preserved on re-init):[^6]

```gitignore
# Installed from catalogs. Reconstructed with `specify bundle install`.
.specify/extensions/*/*
!.specify/extensions/*/*-config.yml
.specify/presets/*
.specify/workflows/*
!.specify/workflows/overlays/

# Runtime state and caches.
.specify/workflows/runs/
.specify/workflows/.cache/
```

Two exceptions are explicit in the negation patterns:

- **Extension project config** (`<ext>-config.yml`) is not catalog-derived. It is project intent and stays tracked. Only the machine-local `local-config.yml` is ignored, which the managed block already handles.
- **Workflow overlays** (`.specify/workflows/overlays/`) are project-local customizations, and they live outside the installed workflow directory precisely so they survive updates.[^7]

<!-- EDITORIAL NOTE (open point 1): Decide before publishing whether to keep the `<ext>-config.yml` exception or take the harder line — ignore installed component trees entirely and manage extension config outside the repo. The user's stated principle ("catalog pulls should not be committed") leans toward the harder line; the exception is kept here because the official model tracks project config. Resolve one way and align the prose. -->

Everything not listed above stays committed: the constitution, templates, `.specify/integration.json`, catalog configuration (`.specify/*-catalogs.yml`, `.specify/extensions.yml`), specs, and bug reports.

Note the negation syntax. `.specify/extensions/*/*` ignores the *contents* of each extension directory but not the directory itself, which is what allows a top-level config file to be re-included. Ignoring `.specify/extensions/` wholesale would make that impossible — git cannot re-include a file inside an excluded directory.

## The reconstruction test

The gitignore decision has one acceptance criterion: **a fresh clone must reach a working state in at most two commands.**

```bash
git clone <repo> && cd <repo>
specify bundle install spec-kit-extended-flow
```

If restoring the project requires more than that — manual `specify extension add` calls, remembered priorities, a wiki page listing what to install — the bundle is under-specified. Every primitive that is gitignored must be owned by a bundle, and the bundle must pin it.

Run the test before trusting the setup. Delete `.specify/extensions/`, `.specify/presets/`, and `.specify/workflows/` from a working checkout, then reconstruct. If anything is missing, the bundle manifest is incomplete.

<!-- EDITORIAL NOTE (open point 2): Consider adding the runtime integration points here — `.specify/workflows/runs/current_run` and `.specify/feature.json` — as the surfaces tooling reads for run and feature state. Left out of the prose for now; decide whether they belong in this section or are out of scope for an organization-focused article. -->

## Release discipline

Installed components carry a version from two places: the component manifest and the bundle pin. If those can drift, `specify bundle info` stops being trustworthy.

Extended Flow uses a single-version policy. One release bumps the preset, the extension, the bundle manifest, all workflows, and the catalog pins to the same version. A `check-release.py` script verifies that every manifest, workflow, and catalog entry carries an identical version string before CI publishes, and fails the job on any mismatch.[^8]

The alternative — independent semver per primitive with strict pins in `bundle.yml` — is valid when components genuinely evolve on different cadences. What is not valid is a mixture: a shared version for some primitives and loose pins for others. That produces a bundle whose stated version no longer describes its contents.

## Anti-patterns

**Commands from a preset.** A preset that registers `speckit.someext.cmd` without `someext` installed is silently skipped. If you need a new command, ship an extension.

**Everything at default priority.** Five presets at priority `10` resolve alphabetically. Assign bands.

**Unpinned bundle entries.** A `bundle.yml` without explicit versions is not reproducible. Pin every component.

**Logic in workflow YAML.** Shell steps that grow beyond one command belong in a script under an extension. The workflow declares sequence; scripts implement behavior.

**Committing installed components.** A checked-in copy of a catalog extension drifts from the catalog the moment someone updates it. Pin the version, ignore the files, reconstruct on clone.

## Organization is a decision about reconstructability

The primitives are deliberately separated, and the docs explain why. What the docs leave to you is the operating model: where a change belongs (extension for new commands, preset for content changes), what is shared intent versus reconstructable install, and how a teammate gets from a clone to a running setup.

Decide those three things explicitly and `.specify/` stays predictable. Leave them implicit and you get the failure this article started from: a stack nobody can resolve, a bundle whose version means nothing, and a setup that only works on the machine where it was built.

---

[^1]: GitHub, "Preset System Architecture — github/spec-kit," `presets/ARCHITECTURE.md`, section "Extension safety check." <https://github.com/github/spec-kit/blob/main/presets/ARCHITECTURE.md>
[^2]: Markus Wondrak, "spec-kit-extended-flow — docs/reference.md," section "Architecture." <https://github.com/markuswondrak/spec-kit-extended-flow/blob/main/docs/reference.md>
[^3]: Markus Wondrak, "spec-kit-extended-flow — preset.yml." <https://github.com/markuswondrak/spec-kit-extended-flow/blob/main/preset.yml>
[^4]: GitHub, "Presets — github/spec-kit reference," sections "Install a Preset" and "List Installed Presets." <https://github.com/github/spec-kit/blob/main/docs/reference/presets.md>
[^5]: Markus Wondrak, "spec-kit-extended-flow — bundle.yml." <https://github.com/markuswondrak/spec-kit-extended-flow/blob/main/bundle.yml>
[^6]: GitHub, "Core Commands — github/spec-kit reference," section "Version control"; and `src/specify_cli/shared_infra.py` (`SPECIFY_GITIGNORE_CONTENT`). <https://github.com/github/spec-kit/blob/main/docs/reference/core.md>
[^7]: GitHub, "Workflows — github/spec-kit reference," section "Interaction with Bundles and Updates." <https://github.com/github/spec-kit/blob/main/docs/reference/workflows.md>
[^8]: Markus Wondrak, "spec-kit-extended-flow — docs/releasing.md." <https://github.com/markuswondrak/spec-kit-extended-flow/blob/main/docs/releasing.md>
