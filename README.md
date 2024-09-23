# IT-Security und K.I. News E-Mail-Bot

## Überblick

Der **IT-Security und K.I. News E-Mail-Bot** ist ein Python-Skript, das täglich die neuesten Nachrichten aus verschiedenen IT-Security- und Cybersecurity-RSS-Feeds abruft und diese per E-Mail an festgelegte Empfänger versendet. 
Das Skript filtert doppelte Nachrichten und verhindert, dass bereits am Vortag gesendete Beiträge erneut verschickt werden, um die Relevanz und Qualität der empfangenen Informationen sicherzustellen.

## Features

- Automatisches Abrufen von RSS-Feeds: Unterstützt eine Vielzahl von renommierten IT-Security- und Cybersecurity-Feeds.
- Duplikat-Filterung: Entfernt doppelte Nachrichten innerhalb des aktuellen Tages.
- Vergleich mit Vortages-Nachrichten: Verhindert das erneute Senden von Nachrichten, die bereits am Vortag verschickt wurden.
- Ansprechendes E-Mail-Design: Sendet HTML-formatierte E-Mails für eine bessere Lesbarkeit und Übersichtlichkeit.
- Einfache Konfiguration: Anpassbare E-Mail-Einstellungen und Feed-Liste direkt im Skript.

## Inhaltsverzeichnis

- Voraussetzungen
- Installation
- Konfiguration
- Verwendung
- Automatisierung
- Anpassungen
- Troubleshooting
- Beiträge
- Lizenz

## Voraussetzungen

- Python 3.6 oder höher
- Internetverbindung zum Abrufen der RSS-Feeds und zum Senden der E-Mails.

## Installation

1. **Python installieren:**

   Stellen Sie sicher, dass Python 3.6 oder höher auf Ihrem System installiert ist. Sie können die Python-Installation überprüfen, indem Sie folgenden Befehl in Ihrem Terminal oder Ihrer Eingabeaufforderung ausführen:

   python --version

   Wenn Python nicht installiert ist, laden Sie es von python.org herunter und installieren Sie es.

2. **Repository klonen:**

   Klonen Sie das Repository von GitHub auf Ihren lokalen Rechner:

   git clone https://github.com/IhrBenutzername/it-security-news-bot.git
   cd it-security-news-bot

3. **Virtuelle Umgebung einrichten (optional, aber empfohlen):**

   Erstellen Sie eine virtuelle Umgebung, um die Abhängigkeiten isoliert zu verwalten:

   python -m venv venv

   Aktivieren Sie die virtuelle Umgebung:

   - Für Unix/Linux/macOS:

     source venv/bin/activate

   - Für Windows (CMD):

     venv\\Scripts\\activate

   - Für Windows (PowerShell):

     venv\\Scripts\\Activate.ps1

4. **Abhängigkeiten installieren:**

   Installieren Sie die benötigten Python-Pakete mit pip:

   pip install -r requirements.txt

## Konfiguration

Öffnen Sie das Python-Skript (news_mailer.py) in Ihrem bevorzugten Texteditor und passen Sie die folgenden Konfigurationsparameter an:

1. **RSS-Feeds:**

   Überprüfen Sie die Liste der RSS-Feeds im Skript. Diese Feeds liefern die neuesten Nachrichten im Bereich IT-Security und Cybersecurity. Sie können Feeds hinzufügen oder entfernen, indem Sie die feeds Liste im Skript bearbeiten.

   feeds = [
       'https://www.heise.de/security/rss/news-atom.xml',
       'https://www.golem.de/rss.php?tp=security',
       'https://feeds.arstechnica.com/arstechnica/security',
       'https://feeds.feedburner.com/TheHackersNews',
       'https://www.darkreading.com/rss_simple.asp',
       'https://feeds.feedburner.com/InfosecurityMagazine',
       'https://krebsonsecurity.com/feed/',
       'https://feeds.feedburner.com/Threatpost',
       'https://www.zdnet.com/topic/security/rss.xml',
       'https://security.googleblog.com/feeds/posts/default',
       'https://www.csoonline.com/index.rss',
       'https://www.scmagazine.com/rss/feed.aspx'
   ]

2. **E-Mail-Konfiguration:**

   Passen Sie die E-Mail-Einstellungen an, indem Sie die folgenden Variablen mit Ihren eigenen Informationen füllen:

   from_email = 'Ihre-Absenderadresse@example.com'
   to_email = 'Empfängeradresse@example.com'
   smtp_server = 'smtp.example.com'
   smtp_port = 587
   smtp_user = 'Ihr-SMTP-Benutzername'
   smtp_password = os.getenv('SMTP_PASSWORD')  # Das Passwort wird über eine Umgebungsvariable bezogen

   **Wichtig:** Stellen Sie sicher, dass die Umgebungsvariable SMTP_PASSWORD gesetzt ist, um das SMTP-Passwort sicher zu verwalten.

   - Setzen der Umgebungsvariable:
     - Unix/Linux/macOS:

       export SMTP_PASSWORD='Ihr_Sicheres_Passwort'

     - Windows (CMD):

       set SMTP_PASSWORD=Ihr_Sicheres_Passwort

     - Windows (PowerShell):

       $env:SMTP_PASSWORD="Ihr_Sicheres_Passwort"

3. **Anzahl der Nachrichten pro Feed:**

   Passen Sie die maximale Anzahl der Nachrichten pro Feed an, die abgerufen und gesendet werden sollen:

   max_items_per_feed = 3

## Verwendung

Führen Sie das Skript aus, um die E-Mail mit den neuesten Nachrichten zu senden:

python news_mailer.py

## Automatisierung

Um das Skript täglich automatisch auszuführen, können Sie einen Cron-Job (für Unix/Linux/macOS) oder eine Geplante Aufgabe (für Windows) einrichten.

### Unix/Linux/macOS:

1. Öffnen Sie den Crontab-Editor:

   crontab -e

2. Fügen Sie eine neue Zeile hinzu, um das Skript täglich um 8 Uhr morgens auszuführen:

   0 8 * * * /usr/bin/python /Pfad/zu/ihrem/script/news_mailer.py

   **Hinweis:** Ersetzen Sie /Pfad/zu/ihrem/script/ durch den tatsächlichen Pfad zu Ihrem Skript.

### Windows:

1. Öffnen Sie die Aufgabenplanung.
2. Erstellen Sie eine neue Aufgabe und konfigurieren Sie den Trigger, um das Skript täglich zu einer gewünschten Zeit auszuführen.
3. Geben Sie als Aktion das Python-Skript an:

   - Programm/Skript: python
   - Argumente hinzufügen: C:\\Pfad\\zu\\ihrem\\script\\news_mailer.py
   - Starten in: C:\\Pfad\\zu\\ihrem\\script\\

## Anpassungen

Sie können das Skript weiter anpassen, um zusätzliche Funktionen oder Verbesserungen hinzuzufügen:

- Weitere Feeds hinzufügen oder entfernen: Bearbeiten Sie die feeds Liste im Skript.
- E-Mail-Design ändern: Passen Sie die format_email_body Funktion an, um das E-Mail-Layout nach Ihren Wünschen zu gestalten.
- Mehrere Empfänger unterstützen: Ändern Sie die to_email Variable in eine Liste und passen Sie die E-Mail-Versendung entsprechend an.
- Schlüsselwort-Filter hinzufügen: Implementieren Sie eine Funktion, die Nachrichten basierend auf bestimmten Schlüsselwörtern filtert.

## Troubleshooting

### Fehler: Umgebungsvariable 'SMTP_PASSWORD' ist nicht gesetzt.

Stellen Sie sicher, dass die Umgebungsvariable SMTP_PASSWORD korrekt gesetzt ist. Überprüfen Sie dies, indem Sie folgenden Befehl ausführen:

- Unix/Linux/macOS:

  echo $SMTP_PASSWORD

- Windows (CMD):

  echo %SMTP_PASSWORD%

- Windows (PowerShell):

  echo $env:SMTP_PASSWORD

Wenn die Variable nicht gesetzt ist, setzen Sie sie wie in der Konfiguration beschrieben.

### Fehler beim Versenden der E-Mail

Überprüfen Sie die folgenden Punkte:

1. **SMTP-Einstellungen:** Stellen Sie sicher, dass smtp_server, smtp_port, smtp_user und smtp_password korrekt sind.
2. **Internetverbindung:** Stellen Sie sicher, dass Ihr System eine aktive Internetverbindung hat.
3. **Firewall/Einstellungen des E-Mail-Providers:** Einige E-Mail-Anbieter blockieren möglicherweise den Zugriff von weniger sicheren Apps. Stellen Sie sicher, dass Ihr Konto entsprechend konfiguriert ist.

## Beiträge

Beiträge sind willkommen! Bitte folgen Sie diesen Schritten, um einen Beitrag zu leisten:

1. Forken Sie das Repository.
2. Erstellen Sie einen neuen Branch für Ihre Änderung (git checkout -b feature/NeueFunktion).
3. Commiten Sie Ihre Änderungen (git commit -m 'Füge neue Funktion hinzu').
4. Pushen Sie den Branch (git push origin feature/NeueFunktion).
5. Erstellen Sie einen Pull-Request.

## Lizenz

Dieses Projekt ist unter der MIT Lizenz lizenziert. Weitere Informationen finden Sie in der Lizenzdatei.
