from pydantic import BaseModel

class ReviewRequest(BaseModel):
    input: str