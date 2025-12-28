from flask import Blueprint, request, jsonify
import os
from payments.finance_service import save_temp_file, parse_file_headers, parse_full_file, validate_records, apply_confirmed_payments

finance_bp = Blueprint('finance', __name__)

# Temporary storage for session-like behavior (in production use Redis or DB)
# Key: file_token, Value: { filepath, mapping, parsed_data }
upload_sessions = {} 

@finance_bp.route('/api/finance/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"}), 400
        
    filepath, filename = save_temp_file(file)
    if filepath:
        # Get headers for mapping
        headers, error = parse_file_headers(filepath)
        if error:
             return jsonify({"success": False, "message": f"Parse error: {error}"}), 400
             
        # Create a session token (using filename for simplicity in this demo, ideally UUID)
        token = filename 
        upload_sessions[token] = { "filepath": filepath }
        
        return jsonify({
            "success": True, 
            "message": "File uploaded", 
            "token": token,
            "columns": headers
        })
    else:
        return jsonify({"success": False, "message": "Invalid file type or save failed"}), 400

@finance_bp.route('/api/finance/preview', methods=['POST'])
def preview_data():
    data = request.get_json()
    token = data.get('token')
    mapping = data.get('mapping') # dict { sys_col: file_col }
    configs = data.get('configs', {}) # { default_meal_type: 'Lunch', ... }
    
    if token not in upload_sessions:
        return jsonify({"success": False, "message": "Session expired or invalid file"}), 404
        
    session = upload_sessions[token]
    filepath = session['filepath']
    
    # Parse full file with mapping
    raw_records, error = parse_full_file(filepath, mapping)
    if error:
        return jsonify({"success": False, "message": f"Mapping error: {error}"}), 400
        
    # Validation
    valid, invalid = validate_records(raw_records, configs)
    
    # Store in session for confirmation step
    session['valid_records'] = valid
    session['configs'] = configs
    
    # Return preview (limited set or full?)
    # Frontend usually paginates, but we send all for this scale (<10k rows usually)
    summary = {
        "total": len(raw_records),
        "valid": len(valid),
        "invalid": len(invalid),
        "preview_data": (valid[:5] + invalid[:5]), # Send a sample mixed
        "all_valid_count": len(valid)
    }
    
    return jsonify({
        "success": True,
        "summary": summary,
        # In a real app, might just return IDs or paginated data. 
        # Here we send full lists for the frontend JS to handle pagination if small.
        "valid_records": valid, # Sending all for frontend render
        "invalid_records": invalid
    })

@finance_bp.route('/api/finance/confirm', methods=['POST'])
def confirm_import():
    data = request.get_json()
    token = data.get('token')
    
    if token not in upload_sessions:
        return jsonify({"success": False, "message": "Session expired"}), 404
        
    session = upload_sessions[token]
    if 'valid_records' not in session:
        return jsonify({"success": False, "message": "No validated data found. Preview first."}), 400
        
    valid_records = session['valid_records']
    configs = session.get('configs', {})
    
    count = apply_confirmed_payments(valid_records, configs)
    
    # Cleanup
    try:
        if os.path.exists(session['filepath']):
            os.remove(session['filepath'])
        del upload_sessions[token]
    except:
        pass
        
    return jsonify({
        "success": True, 
        "message": "Import completed successfully", 
        "processed_count": count
    })
