from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
import json

router = APIRouter()

def render():
    return """
    <div class="util-form">
        <p>Paste your raw JSON below to safely format and validate it:</p>
        <form hx-post="/api/text_utils/json_formatter/format" hx-target="#json-result" class="form-group">
            <textarea name="raw_json" class="form-control" rows="8" placeholder='{"key": "value"}' required style="font-family: monospace;"></textarea>
            <button type="submit" class="btn-primary" style="margin-top: 10px; width: 200px;">Format JSON 🪄</button>
        </form>
        
        <div id="json-result" class="result-box" style="margin-top: 20px;">
        </div>
    </div>
    """

@router.post("/format")
async def format_json(raw_json: str = Form(...)):
    try:
        parsed = json.loads(raw_json)
        formatted = json.dumps(parsed, indent=4)
        return HTMLResponse(f"<pre style='color: #a8b1ff; font-family: monospace; overflow-x: auto;'>{formatted}</pre>")
    except json.JSONDecodeError as e:
        return HTMLResponse(f"<div class='error-panel'><b>Invalid JSON:</b> {str(e)}</div>")
