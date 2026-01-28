import time
from src.database import SessionLocal, get_stale_pending_requests

def monitor_pending_requests():
    while True:
        db = SessionLocal()
        stale = get_stale_pending_requests(db)

        if stale:
            print("\nSLA ALERT – Pending human reviews older than 24h:")
            for r in stale:
                print(f"Request {r.request_id} pending since {r.created_at}")

        db.close()
        time.sleep(3600)   # check every hour
