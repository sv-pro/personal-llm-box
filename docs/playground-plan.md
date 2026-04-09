# Playground Plan

Experiments with repos from [inspiration.md](inspiration.md), organised by theme.
Each experiment targets a specific capability gap in **personal-llm-box** and describes
what to try, what to measure, and what a successful outcome looks like.

---

## 1 — Smarter Retrieval (replace naive full-text search)

### 1.1 PageIndex — vectorless, reasoning-based RAG

| | |
|---|---|
| **Repo** | [VectifyAI/PageIndex](https://github.com/VectifyAI/PageIndex) |
| **Goal** | Replace the current `GET /search` grep-style lookup with page-level index + LLM reasoning |
| **Experiment** | Ingest 50+ knowledge files, build a PageIndex over them, and compare recall/precision against the existing substring search on a fixed set of 20 queries |
| **Success** | Measurably better answers on multi-hop questions without adding a vector DB |

### 1.2 OpenSPG — knowledge graph layer

| | |
|---|---|
| **Repo** | [OpenSPG/openspg](https://github.com/OpenSPG/openspg) |
| **Goal** | Model entities and relations extracted from knowledge files as a semantic graph |
| **Experiment** | Run OpenSPG locally, feed it the output of `/ingest`, query it with SPARQL-style questions, compare to flat search |
| **Success** | Ability to answer relationship queries ("which signals mention company X?") that flat search cannot |

---

## 2 — Memory & Context for Agents

### 2.1 cognee — knowledge engine for agent memory

| | |
|---|---|
| **Repo** | [topoteretes/cognee](https://github.com/topoteretes/cognee) |
| **Goal** | Give the `/digest` pipeline a persistent memory so repeated analyses build on prior context |
| **Experiment** | Wire cognee as a memory backend, run 10 sequential digest calls on related articles, check whether later summaries reference earlier insights |
| **Success** | Digest output improves over a session; the agent "remembers" past analyses |

### 2.2 memvid — single-file memory layer

| | |
|---|---|
| **Repo** | [memvid/memvid](https://github.com/memvid/memvid) |
| **Goal** | Evaluate memvid as a lightweight, serverless alternative to a full vector store for knowledge retrieval |
| **Experiment** | Export all knowledge files into a memvid archive, run the same 20-query benchmark from §1.1, compare latency and accuracy |
| **Success** | Comparable recall to PageIndex with simpler deployment (single file, no extra service) |

### 2.3 supermemory — memory API

| | |
|---|---|
| **Repo** | [supermemoryai/supermemory](https://github.com/supermemoryai/supermemory) |
| **Goal** | Test supermemory as a fast, scalable memory backend behind the `/search` endpoint |
| **Experiment** | Spin up supermemory locally, index all knowledge files, expose a `/search-v2` endpoint that queries it, benchmark response times vs current search |
| **Success** | Sub-100 ms search over 1000+ documents with ranking quality at least on par with current grep |

### 2.4 memU — proactive agent memory

| | |
|---|---|
| **Repo** | [NevaMind-AI/memU](https://github.com/NevaMind-AI/memU) |
| **Goal** | Explore proactive memory: the system surfaces relevant past knowledge *before* the user asks |
| **Experiment** | Integrate memU alongside the `/ingest` pipeline; after each ingest, check if memU auto-surfaces related prior notes |
| **Success** | On ingest of a new article, the system returns ≥1 relevant prior note without an explicit search query |

### 2.5 agentic-context-engine — learning from experience

| | |
|---|---|
| **Repo** | [kayba-ai/agentic-context-engine](https://github.com/kayba-ai/agentic-context-engine) |
| **Goal** | Let the digest agent learn from user feedback over time |
| **Experiment** | Add a `/digest/feedback` endpoint that records thumbs-up/down; feed that into agentic-context-engine; measure whether digest quality improves after 20 feedback cycles |
| **Success** | Average user rating increases between the first and last 5 digests |

---

## 3 — Agent Frameworks & Orchestration

### 3.1 Qwen-Agent — function calling, MCP, RAG

| | |
|---|---|
| **Repo** | [QwenLM/Qwen-Agent](https://github.com/QwenLM/Qwen-Agent) |
| **Goal** | Wrap the existing FastAPI endpoints as Qwen-Agent tools so a Qwen model can orchestrate multi-step knowledge workflows |
| **Experiment** | Define tools for `save`, `ingest`, `search`, `digest`; ask the agent "research topic X, save findings, then digest them"; verify the full pipeline executes end-to-end |
| **Success** | A single natural-language prompt triggers ingest → search → digest → artifact save automatically |

### 3.2 openclaw — personal AI assistant

| | |
|---|---|
| **Repo** | [openclaw/openclaw](https://github.com/openclaw/openclaw) |
| **Goal** | Evaluate openclaw as a front-end alternative to Open WebUI, with deeper integration into the knowledge API |
| **Experiment** | Run openclaw alongside the existing stack, connect it to the FastAPI backend, compare UX for knowledge search and artifact management |
| **Success** | A working openclaw setup that can call `/search` and `/artifact/save` from the chat interface |

### 3.3 ACE — agentic context engineering

| | |
|---|---|
| **Repo** | [ace-agent/ace](https://github.com/ace-agent/ace) |
| **Goal** | Use ACE's context-engineering approach to dynamically select which knowledge files to include in the LLM prompt |
| **Experiment** | Integrate ACE between `/digest` and Ollama; compare token usage and output quality vs. the current "send everything" approach on 10 long documents |
| **Success** | ≥30% reduction in prompt tokens with no loss in digest quality |

---

## 4 — Deep Research & Structured Extraction

### 4.1 MiroThinker — deep research agent

| | |
|---|---|
| **Repo** | [MiroMindAI/MiroThinker](https://github.com/MiroMindAI/MiroThinker) |
| **Goal** | Add a `/research` endpoint that performs multi-step web research and stores results as artifacts |
| **Experiment** | Give MiroThinker a topic, let it browse and reason, pipe its output through `/ingest` and `/digest`, review final artifact quality |
| **Success** | A single API call produces a well-sourced research artifact saved in the knowledge folder |

### 4.2 langextract — structured extraction from text

| | |
|---|---|
| **Repo** | [google/langextract](https://github.com/google/langextract) |
| **Goal** | Extract structured entities (people, dates, claims) from ingested text and store them as metadata |
| **Experiment** | Run langextract over 20 knowledge files, add extracted entities to YAML frontmatter, verify they improve `/search` results |
| **Success** | Search for an entity name returns the correct files even when the name appears only in the extracted metadata |

---

## 5 — Knowledge Management UX

### 5.1 logseq — graph-based knowledge UI

| | |
|---|---|
| **Repo** | [logseq/logseq](https://github.com/logseq/logseq) |
| **Goal** | Use logseq as a read/write UI over the `knowledge/` folder |
| **Experiment** | Point logseq at the knowledge directory, verify bi-directional sync (edits in logseq appear in git, API-saved files appear in logseq) |
| **Success** | A single knowledge folder is editable from both the API and logseq without conflicts |

### 5.2 Personal AI Infrastructure — architecture patterns

| | |
|---|---|
| **Repo** | [danielmiessler/Personal_AI_Infrastructure](https://github.com/danielmiessler/Personal_AI_Infrastructure) |
| **Goal** | Audit personal-llm-box against the design principles in this repo; identify missing layers |
| **Experiment** | Map current components to the Personal AI Infrastructure reference architecture, document gaps, prioritise the top 3 improvements |
| **Success** | A written gap analysis with concrete next steps (candidates for further experiments) |

---

## 6 — Context Management

### 6.1 OpenViking — unified context database

| | |
|---|---|
| **Repo** | [volcengine/OpenViking](https://github.com/volcengine/OpenViking) |
| **Goal** | Unify memory, resources, and skills under a file-system paradigm that aligns with the existing `knowledge/` directory |
| **Experiment** | Run OpenViking, mirror the knowledge folder into it, test hierarchical context delivery when prompting the LLM |
| **Success** | LLM receives a well-scoped context window assembled by OpenViking instead of a flat file dump |

---

## 7 — Security

### 7.1 camel-prompt-injection — prompt injection defence

| | |
|---|---|
| **Repo** | [google-research/camel-prompt-injection](https://github.com/google-research/camel-prompt-injection) |
| **Goal** | Harden the `/digest` endpoint against adversarial inputs that try to hijack the LLM prompt |
| **Experiment** | Build a test suite of 30 prompt-injection payloads, run them against `/digest` before and after applying CAMEL-style defences, measure bypass rate |
| **Success** | Bypass rate drops to <10% with no degradation on benign inputs |

---

## Suggested Experiment Order

| Priority | Experiment | Rationale |
|----------|-----------|-----------|
| 1 | §1.1 PageIndex | Directly improves the weakest current feature (search) |
| 2 | §2.2 memvid | Low-effort memory upgrade, no extra services |
| 3 | §4.2 langextract | Enriches existing data, compounds with better search |
| 4 | §2.1 cognee | Adds session memory to digest, high user-visible impact |
| 5 | §3.1 Qwen-Agent | Unlocks multi-step workflows, biggest capability leap |
| 6 | §7.1 camel-prompt-injection | Security hardening before opening to wider use |
| 7 | §5.1 logseq | Better UX for manual knowledge curation |
| 8 | §5.2 Personal AI Infra | Strategic review to guide long-term roadmap |
| 9 | §1.2 OpenSPG | Advanced graph queries, higher setup cost |
| 10 | §4.1 MiroThinker | New capability (research), depends on stable core |
| 11 | §6.1 OpenViking | Context management, valuable after agent layer exists |
| 12 | §3.2 openclaw | Alternative UI, lower priority than API improvements |
| 13 | §3.3 ACE | Optimisation, most useful at scale |
| 14 | §2.3 supermemory | Scaling play, relevant when document count grows |
| 15 | §2.4 memU | Proactive memory, experimental |
| 16 | §2.5 agentic-context-engine | Feedback loop, requires user traffic first |
