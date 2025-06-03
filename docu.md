# Project Structure

```
├── .docker/
│   └── docker-compose.yml   # Compose file for app, DB, ML service
├── backend/
│   ├── app.py             # Backend Flask application
│   ├── models.py          # Database models
│   ├── seed.py            # Seeder script to populate the database
│   └── requirements.txt   # Backend dependencies
├── frontend/
│   ├── src/
│   └── package.json
├── ml_service/
│   ├── model.py           # ML model code
│   └── requirements.txt
└── README.md
```

# Setup Instructions

1. Build and start the services:

   ```bash
   docker compose -f .docker/docker-compose.yml up --build
   ```

2. Access the backend at `http://localhost:5000`.

3. Access the frontend at `http://localhost:3000`.

4. Run the database seeder:
   
   ```bash
   docker compose -f .docker/docker-compose.yml exec backend python seed.py
   ```

# Milestones

1. Initial project setup with backend, frontend, and ML service.

2. Dockerized all services.

3. Implemented REST API endpoints.

4. Integrated frontend with backend.

5. Database seeder script added.

# Internal Dashboard for Client and Project Insights

## Project Overview

This project is a lightweight, internal web dashboard designed to provide quick insights into clients, projects, and developer activity within the company. It also integrates a basic Machine Learning module to predict developer overload based on current workload data.

## Features

- List of clients and their active projects
- Developer workload overview (project assignments and time tracking)
- Search and filter functionality
- ML-based prediction for developer overload
- Fully containerized using Docker Compose

## Technologies Used

- Backend: Python (FastAPI or Flask)
- Frontend: HTML/CSS/JavaScript or optionally React
- Database: PostgreSQL (preferred) or SQLite (for development)
- ML Module: Python (rule-based or Scikit-learn)
- Containerization: Docker & Docker Compose

## Project Structure

```
/project-root
│
├── backend/             # FastAPI or Flask app
│   └── app/             # API code
│
├── frontend/            # Frontend app (optional React or plain HTML/CSS/JS)
│
├── ml_service/          # ML microservice for overload prediction
│   └── model.py         # ML logic (simple rules or Scikit-learn model)
│
├── db/                  # PostgreSQL or SQLite volume/data (optional)
│
├── docker-compose.yml   # Compose file for app, DB, ML service
├── .env                 # Environment configuration
├── README.md            # Project documentation
└── requirements.txt     # Python dependencies
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/YOUR_USERNAME/internal-dashboard.git
   cd internal-dashboard
   ```

2. Create an `.env` file based on example:
   ```
   cp .env.example .env
   ```

3. Run the full environment:
   ```
   docker-compose up --build
   ```

4. Access:
   - API: http://localhost:8000
   - ML Service: http://localhost:8500
   - Frontend (if React): http://localhost:3000

## API Endpoints

### Backend (FastAPI)

- `GET /clients`  
  Returns list of clients.

- `GET /clients/{id}/projects`  
  Returns projects for a specific client.

- `GET /projects`  
  Returns all projects.

- `GET /developers`  
  Returns all developers.

- `GET /developers/{id}/projects`  
  Returns projects assigned to a developer.

- `POST /worklog`  
  Logs work time for a developer.

### ML Service

- `GET /predict?projects=3&hours=35&critical=2`  
  Returns overload prediction.

  **Example response:**
  ```json
  {
    "overloaded": true,
    "risk_score": 0.82
  }
  ```

## ML Integration Details

The ML module estimates developer overload risk based on:
- Number of assigned projects
- Hours logged in the past week
- Number of critical tasks

The module is written in Python and exposed as a microservice. You can modify the prediction logic in `ml_service/model.py`.

## Milestones

### Milestone 1: Project Initialization
- GitHub repo with README
- Folder structure and basic files
- Docker skeleton

### Milestone 2: Backend API (Clients & Projects)
- Client and project models
- API endpoints
- DB connection
- Docker container running

### Milestone 3: Developer Activity
- Developer model and endpoints
- Worklog logic
- Relations in database

### Milestone 4: Frontend
- Views for client/project/developer info
- API consumption
- Filtering/search

### Milestone 5: Finalization
- Docker Compose full integration
- Sample data loader
- README and docs finalized

### Milestone 6: ML API Integration
- New ML microservice
- Overload prediction logic
- Integrated into backend route

## Weekly Reports

Each week, provide:
- Summary of what’s done
- Plans for the next week
- Issues or blockers
- Optional screenshot or demo

## Contribution Rules

- Use GitHub Issues for task tracking
- Create a branch per feature
- Write clean, documented code
- Commit frequently with meaningful messages

## License

This project is provided for educational and internal use. Contact your mentor for reuse permission.