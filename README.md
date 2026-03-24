# personal-llm-box

A minimal, self-hosted Personal AI Box running on a single server with local LLM, chat UI, artifact storage, and a simple knowledge workflow.

## Architecture

| Component | Technology | Port |
|-----------|-----------|------|
| LLM backend | Ollama (`qwen3:8b`) | 11434 |
| Chat UI | Open WebUI | 3000 |
| API backend | FastAPI (Python) | 8000 |
| Storage | Local `./knowledge/` folder (git-tracked) | – |

## Quick start

```bash
# 1. Clone the repo
git clone https://github.com/sv-pro/personal-llm-box.git
cd personal-llm-box

# 2. Start all services
docker compose up --build -d

# 3. Pull the LLM model (first run only, ~5 GB)
docker exec ollama ollama pull qwen3:8b

# 4. Open the chat UI
open http://localhost:3000

# 5. Use the API
open http://localhost:8000/docs
```

## API endpoints

### `POST /artifact/save`
Save a titled markdown artifact with tags.
```json
{
  "title": "My note",
  "content": "Full content here.",
  "tags": ["research", "ai"]
}
```
Response: `{"status": "saved", "filename": "2024-01-15-my-note.md"}`

---

### `POST /ingest`
Ingest raw text, split into paragraph chunks and save.
```json
{ "text": "Long text to ingest..." }
```
Response: `{"status": "ingested", "filename": "...", "chunks": 3}`

---

### `GET /search?q=<query>`
Full-text search over all saved markdown files.

Response:
```json
{
  "query": "ai",
  "results": [
    {"filename": "2024-01-15-my-note.md", "snippet": "...matching line..."}
  ]
}
```

---

### `POST /digest`
Send text to the LLM and receive a structured analysis.
```json
{ "text": "Article or note to analyse." }
```
Response:
```json
{
  "summary": "...",
  "signals": ["signal 1", "signal 2"],
  "actions": ["action 1"]
}
```

---

### `GET /health`
Returns `{"status": "ok"}`.

## File tree

```
.
├── app/
│   ├── main.py              # FastAPI app
│   ├── routes/
│   │   ├── artifact.py      # POST /artifact/save
│   │   ├── knowledge.py     # POST /ingest
│   │   ├── search.py        # GET  /search
│   │   └── digest.py        # POST /digest
│   ├── services/
│   │   ├── ollama.py        # generate_text() wrapper
│   │   └── storage.py       # Markdown save + git commit
│   └── utils/
│       └── markdown.py      # Text chunking
├── knowledge/               # Mounted volume; git-tracked notes
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Environment variables (backend)

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_URL` | `http://ollama:11434` | Ollama API base URL |
| `OLLAMA_MODEL` | `qwen3:8b` | Model name |
| `KNOWLEDGE_DIR` | `/knowledge` | Path to knowledge folder inside container |
