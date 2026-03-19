from fastapi import APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse
import csv
import io

router = APIRouter()

def render():
    return """
    <div class="util-form" style="max-width: 600px;">
        <p>Select two CSV files to compare their structures and row counts.</p>
        <form hx-post="/api/csv_utils/csv_compare/compare" hx-target="#csv-result" enctype="multipart/form-data" class="form-group">
            <div class="form-group">
                <label>First CSV File</label>
                <input type="file" name="file1" class="form-control" accept=".csv" required>
            </div>
            <div class="form-group" style="margin-top: 10px;">
                <label>Second CSV File</label>
                <input type="file" name="file2" class="form-control" accept=".csv" required>
            </div>
            <button type="submit" class="btn-primary" style="margin-top: 20px;">Compare Files 🚀</button>
        </form>
        
        <div id="csv-result" class="result-box">
            <em style="color: var(--text-secondary);">Results will appear here...</em>
        </div>
    </div>
    """

@router.post("/compare")
async def compare_csvs(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        content1 = await file1.read()
        content2 = await file2.read()
        
        text1 = content1.decode('utf-8')
        text2 = content2.decode('utf-8')
        
        reader1 = list(csv.reader(io.StringIO(text1)))
        reader2 = list(csv.reader(io.StringIO(text2)))
        
        headers1 = reader1[0] if reader1 else []
        headers2 = reader2[0] if reader2 else []
        
        html = f"<h3 style='margin-bottom:12px;color:var(--text-primary);'>Comparison Report</h3>"
        html += f"<p><strong>{file1.filename}</strong>: {len(reader1)} rows, {len(headers1)} columns</p>"
        html += f"<p><strong>{file2.filename}</strong>: {len(reader2)} rows, {len(headers2)} columns</p>"
        
        html += "<hr style='border:none; border-top:1px solid var(--border-glass); margin: 12px 0;'>"
        
        if headers1 == headers2:
            html += "<p style='color: #4ade80;'>✅ Columns match perfectly.</p>"
        else:
            html += "<p style='color: #ef4444;'>❌ Column mismatch detected.</p>"
            set1 = set(headers1)
            set2 = set(headers2)
            if set1 - set2:
                html += f"<p><strong>Only in {file1.filename}:</strong> {', '.join(set1 - set2)}</p>"
            if set2 - set1:
                html += f"<p><strong>Only in {file2.filename}:</strong> {', '.join(set2 - set1)}</p>"
                
        return HTMLResponse(html)
    except Exception as e:
        return HTMLResponse(f"<div class='error-panel'>Error processing files: {str(e)}</div>")
