# Copilot Instructions for AI Coding Agents

## Project Overview
- **Full-stack Todo App**: React (frontend, `src/`) + Django (backend, `backend/` with `todo/` app)
- **API**: Django REST Framework exposes `/api/todos/` endpoints; React uses `axios` for CRUD operations
- **Deployment**: Designed for Heroku (see `Procfile`, `runtime.txt`, `requirements.txt`)

## Key Architecture & Data Flow
- **Frontend**: React app in `src/`, entry in `src/App.js`, communicates with backend via `/api/todos/` (proxy set in `package.json`)
- **Backend**: Django project in `backend/`, main app is `todo/` (models, serializers, views, urls)
- **API Routing**: All API endpoints are under `/api/` (see `backend/urls.py`)
- **CORS**: Managed via `django-cors-headers` (see `backend/settings.py`)
- **Static/Build**: React build output is served by Django in production (see `STATICFILES_DIRS` and `TEMPLATES` in `settings.py`)

## Developer Workflows
- **Backend**:
  - Run server: `python manage.py runserver` (from project root)
  - Migrations: `python manage.py makemigrations` / `migrate`
  - App code: `backend/todo/` (models, serializers, views)
- **Frontend**:
  - Start dev server: `npm start` (from project root)
  - Build for prod: `npm run build`
  - Main code: `src/` (entry: `App.js`)
- **Testing**:
  - React: `npm test`
  - Django: `python manage.py test`
- **Heroku Deploy**:
  - Add both Node and Python buildpacks (Node first)
  - Use `Procfile` for process definition
  - Use `.env` for local DB, Heroku config vars for prod

## Project-Specific Patterns & Conventions
- **API**: All CRUD via `/api/todos/` (see `backend/urls.py`)
- **Serializers**: All API data serialization in `todo/serializers.py`
- **Views**: Use DRF `ModelViewSet` for CRUD (see `todo/views.py`)
- **Frontend API Calls**: Use relative paths (e.g., `axios.get("/api/todos/")`), proxy handles routing
- **CSRF**: React/axios configured for Django CSRF (see `App.js`)
- **Static Files**: React build output is collected/served by Django (`STATICFILES_DIRS`)
- **Database**: SQLite for local, PostgreSQL for Heroku (see `.env`, `dj-database-url`)

## Integration Points
- **React <-> Django**: All data via REST API endpoints
- **Heroku**: Uses both Node and Python buildpacks; static files handled by WhiteNoise
- **Environment Config**: `.env` for local, Heroku config vars for prod

## References
- See `README.md` for full setup, deployment, and troubleshooting details
- Key files: `backend/settings.py`, `backend/urls.py`, `todo/serializers.py`, `todo/views.py`, `src/App.js`, `package.json`, `Procfile`, `.env`, `requirements.txt`, `runtime.txt`

---
_If you are unsure about a workflow or convention, check the `README.md` or ask for clarification._
