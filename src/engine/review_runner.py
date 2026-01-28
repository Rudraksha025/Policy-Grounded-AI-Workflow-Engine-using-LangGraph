from src.engine.langgraph_engine import build_graph

graph = build_graph()

def run_compliance_review(user_input: str, request_id: str, intent_override: bool):
    result = graph.invoke({
        "request_id": request_id,
        "input": user_input,
        "intent_override": intent_override,
        "output": "",
        "validated": False,
        "violations": [],
        "retries": 0,
        "requires_human": False
    })

    return result
