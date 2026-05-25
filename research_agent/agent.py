from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json, uuid

app = FastAPI()
tasks = {}

@app.get("/.well-known/agent.json")
async def agent_card():
    with open("agent_card.json") as f:
        return JSONResponse(json.load(f))

@app.post("/message:send")
async def message_send(request: Request):
    body = await request.json()
    query = body["params"]["message"]["parts"][0]["text"]
    task_id = str(uuid.uuid4())
    result = search_papers(query)
    task = {
        "id": task_id,
        "status": {"state": "TASK_STATE_COMPLETED"},
        "artifacts": [{
            "artifactId": str(uuid.uuid4()),
            "parts": [{"type": "text", "text": result}]
        }]
    }
    return JSONResponse({"jsonrpc": "2.0", "result": {"task": task}})

def search_papers(query: str) -> str:
    # Replace with real API calls (arXiv, Semantic Scholar, etc.)
    return f"Found 3 papers on '{query}':\n1. Paper A\n2. Paper B\n3. Paper C"