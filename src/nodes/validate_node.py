from src.schema.state import ReviewState
from src.shared.utils import validate_text
from src.database import SessionLocal, approve_request

def validate_node(state: ReviewState):
    violations = validate_text(state["output"])

    if state["intent_override"]:
        return {
            "validated": False,
            "violations": ["User attempted to override policy"],
            "requires_human": True
        }

    # If no violations, auto-approve
    if len(violations) == 0:
        db = SessionLocal()
        approve_request(db, state["request_id"], state["output"])
        db.close()

        return {
            "validated": True,
            "violations": [],
            "requires_human": False
        }

    return {
        "validated": False,
        "violations": violations,
        "requires_human": False
    }
