import httpx, uuid

class A2AClient:
    def __init__(self, agent_url: str):
        self.agent_url = agent_url
        self.card = self._fetch_card()

    def _fetch_card(self) -> dict:
        """Phase 1: Discovery — fetch the Agent Card"""
        resp = httpx.get(f"{self.agent_url}/.well-known/agent.json")
        resp.raise_for_status()
        return resp.json()

    def send_task(self, query: str) -> dict:
        """Phase 3: Send a task to the remote agent"""
        payload = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "message/send",
            "params": {
                "message": {
                    "role": "ROLE_USER",
                    "messageId": str(uuid.uuid4()),
                    "parts": [{"text": query}]
                }
            }
        }
        resp = httpx.post(
            f"{self.agent_url}/message:send",
            json=payload,
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()["result"]["task"]

    def get_artifact_text(self, task: dict) -> str:
        """Extract text from the first artifact"""
        artifacts = task.get("artifacts", [])
        if not artifacts:
            return "No artifacts returned."
        parts = artifacts[0].get("parts", [])
        return parts[0].get("text", "") if parts else ""