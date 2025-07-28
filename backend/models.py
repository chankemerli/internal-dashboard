from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy 
db = SQLAlchemy()

# Client 
class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    projects = db.relationship('Project', backref='client', lazy=True)
    industry = db.Column(db.String(100))

# Project 
class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

class Worklog(db.Model):
    __tablename__ = 'worklogs'
    id = db.Column(db.Integer, primary_key=True)
    developer_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    hours = db.Column(db.Float, nullable=False)
