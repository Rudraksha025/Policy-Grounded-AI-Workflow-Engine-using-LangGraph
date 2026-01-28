from src.schema.state import ReviewState
from src.shared.utils import get_llm, get_policy_retriever
from src.database.db import SessionLocal
from src.database.crud import update_ai_draft

llm = get_llm()
retriever = get_policy_retriever()

def generate_node(state: ReviewState):
    
    if state["intent_override"]:
        placeholder = "User attempted to override policy. Escalated for human review."

        db = SessionLocal()
        update_ai_draft(
            db,
            state["request_id"],
            placeholder,
            "PENDING_HUMAN"
        )
        db.close()

        return {
            "output": placeholder,
            "requires_human": True
        }

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

    # Persist AI draft into DB
    db = SessionLocal()
    update_ai_draft(db, state["request_id"], response.content, "PENDING_VALIDATION")
    db.close()

    return {"output": response.content}
