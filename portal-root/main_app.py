from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core.discovery import discover_utilities
import os

app = FastAPI(title="Utility Portal Framework")

# Static and Templates setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")
templates_dir = os.path.join(BASE_DIR, "templates")

# Ensure directories exist
os.makedirs(static_dir, exist_ok=True)
os.makedirs(templates_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

# Discover utilities on startup
registry = discover_utilities()

# Mount all the routers from utilities
for util in registry.utilities_by_id.values():
    if util.router:
        app.include_router(util.router, prefix=f"/api/{util.id}", tags=[util.category])

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Render the main dashboard."""
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "registry": registry
    })

@app.get("/utility/{category}/{utility_name}", response_class=HTMLResponse)
async def wrapper(request: Request, category: str, utility_name: str):
    """Wrapper page for a specific utility."""
    util_id = f"{category}/{utility_name}"
    utility = registry.utilities_by_id.get(util_id)
    
    if not utility:
        raise HTTPException(status_code=404, detail="Utility not found")
        
    utility_html = ""
    if utility.render_func:
        try:
            # We assume it's a `def render()` with no args returning an HTML fragment string
            result = utility.render_func()
            if isinstance(result, str):
                utility_html = result
            else:
                utility_html = str(result)
        except Exception as e:
            utility_html = f'<div class="error-panel">Error rendering utility: {str(e)}</div>'
    else:
        utility_html = '<div class="info-panel">This utility does not provide a UI component via render(). Please use its API endpoints directly.</div>'
        
    return templates.TemplateResponse("utility_wrapper.html", {
        "request": request,
        "registry": registry,
        "utility": utility,
        "utility_html": utility_html
    })
