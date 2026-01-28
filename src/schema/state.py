from typing import TypedDict, List, Optional

class ReviewState(TypedDict):
    request_id: str
    input: str
    intent_override: bool
    output: str
    validated: bool
    violations: List[str]
    retries: int
    requires_human: bool

