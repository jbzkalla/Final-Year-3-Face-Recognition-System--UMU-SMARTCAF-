
# In-memory storage for the active session
# Structure: {"name": "Lunch", "start_time": "...", "status": "active"}
ACTIVE_SESSION = {}

def start_session(session_name, mode="continuous"):
    global ACTIVE_SESSION
    if ACTIVE_SESSION.get("status") == "active":
        return False, "Session already active"
    
    import datetime
    ACTIVE_SESSION = {
        "name": session_name,
        "mode": mode,
        "start_time": datetime.datetime.now().isoformat(),
        "status": "active"
    }
    return True, f"Session '{session_name}' ({mode}) started"

def stop_session():
    global ACTIVE_SESSION
    if ACTIVE_SESSION.get("status") != "active":
        return False, "No active session"
    
    session_name = ACTIVE_SESSION.get("name")
    ACTIVE_SESSION = {
        "status": "inactive"
    }
    return True, f"Session '{session_name}' stopped"

def get_active_session():
    return ACTIVE_SESSION
