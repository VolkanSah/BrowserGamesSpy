# BrowserGamesSpy + GPT
###### System- und Netzwerküberwachungstool | [> Read in english](README.md)
![Broswer Games Spy](browser-games-spy.jpg)

## Inhaltsverzeichnis

- [Einführung](#einführung)
- [Warum Dieses Tool?](#warum-dieses-tool)
- [Benutzerrechte und DSGVO](#benutzerrechte-und-dsgvo)
- [Funktionen](#funktionen)
- [Anforderungen](#anforderungen)
- [Installation](#installation)
- [Verwendung](#verwendung)
- [Code-Erklärung](#code-erklärung)
- [GPTs für Ihre Rechte!](#gpts-für-ihre-rechte)
- [Lizenz](#lizenz)
- [Quelle](#quelle)

- [english Version](README.md)

## Einführung
Dieses Tool überwacht Systemmetriken und Netzwerkverbindungen für browserbasierte Spiele wie "Die Siedler Online". Es sammelt Daten zur CPU-Auslastung, Speichernutzung, Netzwerkaktivität und aktiven Netzwerkverbindungen und zeigt diese Metriken in einer grafischen Benutzeroberfläche (GUI) mit `tkinter` an. Darüber hinaus kann das Tool die gesammelten Daten in einer CSV-Datei speichern und die Metriken mit `matplotlib` visualisieren.

## Warum Dieses Tool?
Online-Spielbetreiber behaupten oft, ihre Systeme seien sicher und harmlos für Ihr System. Viele forensische Experten und Sicherheitsexperten können jedoch das Gegenteil beweisen. Häufige Blue Screens oder Systemabstürze, die zu unsachgemäßen Abschaltungen führen, können folgende Schäden an Ihrem System verursachen:

- **Datenverlust**: Festplattenkorruption
- **Speicherschäden**: Permanente Beschädigung des RAM
- **Überhitzung**: Besonders bei modernen Geräten wie Netbooks und Laptops mit minimaler Kühlung und empfindlichen Bauteilen

Es ist nicht immer klar, wohin Daten gesendet werden, insbesondere unter der Europäischen Datenschutz-Grundverordnung (DSGVO). Als Benutzer möchte ich wissen, wohin meine Daten gestreamt werden. Dieses Tool wurde entwickelt, um Ihnen zu helfen, etwaige Bedenken und potenzielle Schäden zu dokumentieren und Beweise für Verbraucherzentralen oder ähnliche Institutionen bereitzustellen, um der Gewinnsucht auf Kosten von Service und Sicherheit entgegenzuwirken.

### Benutzerrechte und DSGVO
Unter der DSGVO haben Benutzer mehrere Rechte in Bezug auf ihre persönlichen Daten:
- **Recht auf Information**: Sie müssen darüber informiert werden, wie Ihre Daten verwendet werden.
- **Recht auf Zugang**: Sie können auf Ihre persönlichen Daten zugreifen und verstehen, wie sie verarbeitet werden.
- **Recht auf Berichtigung**: Sie können Ihre Daten korrigieren lassen, wenn sie ungenau oder unvollständig sind.
- **Recht auf Löschung**: Sie können die Löschung Ihrer Daten verlangen.
- **Recht auf Einschränkung der Verarbeitung**: Sie können die Nutzung Ihrer Daten einschränken.
- **Recht auf Datenübertragbarkeit**: Sie können Ihre Daten erhalten und für verschiedene Dienste wiederverwenden.
- **Widerspruchsrecht**: Sie können der Verarbeitung Ihrer Daten unter bestimmten Umständen widersprechen.
- **Rechte in Bezug auf automatisierte Entscheidungen**: Sie können Entscheidungen anfechten und eine Überprüfung verlangen, die ohne menschliches Eingreifen getroffen wurden.

Dieses Tool hilft Ihnen, diese Rechte auszuüben, indem es Transparenz über die gesammelten Daten und deren Nutzung bietet.

## Funktionen
- Überwacht CPU-Auslastung, Speichernutzung, gesendete/empfangene Netzwerkbytes und aktive Netzwerkverbindungen.
- Zeigt Metriken in einer `tkinter`-GUI mit Echtzeit-Updates an.
- Ermöglicht dem Benutzer, auszuwählen, welche Metriken angezeigt werden sollen, mittels Kontrollkästchen.
- Speichert gesammelte Daten in einer CSV-Datei.
- Visualisiert Metriken in Diagrammen mit `matplotlib`.

## Anforderungen
- Python 3.x
- `psutil`-Bibliothek für Systemmetriken
- `selenium`-Bibliothek für Browserinteraktionen
- `tkinter`-Bibliothek für die GUI
- `csv`-Modul zum Speichern von Daten
- `matplotlib`-Bibliothek zur Datenvisualisierung
- ChromeDriver für `selenium` (stellen Sie sicher, dass es im PATH ist)

## Installation
1. Installieren Sie die erforderlichen Bibliotheken:
    ```bash
    pip install psutil selenium matplotlib
    ```

2. Laden Sie "ChromeDriver" herunter und installieren Sie es. Stellen Sie sicher, dass es in Ihrem PATH ist.

## Verwendung
1. Klonen Sie das Repository oder laden Sie das Skript herunter.
2. Führen Sie das Skript aus:
    ```bash
    python monitor.py
    ```

3. Die GUI wird geöffnet und beginnt mit der Überwachung der angegebenen URL (https://www.diesiedleronline.de/). Sie können dieses Tool für jedes Browser-Spiel verwenden, bitte ändern Sie die URL nach Bedarf.

4. Verwenden Sie die Kontrollkästchen, um auszuwählen, welche Metriken in den Diagrammen angezeigt werden sollen.

5. Klicken Sie auf die Schaltfläche "Daten speichern", um die gesammelten Daten in einer CSV-Datei zu speichern.

## Code-Erklärung
Der Code besteht aus den folgenden Hauptteilen:

1. **Importe und Funktionen**:
    - Notwendige Bibliotheken importieren.
    - Funktionen definieren, um Systemmetriken und Netzwerkverbindungen zu erhalten.

2. **Metriken aktualisieren**:
    - Alle 5 Sekunden Metriken sammeln.
    - Die GUI mit den neuesten Metriken aktualisieren.
    - Gesammelte Daten in eine Liste aufnehmen, um sie später zu speichern oder zu referenzieren.

3. **Daten speichern**:
    - Die gesammelten Daten in einer CSV-Datei speichern, wenn die Schaltfläche "Daten speichern" geklickt wird.

4. **Daten plotten**:
    - Die ausgewählten Metriken in der GUI mit `matplotlib` darstellen.

5. **Hauptfunktion**:
    - Die `tkinter`-GUI einrichten.
    - Den Chrome-Browser mit `selenium` starten.
    - Den Überwachungs- und Aktualisierungszyklus beginnen.

---

Dieses Tool zielt darauf ab, Benutzer zu stärken, indem es Transparenz und Rechenschaftspflicht von Online-Spielbetreibern gewährleistet, insbesondere im Hinblick auf die DSGVO. Verwenden Sie dieses Tool, um Ihr System zu überwachen, die Auswirkungen von Online-Spielen zu verstehen und Ihre Rechte zu schützen.

Ein besonderer Dank geht an Personen wie BB_Kumakun aus dem Community-Management-Team von "Die Siedler Online". Meiner Meinung nach entstehen Projekte wie dieses durch Menschen, die, meiner Ansicht nach, Einblick und Verständnis für Technologie und ihre eigene Sprache fehlen. Konstruktive Kritik ist wertvoll, auch wenn sie unangenehm ist. Ein Tipp: selektive Behandlung kann als diskriminierend angesehen werden.

> [!WARNUNG]
> Denken Sie daran, spielen Sie keine Spielchen mit mir, denn Sie könnten nicht mögen, wie ich zurückspiele.

## GPTs für Ihre Rechte!

**Ich habe für Sie alle eine GPT erstellt, die Sie als ChatGPT Plus-Benutzer kostenlos nutzen können. Bald wird OpenAI auch den Zugriff auf benutzerdefinierte GPTs für kostenlose Benutzer ermöglichen.**

Was macht dieses GPT? Es hilft Ihnen, Ihre Rechte zu wahren und unterstützt Sie bei der Formulierung Ihrer Beschwerden an Verbraucherzentralen oder ähnliche Organisationen, indem es detaillierte Erklärungen mit technischem und juristischem Wissen bietet.
- [> DSO Support Assistant](https://chatgpt.com/g/g-0BiFNYNhW-dso-support-assistant) 

## Lizenz
Dieses Projekt ist unter der GPLv3-Lizenz lizenziert - siehe die [LICENSE](LICENSE) Datei für Details.

### Quelle
- [BrowserGames-Spy](https://github.com/VolkanSah/BrowserGamesSpy)
