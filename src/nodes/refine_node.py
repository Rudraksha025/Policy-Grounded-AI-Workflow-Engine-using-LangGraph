from src.schema.state import ReviewState
from typing import TypedDict, List
from src.shared.utils import get_llm

llm = get_llm()

def refine_node(state: ReviewState):
    prompt = f"""
Rewrite the explanation so that:

- It strictly enforces loan rejection rules.
- It never suggests alternative actions or additional steps.
- It does not hint at policy circumvention.
- The decision must sound final and authoritative.

Violations:
{state['violations']}

Text:
{state['output']}
"""
    response = llm.invoke(prompt)
    return {
        "output": response.content,
        "retries": state["retries"] + 1
    }