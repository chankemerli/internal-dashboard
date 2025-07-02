from app import app, db
from models import Client, Project, Developer, Worklog

with app.app_context():
    db.create_all()

    Worklog.query.delete()
    Project.query.delete()
    Client.query.delete()
    Developer.query.delete()
    db.session.commit()

    clients = [
        Client(name='Client A', industry='Finance'),
        Client(name='Client B', industry='Healthcare'),
    ]

    for client in clients:
        db.session.add(client)
    db.session.commit()

    projects = [
        Project(name='Project Alpha', client_id=clients[0].id),
        Project(name='Project Beta', client_id=clients[0].id),
        Project(name='Project Gamma', client_id=clients[1].id),
    ]

    for project in projects:
        db.session.add(project)
    db.session.commit()

    developers = [
        Developer(name='Can'),
        Developer(name='Michał'),
    ]

    for dev in developers:
        db.session.add(dev)
    db.session.commit()

    worklogs = [
        Worklog(developer_id=developers[0].id, project_id=projects[0].id, hours=5),
        Worklog(developer_id=developers[1].id, project_id=projects[1].id, hours=3),
    ]

    for w in worklogs:
        db.session.add(w)
    db.session.commit()

    print("Sample data loaded successfully!")
