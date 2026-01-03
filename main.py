from typing import Dict
from schema import ReviewState
from langgraph.graph import StateGraph, END
from shared import get_llm
from nodes import generate_node,refine_node,decide_next,validate_node, human_review_node


llm = get_llm()

#Graph
graph = StateGraph(ReviewState)

# ── Nodes ───────────────────────────────
graph.add_node("generate", generate_node)
graph.add_node("validate", validate_node)
graph.add_node("refine", refine_node)
graph.add_node("human_review", human_review_node)

# ── Entry Point ─────────────────────────
graph.set_entry_point("generate")

# ── Core Flow ───────────────────────────
graph.add_edge("generate", "validate")
graph.add_edge("refine", "validate")

# ── Decision Routing ────────────────────
graph.add_conditional_edges(
    "validate",
    decide_next,
    {
        "refine": "refine",
        "human_review": "human_review",
        "end": END
    }
)

# ── Human Review Exit ───────────────────
graph.add_edge("human_review", END)

# ── Compile ─────────────────────────────
app = graph.compile()


def run_compliance_review(user_input: str):
    result = app.invoke({
    "input": user_input,
    "output": "",
    "validated": False,
    "violations": [],
    "retries": 0,
    "task_id": None,
    "requires_human": False
})

    if result.get("requires_human"):
        return {
            "status": "PENDING_HUMAN_REVIEW",
            "task_id": result["task_id"],
            "final_output": result["output"],
            "violations": result["violations"]
        }

    if result["validated"]:
        return {
            "status": "APPROVED",
            "final_output": result["output"]
        }

    return {
        "status": "REJECTED",
        "final_output": result["output"],
        "violations": result["violations"]
    }   







# if __name__ == "__main__":
#     print(run_compliance_review("Explain why a loan is rejected when credit score is below 600."))
#     print(run_compliance_review("I think maybe the loan should be approved."))
