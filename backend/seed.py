from app import app
from models import db, Client, Project

with app.app_context():
    db.drop_all()
    db.create_all()

    client1 = Client(name="Client A", industry="Finance")
    client2 = Client(name="Client B", industry="Healthcare")

    project1 = Project(name="Project Alpha", client=client1)
    project2 = Project(name="Project Beta", client=client1)
    project3 = Project(name="Project Gamma", client=client2)

    db.session.add_all([client1, client2, project1, project2, project3])
    db.session.commit()

    print("Seeder executed and sample data added.")
