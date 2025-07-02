from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100))
    projects = db.relationship('Project', backref='client', lazy=True)

    def __repr__(self):
        return f"<Client {self.id} - {self.name}>"

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    worklogs = db.relationship('Worklog', backref='project', lazy=True)

    def __repr__(self):
        return f"<Project {self.id} - {self.name}>"

class Developer(db.Model):
    __tablename__ = 'developers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    worklogs = db.relationship('Worklog', backref='developer', lazy=True)

    def __repr__(self):
        return f"<Developer {self.id} - {self.name}>"

class Worklog(db.Model):
    __tablename__ = 'worklogs'
    id = db.Column(db.Integer, primary_key=True)
    developer_id = db.Column(
        db.Integer,
        db.ForeignKey('developers.id', name='fk_worklog_developer'),
        nullable=False
    )
    project_id = db.Column(
        db.Integer,
        db.ForeignKey('projects.id', name='fk_worklog_project'),
        nullable=False
    )
    hours = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Worklog {self.id} - Dev: {self.developer_id}, Proj: {self.project_id}, Hours: {self.hours}>"
