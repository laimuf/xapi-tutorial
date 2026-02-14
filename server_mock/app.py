import logging
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("xapi")

YELLOW = "\033[93m"      # Bright Yellow
ORANGE = "\033[33m"      # Orange/Dark Yellow
PURPLE = "\033[95m"      # Bright Purple
CYAN = "\033[96m"        # Bright Cyan
GREEN = "\033[92m"       # Bright Green
RED = "\033[91m"         # Bright Red
BLUE = "\033[94m"        # Bright Blue
RESET = "\033[0m"

def log_statement(statement_id: str, payload: dict):
    actor = payload.get("actor", {}).get("name", "Unknown")
    verb = payload.get("verb", {}).get("display", {}).get("en-US", "unknown")
    activity = payload.get("object", {}).get("definition", {}).get("name", {}).get("en-US", "unknown")
    

    logger.info(f"\n  [STORED]\n\t{YELLOW}Actor = {PURPLE}{actor}{RESET} \n\t{YELLOW}Verb = {PURPLE}{verb}{RESET} \n\t{YELLOW}Activity = {PURPLE}{activity}{RESET} \n\t{YELLOW}Statement ID = {PURPLE}{statement_id}{RESET}\n")



SERVER_HOST = os.getenv("SERVER_HOST", "localhost")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8080"))

app = FastAPI(
    title="xAPI Mock Server",
    host=SERVER_HOST,
    port=SERVER_PORT,
)

# Allow CORS for all origins for testing purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/xapi/statements")
async def receive_xapi_statement(request: Request):
    """
    Mock endpoint for receiving xAPI statements.
    Accepts any valid JSON payload.
    """
    payload = await request.json()
    log_statement("server-assigned", payload)

    return JSONResponse(
        status_code=200,
        content={
            "message": "xAPI statement received",
            "statement": payload,
        },
    )


@app.put("/xapi/statements")
async def put_xapi_statement(request: Request, statementId: str):
    """
    TinCan.js sendStatement uses PUT with a statementId query parameter.
    """
    payload = await request.json()
    log_statement(statementId, payload)

    return JSONResponse(
        status_code=200,
        content={
            "statementId": statementId,
            "stored": True,
            "statement": payload,
        },
    )


@app.get("/health")
async def health_check():
    return {"status": "ok"}
