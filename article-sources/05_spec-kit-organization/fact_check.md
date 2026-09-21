# Fact Check: "How to Organize Your Spec-Kit Extensions, Presets, Workflows and Bundles"

**File checked:** `05_spec-kit-organization/article.md`
**Date:** 2026-09-21
**Role:** Source Verification & Argumentation Audit

**Compared against:** `github/spec-kit@d4229c0` and `markuswondrak/spec-kit-extended-flow@8e8c2c6`

**Verdict:** Do not publish yet. Two central claims are demonstrably wrong:

1. Presets can now provide new commands with `strategy: replace`. An extension is no longer technically required for that.
2. Extended Flow does not use a single version across bundle, preset, extension, and workflows. The claimed `check-release.py` does not exist.

In addition, the proposed `.gitignore` rules likely do not pass the article's own reconstruction test.

---

## 1. Sources

### [1] Preset System Architecture - GitHub Spec Kit

URL: <https://github.com/github/spec-kit/blob/main/presets/ARCHITECTURE.md>
**Status: stale / claim mismatch**

The document contains the described "Extension safety check". The current implementation contradicts that document outright:

- Preset commands with `strategy: replace` are materialized regardless of a same-named extension.
- The code explicitly comments that `speckit.<namespace>.<command>` is no longer filtered by installed extension.
- Only `prepend`, `append`, and `wrap` require an existing base layer. When it is missing, the command is skipped and a warning is emitted.

This makes the following statements in lines 19-21 and 124 wrong:

> A new command name requires an extension.

> A preset can override a command [...] it cannot bring a new command into existence on its own.

> No error, no warning.

The architecture document inside the current Spec Kit repository is evidently not in sync with `src/specify_cli/presets/__init__.py`.

### [2] Extended Flow reference

URL: <https://github.com/markuswondrak/spec-kit-extended-flow/blob/main/docs/reference.md>
**Status: ok for the listed components, but internally stale**

The source confirms:

- seven commands in the extension,
- two templates in the preset,
- the general split into preset, extension, and workflows.

The source still claims "four workflows", while the current `bundle.yml` contains only three workflows. The article does not repeat the wrong count, but it should cite the concrete manifest rather than the partly stale reference.

### [3] Extended Flow `preset.yml`

URL: <https://github.com/markuswondrak/spec-kit-extended-flow/blob/main/preset.yml>
**Status: verified**

Confirmed:

- 14 command entries,
- the same file `commands/workflow-runtime.md`,
- `strategy: prepend` on each,
- the deliberate exclusion of `project-init` and `documentation-init`.

The statements in lines 36-42 are correct.

### [4] Spec Kit preset reference

URL: <https://github.com/github/spec-kit/blob/main/docs/reference/presets.md>
**Status: ok, with one wording imprecision in the article**

The source confirms:

- default priority `10`,
- lower number means higher precedence,
- alphabetical ordering on ties,
- `replace`, `prepend`, `append`, and `wrap`.

Line 56 should be phrased more precisely. It is not "some lower-priority preset" that must declare the composition strategy, but the **higher-precedence layer, that is the one with the lower number**, which wants to compose with the layer beneath it.

### [5] Extended Flow `bundle.yml`

URL: <https://github.com/markuswondrak/spec-kit-extended-flow/blob/main/bundle.yml>
**Status: ok for priority and manifest field, questionable for operational meaning**

The manifest does contain:

```yaml
priority: 10
strategy: "append"
```

The current bundler implementation, however, passes only `priority` to the `PresetManager` when installing a preset. The bundle-level `strategy` field is validated and stored in the provenance record, but apparently not applied to the individual preset files.

The article may say that the bundle declares this field. It should not suggest that the field drives the actual command or template composition. That comes from the individual `strategy` fields in `preset.yml`.

### [6] Spec Kit core reference and `shared_infra.py`

URL: <https://github.com/github/spec-kit/blob/main/docs/reference/core.md>
**Status: verified**

The managed `.specify/.gitignore` contains exactly:

```gitignore
feature.json
extensions/*/local-config.yml
```

The statement that local additions survive a re-init is also supported by documentation and implementation.

The source, however, explicitly takes a different default policy than the article: Spec Kit intentionally leaves the rest of `.specify/` versionable. "Installed components should not be committed" is therefore an operating-model decision and not an official Spec Kit recommendation.

### [7] Spec Kit workflow reference

URL: <https://github.com/github/spec-kit/blob/main/docs/reference/workflows.md>
**Status: verified**

The source confirms:

- Overlays live under `.specify/workflows/overlays/<workflow-id>/*.yml`.
- They live outside the installed workflow directory.
- Updates and reinstallations therefore preserve them.

The statement in line 91 is correct.

### [8] Extended Flow release documentation

URL: <https://github.com/markuswondrak/spec-kit-extended-flow/blob/main/docs/releasing.md>
**Status: claim mismatch**

The source does not support the statements in line 118.

Actual state:

- There is no `check-release.py`.
- `release-version.py` updates `preset.yml`, `extension.yml`, and `bundle.yml`.
- In the bundle, the script only updates the pins for its own preset and its own extension.
- The workflow versions are not raised to the release version.
- `build-catalog.py` synchronizes the catalog entries with each workflow's own version.

The current manifest demonstrates the independent versions directly:

```text
Bundle:                  0.16.0
Preset:                  0.16.0
extendedflow Extension:  0.16.0
bug Extension:           1.0.0
Feature Workflow:        0.10.1
Bugfix Workflow:         0.2.1
Quick Workflow:          0.1.1
```

The whole paragraph in lines 116-120 describes a release policy the project does not currently use.

---

## 2. Unsourced or Incorrect Claims

### Critical: The extension/preset boundary is no longer technically enforced

**Affected lines:** 15-30, 124

The article's central thesis is incompatible with the current code. A tenable phrasing would be:

> Extensions remain the conventional home for standalone command behavior. Presets can also introduce self-contained commands with `strategy: replace`. Composition strategies such as `prepend`, `append`, and `wrap` require an existing lower layer; without one, Spec Kit warns and skips that command.

This turns the claimed technical boundary into an architectural decision.

### Critical: The `.gitignore` rules leave installation state in the repository

**Affected lines:** 71-97

The proposed rules ignore the components but not the entire associated installation state:

- `.specify/extensions/.registry` stays versionable.
- `.specify/bundle-records.json` stays versionable.
- `.specify/extensions.yml` stays versionable.

This matters for the reconstruction test. The bundler checks installed components primarily through the respective registries. A fresh clone can therefore contain metadata according to which an extension is already installed, even though its files were ignored. The bundler may then skip it.

`.specify/bundle-records.json` is especially problematic: the record contains the bundle version and component ownership. After a later bundle release, a fresh clone with an older checked-in record can reject a normal install and demand `bundle update` or `--refresh` instead.

The ignore policy must be tested in a real fresh clone before publication. It is currently unproven that it works.

### Critical: The proposed reconstruction test deletes project intent

**Affected line:** 110

The article recommends:

> Delete `.specify/extensions/`, `.specify/presets/`, and `.specify/workflows/`

That also removes the content explicitly described as versionable:

- extension project config,
- workflow overlays,
- registries and provenance.

The test should run in a real fresh clone or remove only the actually ignored paths. The blanket deletion of the three directories contradicts the commit policy described earlier.

### High: The release policy is invented or stale

**Affected lines:** 116-120

Neither the repository nor the cited source contains:

- a single-version policy for all workflows,
- a `check-release.py`,
- a CI check for an identical version string.

The statement should be replaced entirely. The current state is mixed versioning: bundle, preset, and own extension share a release version; the workflows and the external `bug` extension keep their own versions.

### High: The recommendation contradicts the official version-control policy

**Affected lines:** 69-73

Spec Kit explicitly describes the rest of `.specify/` as shareable. The article may advocate a stricter policy, but must mark it as its own decision:

> For Extended Flow projects, I use a stricter rule than Spec Kit's default...

The current phrasing "The answer is no" presents a personal operating decision as a general technical fact.

### Medium: Bundles must already be pinned

**Affected line:** 128

Current bundle validation requires a version for extensions, presets, and workflows. An unpinned bundle is therefore not merely "not reproducible" but structurally invalid. Steps are the exception.

More precise:

> Spec Kit rejects unpinned extension, preset, and workflow entries during bundle validation.

### Medium: Scripts do not live in the extension in this project

**Affected line:** 130

The article says:

> Shell steps that grow beyond one command belong in a script under an extension.

Extended Flow itself, however, installs its runtime scripts through the preset:

```text
.specify/presets/spec-kit-extended-flow/scripts/
```

That contradicts the article's own example and the reference, which describes the preset as "templates + scripts + unattended runtime preamble". Either the rule must be more general or the project architecture must change.

### Medium: Bundle pins are not checked on every install

The article treats bundle pins as a permanent guarantee. The official bundle documentation narrows this:

- Pin enforcement happens on first install or on a refresh.
- Already installed components are skipped on a normal `bundle install` by their ID.
- Their on-disk version is not compared against the bundle pin.

For the statements on reproducibility and release discipline, the official bundle reference is therefore missing:

<https://github.com/github/spec-kit/blob/main/docs/reference/bundles.md>

### Low: Mutable `main` links

All sources point at `main`. Several discrepancies in this check became visible precisely because of that. For a durably reliable article, implementation-level evidence should point at a commit or release tag.

---

## 3. Argumentation

### Argumentation gap: The extension/preset boundary is structural

**Issue:** The central premise is false. The rest of the article builds Extended Flow's architectural decision on a technical constraint that no longer exists.

**Suggestion:** Frame the boundary as a deliberate design principle, not an enforced rule. Then explain the special case: composition strategies require a base layer.

### Internal contradiction: What to commit / reconstruction test

**Issue:** The article wants to keep project config and overlays, but later demands deleting their entire parent directories.

**Suggestion:** Test reconstruction exclusively from a real clone. In addition, classify the state of `.registry`, `workflow-registry.json`, `bundle-records.json`, and `.specify/extensions.yml` explicitly.

### Internal contradiction: Release discipline

**Issue:** The article presents Extended Flow as an example of a single-version policy. The current repository visibly uses independent workflow versions.

**Suggestion:** Either actually move the implementation to single-version, or write the section as a deliberate hybrid model.

### Internal contradiction: Logic in workflow YAML

**Issue:** The anti-pattern rule demands scripts in an extension, while Extended Flow ships them in the preset.

**Suggestion:** Cut the rule to the actual separation: workflow YAML describes orchestration; non-trivial logic lives in versioned scripts of the installed package. Whether preset or extension must be justified separately.

### Conclusion grounding

**Issue:** The conclusion on reconstructability is sound, but the concrete ignore policy has not demonstrably been tested against the various registry files.

**Suggestion:** Document the clone test as a verified experiment: initial state, checked-in files, executed commands, and resulting installed versions.

---

## Additional formal finding

The article has no `## Sources` section. The footnotes sit only behind a horizontal rule. That contradicts the repository convention, according to which sources belong in an explicit `## Sources` section.

---

## 4. Clarifications (resolved with author)

### Finding 1 — "The extension/preset boundary is no longer technically enforced" (lines 15-30, 124)

**Resolution:** Confirmed. Code truth stands: `strategy: replace` in a preset can technically introduce a new command without an extension. However, this is not the intended/designed usage of a preset — it remains an unsupported edge case, not a sanctioned path. The article must stop claiming a hard technical enforcement ("This is not a convention — it is enforced", "No error, no warning") and instead present the extension/preset split as the project's deliberate design convention, while accurately noting that the composition strategies (`prepend`, `append`, `wrap`) do require an existing base layer and emit a warning and skip when one is missing.

**Action for article:** Rewrite lines 19-21 and 124 along the lines suggested in the fact check — frame the boundary as an architectural decision, not an enforced technical rule, and correct the "no error, no warning" claim to reflect the actual warn-and-skip behavior for composition strategies.
