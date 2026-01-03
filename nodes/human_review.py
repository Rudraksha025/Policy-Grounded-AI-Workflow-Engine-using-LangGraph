import uuid
from human_review.review import add_review
from schema import ReviewState

def human_review_node(state: ReviewState):
    task_id = str(uuid.uuid4())

    add_review(task_id, {
        "input": state["input"],
        "final_output": state["output"],
        "violations": state["violations"],
        "status": "PENDING"
    })

    state["task_id"] = task_id
    state["requires_human"] = True
    return state
