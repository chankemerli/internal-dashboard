from app import app
from models import db, Client, Project, Developer, Worklog

with app.app_context():
    db.drop_all()
    db.create_all()

    # Clients
    client1 = Client(name="Client A", industry="Finance")
    client2 = Client(name="Client B", industry="Healthcare")

    # Projects
    project1 = Project(name="Project Alpha", client=client1)
    project2 = Project(name="Project Beta", client=client1)
    project3 = Project(name="Project Gamma", client=client2)

    # Developers
    dev1 = Developer(name="Alice")
    dev2 = Developer(name="Bob")
    dev3 = Developer(name="Charlie")

    # Worklogs
    worklog1 = Worklog(developer=dev1, project=project1, hours=10.5)
    worklog2 = Worklog(developer=dev2, project=project1, hours=8.0)
    worklog3 = Worklog(developer=dev3, project=project2, hours=12.0)
    worklog4 = Worklog(developer=dev1, project=project3, hours=6.0)

    # Commit to DB
    db.session.add_all([
        client1, client2,
        project1, project2, project3,
        dev1, dev2, dev3,
        worklog1, worklog2, worklog3, worklog4
    ])
    db.session.commit()

    print("✅ Seeder executed and sample data added.")
