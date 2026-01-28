# 🏦 Compliance AI System  
### Policy-Enforced Loan Review Engine with Human-in-the-Loop

---

## 1. What this project is (and what it is not)

This project implements a **policy-enforced AI compliance workflow**, designed for regulated decision-making scenarios such as loan approvals.

It is **not**:
- a chatbot
- a simple LLM wrapper
- a prompt-engineering demo

It **is**:
- a deterministic AI workflow
- with pre-LLM intent detection
- policy-grounded reasoning (RAG)
- automatic validation and self-correction
- guaranteed human escalation for unsafe intent
- immutable decisions
- full audit logging
- SLA monitoring
- role-separated user and reviewer interfaces

The system is designed to answer one question reliably:

> *When should AI decide, when should it correct itself, and when must a human intervene?*

---

## 2. High-level system flow

At a conceptual level, the system works like this:

User Input
↓
Intent Detection (Pre-LLM)
↓
AI Generation (Policy-Grounded)
↓
Validation (Rules + Behavior)
↓
Decision Routing
├─ Auto-Finalize (APPROVED)
└─ Human Escalation (PENDING_HUMAN)
↓
Human Review
↓
Final Approval



The key idea is that **not all inputs are equal**:
- Some are safe and automatable
- Some are fixable by refinement
- Some are dangerous and must never be auto-approved

---

## 3. Core design principles

This system follows five non-negotiable principles:

1. **Intent must be detected before generation**
2. **Policy overrides must never be auto-handled**
3. **AI decisions must be auditable**
4. **Approved decisions must be immutable**
5. **Humans intervene only when required**

Every file and function exists to enforce one of these principles.

---

## 4. Directory structure overview

.
├── main.py # FastAPI app + LangGraph engine
├── user_app.py # User Streamlit UI
├── reviewer_app.py # Reviewer Streamlit UI
│
├── src/
│ ├── auth/
│ │ └── basic_auth.py # Reviewer authentication
│ │
│ ├── config/
│ │ └── env_var.py # Environment variables
│ │
│ ├── database/
│ │ ├── db.py # SQLAlchemy engine/session
│ │ ├── models.py # ComplianceRequest table
│ │ ├── events.py # ComplianceEvent audit table
│ │ ├── crud.py # Controlled DB operations
│ │ └── init_db.py # DB bootstrap script
│ │
│ ├── engine/
│ │ └── graph_runner.py # run_compliance_review
│ │
│ ├── nodes/
│ │ ├── generate_node.py
│ │ ├── validate_node.py
│ │ ├── refine_node.py
│ │ ├── decide_next.py
│ │ └── human_review.py
│ │
│ ├── policies/
│ │ └── loan_policy.txt # Ground truth policy
│ │
│ ├── schema/
│ │ ├── state.py # ReviewState (graph contract)
│ │ └── pending_review.py # API request schema
│ │
│ ├── shared/
│ │ └── utils.py # LLM, RAG, validation, intent detection
│ │
│ ├── views/
│ │ ├── review.py # Submit request API
│ │ ├── result.py # Poll result API
│ │ ├── pending_reviews.py # Reviewer queue API
│ │ └── human_approve.py # Approve endpoint
│ │
│ └── monitor/
│ └── sla_monitor.py # SLA timeout checker


---

## 5. The data model (source of truth)

### 5.1 compliance_requests

This table stores the **entire lifecycle** of a compliance decision.

Fields:
- `request_id` – immutable identifier
- `user_input` – original user text
- `ai_draft` – AI-generated or placeholder output
- `final_output` – approved decision (nullable)
- `status` – workflow state
- `created_at` – timestamp

This table answers:
> “What decision exists right now?”

---

### 5.2 compliance_events (audit trail)

This table logs **every status transition**.

Fields:
- `id`
- `request_id`
- `old_status`
- `new_status`
- `timestamp`

This table answers:
> “What happened, when, and in what order?”

No compliance system is valid without this.

---

## 6. Intent detection (the most critical layer)

Before the LLM is ever called, the system runs:

```python
detect_intent_conflict(user_input)
This detects whether the user is attempting to:
- ignore policy
- override rules
- coerce approval

The result is a boolean flag:
intent_override = True | False

This flag is:
- computed once
- immutable
- passed into the LangGraph state
- never re-evaluated later

This prevents jailbreaks caused by LLM rewriting.


## 7 ReviewState (LangGraph contract)
All nodes operate on a shared, explicit state:

class ReviewState(TypedDict):
    request_id: str
    input: str
    intent_override: bool
    output: str
    validated: bool
    violations: List[str]
    retries: int
    requires_human: bool
If a field is not declared here, it does not exist in the graph.

This guarantees determinism.

## 8. LangGraph Nodes — Step-by-Step Execution

The decision-making logic is implemented using LangGraph.  
Each node has a **single responsibility** and cannot bypass others.

The graph is deterministic: the same input always produces the same routing behavior.

---

### 8.1 generate_node — Policy-Grounded Generation

**Purpose**
- Generate a compliance explanation strictly based on policy
- OR immediately escalate if the user intent is unsafe

**Execution Logic**
1. If `intent_override == True`
   - The LLM is NOT called
   - A neutral placeholder message is created
   - Status is set to `PENDING_HUMAN`
   - Execution stops

2. If `intent_override == False`
   - Policy text is retrieved using RAG
   - The LLM generates a compliance explanation
   - Draft is stored in the database
   - Status becomes `PENDING_VALIDATION`

This ensures the AI never reasons about policy overrides.

---

### 8.2 validate_node — Compliance Validation

**Purpose**
- Decide whether the AI output is compliant and final

**Validation Checks**
- Weak or uncertain language
- Illegal approvals
- Policy violations
- Intent override flag

**Rules**
- If **any violation exists** → output is NOT valid
- If **no violations exist** → output is final

A strict rejection is considered a valid and complete decision.

---

### 8.3 refine_node — Language Correction Loop

**Purpose**
- Improve clarity and authority of the explanation
- Never change the decision outcome

**Behavior**
- Rewrites the explanation using stricter language
- Increments retry counter
- Does not interact with policy or intent logic

Refinement exists only to fix wording, not decisions.

---

### 8.4 decide_next — Deterministic Routing

**Purpose**
- Decide the next step in the workflow

**Routing Rules**
- If `validated == True` → END
- If retry limit exceeded → `human_review`
- Otherwise → `refine`

This node performs no reasoning. It only routes execution.

---

### 8.5 human_review_node — Human Escalation

**Purpose**
- Persist escalation state
- End AI-driven execution

**Behavior**
- Stores the case as `PENDING_HUMAN`
- Marks the request as requiring human review
- Ends the LangGraph execution

After this node, only a human can finalize the decision.

---

## 9. Human-in-the-Loop Workflow

Cases are escalated to humans only when:
- The user attempts to override policy
- The AI cannot produce a compliant output after retries

### Human Reviewer Capabilities
- View pending cases
- Inspect original input and AI draft
- Edit the final decision
- Approve once

### Constraints
- Approved records cannot be modified
- All approvals are logged
- Authentication is mandatory

This guarantees accountability.

---

## 10. SLA Monitoring

A background monitor continuously checks for requests stuck in:

PENDING_HUMAN > 24hours

This enables:
- SLA tracking
- Operational alerts
- Escalation handling

Compliance systems must monitor unresolved cases.

---

## 11. User Interface Separation

### User Portal
- Submit compliance requests
- Poll request status
- View final decision
- No access to drafts or other users

### Reviewer Portal
- Authenticated access only
- View pending human reviews
- Approve final decisions
- No submission capability

Role separation prevents misuse and confusion.

---

## 12. Authentication

Reviewer endpoints are protected using HTTP Basic Authentication.

Without valid credentials:
- Pending reviews cannot be accessed
- Approvals are rejected

This prevents anonymous or unauthorized approvals.

---

## 13. Why This Architecture Matters

This system clearly defines:
- When AI is allowed to decide
- When AI must stop
- When humans must intervene
- How every decision can be audited later

This is the foundation of regulated AI systems.

---

## 14. Running the System

### Backend
uvicorn main:app --reload

### User Interface
streamlit run user_app.py

### Reviewer Interface
streamlit run reviewer_app.py

