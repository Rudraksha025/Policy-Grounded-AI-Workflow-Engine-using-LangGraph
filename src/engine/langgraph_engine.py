from langgraph.graph import StateGraph, END
from src.schema.state import ReviewState
from src.nodes import generate_node, refine_node, decide_next, validate_node, human_review_node

def build_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("generate", generate_node)
    graph.add_node("validate", validate_node)
    graph.add_node("refine", refine_node)
    graph.add_node("human_review", human_review_node)

    graph.set_entry_point("generate")

    graph.add_edge("generate", "validate")
    graph.add_edge("refine", "validate")

    graph.add_conditional_edges(
        "validate",
        decide_next,
        {
            "refine": "refine",
            "human_review": "human_review",
            "end": END
        }
    )

    graph.add_edge("human_review", END)

    return graph.compile()