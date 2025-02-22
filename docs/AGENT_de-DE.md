# KI-gesteuerter Agent (ReAct)

## Was ist der Agent (ReAct)?

Ein Agent ist ein fortschrittliches KI-System, das große Sprachmodelle (LLMs) als zentrale Recheneinheit nutzt. Es kombiniert die Reasoning-Fähigkeiten von LLMs mit zusätzlichen Funktionen wie Planung und Werkzeugnutzung, um kompexe Aufgaben autonom auszuführen. Agenten können komplizierte Anfragen aufschlüsseln, schrittweise Lösungen generieren und mit externen Werkzeugen oder APIs interagieren, um Informationen zu sammeln oder Teilaufgaben auszuführen.

Diese Implementierung verwendet einen Agenten mit dem [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react) Ansatz. ReAct ermöglicht es dem Agenten, komplexe Aufgaben zu lösen, indem Reasoning und Aktionen in einer iterativen Feedback-Schleife kombiniert werden. Der Agent durchläuft wiederholt drei Schlüsselschritte: Gedanke, Aktion und Beobachtung. Er analysiert die aktuelle Situation mithilfe des LLM, entscheidet über die nächste Aktion, führt die Aktion mit verfügbaren Werkzeugen oder APIs aus und lernt aus den beobachteten Ergebnissen. Dieser kontinuierliche Prozess ermöglicht es dem Agenten, sich an dynamische Umgebungen anzupassen, seine Aufgabenlösungsgenauigkeit zu verbessern und kontextbezogene Lösungen zu liefern.

## Beispielanwendungsfall

Ein Agent, der ReAct verwendet, kann in verschiedenen Szenarien eingesetzt werden und bietet präzise und effiziente Lösungen.

### Text-to-SQL

Ein Benutzer fragt nach "dem Gesamtumsatz des letzten Quartals". Der Agent interpretiert diese Anfrage, konvertiert sie in eine SQL-Abfrage, führt sie gegen die Datenbank aus und präsentiert die Ergebnisse.

### Finanzprognose

Ein Finanzanalyst muss den Umsatz für das nächste Quartal prognostizieren. Der Agent sammelt relevante Daten, führt notwendige Berechnungen mithilfe von Finanzmodellen durch und generiert einen detaillierten Prognosebericht, der die Genauigkeit der Projektionen sicherstellt.

## Die Agent-Funktion verwenden

Um die Agent-Funktionalität für Ihren angepassten Chatbot zu aktivieren, folgen Sie diesen Schritten:

1. Navigieren Sie zum Agent-Bereich im Bildschirm für benutzerdefinierte Bots.

2. Im Agent-Bereich finden Sie eine Liste der verfügbaren Tools, die vom Agent genutzt werden können. Standardmäßig sind alle Tools deaktiviert.

3. Um ein Tool zu aktivieren, schalten Sie einfach den Schalter neben dem gewünschten Tool um. Sobald ein Tool aktiviert ist, hat der Agent Zugriff darauf und kann es bei der Verarbeitung von Benutzeranfragen nutzen.

![](./imgs/agent_tools.png)

> [!Wichtig]
> Es ist wichtig zu beachten, dass die Aktivierung eines Tools im Agent-Bereich automatisch auch die ["Knowledge"-Funktionalität](https://aws.amazon.com/what-is/retrieval-augmented-generation/) als Tool behandelt. Das bedeutet, dass das LLM eigenständig entscheidet, ob es "Knowledge" zur Beantwortung von Benutzeranfragen verwenden soll und es als eines der verfügbaren Tools betrachtet.

4. Standardmäßig wird das Tool "Internet-Suche" bereitgestellt. Dieses Tool ermöglicht es dem Agenten, Informationen aus dem Internet zu suchen, um Benutzerfragen zu beantworten.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

Dieses Tool basiert auf [DuckDuckGo](https://duckduckgo.com/), das Nutzungsbeschränkungen hat. Es eignet sich für Proof of Concept oder Demonstrationszwecke, aber für Produktionsumgebungen empfehlen wir die Verwendung einer anderen Such-API.

5. Sie können eigene benutzerdefinierte Tools entwickeln, um die Fähigkeiten des Agenten zu erweitern. Weitere Informationen zur Erstellung und Integration benutzerdefinierter Tools finden Sie im Abschnitt [Eigene Tools entwickeln](#how-to-develop-your-own-tools).

## Wie Sie Ihre eigenen Tools entwickeln

Um Ihre eigenen benutzerdefinierten Tools für den Agenten zu entwickeln, befolgen Sie diese Richtlinien:

- Erstellen Sie eine neue Klasse, die von der `AgentTool`-Klasse erbt. Obwohl die Schnittstelle mit LangChain kompatibel ist, bietet diese Beispielimplementierung eine eigene `AgentTool`-Klasse, von der Sie erben sollten ([Quelle](../backend/app/agents/tools/agent_tool.py)).

- Beziehen Sie sich auf die Beispielimplementierung eines [BMI-Berechnungstools](../examples/agents/tools/bmi/bmi.py). Dieses Beispiel zeigt, wie Sie ein Tool erstellen, das den Body-Mass-Index (BMI) basierend auf Benutzereingaben berechnet.

  - Der Name und die Beschreibung, die für das Tool deklariert werden, werden verwendet, wenn das LLM entscheidet, welches Tool zur Beantwortung der Benutzerfrage genutzt werden soll. Mit anderen Worten, sie werden in die Eingabeaufforderung eingebettet. Daher wird empfohlen, sie so präzise wie möglich zu beschreiben.

- [Optional] Sobald Sie Ihr benutzerdefiniertes Tool implementiert haben, wird empfohlen, dessen Funktionalität mithilfe eines Testskripts zu überprüfen ([Beispiel](../examples/agents/tools/bmi/test_bmi.py)). Dieses Skript hilft Ihnen sicherzustellen, dass Ihr Tool wie erwartet funktioniert.

- Nachdem Sie die Entwicklung und das Testen Ihres benutzerdefinierten Tools abgeschlossen haben, verschieben Sie die Implementierungsdatei in das Verzeichnis [backend/app/agents/tools/](../backend/app/agents/tools/). Öffnen Sie dann [backend/app/agents/utils.py](../backend/app/agents/utils.py) und bearbeiten Sie `get_available_tools`, damit der Benutzer das entwickelte Tool auswählen kann.

- [Optional] Fügen Sie klare Namen und Beschreibungen für das Frontend hinzu. Dieser Schritt ist optional, aber wenn Sie ihn nicht durchführen, werden der Toolname und die Beschreibung verwendet, die in Ihrem Tool deklariert sind. Diese sind für das LLM gedacht, nicht für den Benutzer, daher wird empfohlen, eine dedizierte Erklärung für eine bessere Benutzererfahrung hinzuzufügen.

  - Bearbeiten Sie i18n-Dateien. Öffnen Sie [en/index.ts](../frontend/src/i18n/en/index.ts) und fügen Sie Ihren eigenen `name` und `description` in `agent.tools` hinzu.
  - Bearbeiten Sie auch `xx/index.ts`. Dabei steht `xx` für den Ländercode, den Sie wünschen.

- Führen Sie `npx cdk deploy` aus, um Ihre Änderungen zu deployen. Dies macht Ihr benutzerdefiniertes Tool im benutzerdefinierten Bot-Bildschirm verfügbar.

## Beitrag

**Beiträge zum Werkzeug-Repository sind willkommen!** Wenn Sie ein nützliches und gut implementiertes Werkzeug entwickeln, erwägen Sie bitte, es dem Projekt beizusteuern, indem Sie ein Issue oder einen Pull Request einreichen.