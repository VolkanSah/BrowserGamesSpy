# BrowserGamesSpy v2
###### System- und Netzwerküberwachungstool | [> Read in English](README.md)

![GameSpy](gamespy.png)

## Inhaltsverzeichnis
- [Einleitung](#einleitung)
- [Warum dieses Tool?](#warum-dieses-tool)
- [Benutzerrechte und DSGVO](#benutzerrechte-und-dsgvo)
- [Funktionen](#funktionen)
- [Neu in Version 2](#neu-in-version-2)
- [Systemanforderungen](#systemanforderungen)
- [Installation](#installation)
- [Verwendung](#verwendung)
- [Codeerklärung](#codeerklärung)
- [Lizenz](#lizenz)
- [Quellen](#quellen)

## Einleitung

Dieses Tool überwacht Systemmetriken und Netzwerkverbindungen für browserbasierte Spiele wie "Die Siedler Online", "Forge of Empires", "Grepolis", "Travian: Legends" und "OGame". Es sammelt Daten zu CPU-Auslastung, Speichernutzung, Netzwerkaktivität und aktiven Netzwerkverbindungen und zeigt diese Metriken in einer grafischen Benutzeroberfläche (GUI) mithilfe von `tkinter` an. Zusätzlich kann das Tool die gesammelten Daten in einer CSV-Datei speichern und die Metriken mit `matplotlib` visualisieren.


## Warum dieses Tool?
Anbieter von Online-Spielen behaupten oft, dass ihre Systeme sicher und unschädlich für Ihr System sind. Viele Forensik-Experten und Sicherheitsadministratoren können jedoch das Gegenteil beweisen. Häufige Bluescreens oder Systemabstürze, die zu unsachgemäßen Shutdowns führen, können folgende Schäden anrichten:

- **Datenverlust**: Beschädigung der Festplatte
- **Speicherschäden**: Permanente Schäden am Arbeitsspeicher (RAM)
- **Überhitzung**: Besonders bei modernen Geräten wie Netbooks und Laptops mit minimaler Kühlung und empfindlichen Bauteilen

Es ist nicht immer klar, wohin Daten gesendet werden, insbesondere im Rahmen der Europäischen Datenschutzgrundverordnung (DSGVO). Als Nutzer möchte ich wissen, wohin meine Daten gestreamt werden. Dieses Tool wurde entwickelt, um Bedenken und potenzielle Schäden zu dokumentieren und Beweise für Verbraucherorganisationen oder ähnliche Stellen bereitzustellen, um den Fokus auf Sicherheit und Service zu lenken, anstatt nur auf Profit.

## Benutzerrechte und DSGVO
Nach der DSGVO haben Benutzer mehrere Rechte in Bezug auf ihre persönlichen Daten:
- **Recht auf Information**: Sie müssen darüber informiert werden, wie Ihre Daten verwendet werden.
- **Recht auf Zugang**: Sie können auf Ihre persönlichen Daten zugreifen und verstehen, wie sie verarbeitet werden.
- **Recht auf Berichtigung**: Sie können Ihre Daten korrigieren lassen, wenn diese ungenau oder unvollständig sind.
- **Recht auf Löschung**: Sie können die Löschung Ihrer Daten beantragen.
- **Recht auf Einschränkung der Verarbeitung**: Sie können einschränken, wie Ihre Daten verwendet werden.
- **Recht auf Datenübertragbarkeit**: Sie können Ihre Daten exportieren und für andere Dienste verwenden.
- **Widerspruchsrecht**: Sie können der Verarbeitung Ihrer Daten unter bestimmten Umständen widersprechen.
- **Rechte in Bezug auf automatisierte Entscheidungsfindung**: Sie können automatisierte Entscheidungen anfechten und eine Überprüfung verlangen.

Dieses Tool unterstützt Sie dabei, diese Rechte auszuüben, indem es Transparenz über die gesammelten Daten und deren Verwendung bietet.

## Funktionen
- Überwacht CPU-Auslastung, Speichernutzung, gesendete/empfangene Netzwerkbytes und aktive Netzwerkverbindungen.
- Zeigt Metriken in einer `tkinter`-GUI mit Echtzeit-Updates an.
- Ermöglicht es dem Benutzer, auszuwählen, welche Metriken in den Diagrammen angezeigt werden sollen.
- Speichert gesammelte Daten in einer CSV-Datei.
- Visualisiert Metriken in Diagrammen mit `matplotlib`.

## Neu in Version 2
Die wichtigsten Änderungen und neuen Funktionen in Version 2 sind:

1. **Detailliertes Logging-System**:
   - Erstellt Logdateien mit Zeitstempel.
   - Protokolliert alle wichtigen Ereignisse und Metriken.
   - Separate Logs für jede Sitzung.

2. **Verbesserte Netzwerküberwachung**:
   - Erkennung und Protokollierung neuer Verbindungen.
   - Speicherung der Verbindungshistorie.
   - Optionale IP-Lokalisierung (erweiterbar).

3. **Zeitstempel für alle Ereignisse**:
   - Jede Metrik wird mit einem genauen Zeitstempel gespeichert.
   - Verbesserte CSV-Dateien mit Zeitinformationen.
   - Zeitstempel in der GUI-Anzeige.

4. **Verbesserte Fehlerbehandlung**:
   - Try-Catch-Blöcke für kritische Operationen.
   - Protokollierung von Fehlermeldungen zur Fehleranalyse.

Die grundlegenden Funktionen bleiben erhalten. Logs finden Sie im Ordner `logs`, und gespeicherte Metriken enthalten jetzt Zeitstempel.

## Systemanforderungen
- Python 3.x
- `psutil`-Bibliothek für Systemmetriken
- `selenium`-Bibliothek für Browser-Interaktionen
- `tkinter`-Bibliothek für die GUI
- `csv`-Modul für das Speichern von Daten
- `matplotlib`-Bibliothek für Diagramme
- ChromeDriver für `selenium` (stellen Sie sicher, dass dieser im PATH ist)

## Installation
1. Installieren Sie die erforderlichen Bibliotheken:
    ```bash
    pip install psutil selenium matplotlib
    ```

2. Laden Sie "ChromeDriver" herunter, installieren Sie ihn und stellen Sie sicher, dass er im PATH ist.

## Verwendung
1. Klonen Sie das Repository oder laden Sie das Script herunter.
2. Führen Sie das Script aus:
    ```bash
    python monitor.py
    ```

3. Die GUI öffnet sich und startet die Überwachung der angegebenen URL (https://www.diesiedleronline.de/). Sie können dieses Tool für jedes Browsergame verwenden, indem Sie die URL entsprechend anpassen.

4. Verwenden Sie die Kontrollkästchen, um auszuwählen, welche Metriken in den Diagrammen angezeigt werden sollen.

5. Klicken Sie auf die Schaltfläche „Daten speichern“, um die gesammelten Daten in einer CSV-Datei zu speichern.

## Codeerklärung
Der Code besteht aus den folgenden Hauptteilen:

1. **Importe und Funktionen**:
    - Importieren der benötigten Bibliotheken.
    - Definieren von Funktionen zur Erfassung von Systemmetriken und Netzwerkverbindungen.

2. **Metriken aktualisieren**:
    - Sammeln von Metriken alle 5 Sekunden.
    - Aktualisieren der GUI mit den neuesten Metriken.
    - Anhängen der gesammelten Daten an eine Liste für zukünftige Referenzen oder das Speichern.

3. **Daten speichern**:
    - Speichern der gesammelten Daten in einer CSV-Datei, wenn die Schaltfläche „Daten speichern“ angeklickt wird.

4. **Daten plotten**:
    - Plotten der ausgewählten Metriken in der GUI mit `matplotlib`.

5. **Hauptfunktion**:
    - Einrichten der `tkinter`-GUI.
    - Starten des Chrome-Browsers mit `selenium`.
    - Beginn der Überwachungs- und Aktualisierungsschleife.

## Lizenz
Dieses Projekt ist unter der GPLv3-Lizenz lizenziert – siehe die Datei [LICENSE](LICENSE) für Details.

## Quellen
- [BrowserGames-Spy](https://github.com/VolkanSah/BrowserGamesSpy)

### Sonstiges

README.md erstellt von Git Repo Manager (GPT) auf [GPT-Store](https://chatgpt.com/g/g-HBNMrjPNU-git-repo-manager) von Volkan Sah


