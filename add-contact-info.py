#!/usr/bin/env python3

import requests
import json
import time
import sys
import random
from typing import Dict, List, Any, Optional
import uuid
import re

# Serper API-Schlüssel
SERPER_API_KEY = "24f44e45b73e32ac7e31b447a0568caa7fa4b0db"

# API-Endpunkte
API_URL = "http://localhost:8000"
EXPERTS_URL = f"{API_URL}/experts"

def get_all_experts() -> List[Dict]:
    """
    Holt alle Experten/Organisationen aus der Datenbank
    """
    try:
        response = requests.get(f"{API_URL}/statistics")
        response.raise_for_status()
        stats = response.json()
        
        total_count = stats["by_type"].get("organization", 0) + stats["by_type"].get("individual", 0)
        print(f"Gefunden: {total_count} Einträge in der Datenbank")
        
        # Hole alle Experten-IDs aus der Datenbank
        all_experts = []
        cities = [city["name"] for city in stats.get("by_city", [])]
        
        # Für jede Stadt Experten holen
        for city_id in range(1, len(cities) + 1):
            print(f"Hole Experten aus Stadt ID {city_id}...")
            response = requests.get(f"{EXPERTS_URL}/city/{city_id}")
            response.raise_for_status()
            city_experts = response.json()
            all_experts.extend(city_experts)
            time.sleep(0.5)  # Kurze Pause zwischen den Anfragen
        
        return all_experts
    except Exception as e:
        print(f"Fehler beim Abrufen aller Experten: {e}")
        return []

def clean_email(email: str) -> str:
    """
    Bereinigt eine E-Mail-Adresse (entfernt abschließende Punkte, etc.)
    """
    # Entferne abschließenden Punkt, falls vorhanden
    if email.endswith('.'):
        email = email[:-1]
    
    # Überprüfe, ob die E-Mail gültig ist (vereinfachte Prüfung)
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return email
    
    return ""

def clean_website(url: str) -> str:
    """
    Bereinigt eine URL (entfernt überflüssige Parameter, etc.)
    """
    # Entferne Tracking-Parameter, falls vorhanden
    if "?" in url:
        url_parts = url.split("?")
        url = url_parts[0]
    
    return url

def get_expert_details(expert_id: str) -> Optional[Dict]:
    """
    Holt Details zu einem bestimmten Experten/Organisation
    """
    try:
        response = requests.get(f"{EXPERTS_URL}/{expert_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Fehler beim Abrufen der Expertendetails für {expert_id}: {e}")
        return None

def search_contact_info(expert: Dict) -> List[Dict]:
    """
    Sucht Kontaktinformationen mithilfe der Serper API
    """
    name = expert.get("name")
    expert_type = expert.get("type")
    
    if not name:
        return []
    
    # Suchanfrage erstellen
    query = f"{name}"
    
    # Für Individuen zusätzliche Informationen hinzufügen
    if expert_type == "individual":
        if expert.get("title") and expert.get("affiliation"):
            query += f" {expert.get('title')} {expert.get('affiliation')}"
        elif expert.get("affiliation"):
            query += f" {expert.get('affiliation')}"
    else:
        # Für Organisationen nach der Stadt suchen
        if expert.get("city_name"):
            query += f" {expert.get('city_name')}"
            
    # "contact" oder "email" hinzufügen, um Kontaktinformationen zu finden
    query += " contact email"
    
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = {
        "q": query,
        "gl": "de",  # Deutschland als geografischer Standort
        "hl": "de",  # Deutsch als Sprache
        "num": 5     # Anzahl der Ergebnisse
    }
    
    try:
        print(f"  Suche nach Kontaktinformationen für: {query}")
        response = requests.post('https://google.serper.dev/search', headers=headers, json=payload)
        response.raise_for_status()
        search_results = response.json()
        
        # Kontaktdaten extrahieren
        contacts = []
        unique_values = {"email": set(), "website": set(), "phone": set()}
        
        # Aus organischen Suchergebnissen
        if 'organic' in search_results:
            for result in search_results['organic'][:3]:  # Beschränkung auf die ersten 3 Ergebnisse
                # Suche nach E-Mail-Adressen im Snippet
                snippet = result.get('snippet', '')
                if '@' in snippet and '.' in snippet:
                    email_parts = [part for part in snippet.split() if '@' in part]
                    for email_part in email_parts:
                        # Bereinigung der E-Mail
                        email = ''.join(c for c in email_part if c.isalnum() or c in ['@', '.', '-', '_'])
                        email = clean_email(email)
                        if email and '@' in email and '.' in email and len(email) > 5:
                            if email not in unique_values["email"]:
                                contacts.append({
                                    "type": "email",
                                    "value": email,
                                    "is_primary": len(contacts) == 0
                                })
                                unique_values["email"].add(email)
                
                # Webseite als Kontakt hinzufügen
                if 'link' in result:
                    website = result.get('link', '')
                    website = clean_website(website)
                    if website and website not in unique_values["website"]:
                        contacts.append({
                            "type": "website",
                            "value": website,
                            "is_primary": len(contacts) == 0
                        })
                        unique_values["website"].add(website)
                        
        # Aus Knowledge Graph (wenn vorhanden)
        if 'knowledgeGraph' in search_results:
            kg = search_results['knowledgeGraph']
            
            # Website
            if 'website' in kg:
                website = kg['website']
                website = clean_website(website)
                if website and website not in unique_values["website"]:
                    contacts.append({
                        "type": "website",
                        "value": website,
                        "is_primary": len(contacts) == 0
                    })
                    unique_values["website"].add(website)
            
            # Telefonnummer
            if 'phone' in kg:
                phone = kg['phone']
                if phone and phone not in unique_values["phone"]:
                    contacts.append({
                        "type": "phone",
                        "value": phone,
                        "is_primary": len(contacts) == 0
                    })
                    unique_values["phone"].add(phone)
                    
            # Social Media
            social_types = ['twitter', 'facebook', 'linkedin', 'instagram']
            for social_type in social_types:
                if social_type in kg:
                    social_url = kg[social_type]
                    if social_url:
                        contacts.append({
                            "type": social_type,
                            "value": social_url,
                            "is_primary": len(contacts) == 0
                        })
        
        return contacts
    except Exception as e:
        print(f"  Fehler bei der Suche nach Kontaktinformationen für {name}: {e}")
        return []

def has_contact_data(expert: Dict) -> bool:
    """
    Überprüft, ob ein Experte/eine Organisation bereits Kontaktdaten hat
    """
    return expert.get("contacts") and len(expert.get("contacts", [])) > 0

def update_expert_contacts(expert_id: str, contacts: List[Dict]) -> bool:
    """
    Aktualisiert die Kontaktdaten eines Experten/einer Organisation
    """
    if not contacts:
        return False
        
    # Bestehende Expertendetails abrufen
    expert_details = get_expert_details(expert_id)
    if not expert_details:
        return False
        
    # Aktualisierungsdaten vorbereiten (nur Kontakte)
    update_data = {
        "name": expert_details.get("name"),  # Erforderlich für die Update-Funktion
        "city_id": expert_details.get("city_id"),  # Erforderlich für die Update-Funktion
        "contacts": contacts
    }
    
    try:
        response = requests.put(f"{EXPERTS_URL}/{expert_id}", json=update_data)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"  Fehler beim Aktualisieren der Kontaktdaten für {expert_id}: {e}")
        return False

def main():
    print("Verarbeite alle Einträge in der Datenbank...")
    all_experts = get_all_experts()
    
    if not all_experts:
        print("Keine Experten gefunden oder Fehler beim Abrufen.")
        return
    
    print(f"Gefunden: {len(all_experts)} Experten/Organisationen.")
    
    # Zähler für erfolgreiche Updates
    success_count = 0
    skip_count = 0
    
    for i, expert in enumerate(all_experts):
        expert_id = expert.get("id")
        
        # Details für jeden Experten abrufen
        expert_details = get_expert_details(expert_id)
        if not expert_details:
            print(f"\nExperte mit ID {expert_id} nicht gefunden.")
            continue
            
        name = expert_details.get("name")
        expert_type = expert_details.get("type")
        
        # Überprüfen, ob bereits Kontaktdaten vorhanden sind
        if has_contact_data(expert_details):
            print(f"\nÜberspringe {i+1}/{len(all_experts)}: {expert_type}: {name} - Hat bereits Kontaktdaten.")
            skip_count += 1
            continue
        
        print(f"\nBearbeite {i+1}/{len(all_experts)}: {expert_type}: {name} (ID: {expert_id})...")
        
        # Kontaktdaten suchen
        contacts = search_contact_info(expert_details)
        
        if contacts:
            print(f"  Gefundene Kontaktdaten: {len(contacts)}")
            for contact in contacts:
                print(f"  - {contact['type']}: {contact['value']}")
                
            # Kontaktdaten aktualisieren (automatisch ohne Nachfrage)
            if update_expert_contacts(expert_id, contacts):
                print(f"  Kontaktdaten erfolgreich aktualisiert.")
                success_count += 1
            else:
                print(f"  Fehler beim Aktualisieren der Kontaktdaten.")
        else:
            print(f"  Keine Kontaktdaten gefunden.")
            
        # Eine Pause zwischen den Anfragen, um API-Limits zu respektieren
        time.sleep(random.uniform(2.0, 4.0))
    
    print(f"\nFertig! Kontaktdaten für {success_count} Experten/Organisationen aktualisiert.")
    print(f"{skip_count} Einträge wurden übersprungen, da sie bereits Kontaktdaten hatten.")

if __name__ == "__main__":
    main() 