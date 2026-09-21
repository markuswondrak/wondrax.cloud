---
title: "How to Organize Your Spec-Kit Extensions, Presets, Workflows and Bundles"
author: "Markus Wondrak"
date: "2026-09-21"
excerpt: "The Spec-Kit docs explain each primitive. They do not tell you where a change belongs, what to version-control, or how a teammate reconstructs your setup from a clone. Field notes from running the Extended Flow bundle."
tags: ["Spec Kit", "Agentic Coding", "Workflow", "Best Practices"]
reading_time: "9 min read"
slug: "spec-kit-organization"
---

I spent the last few days cleaning up my Extended Flow bundle, and the cleanup kept turning into a debugging session for my own assumptions. Half the mess wasn't Spec Kit's fault — it was mine, from installing things without deciding where they belonged. Sorting that out forced me to actually understand the extension/preset boundary instead of gesturing at it.

The Spec-Kit documentation describes extensions, presets, workflows, and bundles thoroughly — what each one is, how catalog resolution works, which CLI flags exist. What it does not answer are the operational questions that appear after the first month: where a specific change belongs, what should be committed, and how a teammate reconstructs your setup from a fresh clone.

These are the field notes from that cleanup — from building and running the [Spec-Kit Extended Flow](https://github.com/markuswondrak/spec-kit-extended-flow) bundle. Every claim below is tied to a concrete decision in that project.

*This article reflects [Spec Kit](https://github.com/github/spec-kit) and its [documentation](https://github.github.io/spec-kit/) as of this writing, and the Extended Flow bundle at bundle/preset/`extendedflow` extension `0.16.0` (`bug` extension `1.0.0`, Feature workflow `0.10.1`, Bugfix workflow `0.2.1`, Quick workflow `0.1.1`). Both projects evolve; re-check current behavior before relying on specifics.*

## The extension/preset boundary is a design convention

The taxonomy is correct but easy to apply incorrectly. The convention I hold to:

**A new command name belongs in an extension. A change to existing command or template content belongs in a preset.**

This is a design convention, not a hard technical wall. Command names follow `speckit.<ext-id>.<cmd-name>`. A preset with `strategy: replace` can technically introduce a brand-new command without a matching extension existing. Composition strategies are where Spec Kit does enforce a rule: `prepend`, `append`, and `wrap` require an existing base layer to compose onto. When that base is missing, Spec Kit skips the command and emits a warning — it is not silent. What is silent is the choice, not the enforcement: nothing stops a preset from replacing its way into a new command, it is simply not what a preset is for. A preset can override a command that an installed extension or the core already provides; treating it as a place to *introduce* new commands defeats the reason for having extensions and presets as separate concepts at all.

Extended Flow is split along exactly this line, matching the [reference documentation](https://github.com/markuswondrak/spec-kit-extended-flow/blob/main/docs/reference.md):

| Component | Kind | Contents |
|---|---|---|
| Seven commands | Extension | `documentation`, `documentation-init`, `finish`, `project-init`, `quick-implement`, `quick-review`, `doc-check` |
| Templates + 14 overrides | Preset | `review-findings.md`, `documentation.md`, and a runtime preamble prepended to existing commands |

The split is functional. The extension can be versioned and reviewed as behavior; the preset can be replaced without removing commands.

## The runtime preamble pattern

The most useful preset pattern I have used: **one file composed onto many commands.**

Extended Flow's preset declares fourteen `type: command` entries, all pointing at the same file — `commands/workflow-runtime.md` — each with `strategy: prepend` (see [`preset.yml`](https://github.com/markuswondrak/spec-kit-extended-flow/blob/main/preset.yml)). The file holds an unattended-runtime preamble: it tells the agent to stay inside the project and not block on a question.

Three decisions make this work:

1. **The preamble is declared once and composed at install time.** The single file is prepended to each target command, so the context is not duplicated fourteen times in the preset source.
2. **It is a preset, not an extension.** It changes the content of existing commands. It introduces nothing.
3. **Interactive commands are excluded deliberately.** `project-init` and `documentation-init` are bootstrap commands run by a human before the flows start. They must be allowed to ask questions, so they do not receive the preamble.

The pattern generalizes: any cross-cutting instruction that every automated command must carry — house style, guardrails, output conventions — belongs in a prepended preset file, not copy-pasted into each command.

## Pick priorities that leave room

Every preset defaults to priority `10`, and ties break alphabetically by preset id (see the [Spec Kit presets reference](https://github.com/github/spec-kit/blob/main/docs/reference/presets.md)). Install everything at the default and your effective stack is arbitrary. Assign bands instead:

| Band | Priority | Contents |
|---|---|---|
| Base | 20 | Organizational standards, compliance |
| Methodology | 10 | Team process. Extended Flow pins its preset here. |
| Project | 5 | Localization, project-specific terminology |

Lower wins. When two presets both `replace` the same template, only the lower number is used — the other is ignored entirely, not merged. If two layers should compose, the higher-precedence preset (the one with the lower priority number) must declare `append`, `prepend`, or `wrap` for that file.

Extended Flow's bundle pins its preset at priority `10` with `strategy: append` (see [`bundle.yml`](https://github.com/markuswondrak/spec-kit-extended-flow/blob/main/bundle.yml)). That reserves 1–9 for project-level overrides and 11+ for organizational layers, without touching the bundle. Note that the bundle-level `strategy` field governs how the bundle's own manifest composes; the composition of individual commands and templates is still driven by the `strategy` set in `preset.yml`.

## What to commit, what to ignore

`specify init` scaffolds a managed `.specify/.gitignore` that contains exactly two patterns (see the [Spec Kit core reference](https://github.com/github/spec-kit/blob/main/docs/reference/core.md)):

```gitignore
feature.json
extensions/*/local-config.yml
```

That covers machine-local state only: the current-feature pointer and per-machine extension config overrides. Spec Kit's own default leaves the rest of `.specify/` shareable and versionable.

For Extended Flow projects, I use a stricter rule than Spec Kit's default, and this is the operating principle the rest of this section builds on: **anything that can be reconstructed by installing it should not be committed.** Anything pulled from a catalog and not meant to be edited locally should not be committed. Its version is pinned in the catalog and in the bundle manifest — that is the source of truth, not a copy checked into git. This is my take on how to handle Spec-Kit-based projects, not an official Spec Kit recommendation.

Add these rules to the managed file (your edits are preserved on re-init):

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

# Installation-state records. Rebuilt by the bundler on reconstruction,
# and stale copies can make it believe an ignored component is present.
.specify/extensions/.registry
.specify/bundle-records.json
.specify/extensions.yml
```

Two exceptions are explicit in the negation patterns:

- **Extension project config** (`<ext>-config.yml`) is not catalog-derived. It is project intent and stays tracked. Only the machine-local `local-config.yml` is ignored, which the managed block already handles.
- **Workflow overlays** (`.specify/workflows/overlays/`) are project-local customizations, and they live outside the installed workflow directory precisely so they survive updates (see the [Spec Kit workflows reference](https://github.com/github/spec-kit/blob/main/docs/reference/workflows.md)).

The three installation-state files above matter as much as the component files themselves. The bundler resolves what is already installed primarily through these registries and records, not by inspecting the filesystem tree alone. If they are committed while the components they describe are ignored, a fresh clone can end up with metadata claiming something is installed when its files are absent — and the bundler may then skip installing it, or refuse a plain install and demand `bundle update`/`--refresh` instead.

Everything not listed above stays committed: the constitution, templates, `.specify/integration.json`, and catalog configuration such as `.specify/*-catalogs.yml`, plus specs and bug reports.

Note the negation syntax. `.specify/extensions/*/*` ignores the *contents* of each extension directory but not the directory itself, which is what allows a top-level config file to be re-included. Ignoring `.specify/extensions/` wholesale would make that impossible — git cannot re-include a file inside an excluded directory.

## The reconstruction test

The gitignore decision has one acceptance criterion: **a fresh clone must reach a working state in at most two commands.**

```bash
git clone <repo> && cd <repo>
specify bundle install spec-kit-extended-flow
```

If restoring the project requires more than that — manual `specify extension add` calls, remembered priorities, a wiki page listing what to install — the bundle is under-specified. Every primitive that is gitignored must be owned by a bundle, and the bundle must pin it.

Run this test against a real fresh clone, not by deleting directories from a working checkout: blanket-deleting `.specify/extensions/`, `.specify/presets/`, and `.specify/workflows/` also removes content this article treats as project intent (extension project config, workflow overlays, registries and provenance), which the ignore rules above deliberately keep tracked. Clone the repository into a clean directory, run the install command, and confirm the resulting installed versions match what the bundle pins before trusting the setup.

<!-- EDITORIAL NOTE (open point 2): Consider adding the runtime integration points here — `.specify/workflows/runs/current_run` and `.specify/feature.json` — as the surfaces tooling reads for run and feature state. Left out of the prose for now; decide whether they belong in this section or are out of scope for an organization-focused article. -->

## Release discipline

Installed components carry a version from two places: the component manifest and the bundle pin. If those can drift, `specify bundle info` stops being trustworthy.

Extended Flow keeps a hybrid model, and this is my own policy, not something Spec Kit enforces. The components the project itself publishes — the bundle manifest, the preset, and its own `extendedflow` extension — are released together and share one version number. Workflows and third-party extensions are a different case: they are foreign components, maintained on their own schedule by whoever publishes them (in Extended Flow's case, the bundled `bug` extension and its individual workflows), and forcing them onto the maintainer's release version would misrepresent who owns that release cadence. So they keep independent versions by design, not because the project's release process is incomplete. This is the same question every project that composes its own components with third-party ones has to answer: sync what you publish, do not claim ownership over the versioning of what you depend on but don't publish.

The alternative — independent semver per primitive with strict pins in `bundle.yml` — is valid on its own when components genuinely evolve on different cadences. What is not valid is an unprincipled mixture: a shared version for some primitives and loose, undocumented pins for others, with no stated rule for which is which. That produces a bundle whose stated version no longer describes its contents.

## Anti-patterns

**Commands from a preset.** A preset that registers `speckit.someext.cmd` via `replace` without `someext` installed can technically work, but it blurs the boundary this article is built on. If you need a new command, ship an extension.

**Everything at default priority.** Five presets at priority `10` resolve alphabetically. Assign bands.

**Unpinned bundle entries.** Spec Kit rejects unpinned extension, preset, and workflow entries during bundle validation. Steps are the documented exception — pin everything else.

**Logic in workflow YAML.** Shell steps that grow beyond one command belong in a script shipped by whichever package installs the runtime — preset or extension, depending on the project's split. The workflow declares sequence; scripts implement behavior. My own recommendation, not a hard rule: once those scripts pass a certain complexity, publish and maintain them as their own versioned package rather than keeping them inline in a preset or extension.

**Committing installed components.** A checked-in copy of a catalog extension, preset, or workflow — or its installation-state record — drifts from the catalog the moment someone updates it. Pin the version, ignore the files and their registries, reconstruct on clone.

## Organization is a decision about reconstructability

The primitives are deliberately separated, and the docs explain why. What the docs leave to you is the operating model: where a change belongs (extension for new commands, preset for content changes), what is shared intent versus reconstructable install, and how a teammate gets from a clone to a running setup.

Decide those three things explicitly and `.specify/` stays predictable. Leave them implicit and you get the failure this article started from: a stack nobody can resolve, a bundle whose version means nothing, and a setup that only works on the machine where it was built.
