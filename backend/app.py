from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


from models import db, Client, Project, Worklog

app = Flask(__name__)
CORS(app)  

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return jsonify({'message': 'Backend is running!'})

@app.route('/clients')
def get_clients():
    clients = Client.query.all()
    return jsonify([{'id': c.id, 'name': c.name} for c in clients])

@app.route('/clients/<int:client_id>/projects')
def get_projects_for_client(client_id):
    projects = Project.query.filter_by(client_id=client_id).all()
    return jsonify([{'id': p.id, 'name': p.name} for p in projects])

@app.route('/projects')
def get_projects():
    projects = Project.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'client_id': p.client_id} for p in projects])

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

    return jsonify({'message': 'Worklog added successfully!'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
