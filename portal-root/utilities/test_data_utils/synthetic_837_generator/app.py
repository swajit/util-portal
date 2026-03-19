def render():
    return """
    <div class="util-form">
        <p>Configure your test data generation batch below:</p>
        <div class="form-group" style="max-width: 400px;">
            <label>Claim Type</label>
            <select class="form-control">
                <option>837 Professional (837P)</option>
                <option>837 Institutional (837I)</option>
                <option>837 Dental (837D)</option>
            </select>
            
            <label style="margin-top: 10px;">Number of Claims to Generate</label>
            <input type="number" class="form-control" value="100" min="1" max="10000">
            
            <label style="margin-top: 10px;">Output Format</label>
            <select class="form-control">
                <option>EDI X12</option>
                <option>JSON</option>
            </select>
            
            <button class="btn-primary" style="margin-top: 20px;" onclick="document.getElementById('mock-result').style.display='block';">Generate Test Data ⚙️</button>
        </div>
        
        <div id="mock-result" class="result-box" style="display: none; border-color: var(--accent-2); max-width: 400px;">
            <p style="color: var(--accent-2);">✅ Generation started! Batch ID: #SYN-99482</p>
        </div>
    </div>
    """
