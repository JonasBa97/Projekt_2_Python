
# 💰 Personal Finance Dashboard

Das **Personal Finance Dashboard** bietet eine umfassende Übersicht über die Finanzen des Benutzers.
Das Ziel dieses Projekts ist es, dem Benutzer zu helfen, seine finanziellen Ziele zu setzen und Fortschritte zu visualisieren.
Die Anwendung wird eine benutzerfreundliche Schnittstelle bieten, um Einnahmen, Ausgaben und Sparziele zu verfolgen.

## 🛠️ Installation
pip install .

## 📦 benötigte Bibliotheken
matplotlib==3.10.3
pandas==2.2.3
openpyxl==3.1.5
tkcalendar==1.6.1
fpdf==1.7.2

## 🧩 Features
- 📊 Tracking von Einnahmen, Ausgaben und verbleibendem Budget
- 📅 Datumsauswahl mit Kalenderfunktion
- 🎯 Verwaltung von Sparzielen
- 📈 Fortschrittsdiagramme für Sparziele mit Farbcodierung
- 📤 Export der Finanzdaten als PDF (standard), CSV oder Excel - ähnlich eines Kontoauszugs
- 💾 Speichern und Laden von Daten aus einer CSV-Datei

## 🚀 Anwendung starten
1. navigiere in den Projektordner: deinVerzeichnis/PFD_App/app
2. Anwendung über Terminalbefehl starten, z.B. Powershell: python main.py

## 🖥️ Bedienung
- Einnahmen/Ausgaben hinzufügen: Gib Datum, Betrag und Kategorie ein
- Sparziele setzen: Wähle ein Ziel und definiere einen Zielbetrag
- Budget zuweisen: Weise einen Teil deines Budgets einem Sparziel zu
- Fortschritt anzeigen / Aktualisieren: Visualisiere deine Sparziele in einem Balkendiagramm
- Daten exportieren: Exportiere deine Finanzdaten als PDF, CSV oder Excel-Datei
- Speichern: Speichere deine Eingaben dauerhaft in einer CSV-Datei (finanzdaten.csv)
- Beenden: Anwendung schließen

## 📤 Exportformate
- PDF: Übersicht von Einnahmen, Ausgaben, Sparzielen und verfügbarem Budget -> ähnlich eines Kontoauszugs
- CSV/Excel: Rohdaten für mögliche weitere Verarbeitung
- beim Export wird ein vorgefertigter Dateiname erstellt (finanzdaten_YYYY_mmdd_HHMM.*), dieser kann bei Bedarf geändert werden

## 🧑‍💻 Resume
Dieses Projekt wurde entwickelt, um die persönliche Finanzplanung zu vereinfachen und visuell ansprechend darzustellen. Viel Spaß bei der Finanzplanung.

Euer
JB