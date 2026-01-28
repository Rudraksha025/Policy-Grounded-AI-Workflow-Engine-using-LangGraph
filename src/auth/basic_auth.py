from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

REVIEWER_USER = "reviewer001"
REVIEWER_PASS = "review123"

def review_auth(Credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(Credentials.username, REVIEWER_USER)
    correct_password = secrets.compare_digest(Credentials.password, REVIEWER_PASS)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )
    return Credentials.username