---
name: research-check
description: Validate sources, find missing references, and audit the argumentation chain in technical articles. Use when the user asks to check sources, verify citations, find references, audit claims, review argumentation, or strengthen the evidence in an article.
---

# Research Check

Performs three checks on an article: source verification, source gaps, and argumentation chain integrity.

## 1. Source Verification

For each cited source:

- **Existence**: Does the URL or reference actually exist? Use WebFetch to check live URLs.
- **Accuracy**: Does the source actually support the claim it is cited for? Read the relevant section.
- **Attribution**: Is the author/organization correctly named and the date correct?
- **Hallucination check**: Flag any source that cannot be verified or where the cited content does not match the article's claim.

Report format per source:
```
[N] Title — Author, Year
  URL: <url>
  Status: ✓ verified / ✗ not found / ⚠ claim mismatch
  Note: (only if status is not ✓)
```

## 2. Source Gaps

Read every factual claim in the article. For each claim that:
- states a specific fact, number, or finding
- attributes behavior to a tool, framework, or organization
- makes a comparative or evaluative statement

...check whether it is sourced. If not, either:
- find a credible source using WebSearch
- flag it as an unsourced claim that needs a citation or should be rewritten as the author's own assessment

Do not invent sources. If no credible source can be found, say so explicitly.

## 3. Argumentation Chain

Read the article's argument from opening claim to conclusion. Check:

- **Logical sequence**: Does each section follow from the previous? Are there non-sequiturs or missing links?
- **Claim-evidence fit**: Is each major claim supported by evidence within the article (data, citations, examples)?
- **Counter-argument coverage**: Are significant objections to the central argument acknowledged or addressed?
- **Conclusion grounding**: Does the conclusion follow from the evidence presented, or does it overreach?
- **Internal consistency**: Are there contradictions between sections?

Flag each issue with:
```
⚠ Argumentation gap: [section name]
  Issue: [what is missing or inconsistent]
  Suggestion: [how to address it]
```

## Workflow

1. Read the full article
2. Run Source Verification (check all cited sources)
3. Run Source Gaps (scan all factual claims)
4. Run Argumentation Chain audit
5. Produce a consolidated report with three sections: Sources, Gaps, Argumentation

## Output Format

```
## Research Check Report

### 1. Sources
[list with status per source]

### 2. Unsourced Claims
[list of claims needing citations, with suggested sources or "no source found"]

### 3. Argumentation
[list of gaps or issues, or "No issues found"]
```

If everything passes, say so clearly. A clean report is useful information too.
