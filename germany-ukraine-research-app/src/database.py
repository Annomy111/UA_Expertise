"""
Datenbank-Modelle und -Utilities für die Germany-Ukraine Contact Research App
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()


class Contact(Base):
    """Kontakt-Modell für Organisationen und Personen"""
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    organization = Column(String(255))
    type = Column(String(100))  # government, ngo, think_tank, university, media, local_initiative
    category = Column(String(100))

    # Kontaktinformationen
    email = Column(String(255))
    phone = Column(String(100))
    website = Column(String(500))
    address = Column(Text)
    city = Column(String(100))
    postal_code = Column(String(20))

    # Social Media
    twitter = Column(String(255))
    linkedin = Column(String(255))
    facebook = Column(String(255))

    # Beschreibung
    description = Column(Text)
    focus_areas = Column(Text)  # JSON-String mit Schwerpunkten

    # Metadaten
    source_url = Column(String(500))
    last_updated = Column(DateTime, default=datetime.utcnow)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Konvertiere Kontakt zu Dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'organization': self.organization,
            'type': self.type,
            'category': self.category,
            'email': self.email,
            'phone': self.phone,
            'website': self.website,
            'address': self.address,
            'city': self.city,
            'postal_code': self.postal_code,
            'twitter': self.twitter,
            'linkedin': self.linkedin,
            'facebook': self.facebook,
            'description': self.description,
            'focus_areas': self.focus_areas,
            'source_url': self.source_url,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'verified': self.verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SearchLog(Base):
    """Log für durchgeführte Suchen"""
    __tablename__ = 'search_logs'

    id = Column(Integer, primary_key=True)
    search_term = Column(String(500))
    source = Column(String(255))
    results_found = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean, default=True)
    error_message = Column(Text)


class DatabaseManager:
    """Manager-Klasse für Datenbankoperationen"""

    def __init__(self, db_path='data/contacts.db'):
        self.db_path = db_path
        self.engine = None
        self.Session = None

    def initialize(self):
        """Initialisiere Datenbank"""
        # Stelle sicher, dass das data-Verzeichnis existiert
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        # Erstelle Engine und Session
        self.engine = create_engine(f'sqlite:///{self.db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

        print(f"✓ Datenbank initialisiert: {self.db_path}")

    def get_session(self):
        """Hole neue Session"""
        if self.Session is None:
            self.initialize()
        return self.Session()

    def add_contact(self, contact_data):
        """Füge neuen Kontakt hinzu oder aktualisiere existierenden"""
        session = self.get_session()
        try:
            # Prüfe ob Kontakt bereits existiert (basierend auf Website oder Name)
            existing = None
            if contact_data.get('website'):
                existing = session.query(Contact).filter_by(
                    website=contact_data['website']
                ).first()

            if not existing and contact_data.get('name'):
                existing = session.query(Contact).filter_by(
                    name=contact_data['name'],
                    organization=contact_data.get('organization')
                ).first()

            if existing:
                # Update existierenden Kontakt
                for key, value in contact_data.items():
                    if value and hasattr(existing, key):
                        setattr(existing, key, value)
                existing.last_updated = datetime.utcnow()
                print(f"  ↻ Aktualisiert: {existing.name}")
            else:
                # Erstelle neuen Kontakt
                contact = Contact(**contact_data)
                session.add(contact)
                print(f"  + Neu: {contact_data.get('name', 'Unbekannt')}")

            session.commit()
            return True
        except Exception as e:
            print(f"  ✗ Fehler beim Speichern: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    def search_contacts(self, query=None, contact_type=None, city=None):
        """Suche Kontakte"""
        session = self.get_session()
        try:
            contacts = session.query(Contact)

            if query:
                search = f"%{query}%"
                contacts = contacts.filter(
                    (Contact.name.like(search)) |
                    (Contact.organization.like(search)) |
                    (Contact.description.like(search)) |
                    (Contact.focus_areas.like(search))
                )

            if contact_type:
                contacts = contacts.filter_by(type=contact_type)

            if city:
                contacts = contacts.filter_by(city=city)

            return [c.to_dict() for c in contacts.all()]
        finally:
            session.close()

    def get_statistics(self):
        """Hole Statistiken"""
        session = self.get_session()
        try:
            total = session.query(Contact).count()
            by_type = {}

            for contact_type in ['government', 'ngo', 'think_tank', 'university', 'media', 'local_initiative']:
                count = session.query(Contact).filter_by(type=contact_type).count()
                if count > 0:
                    by_type[contact_type] = count

            return {
                'total_contacts': total,
                'by_type': by_type,
                'last_updated': datetime.utcnow().isoformat()
            }
        finally:
            session.close()

    def log_search(self, search_term, source, results_found, success=True, error=None):
        """Logge Suchdurchlauf"""
        session = self.get_session()
        try:
            log = SearchLog(
                search_term=search_term,
                source=source,
                results_found=results_found,
                success=success,
                error_message=error
            )
            session.add(log)
            session.commit()
        finally:
            session.close()


# Globale Instanz
db_manager = DatabaseManager()
