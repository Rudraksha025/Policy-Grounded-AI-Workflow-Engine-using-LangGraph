from typing import TypedDict, List, Optional

class ReviewState(TypedDict):
    input: str
    output: str
    validated: bool
    violations: List[str]
    retries: int
    task_id: Optional[str]
    requires_human: bool
