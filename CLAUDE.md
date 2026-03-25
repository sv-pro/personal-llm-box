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
│   ├── main.py             # App entry point, router registration, CORS, static files
│   ├── routes/             # One file per endpoint group
│   │   ├── artifact.py     # POST /artifact/save
│   │   ├── knowledge.py    # POST /ingest
│   │   ├── search.py       # GET /search
│   │   ├── digest.py       # POST /digest
│   │   └── catalogue.py    # GET /catalogue (list all files)
│   ├── services/           # Business logic (no HTTP concerns)
│   │   ├── ollama.py       # Ollama API wrapper
│   │   └── storage.py      # Git-backed markdown file storage
│   └── utils/
│       └── markdown.py     # Text chunking (split on double newlines)
├── web-ui/                 # Web interface (served at /web)
│   ├── index.html          # Single-page app with 5 tabs
│   └── README.md           # Web UI technical docs
├── examples/               # Usage examples (shell scripts, Python)
│   ├── README.md           # Examples documentation
│   ├── save_daily_notes.sh
│   ├── analyze_meeting.py
│   ├── search_knowledge.sh
│   └── web_clipper.sh
├── knowledge/              # Volume-mounted markdown knowledge store
├── docker-compose.yml      # Services: ollama/open-webui/backend (or native Ollama)
├── Dockerfile              # Python 3.12-slim + git + uvicorn
├── setup.sh                # Smart setup script (detects native Ollama, recommends models)
├── requirements.txt        # fastapi, uvicorn, requests, pydantic
├── README.md               # End-user documentation
├── QUICKSTART.md           # Quick start guide
├── WEB_UI_GUIDE.md         # Web UI user guide
├── CATALOGUE_FEATURE.md    # Catalogue feature documentation
├── VERIFICATION_PLAN.md    # Testing procedures
└── VERIFICATION_RESULTS.md # Test results
```

---

## Architecture

```
[Web UI :8000/web] ────┐
                       ▼
[Open WebUI :3000] ──► [Ollama :11434] ◄──┐
                              ▲            │
[FastAPI Backend :8000] ──────┘            │
        │                                  │
        ▼                                  │
[./knowledge/] (markdown files, git-tracked)
        │
        └─► [Native Ollama :11434] (optional, via setup.sh)
```

**Services:**
- **backend** (port 8000) — FastAPI app with REST API + static web UI
- **open-webui** (port 3000) — Chat interface (optional)
- **ollama** — Either Docker container OR native systemd service (auto-detected by setup.sh)

**Smart Setup:**
- Run `./setup.sh` to auto-detect native Ollama or configure Docker Ollama
- Script analyzes system resources (RAM, GPU VRAM) and recommends optimal model
- Generates appropriate `docker-compose.yml` (native Ollama or Docker Ollama)

The `knowledge/` directory is bind-mounted into the backend container at `/knowledge`. The backend auto-initialises it as a git repo and commits every save.

---

## API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/health` | Health check → `{"status": "ok"}` |
| `GET` | `/web/` | Web UI (modern interface for all features) |
| `GET` | `/catalogue` | List all knowledge files with metadata |
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

**GET /catalogue**
```json
{
  "files": [{
    "filename": "...",
    "title": "...",
    "tags": ["..."],
    "created_at": "...",
    "preview": "...",
    "size": 1234,
    "modified": "..."
  }],
  "total": 1
}
```

---

## Search Implementation

### Current: Simple Full-Text Search (main branch)

**File:** `app/routes/search.py`

The current search is a **simple grep-style full-text search**:
- Reads all markdown files sequentially
- Case-insensitive substring matching
- Returns filename + first 3 matching lines as snippet
- Fast for small-medium knowledge bases (<1000 files)
- No indexing, no ranking, no fuzzy matching

**Time complexity:** O(n × m) where n = files, m = avg file size
**Performance:** ~50ms for 100 files, ~500ms for 1000 files

**Limitations:**
- No fuzzy matching (typos won't match)
- No relevance ranking
- No phrase search
- No boolean operators (AND/OR/NOT)
- Linear scan (slower with thousands of files)

### Future: Experimental Retrieval Techniques

To experiment with advanced retrieval without cluttering the main branch:

**Branch strategy:** `experiments/retrieval` is the parent branch for all retrieval experiments.

Create sub-branches off `experiments/retrieval` for specific experiments:
- `experiments/retrieval/vector-search` — Vector embeddings with semantic search
- `experiments/retrieval/fts5` — SQLite FTS5 full-text search
- `experiments/retrieval/whoosh` — Whoosh/Tantivy indexing
- `experiments/retrieval/hybrid` — Combine multiple techniques

**Merge path:**
```
experiments/retrieval/<technique> → experiments/retrieval → main
```

**Guidelines:**
1. **Keep `main` stable** — Simple grep search, proven and working
2. **Branch from `experiments/retrieval`** — Not from main
3. **Document everything** — Create `EXPERIMENTS.md` in branch with results
4. **Compare objectively** — Benchmark speed, accuracy, resource usage
5. **Merge only when proven** — Test thoroughly before merging to main

**Experiment structure:**
```
experiments/retrieval/vector-search/
├── app/services/vector_search.py    # New search implementation
├── app/routes/search_v2.py           # New endpoint (or replace old)
├── requirements-experiment.txt       # Additional dependencies
├── EXPERIMENT.md                     # Results, benchmarks, findings
└── tests/                            # Experiment-specific tests
```

**When to merge to main:**
- Performance is equal or better
- Code quality is maintained
- Dependencies are acceptable (size, licensing)
- Documentation is complete
- Tests pass
- User experience is improved

**Potential retrieval experiments:**

1. **Vector Search** (semantic similarity)
   - Use sentence-transformers or similar
   - Embed documents on save, search by similarity
   - Pros: semantic matching, finds related content
   - Cons: requires embeddings model, more storage, slower indexing

2. **SQLite FTS5** (fast full-text search)
   - Index content in SQLite with FTS5
   - Fast phrase search, ranking, highlights
   - Pros: built-in to Python, fast, battle-tested
   - Cons: needs index maintenance, separate from markdown files

3. **Whoosh/Tantivy** (pure-Python indexing)
   - Create search index on disk
   - Support complex queries, facets, highlighting
   - Pros: powerful query language, fast
   - Cons: index size, maintenance overhead

4. **Hybrid Search** (combine techniques)
   - Use FTS for exact matches + vectors for semantic
   - Re-rank results with LLM
   - Pros: best of both worlds
   - Cons: complex, resource-intensive

5. **Graph-based** (knowledge graph)
   - Build connections between documents
   - Traverse relationships, find patterns
   - Pros: discover non-obvious connections
   - Cons: complex to implement, needs maintenance

**Benchmarking template:**
```markdown
## Experiment: <Name>

### Setup
- Branch: experiments/retrieval/<name>
- Dependencies: <list>
- Storage overhead: <size>

### Performance
- Indexing time: <time>
- Query time: <time>
- Memory usage: <size>

### Accuracy
- Precision: <%>
- Recall: <%>
- F1 Score: <%>

### User Experience
- Setup complexity: <1-5>
- Query complexity: <1-5>
- Result quality: <1-5>

### Recommendation
- Merge to main: YES/NO
- Reason: <why>
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

1. **`app/main.py`** — understand how routers are wired together, CORS setup, web UI mounting
2. **`app/services/storage.py`** — the core persistence layer (git + markdown + YAML)
3. **`app/routes/search.py`** — current simple search implementation (20 lines)
4. **`app/routes/catalogue.py`** — file listing with metadata parsing
5. **`app/routes/digest.py`** — most complex route (LLM + JSON parsing)
6. **`web-ui/index.html`** — single-page web interface (all tabs in one file)
7. **`setup.sh`** — smart configuration script (Ollama detection, model recommendation)
8. **`docker-compose.yml`** — service topology (generated by setup.sh or manual)

---

## Web Interface

**Access:** http://localhost:8000/web/

The web UI is a single-page application with 5 tabs:

1. **📚 Catalogue** (default) — Browse all knowledge files
   - Filter by tag, sort by date/title
   - Shows stats (total items, tags, size)
   - Preview content, click to view (future: full viewer)

2. **🔍 Search** — Full-text keyword search
   - Real-time search as you type
   - Shows matching files with snippets
   - Highlights where term appears

3. **💾 Save Artifact** — Create structured documents
   - Add title, content, tags
   - Auto-saves with YAML frontmatter
   - Git auto-commit on save

4. **📥 Ingest Text** — Import long-form content
   - Paste articles, emails, documents
   - Auto-chunks by paragraphs
   - Saves with timestamp

5. **🤖 AI Digest** — LLM-powered analysis
   - Paste text to analyze
   - Get summary, signals, actions
   - 5-10 second processing time

**Features:**
- Live API status indicator
- Responsive design (mobile-friendly)
- Auto-refresh catalogue on saves
- No authentication (local-first)
- Vanilla JS (no frameworks)

**Technical:**
- Single HTML file at `web-ui/index.html`
- Served via FastAPI StaticFiles at `/web`
- Uses Fetch API for backend communication
- CORS enabled for all origins
