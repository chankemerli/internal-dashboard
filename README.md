# Internal Dashboard - Week 1

--Week 1:

- Setup Python backend in Docker
- Display a simple message from the backend: **"Hello backend!"**
- Push the project to GitHub

Run:

```bash
docker compose up --build

# Internal Dashboard - Week 2
--Week 2:
Accomplishments this week:
Completion of project structure and creation of basic files.

Setup of Flask/FastAPI application on the backend.

Creation of database models (Client model).

Preparation of Docker Compose configuration and running containers.

Adding and testing Client data for basic CRUD operations.

Establishing basic connection between frontend and backend.

Data insertion into the database and validation.

--Obstacles encountered:
Initially experienced connection issues due to Docker containers not running correctly.

Minor issues with and terminal usage, which were resolved.

Import and session errors during Flask app context usage were fixed.

Week 3:
Added Developer and Worklog models in models.py.

Created REST API endpoints in app.py:

GET /developers – Returns all developers.

POST /worklog – Adds a worklog entry for a developer.

Updated and ran seed.py to insert:

Sample clients, projects, and developers into the database.

Verified the following API routes:

http://localhost:5000/clients

http://localhost:5000/projects

http://localhost:5000/developers

Backend service restarted successfully with Docker Compose.

All endpoints tested and responded correctly.
