"""
SMS Distribution System für UMAJA-Core
Sendet Daily Smiles per SMS an Abonnenten

Features:
- SMS-Broadcasts
- Multi-Language Support
- Opt-in/Opt-out (GDPR-konform)
- Low-bandwidth friendly
- Twilio & andere Gateways support
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SMSDistributor:
    """
    SMS-Verteiler für UMAJA Daily Smiles
    """
    
    def __init__(
        self,
        provider: str = "twilio",
        account_sid: str = None,
        auth_token: str = None,
        from_number: str = None,
        subscribers_file: str = "data/sms_subscribers.json"
    ):
        """
        Initialisiere SMS-Verteiler
        
        Args:
            provider: SMS-Gateway-Provider (twilio, plivo, etc.)
            account_sid: Account SID
            auth_token: Auth Token
            from_number: Absender-Telefonnummer
            subscribers_file: Pfad zur Abonnenten-Datenbank
        """
        self.provider = provider
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number
        
        self.subscribers_file = Path(subscribers_file)
        self.subscribers_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.subscribers = self._load_subscribers()
        
        # Initialisiere Provider-Client
        self.client = self._init_provider_client()
    
    def _init_provider_client(self):
        """Initialisiere SMS-Provider-Client"""
        if self.provider == "twilio":
            try:
                from twilio.rest import Client
                return Client(self.account_sid, self.auth_token)
            except ImportError:
                logger.warning("Twilio nicht installiert. Installiere mit: pip install twilio")
                return None
        
        elif self.provider == "plivo":
            try:
                import plivo
                return plivo.RestClient(self.account_sid, self.auth_token)
            except ImportError:
                logger.warning("Plivo nicht installiert. Installiere mit: pip install plivo")
                return None
        
        else:
            logger.warning(f"Unbekannter SMS-Provider: {self.provider}")
            return None
    
    def _load_subscribers(self) -> Dict:
        """Lade Abonnenten-Datenbank"""
        if self.subscribers_file.exists():
            try:
                with open(self.subscribers_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Konnte SMS-Abonnenten nicht laden: {e}")
        
        return {
            "subscribers": [],
            "unsubscribed": [],
            "stats": {
                "total_sent": 0,
                "total_delivered": 0,
                "total_failed": 0
            }
        }
    
    def _save_subscribers(self):
        """Speichere Abonnenten-Datenbank"""
        with open(self.subscribers_file, 'w') as f:
            json.dump(self.subscribers, f, indent=2)
    
    def add_subscriber(
        self,
        phone_number: str,
        name: str = None,
        language: str = "en",
        country_code: str = None,
        source: str = "website"
    ) -> bool:
        """
        Füge neuen SMS-Abonnenten hinzu
        
        Args:
            phone_number: Telefonnummer (mit Ländervorwahl)
            name: Name (optional)
            language: Bevorzugte Sprache
            country_code: Ländercode (z.B. "DE", "US")
            source: Quelle der Anmeldung
            
        Returns:
            True wenn erfolgreich hinzugefügt
        """
        # Normalisiere Telefonnummer
        phone_number = self._normalize_phone_number(phone_number)
        
        # Prüfe ob bereits abonniert
        if any(sub['phone'] == phone_number for sub in self.subscribers['subscribers']):
            logger.info(f"Nummer {phone_number} bereits abonniert")
            return False
        
        subscriber = {
            "phone": phone_number,
            "name": name,
            "language": language,
            "country_code": country_code,
            "source": source,
            "subscribed_at": datetime.utcnow().isoformat(),
            "status": "active",
            "confirmed": False  # Benötigt Double-Opt-In
        }
        
        self.subscribers['subscribers'].append(subscriber)
        self._save_subscribers()
        
        logger.info(f"Neuer SMS-Abonnent: {phone_number} ({language})")
        return True
    
    def remove_subscriber(self, phone_number: str) -> bool:
        """
        Entferne Abonnenten (Unsubscribe)
        
        Args:
            phone_number: Telefonnummer
            
        Returns:
            True wenn erfolgreich entfernt
        """
        phone_number = self._normalize_phone_number(phone_number)
        
        # Finde und entferne Abonnenten
        subscriber = None
        for i, sub in enumerate(self.subscribers['subscribers']):
            if sub['phone'] == phone_number:
                subscriber = self.subscribers['subscribers'].pop(i)
                break
        
        if subscriber:
            subscriber['unsubscribed_at'] = datetime.utcnow().isoformat()
            self.subscribers['unsubscribed'].append(subscriber)
            self._save_subscribers()
            
            logger.info(f"SMS-Abonnent entfernt: {phone_number}")
            return True
        
        return False
    
    def send_daily_smile(
        self,
        smile_content: str,
        language: str = None,
        test_mode: bool = False,
        test_number: str = None,
        max_length: int = 160
    ) -> Dict:
        """
        Sende Daily Smile per SMS an alle Abonnenten
        
        Args:
            smile_content: Der Daily Smile Text
            language: Sprache (None = alle Sprachen)
            test_mode: Wenn True, nur an test_number senden
            test_number: Test-Telefonnummer
            max_length: Maximale SMS-Länge (160 = Standard)
            
        Returns:
            Dictionary mit Statistiken
        """
        if not self.client:
            logger.error("SMS-Provider-Client nicht initialisiert")
            return {
                "sent": 0,
                "failed": 0,
                "error": "SMS-Provider nicht verfügbar"
            }
        
        # Kürze Text wenn nötig
        sms_text = self._prepare_sms_text(smile_content, max_length)
        
        # Filtere Empfänger
        if test_mode and test_number:
            recipients = [{"phone": test_number, "name": "Test User", "language": language}]
        else:
            recipients = [
                sub for sub in self.subscribers['subscribers']
                if sub['status'] == 'active' and sub['confirmed']
                and (language is None or sub['language'] == language)
            ]
        
        # Sende SMS
        sent_count = 0
        failed_count = 0
        
        for recipient in recipients:
            try:
                self._send_sms(
                    to_number=recipient['phone'],
                    message=sms_text
                )
                sent_count += 1
                logger.info(f"SMS gesendet an: {recipient['phone']}")
            
            except Exception as e:
                failed_count += 1
                logger.error(f"Fehler beim Senden an {recipient['phone']}: {e}")
        
        # Update Statistiken
        self.subscribers['stats']['total_sent'] += sent_count
        self.subscribers['stats']['total_failed'] += failed_count
        self._save_subscribers()
        
        return {
            "sent": sent_count,
            "failed": failed_count,
            "total_recipients": len(recipients),
            "language": language,
            "test_mode": test_mode,
            "message_length": len(sms_text)
        }
    
    def _send_sms(self, to_number: str, message: str):
        """
        Sende einzelne SMS via Provider
        
        Args:
            to_number: Empfänger-Telefonnummer
            message: SMS-Text
        """
        if self.provider == "twilio":
            self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
        
        elif self.provider == "plivo":
            self.client.messages.create(
                src=self.from_number,
                dst=to_number,
                text=message
            )
        
        else:
            raise Exception(f"Provider {self.provider} nicht unterstützt")
    
    def _prepare_sms_text(self, content: str, max_length: int = 160) -> str:
        """
        Bereite Text für SMS vor (kürzen wenn nötig)
        
        Args:
            content: Original-Text
            max_length: Maximale Länge
            
        Returns:
            Gekürzter Text mit Emoji und Unsubscribe-Info
        """
        # Füge Emoji hinzu
        prefix = "😊 "
        suffix = "\n\nSTOP: Reply STOP"
        
        available_length = max_length - len(prefix) - len(suffix)
        
        # Kürze Text wenn nötig
        if len(content) > available_length:
            content = content[:available_length-3] + "..."
        
        return f"{prefix}{content}{suffix}"
    
    def _normalize_phone_number(self, phone: str) -> str:
        """
        Normalisiere Telefonnummer
        
        Args:
            phone: Telefonnummer (verschiedene Formate)
            
        Returns:
            Normalisierte Nummer im Format +49123456789
        """
        # Entferne alle Nicht-Ziffern außer +
        import re
        phone = re.sub(r'[^\d+]', '', phone)
        
        # Stelle sicher dass + am Anfang steht
        if not phone.startswith('+'):
            # Default: Deutsche Vorwahl wenn keine angegeben
            phone = '+49' + phone.lstrip('0')
        
        return phone
    
    def get_statistics(self) -> Dict:
        """Hole Statistiken über SMS-Distribution"""
        active_subscribers = [
            sub for sub in self.subscribers['subscribers']
            if sub['status'] == 'active'
        ]
        
        # Sprachen-Verteilung
        language_distribution = {}
        for sub in active_subscribers:
            lang = sub.get('language', 'en')
            language_distribution[lang] = language_distribution.get(lang, 0) + 1
        
        # Länder-Verteilung
        country_distribution = {}
        for sub in active_subscribers:
            country = sub.get('country_code', 'Unknown')
            country_distribution[country] = country_distribution.get(country, 0) + 1
        
        return {
            "total_subscribers": len(active_subscribers),
            "confirmed_subscribers": len([s for s in active_subscribers if s.get('confirmed')]),
            "unsubscribed": len(self.subscribers['unsubscribed']),
            "language_distribution": language_distribution,
            "country_distribution": country_distribution,
            "total_sent": self.subscribers['stats']['total_sent'],
            "total_delivered": self.subscribers['stats']['total_delivered'],
            "total_failed": self.subscribers['stats']['total_failed']
        }
    
    def send_confirmation_sms(self, phone_number: str) -> bool:
        """
        Sende Bestätigungs-SMS für Double-Opt-In
        
        Args:
            phone_number: Telefonnummer
            
        Returns:
            True wenn erfolgreich gesendet
        """
        if not self.client:
            return False
        
        message = """😊 UMAJA Daily Smiles

Welcome! Reply YES to confirm your subscription.

You'll receive one smile per day.

Reply STOP to unsubscribe anytime."""
        
        try:
            self._send_sms(phone_number, message)
            logger.info(f"Bestätigungs-SMS gesendet an: {phone_number}")
            return True
        except Exception as e:
            logger.error(f"Fehler beim Senden der Bestätigungs-SMS: {e}")
            return False


# ============================================
# Command-Line Interface
# ============================================

if __name__ == "__main__":
    import argparse
    import sys
    
    # Füge src zu path hinzu
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from personality_engine import PersonalityEngine
    
    parser = argparse.ArgumentParser(description="UMAJA SMS Distribution System")
    parser.add_argument("--add", metavar="PHONE", help="Füge neuen Abonnenten hinzu")
    parser.add_argument("--name", metavar="NAME", help="Name des Abonnenten")
    parser.add_argument("--language", default="en", help="Sprache (en, es, hi, ar, zh, pt, fr, ru)")
    parser.add_argument("--country", metavar="CODE", help="Ländercode (z.B. DE, US)")
    parser.add_argument("--remove", metavar="PHONE", help="Entferne Abonnenten")
    parser.add_argument("--send", action="store_true", help="Sende Daily Smile")
    parser.add_argument("--test", metavar="PHONE", help="Test-Modus: Sende nur an diese Nummer")
    parser.add_argument("--stats", action="store_true", help="Zeige Statistiken")
    parser.add_argument("--confirm", metavar="PHONE", help="Sende Bestätigungs-SMS")
    
    args = parser.parse_args()
    
    # Initialisiere Distributor (benötigt Env-Variablen)
    import os
    distributor = SMSDistributor(
        provider=os.getenv('SMS_PROVIDER', 'twilio'),
        account_sid=os.getenv('SMS_ACCOUNT_SID'),
        auth_token=os.getenv('SMS_AUTH_TOKEN'),
        from_number=os.getenv('SMS_FROM_NUMBER')
    )
    
    if args.add:
        success = distributor.add_subscriber(
            phone_number=args.add,
            name=args.name,
            language=args.language,
            country_code=args.country
        )
        if success:
            print(f"✅ SMS-Abonnent hinzugefügt: {args.add}")
            # Sende Bestätigungs-SMS
            if distributor.send_confirmation_sms(args.add):
                print(f"📱 Bestätigungs-SMS gesendet")
        else:
            print(f"⚠️  Abonnent existiert bereits: {args.add}")
    
    elif args.remove:
        success = distributor.remove_subscriber(args.remove)
        if success:
            print(f"✅ SMS-Abonnent entfernt: {args.remove}")
        else:
            print(f"⚠️  Abonnent nicht gefunden: {args.remove}")
    
    elif args.send:
        # Generiere Daily Smile
        engine = PersonalityEngine()
        smile = engine.generate_daily_smile()
        
        # Sende SMS
        if args.test:
            print(f"📱 Sende Test-SMS an {args.test}...")
            result = distributor.send_daily_smile(
                smile_content=smile['content'],
                test_mode=True,
                test_number=args.test
            )
        else:
            print("📱 Sende Daily Smiles an alle SMS-Abonnenten...")
            result = distributor.send_daily_smile(smile_content=smile['content'])
        
        print(f"\n✅ Ergebnis:")
        print(f"   Gesendet: {result['sent']}")
        print(f"   Fehler: {result['failed']}")
        print(f"   Gesamt: {result['total_recipients']}")
        print(f"   Nachrichtenlänge: {result['message_length']} Zeichen")
    
    elif args.confirm:
        if distributor.send_confirmation_sms(args.confirm):
            print(f"✅ Bestätigungs-SMS gesendet an: {args.confirm}")
        else:
            print(f"❌ Fehler beim Senden der Bestätigungs-SMS")
    
    elif args.stats:
        stats = distributor.get_statistics()
        print("\n📊 SMS-Statistiken:")
        print(f"   Aktive Abonnenten: {stats['total_subscribers']}")
        print(f"   Bestätigt: {stats['confirmed_subscribers']}")
        print(f"   Abgemeldet: {stats['unsubscribed']}")
        print(f"   Gesendete SMS: {stats['total_sent']}")
        print(f"   Zugestellt: {stats['total_delivered']}")
        print(f"   Fehler: {stats['total_failed']}")
        print(f"\n   Sprachen-Verteilung:")
        for lang, count in stats['language_distribution'].items():
            print(f"      {lang}: {count}")
        print(f"\n   Länder-Verteilung:")
        for country, count in stats['country_distribution'].items():
            print(f"      {country}: {count}")
    
    else:
        parser.print_help()
