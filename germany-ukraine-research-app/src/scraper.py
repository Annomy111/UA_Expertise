#!/usr/bin/env python3
"""
Web-Scraper für Germany-Ukraine Contact Research
Durchsucht verschiedene Quellen nach aktuellen Ukraine-Kontakten in Deutschland
"""

import requests
from bs4 import BeautifulSoup
import yaml
import time
import re
from datetime import datetime
from fake_useragent import UserAgent
from dotenv import load_dotenv
from database import db_manager
import json

# Lade Umgebungsvariablen
load_dotenv()


class ContactScraper:
    """Haupt-Scraper-Klasse"""

    def __init__(self, config_path='config/sources.yaml'):
        self.config = self.load_config(config_path)
        self.ua = UserAgent()
        self.session = requests.Session()
        self.results = []

    def load_config(self, config_path):
        """Lade Konfiguration"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get_headers(self):
        """Generiere Headers"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'de-DE,de;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }

    def extract_contact_info(self, soup, base_url):
        """Extrahiere Kontaktinformationen aus HTML"""
        contact_info = {}

        # E-Mail-Adressen
        emails = set()
        for link in soup.find_all('a', href=re.compile(r'^mailto:')):
            email = link['href'].replace('mailto:', '').split('?')[0]
            emails.add(email.lower())

        # Auch im Text suchen
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        text = soup.get_text()
        found_emails = re.findall(email_pattern, text)
        emails.update([e.lower() for e in found_emails])

        if emails:
            contact_info['email'] = list(emails)[0]  # Nehme erste gefundene E-Mail

        # Telefonnummern
        phone_patterns = [
            r'\+49[\s\-]?\d{1,4}[\s\-]?\d{1,10}',
            r'0\d{2,5}[\s\-]?\d{1,10}',
        ]
        phones = set()
        for pattern in phone_patterns:
            found = re.findall(pattern, text)
            phones.update(found)

        if phones:
            contact_info['phone'] = list(phones)[0]

        # Adresse (vereinfacht)
        address_keywords = ['straße', 'strasse', 'platz', 'weg', 'allee']
        for line in text.split('\n'):
            line = line.strip()
            if any(keyword in line.lower() for keyword in address_keywords):
                if len(line) < 100:  # Nur kurze Zeilen (wahrscheinlich Adressen)
                    contact_info['address'] = line
                    break

        # Social Media
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'twitter.com' in href:
                contact_info['twitter'] = href
            elif 'linkedin.com' in href:
                contact_info['linkedin'] = href
            elif 'facebook.com' in href:
                contact_info['facebook'] = href

        return contact_info

    def scrape_website(self, source):
        """Scrape eine einzelne Website"""
        url = source.get('url')
        name = source.get('name')
        source_type = source.get('type')
        keywords = source.get('keywords', [])

        print(f"\n🔍 Durchsuche: {name}")
        print(f"   URL: {url}")

        try:
            # Hauptseite abrufen
            response = self.session.get(
                url,
                headers=self.get_headers(),
                timeout=self.config['scraping']['timeout']
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extrahiere Kontaktinformationen
            contact_info = self.extract_contact_info(soup, url)

            # Versuche Beschreibung zu finden
            description = ""
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                description = meta_desc['content']

            # Suche nach Ukraine-relevanten Seiten
            ukraine_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                link_text = link.get_text().lower()

                # Prüfe ob Link Ukraine-relevant ist
                if any(keyword.lower() in link_text for keyword in keywords):
                    if href.startswith('http'):
                        ukraine_links.append(href)
                    elif href.startswith('/'):
                        ukraine_links.append(f"{url.rstrip('/')}{href}")

            # Erstelle Kontakt-Eintrag
            contact_data = {
                'name': name,
                'organization': name,
                'type': source_type,
                'website': url,
                'description': description,
                'focus_areas': json.dumps(keywords, ensure_ascii=False),
                'source_url': url,
                **contact_info
            }

            # Speichere in Datenbank
            db_manager.add_contact(contact_data)

            # Durchsuche Ukraine-spezifische Unterseiten
            for ukraine_url in ukraine_links[:3]:  # Max 3 Unterseiten
                try:
                    time.sleep(self.config['scraping']['delay_between_requests'])
                    sub_response = self.session.get(
                        ukraine_url,
                        headers=self.get_headers(),
                        timeout=self.config['scraping']['timeout']
                    )
                    sub_soup = BeautifulSoup(sub_response.content, 'html.parser')
                    sub_contact_info = self.extract_contact_info(sub_soup, ukraine_url)

                    # Wenn neue Kontaktinfos gefunden, aktualisiere
                    if sub_contact_info:
                        contact_data.update(sub_contact_info)
                        contact_data['source_url'] = ukraine_url
                        db_manager.add_contact(contact_data)

                except Exception as e:
                    print(f"   ⚠ Unterseite {ukraine_url} konnte nicht geladen werden")

            db_manager.log_search(
                search_term=f"{name} - {', '.join(keywords)}",
                source=url,
                results_found=1,
                success=True
            )

            print(f"   ✓ Erfolgreich")
            return True

        except Exception as e:
            print(f"   ✗ Fehler: {e}")
            db_manager.log_search(
                search_term=f"{name}",
                source=url,
                results_found=0,
                success=False,
                error=str(e)
            )
            return False

    def search_web(self, search_term, city=None):
        """
        Führe Web-Suche durch (würde normalerweise Google Search API nutzen)
        Placeholder-Implementierung - in Produktion würde man SerpAPI oder ähnliches nutzen
        """
        print(f"\n🔎 Web-Suche: {search_term}")
        if city:
            search_term = f"{search_term} {city}"

        # Hier würde man SerpAPI oder ähnliches integrieren
        # Placeholder für Demo-Zwecke
        print(f"   ℹ Web-Suche würde hier durchgeführt: '{search_term}'")
        print(f"   ℹ Für echte Web-Suche: SerpAPI-Key in .env eintragen")

        return []

    def run_full_scan(self):
        """Führe vollständigen Scan aller Quellen durch"""
        print("=" * 60)
        print("🚀 Starte vollständigen Scan")
        print("=" * 60)

        db_manager.initialize()

        total_sources = 0
        successful = 0

        # Durchlaufe alle Kategorien
        for category, sources in self.config['sources'].items():
            if category == 'local':
                # Für lokale Initiativen: Web-Suche
                print(f"\n📍 Kategorie: {category}")
                for source in sources:
                    search_term = source.get('search_term')
                    if search_term:
                        self.search_web(search_term)
                        time.sleep(self.config['scraping']['delay_between_requests'])
            else:
                # Für bekannte Organisationen: Direct Scraping
                print(f"\n📂 Kategorie: {category}")
                for source in sources:
                    total_sources += 1
                    if self.scrape_website(source):
                        successful += 1
                    time.sleep(self.config['scraping']['delay_between_requests'])

        # Statistiken
        print("\n" + "=" * 60)
        print("📊 Scan abgeschlossen")
        print("=" * 60)
        print(f"Quellen durchsucht: {total_sources}")
        print(f"Erfolgreich: {successful}")
        print(f"Fehler: {total_sources - successful}")

        stats = db_manager.get_statistics()
        print(f"\n📈 Datenbank-Statistiken:")
        print(f"Gesamt Kontakte: {stats['total_contacts']}")
        for contact_type, count in stats['by_type'].items():
            print(f"  - {contact_type}: {count}")

    def update_contacts(self):
        """Aktualisiere existierende Kontakte"""
        print("🔄 Aktualisiere existierende Kontakte...")
        # Diese Funktion würde alle Kontakte durchgehen und aktualisieren
        self.run_full_scan()


def main():
    """Hauptfunktion"""
    scraper = ContactScraper()
    scraper.run_full_scan()


if __name__ == '__main__':
    main()
