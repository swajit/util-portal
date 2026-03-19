from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse

router = APIRouter()

def render():
    return """
    <div class="util-form">
        <p>Paste your raw X12 EDI payload below to format and highlight its structure:</p>
        <form hx-post="/api/x12_utils/x12_formatter/format" hx-target="#x12-result" class="form-group">
            <textarea name="raw_edi" class="form-control" rows="8" placeholder="ISA*00*          *00*          *ZZ*SUBMITTER      *ZZ*RECEIVER       *200101*1230*^*00501*000000001*0*T*:~GS*HC*...~" required style="font-family: monospace;"></textarea>
            <button type="submit" class="btn-primary" style="margin-top: 10px; width: 250px;">Format & Highlight X12 🪄</button>
        </form>
        
        <div id="x12-result" class="result-box" style="margin-top: 20px; padding: 0; background: transparent; border: none;">
        </div>
    </div>
    """

@router.post("/format")
async def format_x12(raw_edi: str = Form(...)):
    if not str(raw_edi).strip():
        return HTMLResponse("<div class='error-panel'>Input is empty</div>")
        
    # Clean up any literal newlines user might have pasted
    edi = raw_edi.replace('\\r', '').replace('\\n', '').strip()
    
    segment_term = '~'
    element_term = '*'
    if edi.startswith('ISA') and len(edi) > 105:
        # Standard X12 places element separator at index 3
        element_term = edi[3]
        # Standard X12 places segment terminator at index 105
        segment_term = edi[105]

    segments = [s.strip() for s in edi.split(segment_term) if s.strip()]
    
    html = "<div style='font-family: Inconsolata, monospace; line-height: 1.6; background: rgba(10, 10, 15, 0.8); padding: 16px; border-radius: 8px; overflow-x: auto; white-space: pre; border: 1px solid var(--border-glass); font-size: 0.95rem;'>"
    
    for seg in segments:
        elements = seg.split(element_term)
        seg_id = elements[0]
        
        # Segment ID
        line_html = f"<span style='color: #4ade80; font-weight: bold;'>{seg_id}</span>"
        
        for i, el in enumerate(elements[1:], start=1):
            # Element Separator
            line_html += f"<span style='color: #6b7280;'>{element_term}</span>"
            # Element Value (with hover effect and tooltip)
            tooltip_text = f"Element: {seg_id}-{i:02d}"
            line_html += f'<span style="color: #e2e8f0; transition: color 0.2s; cursor: pointer; padding: 0 2px;" title="{tooltip_text}" onmouseover="this.style.color=\\'#fde047\\'" onmouseout="this.style.color=\\'#e2e8f0\\'">{el}</span>'
            
        # Segment Terminator
        line_html += f"<span style='color: #f87171; font-weight: bold;'>{segment_term}</span>"
        html += f"<div>{line_html}</div>"
        
    html += "</div>"
    
    return HTMLResponse(html)
