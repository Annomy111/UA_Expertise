"""
Datenbank-Modelle und -Utilities für die Germany-Ukraine Contact Research App
Firebase/Firestore Backend
"""

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
import json
from typing import Optional, List, Dict
import hashlib


class FirebaseManager:
    """Manager-Klasse für Firebase/Firestore Operationen"""

    def __init__(self):
        self.db = None
        self.app = None
        self.initialized = False

    def initialize(self):
        """Initialisiere Firebase-Verbindung"""
        if self.initialized:
            print("ℹ Firebase bereits initialisiert")
            return

        try:
            # Lade Firebase-Konfiguration
            firebase_config_path = os.getenv('FIREBASE_CONFIG_PATH', 'config/firebase-config.json')
            firebase_url = os.getenv('FIREBASE_URL')

            if not os.path.exists(firebase_config_path):
                raise FileNotFoundError(
                    f"Firebase-Konfiguration nicht gefunden: {firebase_config_path}\n"
                    "Bitte erstelle die Datei oder setze FIREBASE_CONFIG_PATH in .env"
                )

            # Initialisiere Firebase Admin SDK
            cred = credentials.Certificate(firebase_config_path)

            # Für self-hosted Firebase, setze databaseURL
            firebase_options = {}
            if firebase_url:
                firebase_options['databaseURL'] = firebase_url

            self.app = firebase_admin.initialize_app(cred, firebase_options)
            self.db = firestore.client()
            self.initialized = True

            print(f"✓ Firebase/Firestore initialisiert")
            if firebase_url:
                print(f"  Verbunden mit: {firebase_url}")

        except Exception as e:
            print(f"✗ Fehler beim Initialisieren von Firebase: {e}")
            raise

    def get_db(self):
        """Hole Firestore-Client"""
        if not self.initialized:
            self.initialize()
        return self.db

    def _generate_contact_id(self, contact_data):
        """Generiere eindeutige ID für Kontakt basierend auf Website oder Name"""
        if contact_data.get('website'):
            return hashlib.md5(contact_data['website'].encode()).hexdigest()
        elif contact_data.get('name'):
            identifier = f"{contact_data['name']}_{contact_data.get('organization', '')}"
            return hashlib.md5(identifier.encode()).hexdigest()
        else:
            # Fallback: Timestamp-basierte ID
            return None

    def _prepare_contact_data(self, contact_data):
        """Bereite Kontaktdaten für Firestore vor"""
        prepared = {}

        # Alle Felder mit Standardwerten
        fields = [
            'name', 'organization', 'type', 'category',
            'email', 'phone', 'website', 'address', 'city', 'postal_code',
            'twitter', 'linkedin', 'facebook',
            'description', 'focus_areas', 'source_url'
        ]

        for field in fields:
            prepared[field] = contact_data.get(field, '')

        # Boolean-Felder
        prepared['verified'] = contact_data.get('verified', False)

        # Timestamps
        if 'last_updated' not in contact_data:
            prepared['last_updated'] = firestore.SERVER_TIMESTAMP
        else:
            prepared['last_updated'] = contact_data['last_updated']

        if 'created_at' not in contact_data:
            prepared['created_at'] = firestore.SERVER_TIMESTAMP
        else:
            prepared['created_at'] = contact_data['created_at']

        return prepared

    def add_contact(self, contact_data):
        """Füge neuen Kontakt hinzu oder aktualisiere existierenden"""
        try:
            db = self.get_db()
            contacts_ref = db.collection('contacts')

            # Generiere oder hole ID
            doc_id = self._generate_contact_id(contact_data)

            if doc_id:
                # Prüfe ob Kontakt existiert
                doc_ref = contacts_ref.document(doc_id)
                doc = doc_ref.get()

                prepared_data = self._prepare_contact_data(contact_data)

                if doc.exists:
                    # Update existierenden Kontakt
                    prepared_data['last_updated'] = firestore.SERVER_TIMESTAMP
                    doc_ref.update(prepared_data)
                    print(f"  ↻ Aktualisiert: {contact_data.get('name', 'Unbekannt')}")
                else:
                    # Erstelle neuen Kontakt
                    doc_ref.set(prepared_data)
                    print(f"  + Neu: {contact_data.get('name', 'Unbekannt')}")
            else:
                # Kein eindeutiger Identifier - erstelle mit Auto-ID
                prepared_data = self._prepare_contact_data(contact_data)
                contacts_ref.add(prepared_data)
                print(f"  + Neu: {contact_data.get('name', 'Unbekannt')}")

            return True

        except Exception as e:
            print(f"  ✗ Fehler beim Speichern: {e}")
            return False

    def search_contacts(self, query: Optional[str] = None,
                       contact_type: Optional[str] = None,
                       city: Optional[str] = None) -> List[Dict]:
        """Suche Kontakte"""
        try:
            db = self.get_db()
            contacts_ref = db.collection('contacts')

            # Basis-Query
            contacts_query = contacts_ref

            # Firestore unterstützt keine OR-Queries direkt für Textsuche
            # Daher müssen wir erst filtern und dann in Python weitersuchen

            # Filter nach Typ
            if contact_type:
                contacts_query = contacts_query.where('type', '==', contact_type)

            # Filter nach Stadt
            if city:
                contacts_query = contacts_query.where('city', '==', city)

            # Hole alle Dokumente
            docs = contacts_query.stream()

            results = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id

                # Konvertiere Timestamps zu ISO-Format
                if 'last_updated' in data and data['last_updated']:
                    if hasattr(data['last_updated'], 'isoformat'):
                        data['last_updated'] = data['last_updated'].isoformat()
                    else:
                        data['last_updated'] = str(data['last_updated'])

                if 'created_at' in data and data['created_at']:
                    if hasattr(data['created_at'], 'isoformat'):
                        data['created_at'] = data['created_at'].isoformat()
                    else:
                        data['created_at'] = str(data['created_at'])

                # Textsuche in Python (Firestore hat keine LIKE-Suche)
                if query:
                    search_fields = [
                        data.get('name', ''),
                        data.get('organization', ''),
                        data.get('description', ''),
                        data.get('focus_areas', '')
                    ]
                    search_text = ' '.join(search_fields).lower()

                    if query.lower() in search_text:
                        results.append(data)
                else:
                    results.append(data)

            return results

        except Exception as e:
            print(f"✗ Fehler bei der Suche: {e}")
            return []

    def get_contact_by_id(self, contact_id: str) -> Optional[Dict]:
        """Hole einzelnen Kontakt per ID"""
        try:
            db = self.get_db()
            doc_ref = db.collection('contacts').document(contact_id)
            doc = doc_ref.get()

            if doc.exists:
                data = doc.to_dict()
                data['id'] = doc.id

                # Konvertiere Timestamps
                if 'last_updated' in data and data['last_updated']:
                    if hasattr(data['last_updated'], 'isoformat'):
                        data['last_updated'] = data['last_updated'].isoformat()
                    else:
                        data['last_updated'] = str(data['last_updated'])

                if 'created_at' in data and data['created_at']:
                    if hasattr(data['created_at'], 'isoformat'):
                        data['created_at'] = data['created_at'].isoformat()
                    else:
                        data['created_at'] = str(data['created_at'])

                return data
            return None

        except Exception as e:
            print(f"✗ Fehler beim Abrufen des Kontakts: {e}")
            return None

    def get_statistics(self) -> Dict:
        """Hole Statistiken"""
        try:
            db = self.get_db()
            contacts_ref = db.collection('contacts')

            # Hole alle Kontakte
            all_contacts = list(contacts_ref.stream())
            total = len(all_contacts)

            # Zähle nach Typ
            by_type = {}
            for doc in all_contacts:
                data = doc.to_dict()
                contact_type = data.get('type', 'unknown')
                by_type[contact_type] = by_type.get(contact_type, 0) + 1

            # Entferne Typen mit 0 Einträgen
            by_type = {k: v for k, v in by_type.items() if v > 0}

            return {
                'total_contacts': total,
                'by_type': by_type,
                'last_updated': datetime.utcnow().isoformat()
            }

        except Exception as e:
            print(f"✗ Fehler beim Abrufen der Statistiken: {e}")
            return {
                'total_contacts': 0,
                'by_type': {},
                'last_updated': datetime.utcnow().isoformat()
            }

    def log_search(self, search_term: str, source: str, results_found: int,
                   success: bool = True, error: Optional[str] = None):
        """Logge Suchdurchlauf"""
        try:
            db = self.get_db()
            logs_ref = db.collection('search_logs')

            log_data = {
                'search_term': search_term,
                'source': source,
                'results_found': results_found,
                'timestamp': firestore.SERVER_TIMESTAMP,
                'success': success,
                'error_message': error or ''
            }

            logs_ref.add(log_data)

        except Exception as e:
            print(f"⚠ Fehler beim Logging: {e}")

    def delete_contact(self, contact_id: str) -> bool:
        """Lösche Kontakt"""
        try:
            db = self.get_db()
            db.collection('contacts').document(contact_id).delete()
            print(f"✓ Kontakt {contact_id} gelöscht")
            return True
        except Exception as e:
            print(f"✗ Fehler beim Löschen: {e}")
            return False

    def get_all_cities(self) -> List[str]:
        """Hole alle Städte aus der Datenbank"""
        try:
            db = self.get_db()
            contacts = db.collection('contacts').stream()

            cities = set()
            for doc in contacts:
                data = doc.to_dict()
                if data.get('city'):
                    cities.add(data['city'])

            return sorted(list(cities))
        except Exception as e:
            print(f"✗ Fehler beim Abrufen der Städte: {e}")
            return []


# Globale Instanz
db_manager = FirebaseManager()
