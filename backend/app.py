import os
import logging
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import requests
from dotenv import load_dotenv

from models import db, Client, Project, Worklog, Developer

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

ML_SERVICE_URL = os.getenv('ML_SERVICE_URL', 'http://ml_service:8500/predict')
ML_REQUEST_TIMEOUT = 3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/')
def home():
    return jsonify({'message': 'Backend is running!'})

@app.route('/clients')
def get_clients():
    clients = Client.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'industry': c.industry} for c in clients])

@app.route('/clients/<int:client_id>')
def get_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    return jsonify({'id': client.id, 'name': client.name, 'industry': client.industry})

@app.route('/clients/<int:client_id>/projects')
def get_projects_for_client(client_id):
    projects = Project.query.filter_by(client_id=client_id).all()
    return jsonify([{'id': p.id, 'name': p.name} for p in projects])

@app.route('/projects')
def get_projects():
    projects = Project.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'client_id': p.client_id} for p in projects])

@app.route('/developers')
def get_developers():
    developers = Developer.query.all()
    return jsonify([{'id': d.id, 'name': d.name} for d in developers])

@app.route('/developers/<int:developer_id>/projects')
def get_projects_for_developer(developer_id):
    worklogs = Worklog.query.filter_by(developer_id=developer_id).all()
    projects = list({w.project for w in worklogs})
    return jsonify([{'id': p.id, 'name': p.name, 'client_id': p.client_id} for p in projects])

@app.route('/worklog', methods=['POST'])
def add_worklog():
    data = request.get_json()
    developer_id = data.get('developer_id')
    project_id = data.get('project_id')
    hours = data.get('hours')

    if not all([developer_id, project_id, hours]):
        return jsonify({'error': 'Missing data'}), 400

    if not isinstance(hours, (int, float)):
        try:
            hours = float(hours)
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid hours type'}), 400

    worklog = Worklog(developer_id=developer_id, project_id=project_id, hours=hours)
    db.session.add(worklog)
    db.session.commit()

    return jsonify({'message': 'Worklog added successfully!'})

@app.route('/developers/<int:developer_id>/risk')
def check_developer_risk(developer_id):
    worklogs = Worklog.query.filter_by(developer_id=developer_id).all()
    total_hours = sum([w.hours for w in worklogs])
    project_ids = list({w.project_id for w in worklogs})
    project_count = len(project_ids)
    critical_tasks = 2

    params = {
        'projects': project_count,
        'hours': total_hours,
        'critical': critical_tasks
    }

    try:
        response = requests.get(ML_SERVICE_URL, params=params, timeout=ML_REQUEST_TIMEOUT)
        response.raise_for_status()
        prediction = response.json()
    except Exception as e:
        logger.error(f"Error contacting ML service: {e}")
        return jsonify({'message': 'Service temporarily unavailable. Please try again later.'}), 503

    return jsonify({
        'developer_id': developer_id,
        'projects': project_count,
        'hours': total_hours,
        'critical_tasks': critical_tasks,
        'overloaded': prediction.get('overloaded'),
        'risk_score': prediction.get('risk_score')
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
