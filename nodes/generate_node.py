from schema.state import ReviewState
from shared.utils import get_llm, get_policy_retriever

llm = get_llm()
retriever = get_policy_retriever()


def generate_node(state: ReviewState):
    policy_docs = retriever.invoke(state["input"])
    policy_context = "\n".join(doc.page_content for doc in policy_docs)

    prompt = f"""
    You are a loan compliance AI assistant.

    Follow this policy strictly:
    {policy_context}

    Rules:
    - NEVER provide advice on bypassing or weakening policy.
    - NEVER offer alternative approval steps.
    - If user input contains uncertainty, rewrite it professionally.
    - If user asks something unrelated to loan compliance, respond with:
    "This system only answers loan compliance questions."

    User Request:
    {state['input']}
    """

    response = llm.invoke(prompt)
    return {"output": response.content}
