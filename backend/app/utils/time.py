from datetime import datetime
def now_iso():
    return datetime.now().strftime("%Y-%m-%d %H:%M")
