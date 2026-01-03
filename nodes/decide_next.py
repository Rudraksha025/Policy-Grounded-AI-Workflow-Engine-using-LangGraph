from schema.state import ReviewState

MAX_RETRIES = 2

def decide_next(state: ReviewState):
    if state["validated"]:
        return "end"

    if state["retries"] >= MAX_RETRIES:
        state["requires_human"] = True
        return "human_review"

    return "refine"
