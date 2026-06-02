from datetime import datetime

def current_time():
    """Returns the current date and time."""

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
