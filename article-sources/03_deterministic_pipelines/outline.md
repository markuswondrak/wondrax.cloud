
# Wenn Orchestratoren driften: Warum harte Workflows nicht in den Agenten-Flow gehören

### 1. Das Versprechen: Die agentische Orchestrierung
*   **Der ideale Aufbau:** Ein zentraler **Orchestrator-Agent** steuert spezialisierte **Worker-Agenten** für Aufgaben wie Research, Coding oder Testing.
*   **Die Erwartung:** Das System soll komplexe Ziele interpretieren, Aufgaben autonom dekomponieren und dynamisch entscheiden, welche Tools oder Agenten als Nächstes aufgerufen werden.
*   **Agentic AI:** Im Gegensatz zu einfachen Assistenten zeichnen sich diese Systeme durch Planung, Gedächtnis und Multi-Step-Execution aus.

### 2. Das Problem: Der „Agentic Drift“
*   **Beobachtung:** Agenten neigen dazu, in langen Sitzungen den Kontext und viel schlimmer den Fokus zu verlieren.
*   **Struktureller Zerfall:** Ohne äußere Zwänge überspringen Agenten dann wichtige Phasen wie die Planung und springen direkt zur Implementierung.
*   **Stochastische Natur:** Da LLMs auf Wahrscheinlichkeiten basieren, ist ihr Ausführungspfad unvorhersehbar und divergiert bei wiederholten Läufen.
*   **Recursive Hallucination:** Agenten können plausible, aber physisch oder logisch unsinnige Ergebnisse liefern, wenn sie nicht determinstisch geerdet sind. --> Bei langlaufenden Sessions kann das dann exponentiell wachsen

### 3. Kernaussage: Struktur gehört nicht in den Agenten-Flow
*   **Determinismus-Dilemma:** Software-Engineering verlangt deterministische Garantien (Syntax, API-Verträge), während Agenten probabilistische „Token-Vorhersager“ sind.
*   **Workflow vs. Agent:** Ein Workflow ist ein engineered Prozess mit fester Sequenz, während ein Agent dynamisch in einer Schleife entscheidet.
*   **Dual-State-Architektur:** Die Lösung liegt in der Trennung des **deterministischen Kontrollflusses** ($S_{workflow}$) von der **stochastischen Inhaltsgenerierung** ($S_{env}$).
*   **Post-Condition Guards:** Statt dem Agenten zu vertrauen, müssen deterministische Wächter-Funktionen den Output prüfen, bevor der Prozess fortgesetzt wird.

### 4. Die Kurve zum SDLC: Struktur als Rettungsanker
*   **Engineering-Disziplin:** Zuverlässige Software erfordert harte Phasen: Design, Planung, Implementierung und Review.
*   **Qualitätssicherung:** Standardpraktiken wie Branching, Pull Requests (PRs), Testing und Linting müssen den Rahmen bilden.
*   **Vermeidung technischer Schulden:** Unstrukturierte KI-Generierung führt oft zu Sicherheitslücken und schlechter Architektur, die später mühsam korrigiert werden müssen.

### 5. GitHub Spec-Kit: Spec-Driven Development (SDD)
*   **Das Konzept:** Die Spezifikation (Intention) wird zum primären Artefakt, das den gesamten Prozess steuert.
*   **Phasenbasiertes Arbeiten:** Spec-Kit erzwingt definierte Phasen wie **Constitution** (Grundregeln), **Specify** (Was/Warum), **Plan** (Wie), **Tasks** (Zersetzung) und **Implement**.
*   **Gating:** Jede Phase endet an einem Punkt, der ein menschliches Review erfordert, bevor die KI weitermachen darf.
*   **Workflows & Extensions:**
    *   Spec-Kit bietet jetzt echte **Workflows** an, die über einen **Extension-Mechanismus** (ZIP-Archive mit `extension.yml`) angepasst werden können.
    *   Teams können eigene Slash-Commands definieren und benutzerdefinierte Logik (z. B. Compliance-Prüfungen oder Jira-Sync) in den Lebenszyklus einklinken.

### 6. Einführung und Nutzung strukturierter Workflows
*   **Initialisierung:** Der Start erfolgt über `specify init`, um die notwendige Projektstruktur und Memory-Dateien anzulegen.
*   **Steuerung:** Befehle wie `/specify` oder `/plan` leiten den Agenten gezielt durch die SDLC-Phasen, wobei die Intention als „Source of Truth“ dient.
*   **Anpassung:** Über **Presets** können Organisationen Standards (z. B. Architekturregeln) projektübergreifend durchsetzen, ohne das Core-Framework zu verändern.

### 7. Fazit: Intention als neue „Source of Truth“
*   Wir bewegen uns weg von „Code ist die Wahrheit“ hin zu **„Intention (Spezifikation) ist die Wahrheit“**.
*   Agenten sind brillante „Junior-Entwickler“, brauchen aber ein **deterministisches Korsett** (den Workflow) außerhalb ihres eigenen Reasonings, um produktionsreif zu sein.
*   **Abschlussplädoyer:** Nutze Agenten für die generative Arbeit, aber behalte die Kontrolle über die Struktur durch klassisches Workflow-Design.

***

Soll ich dir zu einem bestimmten Punkt, beispielsweise zur **Dual-State-Architektur** oder den Details der **extension.yml**, noch weitere Details ausarbeiten?


Hier sind die in den Quellen genannten Links, die für deine Artikel-Storyline relevant sind:

### Zentrale Quellen & Tools
*   **GitHub Spec-Kit Repository:** [https://github.com/github/spec-kit](https://github.com/github/spec-kit)
*   **Dein Vorartikel (Re-evaluating GitHub's Spec Kit):** [https://markus.wondrax.cloud/articles/spec-kit-reevaluation.html](https://markus.wondrax.cloud/articles/spec-kit-reevaluation.html) (aus deiner Storyline)
*   **GitHub Blog (Einführung Spec-Kit):** [https://github.blog/2025-09-02-spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/](https://github.blog/2025-09-02-spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
*   **Model Context Protocol (MCP) Dokumentation:** [https://modelcontextprotocol.io](https://modelcontextprotocol.io)

### Theoretische Vertiefung & Studien
*   **Managing the Stochastic (Dual-State Architektur):** [https://arxiv.org/abs/2512.20660](https://arxiv.org/abs/2512.20660)
*   **AI Agents vs. AI Pipelines (Vergleichs-Guide):** [https://datavizandai.github.io/2024/09/28/AI_Agents_vs._AI_Pipelines-3A_a_Practical_Guide_to_Coding_Your_LLM_Application.html](https://datavizandai.github.io/2024/09/28/AI_Agents_vs._AI_Pipelines-3A_a_Practical_Guide_to_Coding_Your_LLM_Application.html)
*   **Capgemini Research (Rise of Agentic AI):** [https://www.capgemini.com/insights/research-institute/](https://www.capgemini.com/insights/research-institute/)
*   **Microsoft Agent Framework (8-Schritte-Framework):** [aka.ms/frontierfirmscenarios](https://aka.ms/frontierfirmscenarios)

### Community & Praktische Beispiele
*   **LinkedIn Learning Kurs zum Spec-Kit:** [https://github.com/LinkedInLearning/spec-driven-development-with-github-spec-kit-4641001](https://github.com/LinkedInLearning/spec-driven-development-with-github-spec-kit-4641001)
*   **Spec-Kit Archive Extension (Double-Loop Parity):** [https://github.com/stn1slv/spec-kit-archive](https://github.com/stn1slv/spec-kit-archive)
*   **INSIDE Industry Association Online-Magazin:** [https://inside-association.eu](https://inside-association.eu)

Soll ich dir zu einem dieser Links noch spezifische Hintergrundinformationen oder Zitate aus dem Text heraussuchen?
