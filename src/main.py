from fastapi import APIRouter

from src.views.review import app as review_router
from src.views.pending_reviews import app as pending_reviews_router
from src.views.human_approve import app as humna_approve_router
from src.views.result import app as result_router

policy_langgraph_router = APIRouter()

policy_langgraph_router.include_router(review_router, tags=["Start Review User Input"])
policy_langgraph_router.include_router(pending_reviews_router, tags=["All Pending Reviews"])
policy_langgraph_router.include_router(humna_approve_router, tags=["Revies To approve by human"])
policy_langgraph_router.include_router(result_router, tags=["Get results from Db "])
