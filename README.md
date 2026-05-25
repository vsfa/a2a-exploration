# A2A exploration project

## Core concepts
Three objects make up everything in A2A. Understanding them makes the rest obvious.
### Agent Card
Every A2A server publishes a JSON file at /.well-known/agent.json. It describes the agent's identity, skills, and authentication requirements. Client agents fetch this file for discovery — no registry, no manual configuration. The card declares the agent's name, description, URL, version, the skills it offers (including their input and output modes), and the authentication schemes it supports.

### Task
The Task is the unit of work. A client sends a message; the server creates a Task object and manages its lifecycle. A Task can complete immediately or evolve over many round-trips.
The six possible Task states are:

`TASK_STATE_SUBMITTED` — received, not yet started
`TASK_STATE_WORKING` — agent is processing
`TASK_STATE_INPUT_NEEDED` — agent needs clarification from the client
`TASK_STATE_COMPLETED` — done; artifacts are ready
`TASK_STATE_FAILED` — unrecoverable error
`TASK_STATE_CANCELLED` — explicitly cancelled by the client

### Artifact
The Artifact is the output of a completed Task. An Artifact contains one or more Parts — fully-formed pieces of content. Parts carry a media type so both sides know how to render or consume the content. A single Artifact can carry a human-readable text summary alongside structured JSON data, for example.

## Protocol flow
Every A2A interaction follows the same four-phase pattern.

## Phase 1 — Discovery via Agent Card
The client agent issues a plain HTTP GET to the remote agent's well-known URL and receives the Agent Card JSON in response. This is the handshake — no manual registration, no out-of-band configuration. The client reads the card to understand what skills the agent offers and how to authenticate.

### Phase 2 — Authentication
The client authenticates using the scheme declared in the Agent Card. A2A supports OAuth 2.0, API keys, and OpenID Connect — aligned with OpenAPI security schemes. The bearer token or equivalent credential is included on every subsequent request.

### Phase 3 — Sending a task (message/send)
The client sends a JSON-RPC 2.0 request to the message/send endpoint. The request body contains a message with a role, a message ID, and one or more parts carrying the actual content. The server creates a Task, begins processing, and returns the Task object in the response. For short tasks the state may already be TASK_STATE_COMPLETED; for longer work it will be TASK_STATE_WORKING.

### Phase 4 — Streaming results via SSE
For long-running tasks the server streams updates via Server-Sent Events. The stream carries two event types: task_status_update (state changes) and task_artifact_update (partial or final artifact content). The client reassembles the stream into the completed Artifact once TASK_STATE_COMPLETED arrives.

## Architecture overview
A typical A2A system has an Orchestrator (the client agent) that reads multiple Agent Cards at startup, then fans tasks out to the appropriate remote agents. Each remote agent is an independent server. Results stream back to the Orchestrator, which assembles the final output for the user. The agents never communicate with each other directly — all coordination goes through the Orchestrator.

## A2A vs MCP

| | MCP (Model Context Protocol) | A2A (Agent2Agent) |
|---|---|---|
| **Connects** | Agent ↔ Tools / Data | Agent ↔ Agent |
| **Use for** | Databases, APIs, files, external resources | Delegating tasks to other agents across vendors |
| **Origin** | Anthropic | Google / Linux Foundation |
| **Think of it as** | How an agent *gets information* | How agents *collaborate* |

## How to run

### Setup
Each agent is its own isolated uv project with its own virtual environment. The Research Agent requires `fastapi` and `uvicorn[standard]`; the Orchestrator requires `httpx`. Dependencies are declared with `uv add` and installed into the local `.venv`. Scripts are always run with `uv run` so the correct virtual environment is used automatically — never invoke `python` directly.

The Research Agent server is started with `uv run uvicorn agent:app --port 8001 --reload`. The Orchestrator is run in a second terminal with `uv run python main.py`. The `--reload` flag means changes to `agent.py` hot-reload without interrupting the client.

The Agent Card can be verified independently at any time by curling `http://localhost:8001/.well-known/agent.json`.

### Research Agent
cd research_agent
uv run uvicorn agent:app --port 8001 --reload

### Writer Agent
cd writer_agent
uv run uvicorn agent:app --port 8002 --reload

## Orchestrator
cd orchestrator
uv run python main.py

