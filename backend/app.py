from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restx import Api, Resource, fields
from dotenv import load_dotenv
import os

from models import db, Client, Project, Worklog, Developer

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app, version='1.0', title='Internship Project API',
          description='REST API for managing clients, projects, developers, and worklogs.')

ns_clients = api.namespace('clients', description='Client operations')
ns_projects = api.namespace('projects', description='Project operations')
ns_developers = api.namespace('developers', description='Developer operations')
ns_worklog = api.namespace('worklog', description='Worklog operations')

worklog_model = api.model('Worklog', {
    'developer_id': fields.Integer(required=True, description='Developer ID'),
    'project_id': fields.Integer(required=True, description='Project ID'),
    'hours': fields.Float(required=True, description='Worked hours'),
})

@api.route('/')
class Home(Resource):
    def get(self):
        return {'message': '✅ Backend is running!'}

@ns_clients.route('/')
class ClientList(Resource):
    def get(self):
        clients = Client.query.all()
        return [{'id': c.id, 'name': c.name, 'industry': c.industry} for c in clients]

@ns_clients.route('/<int:client_id>/projects')
class ClientProjects(Resource):
    def get(self, client_id):
        projects = Project.query.filter_by(client_id=client_id).all()
        return [{'id': p.id, 'name': p.name} for p in projects]

@ns_projects.route('/')
class ProjectList(Resource):
    def get(self):
        projects = Project.query.all()
        return [{'id': p.id, 'name': p.name, 'client_id': p.client_id} for p in projects]

@ns_developers.route('/')
class DeveloperList(Resource):
    def get(self):
        developers = Developer.query.all()
        return [{'id': d.id, 'name': d.name} for d in developers]

@ns_developers.route('/<int:developer_id>/projects')
class DeveloperProjects(Resource):
    def get(self, developer_id):
        worklogs = Worklog.query.filter_by(developer_id=developer_id).all()
        projects = list({w.project for w in worklogs})
        return [{'id': p.id, 'name': p.name, 'client_id': p.client_id} for p in projects]

@ns_worklog.route('/')
class WorklogCreate(Resource):
    @ns_worklog.expect(worklog_model)
    def post(self):
        data = request.get_json()
        developer_id = data.get('developer_id')
        project_id = data.get('project_id')
        hours = data.get('hours')

        if not all([developer_id, project_id, hours]):
            return {'error': 'Missing data'}, 400

        worklog = Worklog(developer_id=developer_id, project_id=project_id, hours=hours)
        db.session.add(worklog)
        db.session.commit()

        return {'message': '✅ Worklog added successfully!'}

if __name__ == '__main__':
    host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_RUN_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'

    app.run(debug=debug, host=host, port=port)
