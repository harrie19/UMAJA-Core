"""
Email Distribution System für UMAJA-Core
Sendet Daily Smiles per Email an Abonnenten

Features:
- Newsletter-Verwaltung
- Multi-Language Support (8 Sprachen)
- GDPR-konform mit Opt-in/Opt-out
- Automatisierte Daily Smiles
- HTML + Plain Text Format
"""

import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailDistributor:
    """
    Email-Verteiler für UMAJA Daily Smiles
    """
    
    def __init__(
        self,
        smtp_host: str = "smtp.gmail.com",
        smtp_port: int = 587,
        smtp_user: str = None,
        smtp_password: str = None,
        subscribers_file: str = "data/email_subscribers.json"
    ):
        """
        Initialisiere Email-Verteiler
        
        Args:
            smtp_host: SMTP Server Host
            smtp_port: SMTP Server Port
            smtp_user: SMTP Username/Email
            smtp_password: SMTP Passwort
            subscribers_file: Pfad zur Abonnenten-Datenbank
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        
        self.subscribers_file = Path(subscribers_file)
        self.subscribers_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.subscribers = self._load_subscribers()
    
    def _load_subscribers(self) -> Dict:
        """Lade Abonnenten-Datenbank"""
        if self.subscribers_file.exists():
            try:
                with open(self.subscribers_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Konnte Abonnenten nicht laden: {e}")
        
        return {
            "subscribers": [],
            "unsubscribed": [],
            "stats": {
                "total_sent": 0,
                "total_opened": 0,
                "total_clicked": 0
            }
        }
    
    def _save_subscribers(self):
        """Speichere Abonnenten-Datenbank"""
        with open(self.subscribers_file, 'w') as f:
            json.dump(self.subscribers, f, indent=2)
    
    def add_subscriber(
        self,
        email: str,
        name: str = None,
        language: str = "en",
        source: str = "website"
    ) -> bool:
        """
        Füge neuen Abonnenten hinzu
        
        Args:
            email: Email-Adresse
            name: Name (optional)
            language: Bevorzugte Sprache (en, es, hi, ar, zh, pt, fr, ru)
            source: Quelle der Anmeldung
            
        Returns:
            True wenn erfolgreich hinzugefügt
        """
        # Prüfe ob bereits abonniert
        if any(sub['email'] == email for sub in self.subscribers['subscribers']):
            logger.info(f"Email {email} bereits abonniert")
            return False
        
        subscriber = {
            "email": email,
            "name": name,
            "language": language,
            "source": source,
            "subscribed_at": datetime.utcnow().isoformat(),
            "status": "active",
            "confirmed": False  # Benötigt Double-Opt-In
        }
        
        self.subscribers['subscribers'].append(subscriber)
        self._save_subscribers()
        
        logger.info(f"Neuer Abonnent: {email} ({language})")
        return True
    
    def remove_subscriber(self, email: str) -> bool:
        """
        Entferne Abonnenten (Unsubscribe)
        
        Args:
            email: Email-Adresse
            
        Returns:
            True wenn erfolgreich entfernt
        """
        # Finde und entferne Abonnenten
        subscriber = None
        for i, sub in enumerate(self.subscribers['subscribers']):
            if sub['email'] == email:
                subscriber = self.subscribers['subscribers'].pop(i)
                break
        
        if subscriber:
            subscriber['unsubscribed_at'] = datetime.utcnow().isoformat()
            self.subscribers['unsubscribed'].append(subscriber)
            self._save_subscribers()
            
            logger.info(f"Abonnent entfernt: {email}")
            return True
        
        return False
    
    def send_daily_smile(
        self,
        smile_content: str,
        subject: str = None,
        language: str = "en",
        test_mode: bool = False,
        test_email: str = None
    ) -> Dict:
        """
        Sende Daily Smile an alle Abonnenten
        
        Args:
            smile_content: Der Daily Smile Text
            subject: Email-Betreff (optional)
            language: Sprache (None = alle Sprachen)
            test_mode: Wenn True, nur an test_email senden
            test_email: Test-Email-Adresse
            
        Returns:
            Dictionary mit Statistiken
        """
        if subject is None:
            subject = f"🌞 Your Daily Smile - {datetime.utcnow().strftime('%B %d, %Y')}"
        
        # Erstelle HTML und Plain Text
        html_body = self._create_html_email(smile_content, subject)
        text_body = self._create_text_email(smile_content)
        
        # Filtere Empfänger
        if test_mode and test_email:
            recipients = [{"email": test_email, "name": "Test User", "language": language}]
        else:
            recipients = [
                sub for sub in self.subscribers['subscribers']
                if sub['status'] == 'active' and sub['confirmed']
                and (language is None or sub['language'] == language)
            ]
        
        # Sende Emails
        sent_count = 0
        failed_count = 0
        
        for recipient in recipients:
            try:
                self._send_email(
                    to_email=recipient['email'],
                    to_name=recipient.get('name'),
                    subject=subject,
                    html_body=html_body,
                    text_body=text_body
                )
                sent_count += 1
                logger.info(f"Email gesendet an: {recipient['email']}")
            
            except Exception as e:
                failed_count += 1
                logger.error(f"Fehler beim Senden an {recipient['email']}: {e}")
        
        # Update Statistiken
        self.subscribers['stats']['total_sent'] += sent_count
        self._save_subscribers()
        
        return {
            "sent": sent_count,
            "failed": failed_count,
            "total_recipients": len(recipients),
            "language": language,
            "test_mode": test_mode
        }
    
    def _send_email(
        self,
        to_email: str,
        to_name: Optional[str],
        subject: str,
        html_body: str,
        text_body: str
    ):
        """
        Sende einzelne Email via SMTP
        
        Args:
            to_email: Empfänger-Email
            to_name: Empfänger-Name
            subject: Betreff
            html_body: HTML-Inhalt
            text_body: Plain-Text-Inhalt
        """
        # Erstelle Multipart-Nachricht
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"UMAJA Daily Smiles <{self.smtp_user}>"
        msg['To'] = f"{to_name} <{to_email}>" if to_name else to_email
        
        # Füge Plain Text und HTML hinzu
        part1 = MIMEText(text_body, 'plain', 'utf-8')
        part2 = MIMEText(html_body, 'html', 'utf-8')
        
        msg.attach(part1)
        msg.attach(part2)
        
        # Sende via SMTP
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
    
    def _create_html_email(self, content: str, title: str) -> str:
        """Erstelle HTML-Email-Template"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            background-color: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #FF6B6B;
            margin: 0;
            font-size: 28px;
        }}
        .emoji {{
            font-size: 48px;
            margin: 20px 0;
        }}
        .content {{
            font-size: 16px;
            line-height: 1.8;
            margin: 20px 0;
            padding: 20px;
            background-color: #FFF9E6;
            border-left: 4px solid #FFD93D;
            border-radius: 5px;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 14px;
            color: #666;
        }}
        .unsubscribe {{
            color: #999;
            font-size: 12px;
            margin-top: 20px;
        }}
        .unsubscribe a {{
            color: #999;
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="emoji">😊</div>
            <h1>{title}</h1>
        </div>
        
        <div class="content">
            {content.replace(chr(10), '<br>')}
        </div>
        
        <div class="footer">
            <p><strong>UMAJA-Core</strong></p>
            <p>Bringing smiles to all 8 billion people on Earth 🌍</p>
            <p style="color: #FF6B6B;">40% of our revenue goes to charity 💝</p>
            
            <div class="unsubscribe">
                <p>Du erhältst diese Email, weil du dich für UMAJA Daily Smiles angemeldet hast.</p>
                <p><a href="mailto:{self.smtp_user}?subject=Unsubscribe">Abmelden</a></p>
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    def _create_text_email(self, content: str) -> str:
        """Erstelle Plain-Text-Email"""
        return f"""
╔════════════════════════════════════════════════════════════════╗
║                    🌞 YOUR DAILY SMILE                         ║
╚════════════════════════════════════════════════════════════════╝

{content}

────────────────────────────────────────────────────────────────

UMAJA-Core - Bringing smiles to all 8 billion people on Earth 🌍
40% of our revenue goes to charity 💝

Du erhältst diese Email, weil du dich für UMAJA Daily Smiles 
angemeldet hast.

Abmelden: Antworte mit "UNSUBSCRIBE" auf diese Email

────────────────────────────────────────────────────────────────
"""
    
    def get_statistics(self) -> Dict:
        """Hole Statistiken über Email-Distribution"""
        active_subscribers = [
            sub for sub in self.subscribers['subscribers']
            if sub['status'] == 'active'
        ]
        
        # Sprachen-Verteilung
        language_distribution = {}
        for sub in active_subscribers:
            lang = sub.get('language', 'en')
            language_distribution[lang] = language_distribution.get(lang, 0) + 1
        
        return {
            "total_subscribers": len(active_subscribers),
            "confirmed_subscribers": len([s for s in active_subscribers if s.get('confirmed')]),
            "unsubscribed": len(self.subscribers['unsubscribed']),
            "language_distribution": language_distribution,
            "total_sent": self.subscribers['stats']['total_sent'],
            "total_opened": self.subscribers['stats']['total_opened'],
            "total_clicked": self.subscribers['stats']['total_clicked']
        }


# ============================================
# Command-Line Interface
# ============================================

if __name__ == "__main__":
    import argparse
    import sys
    
    # Füge src zu path hinzu
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from personality_engine import PersonalityEngine
    
    parser = argparse.ArgumentParser(description="UMAJA Email Distribution System")
    parser.add_argument("--add", metavar="EMAIL", help="Füge neuen Abonnenten hinzu")
    parser.add_argument("--name", metavar="NAME", help="Name des Abonnenten")
    parser.add_argument("--language", default="en", help="Sprache (en, es, hi, ar, zh, pt, fr, ru)")
    parser.add_argument("--remove", metavar="EMAIL", help="Entferne Abonnenten")
    parser.add_argument("--send", action="store_true", help="Sende Daily Smile")
    parser.add_argument("--test", metavar="EMAIL", help="Test-Modus: Sende nur an diese Email")
    parser.add_argument("--stats", action="store_true", help="Zeige Statistiken")
    
    args = parser.parse_args()
    
    # Initialisiere Distributor (benötigt Env-Variablen für SMTP)
    import os
    distributor = EmailDistributor(
        smtp_user=os.getenv('SMTP_USER'),
        smtp_password=os.getenv('SMTP_PASSWORD')
    )
    
    if args.add:
        success = distributor.add_subscriber(
            email=args.add,
            name=args.name,
            language=args.language
        )
        if success:
            print(f"✅ Abonnent hinzugefügt: {args.add}")
        else:
            print(f"⚠️  Abonnent existiert bereits: {args.add}")
    
    elif args.remove:
        success = distributor.remove_subscriber(args.remove)
        if success:
            print(f"✅ Abonnent entfernt: {args.remove}")
        else:
            print(f"⚠️  Abonnent nicht gefunden: {args.remove}")
    
    elif args.send:
        # Generiere Daily Smile
        engine = PersonalityEngine()
        smile = engine.generate_daily_smile()
        
        # Sende Email
        if args.test:
            print(f"📧 Sende Test-Email an {args.test}...")
            result = distributor.send_daily_smile(
                smile_content=smile['content'],
                test_mode=True,
                test_email=args.test
            )
        else:
            print("📧 Sende Daily Smiles an alle Abonnenten...")
            result = distributor.send_daily_smile(smile_content=smile['content'])
        
        print(f"\n✅ Ergebnis:")
        print(f"   Gesendet: {result['sent']}")
        print(f"   Fehler: {result['failed']}")
        print(f"   Gesamt: {result['total_recipients']}")
    
    elif args.stats:
        stats = distributor.get_statistics()
        print("\n📊 Email-Statistiken:")
        print(f"   Aktive Abonnenten: {stats['total_subscribers']}")
        print(f"   Bestätigt: {stats['confirmed_subscribers']}")
        print(f"   Abgemeldet: {stats['unsubscribed']}")
        print(f"   Gesendete Emails: {stats['total_sent']}")
        print(f"\n   Sprachen-Verteilung:")
        for lang, count in stats['language_distribution'].items():
            print(f"      {lang}: {count}")
    
    else:
        parser.print_help()
