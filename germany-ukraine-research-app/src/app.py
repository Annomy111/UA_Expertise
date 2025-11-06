#!/usr/bin/env python3
"""
Flask Web-App für Germany-Ukraine Contact Research
"""

from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
from database import db_manager
import os
from datetime import datetime

# Lade Umgebungsvariablen
load_dotenv()

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

# Initialisiere Datenbank
db_manager.initialize()


@app.route('/')
def index():
    """Hauptseite"""
    stats = db_manager.get_statistics()
    return render_template('index.html', stats=stats)


@app.route('/api/search')
def search():
    """API-Endpunkt für Suche"""
    query = request.args.get('q', '')
    contact_type = request.args.get('type', '')
    city = request.args.get('city', '')

    results = db_manager.search_contacts(
        query=query if query else None,
        contact_type=contact_type if contact_type else None,
        city=city if city else None
    )

    return jsonify({
        'results': results,
        'total': len(results)
    })


@app.route('/api/contacts')
def get_contacts():
    """Hole alle Kontakte"""
    results = db_manager.search_contacts()
    return jsonify({
        'results': results,
        'total': len(results)
    })


@app.route('/api/statistics')
def statistics():
    """Statistiken"""
    stats = db_manager.get_statistics()
    return jsonify(stats)


@app.route('/api/export/<format>')
def export_data(format):
    """Exportiere Daten"""
    from export import export_to_format

    results = db_manager.search_contacts()

    try:
        file_path = export_to_format(results, format)
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f'ukraine_contacts_{datetime.now().strftime("%Y%m%d")}.{format}'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/contact/<contact_id>')
def contact_detail(contact_id):
    """Detail-Seite für einen Kontakt"""
    contact = db_manager.get_contact_by_id(contact_id)

    if contact:
        return render_template('contact_detail.html', contact=contact)
    else:
        return "Kontakt nicht gefunden", 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
