# BrowserGamesSpy

Importieren notwendiger Bibliotheken:

    psutil für System-Metriken (CPU, RAM, Netzwerkverbindungen).
    selenium für Browser-Interaktion.
    time für Zeitsteuerung.

Initialisieren des Webbrowsers:

    Verwenden von selenium, um den Browser zu starten und die URL des Spiels zu öffnen.

System-Metriken und Netzwerkverbindungen sammeln:

    CPU-Auslastung
    RAM-Nutzung
    Netzwerkaktivität (gesendete und empfangene Bytes)
    Netzwerkverbindungen (IP-Adressen und Ports)

Daten sammeln und anzeigen:

    Regelmäßige Abfrage der Metriken und Netzwerkverbindungen.
    Darstellung der Ergebnisse in einer benutzerfreundlichen Weise (z.B. Konsolenausgabe).

Browser schließen:

    Nach Beendigung des Tests den Browser schließen.


Anforderungen:

    psutil installieren:

    bash

pip install psutil

selenium und den passenden WebDriver installieren:

bash

pip install selenium

Lade den ChromeDriver herunter und stelle sicher, dass er im PATH ist.
