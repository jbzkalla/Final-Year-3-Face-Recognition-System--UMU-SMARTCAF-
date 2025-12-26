import datetime
import time

def get_current_timestamp():
    """
    Returns the current timestamp in 'YYYY-MM-DD HH:MM:SS' format.
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_current_date():
    """
    Returns the current date in 'YYYY-MM-DD' format.
    """
    return datetime.datetime.now().strftime("%Y-%m-%d")

def get_current_time():
    """
    Returns the current time in 'HH:MM:SS' format.
    """
    return datetime.datetime.now().strftime("%H:%M:%S")

def format_datetime(dt_obj):
    """
    Formats a datetime object to string.
    """
    if isinstance(dt_obj, datetime.datetime):
        return dt_obj.strftime("%Y-%m-%d %H:%M:%S")
    return str(dt_obj)

def time_diff_minutes(start_time, end_time=None):
    """
    Calculates the difference in minutes between two timestamps.
    If end_time is None, uses current time.
    """
    if end_time is None:
        end_time = datetime.datetime.now()
        
    if isinstance(start_time, str):
        try:
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        except:
            return 0
            
    diff = end_time - start_time
    return diff.total_seconds() / 60
