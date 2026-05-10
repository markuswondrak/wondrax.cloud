
# Wenn Orchestratoren driften: Warum harte Workflows nicht in den Agenten-Flow gehören

### 1. Das Versprechen: Die agentische Orchestrierung
*   **Der ideale Aufbau:** Ein zentraler **Orchestrator-Agent** steuert spezialisierte **Worker-Agenten** für Aufgaben wie Research, Coding oder Testing.
*   **Die Erwartung:** Das System soll komplexe Ziele interpretieren, Aufgaben autonom dekomponieren und dynamisch entscheiden, welche Tools oder Agenten als Nächstes aufgerufen werden.
*   **Agentic AI:** Im Gegensatz zu einfachen Assistenten zeichnen sich diese Systeme durch Planung, Gedächtnis und Multi-Step-Execution aus.

### 2. Das Problem: Der „Agentic Drift"
*   **Beobachtung:** Agenten neigen dazu, in langen Sitzungen den Kontext und viel schlimmer den Fokus zu verlieren.
*   **Struktureller Zerfall:** Ohne äußere Zwänge überspringen Agenten dann wichtige Phasen wie die Planung und springen direkt zur Implementierung.
*   **Stochastische Natur:** Da LLMs auf Wahrscheinlichkeiten basieren, ist ihr Ausführungspfad unvorhersehbar und divergiert bei wiederholten Läufen.
*   **Recursive Hallucination:** Agenten können plausible, aber physisch oder logisch unsinnige Ergebnisse liefern, wenn sie nicht deterministisch geerdet sind. --> Bei langlaufenden Sessions kann das dann exponentiell wachsen

### 3. Kernaussage: Struktur gehört nicht in den Agenten-Flow
*   **Determinismus-Dilemma:** Software-Engineering verlangt deterministische Garantien (Syntax, API-Verträge), während Agenten probabilistische „Token-Vorhersager" sind.
*   **Workflow vs. Agent:** Ein Workflow ist ein engineered Prozess mit fester Sequenz, während ein Agent dynamisch in einer Schleife entscheidet.
*   **Dual-State-Architektur:** Die Lösung liegt in der Trennung des **deterministischen Kontrollflusses** ($S_{workflow}$) von der **stochastischen Inhaltsgenerierung** ($S_{env}$).
*   **Post-Condition Guards:** Statt dem Agenten zu vertrauen, müssen deterministische Wächter-Funktionen den Output prüfen, bevor der Prozess fortgesetzt wird.

### 4. Die Kurve zum SDLC: Struktur als Rettungsanker
*   **Engineering-Disziplin:** Zuverlässige Software erfordert harte Phasen: Design, Planung, Implementierung und Review.
*   **Qualitätssicherung:** Standardpraktiken wie Branching, Pull Requests (PRs), Testing und Linting müssen den Rahmen bilden.
*   **Vermeidung technischer Schulden:** Unstrukturierte KI-Generierung führt oft zu Sicherheitslücken und schlechter Architektur, die später mühsam korrigiert werden müssen.

### 5. GitHub Spec-Kit: Spec-Driven Development (SDD)
*   **Das Konzept:** Die Spezifikation (Intention) wird zum primären Artefakt, das den gesamten Prozess steuert.
*   **Phasenbasiertes Arbeiten:** Spec-Kit erzwingt vier definierte Phasen: **Specify** (Was/Warum), **Plan** (Wie), **Tasks** (Zersetzung) und **Implement**. Eine optionale **Constitution**-Datei (Grundregeln für den Agenten, z.B. Architektur-Constraints) kann als dauerhaftes Konfigurations-Artefakt angelegt werden — sie ist keine eigenständige SDLC-Phase, sondern ein persistentes Regelwerk, das alle Phasen beeinflusst.
*   **Gating:** Jede Phase endet an einem Punkt, der ein menschliches Review erfordert, bevor die KI weitermachen darf.
*   **Workflows & Extensions:**
    *   Spec-Kit bietet echte **Workflows** an (Feature gemerged April 2026, [Issue #2142](https://github.com/github/spec-kit/issues/2142)), die über einen **Extension-Mechanismus** (Git-Repos mit `extension.yml`) angepasst werden können. Eine ZIP-Archive-basierte Distribution ist als zukünftiges Feature geplant (aktuell: lokale Dev-Installation + Community-Catalog via Issue-Submission).
    *   Teams können eigene Slash-Commands definieren und benutzerdefinierte Logik (z. B. Compliance-Prüfungen oder Jira-Sync) in den Lebenszyklus einklinken.
    *   Extensions können auch eigene **Step-Typen** mitbringen (z.B. einen `deploy`-Step), die dann in eigenen Workflows genutzt werden können.

*   **Workflow-Engine — die Architektur des deterministischen Kontrollflusses:**
    *   Die CLI agiert als **deterministischer Orchestrator**, der KI-Integrationen als austauschbare Executor dispatcht — die Kontrollstruktur liegt außerhalb des Agenten-Reasonings.
    *   Workflows sind YAML-Dateien mit `schema_version: "1.0"` und einer klar definierten Struktur aus `inputs`, `steps` und `requires`-Constraints.
    *   **Eingebaute Workflow-Varianten** im Repo ([`workflows/`](https://github.com/github/spec-kit/tree/main/workflows)):
        *   `speckit` — Full SDD Cycle: `specify → gate → plan → gate → tasks → implement` (zwei Human-Review-Checkpoints)
        *   `speckit-quick` — `specify → implement` ohne Gates (für schnelle Iteration)
        *   `speckit-review` — `specify → plan → gate → tasks` (review-fokussiert, kein Auto-Implement)

*   **Step-Typen — das Vokabular des deterministischen Flows** ([Referenz](https://github.com/github/spec-kit/blob/main/docs/reference/workflows.md)):

    | Typ | Zweck |
    |-----|-------|
    | `command` | Ruft einen Spec-Kit-Befehl auf (z.B. `speckit.plan`) |
    | `gate` | Pausiert für Human-Review; `on_reject: abort` bricht ab |
    | `shell` | Führt Shell-Befehle aus, ohne Agenten zu involvieren |
    | `prompt` | Sendet freien Prompt an den Agenten |
    | `if` / `switch` | Bedingte Verzweigung basierend auf Step-Outputs |
    | `while` / `do-while` | Schleifen mit `max_iterations`-Sicherheitslimit |
    | `fan-out` | Parallele Dispatch einer Collection mit `max_concurrency` |
    | `fan-in` | Sammelpunkt: blockiert bis alle Fan-out-Zweige fertig sind |

*   **Gate-Semantik als Kern des Human-in-the-Loop:**
    ```yaml
    - id: review-spec
      type: gate
      message: "Review the generated spec before planning."
      options: [approve, reject]
      on_reject: abort
    ```
    Der Workflow pausiert hier vollständig. `specify workflow resume <run-id>` setzt ihn nach dem Review fort. Der Zustand wird persistent gespeichert — kein Drift, kein Verlust. Entscheidend: Der Agent kann **nicht eigenständig fortfahren** — die Kontrolle liegt beim Menschen, nicht beim Modell.

*   **Fan-out — parallele Tasks mit deterministischer Kontrolle:**
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
    Statt dem Agenten zu überlassen, welche Tasks parallel laufen, steuert die Workflow-Engine die Parallelität deterministisch. Praktisches Beispiel aus dem Test-Fix-Loop:
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
    Der Agent iteriert, aber die **Abbruchbedingung und das Limit** kontrolliert der Workflow.

*   **Expressions — deterministischer Datenfluss zwischen Steps:**
    *   Outputs eines Steps werden typsicher als Inputs des nächsten übergeben: `{{ steps.specify.output.file }}`
    *   Bedingte Verzweigung basiert auf konkreten Step-Ergebnissen, nicht auf LLM-Entscheidungen: `{{ steps.plan.output.task_count > 5 }}`
    *   Sandboxed Jinja2-Subset — kein File-I/O, keine Imports, keine Code-Injektion möglich
    *   Verfügbare Filter: `default`, `join`, `contains`, `map`

*   **Multi-Integration-Dispatch pro Step:**
    *   Verschiedene KI-Modelle können pro Step konfiguriert werden — der Workflow entscheidet, welche KI wann optimal ist:
        *   Specify: Claude (schnell für initiale Spezifikation)
        *   Plan: Gemini 2.5 Pro mit `thinking-budget: 32768` (reasoning-intensiv)
        *   Implement: Claude Opus (höchste Codequalität)
    *   Resolution-Order: Step-Level → Workflow-Level → Projekt-Default
    *   IDE-basierte Integrationen (Copilot, Cursor) werden bewusst ausgeschlossen — Workflows sind CLI-only

*   **State-Persistenz — Resumability als Designprinzip:**
    *   Jeder Workflow-Run speichert seinen Zustand unter `.specify/workflows/runs/<run-id>/`:
        *   `state.json` — aktueller Step, alle Step-Outputs, Gate-Entscheidungen
        *   `inputs.json` — aufgelöste Input-Werte
        *   `log.jsonl` — append-only Execution-Log
    *   `specify workflow resume <run-id>` setzt einen pausierten (Gate) oder fehlgeschlagenen Run exakt am letzten Step fort — kein Neustart, kein Kontextverlust
    *   Run-Lifecycle: `created → running → paused (gate) → running → completed / failed / aborted`

### 6. Einführung und Nutzung strukturierter Workflows
*   **Initialisierung:** Der Start erfolgt über `specify init`, um die notwendige Projektstruktur und Memory-Dateien anzulegen. Der `speckit`-Workflow (Full SDD Cycle) wird dabei **automatisch mitinstalliert** — kein separater Setup-Schritt nötig.
*   **Steuerung:** Befehle wie `/specify` oder `/plan` leiten den Agenten gezielt durch die SDLC-Phasen, wobei die Intention als „Source of Truth" dient.
*   **Workflow-CLI — Befehle im Überblick:**
    ```bash
    # Workflow starten (interaktive Input-Prompts oder via -i Flag)
    specify workflow run speckit -i spec="Build a kanban board with drag-and-drop"

    # Nach Gate-Pause fortsetzen
    specify workflow resume <run-id>

    # Status eines oder aller Runs anzeigen
    specify workflow status [<run-id>]

    # Installierte Workflows verwalten
    specify workflow list
    specify workflow add <source>      # Katalog-ID, URL oder lokaler Pfad
    specify workflow remove <id>
    specify workflow search [query]    # In Katalogen suchen (--tag Filter)
    specify workflow info <id>         # Details inkl. Step-Graph

    # Katalog-Quellen verwalten
    specify workflow catalog list
    specify workflow catalog add <url>
    ```
*   **Katalog-System — Resolution-Order (first match wins):**
    1. Umgebungsvariable `SPECKIT_WORKFLOW_CATALOG_URL` (überschreibt alles)
    2. Projekt-Config: `.specify/workflow-catalogs.yml`
    3. User-Config: `~/.specify/workflow-catalogs.yml`
    4. Built-in Defaults: offizieller Katalog + Community-Katalog (discovery-only, kein Auto-Install)
*   **Workflow-Varianten direkt verfügbar:**
    *   `specify workflow run speckit` — Full SDD Cycle mit zwei Review-Gates
    *   `specify workflow run speckit-quick` — Schnell-Iteration ohne Gates
    *   `specify workflow run speckit-review` — Review-fokussierter Ablauf (kein Auto-Implement)
*   **Anpassung:** Über **Presets** können Organisationen Standards (z. B. Architekturregeln) projektübergreifend durchsetzen, ohne das Core-Framework zu verändern.

### 7. Fazit: Intention als neue „Source of Truth"
*   Wir bewegen uns weg von „Code ist die Wahrheit" hin zu **„Intention (Spezifikation) ist die Wahrheit"**.
*   Agenten sind brillante „Junior-Entwickler", brauchen aber ein **deterministisches Korsett** (den Workflow) außerhalb ihres eigenen Reasonings, um produktionsreif zu sein.
*   **Abschlussplädoyer:** Nutze Agenten für die generative Arbeit, aber behalte die Kontrolle über die Struktur durch klassisches Workflow-Design.


Hier sind die in den Quellen genannten Links, die für deine Artikel-Storyline relevant sind:

### Zentrale Quellen & Tools
*   **GitHub Spec-Kit Repository:** [https://github.com/github/spec-kit](https://github.com/github/spec-kit) ✅ verifiziert, 95k Stars
*   **Spec-Kit Workflow-Referenz:** [https://github.com/github/spec-kit/blob/main/docs/reference/workflows.md](https://github.com/github/spec-kit/blob/main/docs/reference/workflows.md) ✅ verifiziert
*   **Spec-Kit Extension-Dev-Guide:** [https://github.com/github/spec-kit/blob/main/extensions/EXTENSION-DEVELOPMENT-GUIDE.md](https://github.com/github/spec-kit/blob/main/extensions/EXTENSION-DEVELOPMENT-GUIDE.md) ✅ verifiziert
*   **Spec-Kit Workflow-Engine (Issue #2142):** [https://github.com/github/spec-kit/issues/2142](https://github.com/github/spec-kit/issues/2142) ✅ verifiziert, gemerged April 2026
*   **Dein Vorartikel (Re-evaluating GitHub's Spec Kit):** [https://markus.wondrax.cloud/articles/spec-kit-reevaluation.html](https://markus.wondrax.cloud/articles/spec-kit-reevaluation.html) (aus deiner Storyline)
*   **GitHub Blog (Einführung Spec-Kit):** [https://github.blog/2025-09-02-spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/](https://github.blog/2025-09-02-spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) ✅ verifiziert
*   **Model Context Protocol (MCP) Dokumentation:** [https://modelcontextprotocol.io](https://modelcontextprotocol.io)

### Theoretische Vertiefung & Studien
*   **Managing the Stochastic (Dual-State Architektur):** [https://arxiv.org/abs/2512.20660](https://arxiv.org/abs/2512.20660) ✅ verifiziert — DSAP-Paper von Matthew Thompson; formalisiert $S_{workflow} \times S_{env}$, Guard-Funktionen und Recovery-Hierarchie
*   **AI Agents vs. AI Pipelines (Vergleichs-Guide):** [https://datavizandai.github.io/2024/09/28/AI_Agents_vs._AI_Pipelines-3A_a_Practical_Guide_to_Coding_Your_LLM_Application.html](https://datavizandai.github.io/2024/09/28/AI_Agents_vs._AI_Pipelines-3A_a_Practical_Guide_to_Coding_Your_LLM_Application.html) ⚠️ nicht verifiziert
*   **Capgemini Research (Rise of Agentic AI):** [https://www.capgemini.com/insights/research-institute/](https://www.capgemini.com/insights/research-institute/) ⚠️ nur Landing Page verlinkt — kein spezifischer Report; konkreten Report-Link nachrecherchieren
*   **Microsoft Agent Framework (8-Schritte-Framework):** [aka.ms/frontierfirmscenarios](https://aka.ms/frontierfirmscenarios) ⚠️ Redirect-URL, nicht verifizierbar

### Community & Praktische Beispiele
*   **LinkedIn Learning Kurs zum Spec-Kit:** [https://github.com/LinkedInLearning/spec-driven-development-with-github-spec-kit-4641001](https://github.com/LinkedInLearning/spec-driven-development-with-github-spec-kit-4641001) ✅ verifiziert
*   **Spec-Kit Archive Extension:** [https://github.com/stn1slv/spec-kit-archive](https://github.com/stn1slv/spec-kit-archive) ✅ verifiziert — **Achtung:** Extension archiviert abgeschlossene Feature-Specs und Pläne in die Projekt-Dokumentation (Memory-Konsolidierung), nicht „Double-Loop Parity" wie ursprünglich beschrieben
*   **INSIDE Industry Association Online-Magazin:** [https://inside-association.eu](https://inside-association.eu)

Soll ich dir zu einem dieser Links noch spezifische Hintergrundinformationen oder Zitate aus dem Text heraussuchen?
