from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import requests  # ML servisine istek atmak için

from models import db, Client, Project, Worklog, Developer

app = Flask(__name__)
CORS(app)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB and Migrate
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return jsonify({'message': '✅ Backend is running!'})

# ---- CLIENTS ----
@app.route('/clients')
def get_clients():
    clients = Client.query.all()
    return jsonify([
        {'id': c.id, 'name': c.name, 'industry': c.industry}
        for c in clients
    ])

@app.route('/clients/<int:client_id>/projects')
def get_projects_for_client(client_id):
    projects = Project.query.filter_by(client_id=client_id).all()
    return jsonify([
        {'id': p.id, 'name': p.name}
        for p in projects
    ])

# ---- PROJECTS ----
@app.route('/projects')
def get_projects():
    projects = Project.query.all()
    return jsonify([
        {'id': p.id, 'name': p.name, 'client_id': p.client_id}
        for p in projects
    ])

# ---- DEVELOPERS ----
@app.route('/developers')
def get_developers():
    developers = Developer.query.all()
    return jsonify([
        {'id': d.id, 'name': d.name}
        for d in developers
    ])

@app.route('/developers/<int:developer_id>/projects')
def get_projects_for_developer(developer_id):
    worklogs = Worklog.query.filter_by(developer_id=developer_id).all()
    projects = list({w.project for w in worklogs})  # Set to avoid duplicates
    return jsonify([
        {'id': p.id, 'name': p.name, 'client_id': p.client_id}
        for p in projects
    ])

# ---- WORKLOG ----
@app.route('/worklog', methods=['POST'])
def add_worklog():
    data = request.get_json()
    developer_id = data.get('developer_id')
    project_id = data.get('project_id')
    hours = data.get('hours')

    if not all([developer_id, project_id, hours]):
        return jsonify({'error': 'Missing data'}), 400

    worklog = Worklog(developer_id=developer_id, project_id=project_id, hours=hours)
    db.session.add(worklog)
    db.session.commit()

    return jsonify({'message': '✅ Worklog added successfully!'})

# ---- ML OVERLOAD CHECK ----
@app.route('/developers/<int:developer_id>/risk')
def check_developer_risk(developer_id):
    # Worklog'lardan kaç saat çalıştığını ve kaç projede çalıştığını bul
    worklogs = Worklog.query.filter_by(developer_id=developer_id).all()
    total_hours = sum([w.hours for w in worklogs])
    project_ids = list({w.project_id for w in worklogs})
    project_count = len(project_ids)

    # Şu an kritik görev sayısını sabit alalım (opsiyonel: veritabanına sonra eklenebilir)
    critical_tasks = 2

    try:
        # ML servisinin URL'si (Docker'da servisin adı ile çalışır)
        ml_url = 'http://ml_service:8500/predict'
        params = {
            'projects': project_count,
            'hours': total_hours,
            'critical': critical_tasks
        }
        response = requests.get(ml_url, params=params, timeout=3)
        prediction = response.json()
    except Exception as e:
        return jsonify({'error': 'ML servisine erişilemedi', 'details': str(e)}), 500

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
