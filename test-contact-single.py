#!/usr/bin/env python3

import requests
import json
from typing import Dict, List, Any, Optional

# Serper API-Schlüssel
SERPER_API_KEY = "24f44e45b73e32ac7e31b447a0568caa7fa4b0db"

# Test für einen einzelnen Experten
EXPERT_ID = "1e585dde-1732-4fdb-80f3-822dce0a956a"  # Promote Ukraine (aus den obigen Ergebnissen)
API_URL = "http://localhost:8000"
EXPERTS_URL = f"{API_URL}/experts"

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
    
    if not name:
        return []
    
    # Suchanfrage erstellen
    query = f"{name} contact email"
    
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = {
        "q": query,
        "gl": "de",
        "hl": "de",
        "num": 5
    }
    
    try:
        print(f"Suche nach Kontaktinformationen für: {query}")
        response = requests.post('https://google.serper.dev/search', headers=headers, json=payload)
        response.raise_for_status()
        
        search_results = response.json()
        print("Rohe Suchergebnisse:")
        print(json.dumps(search_results, indent=2))
        
        # Kontaktdaten extrahieren
        contacts = []
        
        # Aus organischen Suchergebnissen
        if 'organic' in search_results:
            for result in search_results['organic'][:3]:
                # Webseite als Kontakt hinzufügen
                if 'link' in result:
                    website = result.get('link', '')
                    if website and not any(c['type'] == 'website' and c['value'] == website for c in contacts):
                        contacts.append({
                            "type": "website",
                            "value": website,
                            "is_primary": len(contacts) == 0
                        })
                
                # Suche nach E-Mail-Adressen im Snippet
                snippet = result.get('snippet', '')
                if '@' in snippet and '.' in snippet:
                    email_parts = [part for part in snippet.split() if '@' in part]
                    for email_part in email_parts:
                        # Bereinigung der E-Mail
                        email = ''.join(c for c in email_part if c.isalnum() or c in ['@', '.', '-', '_'])
                        if '@' in email and '.' in email and len(email) > 5:
                            contacts.append({
                                "type": "email",
                                "value": email,
                                "is_primary": len(contacts) == 0
                            })
        
        return contacts
    except Exception as e:
        print(f"Fehler bei der Suche nach Kontaktinformationen für {name}: {e}")
        return []

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
        "name": expert_details.get("name"),
        "city_id": expert_details.get("city_id"),
        "contacts": contacts
    }
    
    try:
        print(f"Aktualisiere Kontaktdaten für {expert_id}:")
        print(json.dumps(update_data, indent=2))
        
        response = requests.put(f"{EXPERTS_URL}/{expert_id}", json=update_data)
        response.raise_for_status()
        print(f"Antwort: {response.status_code} {response.text}")
        return True
    except Exception as e:
        print(f"Fehler beim Aktualisieren der Kontaktdaten für {expert_id}: {e}")
        return False

def main():
    # Expert-Details holen
    expert = get_expert_details(EXPERT_ID)
    if not expert:
        print(f"Experte mit ID {EXPERT_ID} nicht gefunden.")
        return
        
    print(f"Teste Kontaktsuche für {expert['name']} (ID: {EXPERT_ID})...")
    
    # Kontaktdaten suchen
    contacts = search_contact_info(expert)
    
    if contacts:
        print(f"Gefundene Kontaktdaten: {len(contacts)}")
        for contact in contacts:
            print(f"- {contact['type']}: {contact['value']}")
            
        # Automatisch aktualisieren ohne Nachfrage
        if update_expert_contacts(EXPERT_ID, contacts):
            print("Kontaktdaten erfolgreich aktualisiert.")
        else:
            print("Fehler beim Aktualisieren der Kontaktdaten.")
    else:
        print("Keine Kontaktdaten gefunden.")

if __name__ == "__main__":
    main() 