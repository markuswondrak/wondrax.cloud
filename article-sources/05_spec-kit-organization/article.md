---
title: "Managing Spec-Kit Extensions, Presets, Workflows, and Bundles as Packages"
author: "Markus Wondrak"
date: "2026-09-21"
excerpt: "Spec-Kit artifacts are packages and dependencies: catalogs publish what is available, bundles pin what a project installs, and the repository keeps only project intent and project-owned customization."
tags: ["Spec Kit", "Agentic Coding", "Workflow", "Best Practices"]
reading_time: "9 min read"
slug: "spec-kit-organization"
image: infografik_spec-kit.png
---

I spent the last few days cleaning up Extended Flow so I can use it in Workflow Cockpit. The hard part was not where files should sit inside `.specify/`. The hard part was that `.specify/` mixes things with different owners and lifecycles, yet it is easy to treat all of them as ordinary project files.

That mistake creates practical uncertainty fast. What belongs in git, what should be reconstructed from catalogs, and what needs a pinned version so a fresh clone means the same thing next week? The Spec-Kit documentation describes extensions, presets, workflows, and bundles thoroughly - what each primitive is, how catalog resolution works, and which CLI flags exist. It does not necessarily answer the operating question that appears after a few installations of your own: what is package source, what is project intent, and what is only the result of an installation?

This article uses the Extended Flow cleanup as a case study, but the point is broader. I think Spec-Kit extensions, presets, workflows, and bundles should be handled as packages and dependencies. Catalogs declare what is available. Bundles declare and pin what a project depends on. The repository tracks project intent and project-owned customization. Installed package copies, installation records, and runtime state are reconstructed.

*This article reflects [Spec Kit](https://github.com/github/spec-kit) and its [documentation](https://github.github.io/spec-kit/) as of this writing, and the Extended Flow bundle at bundle/preset/`extendedflow` extension `0.16.0` (`bug` extension `1.0.0`, Feature workflow `0.10.1`, Bugfix workflow `0.2.1`, Quick workflow `0.1.1`). Both projects evolve; re-check current behavior before relying on specifics.*

## Treat Spec-Kit artifacts as packages, not project files

The core problem is that one directory tree hides three different kinds of things. If they are all treated as "files under `.specify/`", repository boundaries become arbitrary and updates become harder to reason about.

I have found it more useful to separate them into three categories:

- **Package definitions and catalog-published components.** Extensions, presets, workflows, and bundles are versioned artifacts with their own manifests and release cadence. Catalogs answer one question: which packages are available to install?
- **Project intent and project-owned customizations.** Bundle declarations, catalog configuration, constitution, specs, extension project config, and workflow overlays describe what this project wants and which local customizations it owns.
- **Installed artifacts and runtime state.** Installed copies under `.specify/extensions/`, `.specify/presets/`, and `.specify/workflows/`, plus registries, bundle records, caches, and run state, are outputs of installation and execution.

In practice, that means keeping declarations and project-owned customizations in the repository, while installed packages and runtime state can be recreated when needed. Spec Kit does not enforce that repository policy for you. It gives you the primitives. You still need to decide which files are the declaration of a dependency and which files are only the materialized result.

## Choose the package that owns the behavior

The extension-versus-preset distinction becomes confusing when you start from file locations alone. Both can affect what the agent sees, and a preset can technically do more than it should. That is why teams need an ownership rule before they start composing packages.

Spec Kit distinguishes between extensions and presets. **Extensions are the conventional home for new command names. Presets modify existing commands or template content, and with `strategy: replace` they can also materialize a brand-new command on their own.** That makes the boundary architectural, not hard-enforced, but the distinction still reflects the intended semantics of the package types. What Spec Kit does enforce are the composition strategies documented in the [presets reference](https://github.com/github/spec-kit/blob/main/docs/reference/presets.md): `prepend`, `append`, and `wrap` require an existing base layer to compose onto. When that base is missing, Spec Kit skips the command and emits a warning. What remains your responsibility is choosing the right package owner.

| Kind | Contents |
|---|---|
| Extension | Seven commands: `documentation`, `documentation-init`, `finish`, `project-init`, `quick-implement`, `quick-review`, `doc-check` |
| Preset | Templates + 14 overrides: `review-findings.md`, `documentation.md`, and a runtime preamble prepended to existing commands |

This split matches the shipped manifests: [`extension.yml`](https://github.com/markuswondrak/spec-kit-extended-flow/blob/main/extension.yml) contributes named behavior, and [`preset.yml`](https://github.com/markuswondrak/spec-kit-extended-flow/blob/main/preset.yml) changes how existing behavior is rendered and composed. Once ownership is clear, composition stops being accidental.

## Compose packages deliberately

Choosing the right owner solves only the first half of the problem. A Spec-Kit project usually installs multiple packages, and their interaction is where drift and surprise appear.

Two composition problems matter in practice:

- Shared cross-cutting instructions copied into many commands drift over time.
- Competing preset changes need a deliberate precedence policy or resolution becomes arbitrary.

### One runtime preamble beats fourteen copies

The first problem showed up immediately in Extended Flow. I wanted the automated commands to run unattended, stay inside the project, and not stop to ask a human question. Copying that instruction into every command would have worked for one release and then drifted.

So I wrote it once instead. Spec Kit lets one preset entry compose onto many commands, so I pointed fourteen `type: command` entries at the same file - `commands/workflow-runtime.md` - each with `strategy: prepend` (see [`preset.yml`](https://github.com/markuswondrak/spec-kit-extended-flow/blob/main/preset.yml)). That keeps the policy in one place; the commands themselves stay free of duplicated boilerplate. I left `project-init` and `documentation-init` out because a human runs them before the flows start, so the preamble doesn't apply.

### Use priorities to define how presets compose

The second problem is less visible until two presets overlap. Every preset defaults to priority `10`, and ties break alphabetically by preset id (see the [Spec Kit presets reference](https://github.com/github/spec-kit/blob/main/docs/reference/presets.md)). Leave everything at the default and your effective stack is technically valid but operationally arbitrary.

The fix is to treat priority as policy, not as leftover metadata. I assign bands like this:

| Band | Priority | Contents |
|---|---|---|
| Base | 20 | Organizational standards, compliance |
| Methodology | 10 | Team process. Extended Flow pins its preset here. |
| Project | 5 | Localization, project-specific terminology |

Lower wins. When two presets both `replace` the same template, only the lower number is used; the other is ignored, not merged. If two layers should compose, the higher-precedence preset, the one with the lower number, must declare `append`, `prepend`, or `wrap` for that file. Extended Flow's [`bundle.yml`](https://github.com/markuswondrak/spec-kit-extended-flow/blob/main/bundle.yml) pins its preset at priority `10`, while the actual file-level composition strategies live in [`preset.yml`](https://github.com/markuswondrak/spec-kit-extended-flow/blob/main/preset.yml). That leaves room for project overrides above it and organizational layers below it without changing the bundle itself.

Once ownership and precedence are clear, repository boundaries become a dependency-management question rather than a generic Git question.

## Commit intent; reconstruct installations

The practical failure mode here is ending up with two competing truths. Catalogs and bundle manifests describe which packages the project depends on and which versions it expects. The other lives in checked-in installed copies and registries. The moment those drift apart, the repository no longer tells you which truth to trust.

Spec Kit's own default is intentionally narrow. `specify init` scaffolds a managed `.specify/.gitignore` that contains exactly two patterns (see the [Spec Kit core reference](https://github.com/github/spec-kit/blob/main/docs/reference/core.md)):

```gitignore
feature.json
extensions/*/local-config.yml
```

That excludes only machine-local state. For Extended Flow projects, I use a stricter policy: ignore anything that can be recreated by installing a declared dependency. Anything pulled from a catalog and not meant to be edited locally should not be committed. 

Add these rules to the managed file:

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

The exceptions matter because they show this is not a blanket "ignore `.specify/`" rule:

- **Extension project config** (`<ext>-config.yml`) is project intent. It is not catalog-derived, so it stays tracked. Only the machine-local `local-config.yml` stays ignored.
- **Workflow overlays** (`.specify/workflows/overlays/`) are project-owned customizations. The [workflows reference](https://github.com/github/spec-kit/blob/main/docs/reference/workflows.md) explicitly keeps them outside installed workflow directories so they survive updates.

The installation-state records matter as much as the installed package copies. The bundler resolves what is already installed primarily through these registries and records, not by inspecting the filesystem tree alone. If they are committed while the components they describe are ignored, a fresh clone can claim a component is already installed when its files are absent.

Everything not listed above stays committed: the constitution, templates, `.specify/integration.json`, catalog configuration such as `.specify/*-catalogs.yml`, plus specs and bug reports. The negation syntax is part of the design. `.specify/extensions/*/*` ignores the contents of each extension directory but not the directory itself, which is what allows a top-level config file to be re-included. Ignoring `.specify/extensions/` wholesale would make that impossible.

If bundle declarations are the source of truth, the next step is to prove that they are actually sufficient.

## Make a fresh clone the acceptance test

A declarative dependency story is only real if a new checkout can reconstruct it. Otherwise the repository still depends on human memory.

A useful acceptance test is whether a fresh clone can reach a working state with an easy init command:

```bash
git clone <repo> && cd <repo>
specify bundle install spec-kit-extended-flow
```

If restoring the project requires more than that - manual `specify extension add` calls, remembered priorities, or a wiki page that lists extra steps - the dependency declaration is incomplete. A missing step usually means one of three things is absent from the package model: a bundle dependency, a version pin, or project-owned customization that should have been committed.

Run this test against a real fresh clone, not by deleting directories from an existing checkout. Deleting `.specify/extensions/`, `.specify/presets/`, and `.specify/workflows/` from a working tree also deletes tracked project intent such as extension project config, workflow overlays, and installation metadata that this article treats deliberately. Clone into a clean directory, run the install command, and confirm the resulting installed versions match what the bundle pins.

That reconstruction test answers the present-tense question. Reproducibility over time depends on versioning discipline.

## Pin versions so reconstruction means the same thing tomorrow

Package management is temporal as well as structural. It is not enough that a project can be reconstructed today. The reconstructed result needs to mean the same thing when someone repeats the install later.

That is why bundles matter. The [Spec Kit bundles reference](https://github.com/github/spec-kit/blob/main/docs/reference/bundles.md) defines a bundle as a versioned composition layer over extensions, presets, workflows, and steps, and `bundle info` expands the pinned component set. Spec Kit rejects unpinned extension, preset, and workflow entries during bundle validation. If installed components carry one version in their own manifest and a different one in the bundle pin, the bundle stops being a trustworthy description of the environment.

Extended Flow keeps a hybrid release model, and this is my policy, not something Spec Kit enforces. The components the project itself publishes - the bundle manifest, the preset, and its own `extendedflow` extension - are released together and share one version number. Workflows and third-party extensions are different. They are foreign components, maintained on their own cadence, so forcing them onto the bundle's version would misstate ownership of that release cycle.

An alternative is to version each primitive independently and pin those versions in `bundle.yml`. That works when components genuinely evolve on different cadences. What does not work is an accidental mixture with no stated rule - some primitives share versions, others float loosely, and the bundle version no longer describes its contents. Reconstruction then becomes time-sensitive in exactly the wrong way.

The easiest way to see whether the model holds is to look at what breaks when it does not.

## Failure modes come from breaking the package model

The anti-patterns here are not disconnected style mistakes. Each one is a way of smuggling package behavior back into ad hoc project files.

- **Commands from a preset.** A preset that registers `speckit.someext.cmd` via `replace` without `someext` installed can work technically, but it hides new behavior inside the wrong package type.
- **Everything at default priority.** Five presets at priority `10` resolve alphabetically. That is a tie-breaker, not a composition policy.
- **Missing or stale bundle pins.** Spec Kit expects extension, preset, and workflow entries to be pinned, and stale pins still break reproducibility by describing a different environment than the one people actually install.
- **Logic in workflow YAML.** Shell steps that grow beyond one command blur the boundary between orchestration and packaged runtime behavior. The workflow should declare sequence; scripts shipped by a preset or extension should implement the logic.
- **Committing installed components or their registries.** A checked-in copy of a catalog extension, preset, or workflow drifts from the declared dependency the moment someone updates it.

All of these failure modes blur the distinction between declared dependencies and installed artifacts.

## Package management is the operating model

Spec Kit already gives the primitive types. The real design choice is how you operate them together. In my view, the cleanest model is to treat extensions, presets, workflows, and bundles as packages, not as a loose collection of project files under `.specify/`.

Extended Flow's own repository reflects the split now: extensions and presets are pinned, `.specify/extensions/` and `.specify/presets/` are gitignored, and a fresh clone rebuilds them with one install command. The next test is whether it holds up in Workflow Cockpit, the project this cleanup was for.
