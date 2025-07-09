week-6:
Backend:

Added new /health endpoint for health check.

Implemented routes to handle clients, projects, developers, and worklogs.

Integrated a route to communicate with the ML service to assess developer risk.

Added error handling and logging for ML service communication.

Machine Learning Service:

Set up the ML prediction endpoint (/predict).

Ensured proper health checks and environment configuration.

Frontend:

Connected frontend to backend API to display client and project data.

Ensured seamless data fetching and UI updates.

Docker:

Improved docker-compose.yml to include healthchecks for all services.

Set service dependencies for proper startup order.

Mapped ports and mounted volumes for local development convenience.

Testing
Verified all services start successfully with docker-compose up.

Accessed http://localhost:5000/health and confirmed backend health status.

Tested frontend UI displays client lists correctly.

Validated ML service predictions through API calls.
