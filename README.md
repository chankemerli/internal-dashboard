
# Internal Dashboard

## Project Overview
Internal Dashboard is a fully integrated web application designed to manage clients, projects, developers, and worklogs within a company. The backend is built with Flask, and the frontend is developed with React. All services can be run via Docker Compose.

---

## Running Instructions

Make sure Docker and Docker Compose are installed.

```bash
docker compose up --build
```

This command will start backend, frontend, and ML service containers.

---

## Loading Sample Data

To load sample data, run the `load_sample_data.py` script located in the backend folder:

```bash
python load_sample_data.py
```

This will insert sample clients, projects, developers, and worklogs into the database.

---

## API Endpoints

The backend service provides the following API endpoints:

- `GET /clients` — List all clients
- `GET /clients/<id>` — Get details of a specific client
- `GET /clients/<id>/projects` — Get projects for a client
- `GET /developers` — List all developers
- `POST /worklog` — Add a worklog entry for a developer
- `GET /developers/<id>/risk` — Analyze developer risk status

---

## Frontend

- React-based frontend displays the client list at `/`.
- Clicking on a client name shows client details and projects.
- Accessible at `localhost:3000`.


## Issues and Fixes

- Resolved Docker container connectivity issues.
- Fixed Flask app context errors.
- Added error handling for data loading and API requests.


