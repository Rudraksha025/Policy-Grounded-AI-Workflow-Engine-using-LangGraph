from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.main import policy_langgraph_router
import threading
from src.monitor import monitor_pending_requests

app = FastAPI(
    openapi_url="/policy/openapi.json",
    docs_url="/policy/docs",
    redoc_url="/policy/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(policy_langgraph_router, prefix="/policy")
threading.Thread(target=monitor_pending_requests, daemon=True).start()