.DEFAULT_GOAL := help

-include .env
export WEBUI_TOKEN

# ── Python ────────────────────────────────────────────────────────────────────

pip-install: ## Install Python dependencies
	pip install -r requirements.txt

pip-install-eval: ## Install evaluation dependencies
	pip install -r evaluation/requirements.txt

# ── Docker ────────────────────────────────────────────────────────────────────

up: ## Start all services
	docker compose up -d

build: ## Rebuild and start backend
	docker compose up -d --build backend

down: ## Stop all services
	docker compose down

logs: ## Tail backend logs
	docker compose logs -f backend

restart: ## Restart backend container
	docker compose restart backend

# ── Ollama ────────────────────────────────────────────────────────────────────

update-webui: ## Pin Open WebUI to latest release and recreate container
	$(eval VERSION := $(shell curl -s https://api.github.com/repos/open-webui/open-webui/releases/latest | grep '"tag_name"' | cut -d'"' -f4))
	@echo "Updating Open WebUI to $(VERSION)"
	sed -i 's|ghcr.io/open-webui/open-webui:.*|ghcr.io/open-webui/open-webui:$(VERSION)|' docker-compose.yml
	docker compose pull open-webui
	docker compose up -d open-webui

pull-model: ## Pull the default LLM model
	docker exec personal-ai-box-backend sh -c 'ollama pull $$OLLAMA_MODEL' 2>/dev/null || \
	ollama pull $$(grep OLLAMA_MODEL docker-compose.yml | head -1 | cut -d= -f2)

# ── API smoke tests ───────────────────────────────────────────────────────────

health: ## Check API health
	curl -s http://localhost:8000/health | python3 -m json.tool

search: ## Search knowledge base (usage: make search Q="your query")
	curl -s "http://localhost:8000/search?q=$(Q)" | python3 -m json.tool

# ── Evaluation ────────────────────────────────────────────────────────────────

eval: ## Run multi_query evaluation (default)
	python evaluation/evaluate.py --strategy multi_query

eval-vector: ## Run vector_search evaluation
	python evaluation/evaluate.py --strategy vector_search

eval-all: ## Run all strategies and compare
	python evaluation/evaluate.py --strategy all --output evaluation/results/latest-comparison.json

eval-hard: ## Run multi_query on hard questions
	python evaluation/evaluate.py --strategy multi_query --questions evaluation/data/questions-hard.json

# ── Knowledge ─────────────────────────────────────────────────────────────────

knowledge-log: ## Show git log of knowledge base
	git -C knowledge log --oneline -20

knowledge-count: ## Count knowledge files
	@ls knowledge/*.md 2>/dev/null | wc -l | xargs echo "knowledge files:"

sync-docs: ## Sync docs/ into Open WebUI "Project Docs" KB (requires WEBUI_TOKEN)
	@test -n "$(WEBUI_TOKEN)" || (echo "Error: WEBUI_TOKEN is not set."; exit 1)
	python scripts/sync_knowledge.py --url http://localhost:3000 --token $(WEBUI_TOKEN) --kb-name "Project Docs" --dir docs

sync-knowledge: ## Sync knowledge/ into Open WebUI (requires WEBUI_TOKEN env var)
	@test -n "$(WEBUI_TOKEN)" || (echo "Error: WEBUI_TOKEN is not set. Export it first: export WEBUI_TOKEN=<your-api-token>"; exit 1)
	python scripts/sync_knowledge.py --url http://localhost:3000 --token $(WEBUI_TOKEN)

sync-knowledge-dry: ## Dry run: show what would be synced (requires WEBUI_TOKEN)
	@test -n "$(WEBUI_TOKEN)" || (echo "Error: WEBUI_TOKEN is not set. Export it first: export WEBUI_TOKEN=<your-api-token>"; exit 1)
	python scripts/sync_knowledge.py --url http://localhost:3000 --token $(WEBUI_TOKEN) --dry-run

# ── Help ──────────────────────────────────────────────────────────────────────

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*##' Makefile | \
		awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'
