pending_reviews = {}

def add_review(task_id: str, data=dict):
    pending_reviews[task_id] = data

def get_reviews():
    return pending_reviews

def approve_review(task_id: str, edited_output: str | None = None):
    task = pending_reviews.pop(task_id)

    if edited_output:
        task["final_output"] = edited_output
    
    task["status"] = "APPROVED BY HUMAN"
    return task