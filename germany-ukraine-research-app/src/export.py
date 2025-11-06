#!/usr/bin/env python3
"""
Export-Funktionen für verschiedene Formate
"""

import pandas as pd
import json
import os
from datetime import datetime
from database import db_manager


def export_to_csv(contacts, filename='export.csv'):
    """Exportiere als CSV"""
    df = pd.DataFrame(contacts)
    output_dir = 'exports'
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    print(f"✓ Exportiert nach: {filepath}")
    return filepath


def export_to_json(contacts, filename='export.json'):
    """Exportiere als JSON"""
    output_dir = 'exports'
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    export_data = {
        'export_date': datetime.now().isoformat(),
        'total_contacts': len(contacts),
        'contacts': contacts
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

    print(f"✓ Exportiert nach: {filepath}")
    return filepath


def export_to_excel(contacts, filename='export.xlsx'):
    """Exportiere als Excel"""
    df = pd.DataFrame(contacts)
    output_dir = 'exports'
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    # Erstelle Excel-Writer
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        # Haupt-Sheet mit allen Daten
        df.to_excel(writer, sheet_name='Alle Kontakte', index=False)

        # Separate Sheets nach Typ
        for contact_type in df['type'].unique():
            if pd.notna(contact_type):
                type_df = df[df['type'] == contact_type]
                sheet_name = contact_type[:31]  # Excel limit
                type_df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"✓ Exportiert nach: {filepath}")
    return filepath


def export_to_format(contacts, format_type):
    """Exportiere in gewünschtem Format"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    if format_type.lower() == 'csv':
        return export_to_csv(contacts, f'ukraine_contacts_{timestamp}.csv')
    elif format_type.lower() == 'json':
        return export_to_json(contacts, f'ukraine_contacts_{timestamp}.json')
    elif format_type.lower() in ['xlsx', 'excel']:
        return export_to_excel(contacts, f'ukraine_contacts_{timestamp}.xlsx')
    else:
        raise ValueError(f"Unbekanntes Format: {format_type}")


def main():
    """CLI für Export"""
    import argparse

    parser = argparse.ArgumentParser(description='Exportiere Ukraine-Kontakte')
    parser.add_argument('--format', choices=['csv', 'json', 'excel'], default='csv',
                        help='Export-Format')
    parser.add_argument('--type', help='Filtere nach Kontakt-Typ')
    parser.add_argument('--city', help='Filtere nach Stadt')

    args = parser.parse_args()

    print("📤 Exportiere Kontakte...")

    db_manager.initialize()
    contacts = db_manager.search_contacts(
        contact_type=args.type,
        city=args.city
    )

    print(f"Gefundene Kontakte: {len(contacts)}")

    if contacts:
        export_to_format(contacts, args.format)
    else:
        print("Keine Kontakte zum Exportieren gefunden")


if __name__ == '__main__':
    main()
