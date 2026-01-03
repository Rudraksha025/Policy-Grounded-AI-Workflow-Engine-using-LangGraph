from schema.state import ReviewState
from shared.utils import validate_text, detect_intent_conflict

def validate_node(state: ReviewState):
    violations = validate_text(state["output"])

    if detect_intent_conflict(state["input"]):
        violations.append("User explicitly requested policy override")

    return {
        "validated": len(violations) == 0,
        "violations": violations,
        "requires_human": False if len(violations) == 0 else state.get("requires_human", False)
    }

