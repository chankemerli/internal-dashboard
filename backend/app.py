from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
