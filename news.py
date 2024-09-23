import feedparser
import smtplib
import os
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

# RSS-Feeds
feeds = [
    'https://www.heise.de/security/rss/news-atom.xml',
    'https://www.golem.de/rss.php?tp=security',
    'https://feeds.arstechnica.com/arstechnica/security',
    'https://feeds.feedburner.com/TheHackersNews',
    'https://techcrunch.com/tag/artificial-intelligence/feed/',
    'https://www.darkreading.com/rss_simple.asp',
    'https://feeds.feedburner.com/InfosecurityMagazine',
    'https://krebsonsecurity.com/feed/',
    'https://feeds.feedburner.com/Threatpost',
    'https://www.zdnet.com/topic/security/rss.xml',
    'https://security.googleblog.com/feeds/posts/default',
    'https://www.csoonline.com/index.rss',
    'https://www.scmagazine.com/rss/feed.aspx'
]

# E-Mail-Konfiguration
from_email = ''
to_email = ''
smtp_server = ''
smtp_port = 587
smtp_user = ''
smtp_password = os.getenv('SMTP_PASSWORD')
if not smtp_password:
    print("Umgebungsvariable 'SMTP_PASSWORD' ist nicht gesetzt.")
    exit(1)

max_items_per_feed = 3
sent_news_file = 'sent_news.json'

def fetch_news(max_items=5):
    """Ruft die neuesten Nachrichten aus den konfigurierten RSS-Feeds ab."""
    news_items = []
    for feed in feeds:
        print(f"Abrufen von Feed: {feed}")
        parsed_feed = feedparser.parse(feed)
        for entry in parsed_feed.entries[:max_items]:
            news_items.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.get('published', 'Keine Daten'),
                'source': feed
            })
    return news_items

def remove_duplicates(news_items):
    """Entfernt doppelte Nachrichten basierend auf Titel und Link."""
    seen = set()
    unique_news = []
    for item in news_items:
        identifier = (item['title'], item['link'])
        if identifier not in seen:
            unique_news.append(item)
            seen.add(identifier)
    return unique_news

def load_sent_news(file_path):
    """Lädt die Liste der am Vortag gesendeten Nachrichten aus einer JSON-Datei."""
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError:
            return []

def save_sent_news(file_path, news_items):
    """Speichert die Liste der gesendeten Nachrichten in einer JSON-Datei."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(news_items, file, ensure_ascii=False, indent=4)

def filter_new_news(current_news, sent_news):
    """Filtert Nachrichten, die bereits am Vortag gesendet wurden."""
    sent_titles = set(item['title'] for item in sent_news)
    new_news = [item for item in current_news if item['title'] not in sent_titles]
    return new_news

def format_email_body(news_items):
    """Formatiert den E-Mail-Inhalt im erweiterten HTML-Format mit zusätzlichen Verbesserungen."""
    grouped_news = {}
    for item in news_items:
        source = item['source']
        if source not in grouped_news:
            grouped_news[source] = []
        grouped_news[source].append(item)
    html = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    color: #333333;
                }}
                .container {{
                    width: 80%;
                    margin: auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    padding-bottom: 20px;
                    border-bottom: 2px solid #e0e0e0;
                }}
                .header h1 {{
                    margin: 0;
                    color: #2c3e50;
                }}
                .header img {{
                    max-width: 150px;
                    margin-bottom: 10px;
                }}
                .news-section {{
                    margin-top: 20px;
                }}
                .news-section h2 {{
                    background-color: #2c3e50;
                    color: #ffffff;
                    padding: 10px;
                    border-radius: 3px;
                }}
                .news-item {{
                    margin-bottom: 15px;
                }}
                .news-item h3 {{
                    margin: 0;
                    color: #2980b9;
                }}
                .news-item p {{
                    margin: 5px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    font-size: 12px;
                    color: #777777;
                    border-top: 1px solid #e0e0e0;
                    padding-top: 10px;
                }}
                a {{
                    color: #2980b9;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                    color: #1abc9c;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>IT-Security und K.I. News</h1>
                    <p>{datetime.now().strftime('%Y-%m-%d')}</p>
                </div>
    """
    for source, items in grouped_news.items():
        source_name = get_source_name(source)
        html += f"""
                <div class="news-section">
                    <h2>Quelle: {source_name}</h2>
        """
        for item in items:
            html += f"""
                    <div class="news-item">
                        <h3>{item['title']}</h3>
                        <p><a href="{item['link']}">Artikel lesen</a></p>
                        <p><strong>Veröffentlicht:</strong> {item['published']}</p>
                    </div>
            """
        html += """
                </div>
        """
    
    # Footer hinzufügen
    html += """
                <div class="footer">
                    <p>Dies ist eine automatisch generierte E-Mail mit den wichtigsten News des Tage im Bereich Cybersecurity.</p>
                </div>
            </div>
        </body>
    </html>
    """
    return html

def get_source_name(source_url):
    """Extrahiert einen lesbaren Namen aus der Quell-URL."""
    if 'heise.de' in source_url:
        return 'Heise Security'
    elif 'golem.de' in source_url:
        return 'Golem Security'
    elif 'arstechnica.com' in source_url:
        return 'Ars Technica Security'
    elif 'thehackernews.com' in source_url:
        return 'The Hacker News'
    elif 'darkreading.com' in source_url:
        return 'Dark Reading'
    elif 'infosecurity-magazine.com' in source_url:
        return 'InfoSecurity Magazine'
    elif 'krebsonsecurity.com' in source_url:
        return 'Krebs on Security'
    elif 'threatpost.com' in source_url:
        return 'Threatpost'
    elif 'zdnet.com' in source_url:
        return 'ZDNet Security'
    elif 'security.googleblog.com' in source_url:
        return 'Google Security Blog'
    elif 'csoonline.com' in source_url:
        return 'CSO Online'
    elif 'scmagazine.com' in source_url:
        return 'SC Magazine'
    else:
        return 'Unbekannte Quelle'


def send_email(news_items):
    """Sendet eine E-Mail mit den abgerufenen Nachrichten."""
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = f"IT-Security und K.I. News - {datetime.now().strftime('%Y-%m-%d')}"
    
    body = format_email_body(news_items)
    msg.attach(MIMEText(body, 'html'))
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())
        print("E-Mail erfolgreich versendet.")
    except Exception as e:
        print(f"Fehler beim Versenden der E-Mail: {e}")

def main():
    """Hauptfunktion des Skripts."""
    print("Skript gestartet.")
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    sent_news = load_sent_news(sent_news_file)
    news_items = fetch_news(max_items_per_feed)
    unique_news = remove_duplicates(news_items)
    new_news = filter_new_news(unique_news, sent_news)
    
    if not new_news:
        print("Keine neuen Nachrichten zum Versenden.")
        return
    send_email(new_news)
    save_sent_news(sent_news_file, new_news)
    
    print("Skript beendet.")

if __name__ == "__main__":
    main()
