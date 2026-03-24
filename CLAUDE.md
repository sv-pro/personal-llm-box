# CLAUDE.md — AI Assistant Guide for personal-llm-box

## Project Overview

**personal-llm-box** is a minimal, self-hosted AI system that combines a local LLM backend (Ollama), a chat UI (Open WebUI), and a custom FastAPI knowledge management API. Everything runs via Docker Compose with no external API dependencies.

### Core Purpose
- Store and search a personal knowledge base (markdown files, git-tracked)
- Ingest text and chunk it into searchable paragraphs
- Use a local LLM to digest/analyze text (summary, signals, actions)
- Preserve titled artifacts with tags and metadata

---

## Repository Structure

```
personal-llm-box/
├── app/                    # FastAPI application
│   ├── main.py             # App entry point, router registration, /health endpoint
│   ├── routes/             # One file per endpoint group
│   │   ├── artifact.py     # POST /artifact/save
│   │   ├── knowledge.py    # POST /ingest
│   │   ├── search.py       # GET /search
│   │   └── digest.py       # POST /digest
│   ├── services/           # Business logic (no HTTP concerns)
│   │   ├── ollama.py       # Ollama API wrapper
│   │   └── storage.py      # Git-backed markdown file storage
│   └── utils/
│       └── markdown.py     # Text chunking (split on double newlines)
├── knowledge/              # Volume-mounted markdown knowledge store (.gitkeep)
├── docker-compose.yml      # Three services: ollama, open-webui, backend
├── Dockerfile              # Python 3.12-slim + git + uvicorn
├── requirements.txt        # fastapi, uvicorn, requests, pydantic
└── README.md               # End-user documentation
```

---

## Architecture

```
[Open WebUI :3000] ──► [Ollama :11434]
                              ▲
[FastAPI Backend :8000] ──────┘
        │
        ▼
[./knowledge/] (markdown files, git-tracked)
```

Three Docker services:
- **ollama** — serves the local LLM (default model: `qwen3:8b`)
- **open-webui** — chat interface (port 3000)
- **backend** — custom FastAPI app (port 8000)

The `knowledge/` directory is bind-mounted into the backend container at `/knowledge`. The backend auto-initialises it as a git repo and commits every save.

---

## API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/health` | Health check → `{"status": "ok"}` |
| `POST` | `/artifact/save` | Save a titled markdown artifact |
| `POST` | `/ingest` | Chunk text into paragraphs and save |
| `GET` | `/search?q=...` | Full-text search across knowledge files |
| `POST` | `/digest` | LLM analysis: summary + signals + actions |

### Request/Response shapes

**POST /artifact/save**
```json
// request
{ "title": "...", "content": "...", "tags": ["tag1"] }
// response
{ "status": "saved", "filename": "YYYY-MM-DD-slug.md" }
```

**POST /ingest**
```json
// request
{ "text": "long text..." }
// response
{ "status": "ingested", "filename": "YYYY-MM-DD-HHMMSSffffff.md", "chunks": 4 }
```

**GET /search?q=query**
```json
{ "query": "query", "results": [{ "filename": "...", "snippet": "..." }] }
```

**POST /digest**
```json
// request
{ "text": "..." }
// response
{ "summary": "...", "signals": ["..."], "actions": ["..."] }
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_URL` | `http://ollama:11434` | Ollama API base URL |
| `OLLAMA_MODEL` | `qwen3:8b` | LLM model identifier |
| `KNOWLEDGE_DIR` | `/knowledge` | Path to knowledge directory |

Set via `environment:` in `docker-compose.yml` or a local `.env` file.

---

## Development Conventions

### Language & Framework
- **Python 3.12**, **FastAPI 0.115**, **Pydantic v2**, **uvicorn**
- No database — file-based storage only (markdown + YAML frontmatter + git)

### Code Style
- Snake_case for all functions and variables
- Each route group lives in its own file under `app/routes/`
- Services contain pure business logic with no HTTP/FastAPI imports
- Use `os.getenv("VAR", "default")` for configuration
- Minimal type hints — use them on function signatures, not everywhere
- No docstrings required; favour descriptive names instead

### File Storage Conventions
Markdown files written by `storage.py` follow this format:

```markdown
---
title: "My Title"
tags: ["tag1", "tag2"]
created_at: 2024-01-15T10:30:00+00:00
---

Content here...
```

Filenames use date-based slugs: `YYYY-MM-DD-<title-slug>.md` for artifacts, `YYYY-MM-DD-HHMMSSffffff.md` for ingested chunks.

Every save triggers a `git add -A && git commit` inside the container (git is installed in the image for this purpose).

### Adding a New Endpoint
1. Create `app/routes/<name>.py` with an `APIRouter`
2. Add business logic to a new or existing file in `app/services/`
3. Register the router in `app/main.py` with `app.include_router(...)`

### LLM Integration
`app/services/ollama.py` wraps the Ollama `/api/generate` endpoint. The `digest` route expects the LLM to return valid JSON; it falls back to raw text if JSON parsing fails. When modifying prompts in `digest.py`, keep the JSON schema (`summary`, `signals`, `actions`) stable.

---

## Running Locally

```bash
# Start all services
docker compose up -d

# Pull the default model (first run only)
docker exec personal-llm-box-ollama-1 ollama pull qwen3:8b

# View backend logs
docker compose logs -f backend

# Rebuild after code changes
docker compose up -d --build backend
```

The backend auto-reloads are **not** enabled in the Dockerfile — rebuild the image after changes.

---

## No Tests / No CI

There are currently no automated tests and no CI/CD pipelines. When adding tests:
- Use **pytest** (add to `requirements.txt`)
- Place tests in `tests/` at the repo root
- Mock `ollama.py` and `storage.py` in route tests to avoid side effects

---

## Key Files to Read First

When exploring or modifying the codebase, start with:

1. `app/main.py` — understand how routers are wired together
2. `app/services/storage.py` — the core persistence layer
3. `app/routes/digest.py` — most complex route (LLM + JSON parsing)
4. `docker-compose.yml` — service topology and volume mounts
