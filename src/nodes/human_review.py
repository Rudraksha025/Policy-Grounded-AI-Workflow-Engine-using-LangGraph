from src.schema import ReviewState
from src.database import SessionLocal, update_ai_draft

def human_review_node(state: ReviewState):
    db = SessionLocal()

    update_ai_draft(
        db,
        state["request_id"],
        state["output"],
        "PENDING_HUMAN"
    )

    db.close()

    state["requires_human"] = True
    return state
