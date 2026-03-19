# Lightweight Python Utility Portal

A fast, visually-stunning, and extensible Python-based UI portal framework that serves as a centralized dashboard for utility tools.

## Architecture
- **Framework:** FastAPI
- **UI:** Jinja2 templates + Vanilla CSS & JavaScript + Glassmorphism design
- **Data:** File system driven. No database is required.

## Adding a New Utility
Utilities are auto-discovered on startup. To add a new utility:
1. Create a category folder in `utilities/` (e.g., `utilities/csv_utils/`).
2. Create your utility folder inside the category (e.g., `utilities/csv_utils/csv_compare/`).
3. Add a `README.md` to your utility folder. The first header (`# title`) will be the utility name. The rest is the description. Add tags like `Tags: csv, data`.
4. Add an `app.py` that exposes a `def render()` returning an HTML snippet (or Jinja template).
5. Optionally, expose an `APIRouter()` named `router` in `app.py` to handle backend logic. It will be automatically mounted at `/api/{category}/{utility_name}`.

## Running Locally
```bash
pip install -r requirements.txt
uvicorn main_app:app --reload
```
Navigate to http://localhost:8000

## Deploying with Docker
```bash
docker build -t utility-portal .
docker run -p 8000:8000 utility-portal
```
