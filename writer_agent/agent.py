from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json, uuid

app = FastAPI()

@app.get("/.well-known/agent.json")
async def agent_card():
    with open("agent_card.json") as f:
        return JSONResponse(json.load(f))

@app.post("/message:send")
async def message_send(request: Request):
    body = await request.json()
    findings = body["params"]["message"]["parts"][0]["text"]
    report = write_report(findings)
    task = {
        "id": str(uuid.uuid4()),
        "status": {"state": "TASK_STATE_COMPLETED"},
        "artifacts": [{
            "artifactId": str(uuid.uuid4()),
            "parts": [{"type": "text", "text": report}]
        }]
    }
    return JSONResponse({"jsonrpc": "2.0", "result": {"task": task}})

def write_report(findings: str) -> str:
    # Replace with an LLM call (e.g. Claude / GPT) for real formatting
    lines = findings.strip().split("\n")
    papers = [l for l in lines if l.strip().startswith(("1.", "2.", "3."))]
    report_lines = [
        "# Research Report",
        "",
        "## Summary",
        lines[0] if lines else "No findings provided.",
        "",
        "## Papers",
    ] + [f"- {p.split('. ', 1)[-1]}" for p in papers] + [
        "",
        "## Next Steps",
        "- Review each paper for methodology",
        "- Cross-reference citations",
        "- Identify gaps for further research",
    ]
    return "\n".join(report_lines)