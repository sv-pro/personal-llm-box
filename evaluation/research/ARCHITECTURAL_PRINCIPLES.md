# Architectural Principles: Constraints That Guide Design

## Principle 1: The Lobotomy Test (Graceful Degradation)

### Definition

**The Lobotomy Test:** The system should remain useful even when all smart components (search, LLM, reasoning) fail.

**Metaphor:** If you lobotomize the AI components, the knowledge should still be accessible to humans.

### Requirements

**Must survive:**
- LLM failure (Ollama crashes, API key expired)
- Search failure (indexing broken, database corrupted)
- Reasoning failure (logic engine bugs)
- Complete system failure (power outage, decades later)

**Human accessibility:**
- Knowledge readable without specialized tools
- Structure understandable without documentation
- Self-documenting (metadata explains itself)
- Future-proof (uses open formats)

### Current State: PASSES ✓

```
knowledge/
└── 2026-01-22-auth-memory-leak-investigation.md

File contents:
---
title: "Auth Memory Leak Investigation"
tags: ["debugging", "authentication"]
created_at: 2026-01-22T09:15:00+00:00
---

# Memory Leak Investigation - Authentication Service

**Issue:** Memory consumption grows unbounded...

## Root Cause
The TokenCache class...
```

**Human can:**
- ✓ Open file in text editor
- ✓ Read markdown
- ✓ Understand YAML frontmatter
- ✓ Navigate by filename dates
- ✓ Grep for keywords
- ✓ Use git history

**No tools required:** Works with basic text editor + file browser.

### What FAILS the Lobotomy Test

**❌ Binary graph databases**
```
knowledge.db (Neo4j, SQLite binary)
```
- Cannot read without database software
- Structure opaque to humans
- Requires running database to access
- If DB corrupts, knowledge lost

**❌ Opaque vector embeddings**
```
embeddings/
├── doc1.npy  # 384-dimensional vector
├── doc2.npy  # Meaningless to humans
└── index.faiss
```
- Embeddings are not human-readable
- Cannot infer content from vectors
- Requires model to decode

**❌ Proprietary formats**
```
knowledge.notion  # Notion export
knowledge.roam    # Roam Research
```
- Vendor lock-in
- May become unsupported
- Not future-proof

**❌ Complex schemas requiring tools**
```json
{
  "nodes": [{"id": "n1", "type": "entity", "props": {...}}],
  "edges": [{"from": "n1", "to": "n2", "rel": "causes"}]
}
```
- Structure not self-evident
- Requires visualization tool
- Hard to edit manually

### Design Constraints from Lobotomy Test

**✓ Allowed:**
- Plain markdown files
- Human-readable YAML frontmatter
- Directory hierarchies (filesystem structure)
- Git for version control
- Text-based formats (JSON, YAML, CSV)

**✗ Forbidden (as primary storage):**
- Binary databases (can use as index, not source of truth)
- Opaque embeddings (can cache, but docs are source)
- Proprietary formats
- Anything requiring specialized software to read

**✓ Acceptable (as auxiliary):**
- SQLite index (regenerable from markdown)
- Vector embeddings (regenerable from markdown)
- Graph database (regenerable from markdown)

**Key:** Source of truth = human-readable. Indexes = regenerable.

### Implementation Pattern: Regenerable Indexes

```
knowledge/           ← Source of truth (markdown)
    ├── doc1.md
    └── doc2.md

.indexes/           ← Generated indexes (can delete)
    ├── vectors.faiss     (regenerated from markdown)
    ├── graph.db          (regenerated from markdown)
    └── fulltext.db       (regenerated from markdown)

.indexes/.gitignore  ← Indexes not tracked in git
```

**Regeneration script:**
```bash
# Delete all indexes
rm -rf .indexes/

# Rebuild from markdown
python build_indexes.py

# System fully functional again
```

**Lobotomy scenario:**
```bash
# All tooling broken
rm -rf .indexes/
rm -rf venv/
uninstall ollama

# Knowledge still accessible:
cat knowledge/*.md  # Read with basic tools
ls knowledge/       # Navigate by filename
grep "memory leak" knowledge/*  # Basic search
git log --follow knowledge/doc.md  # History
```

---

## Principle 2: Model-Knowledge Decoupling via MCP

### Definition

**Model-Knowledge Decoupling:** The retrieval/reasoning layer should be accessible via MCP (Model Context Protocol), keeping the model loosely coupled from knowledge access.

### Why MCP?

**Model Context Protocol (MCP)** is a standardized way for LLMs to call external tools. It enables:

**Tool definition:**
```json
{
  "name": "search_knowledge",
  "description": "Search personal knowledge base",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {"type": "string"},
      "max_results": {"type": "integer"}
    }
  }
}
```

**Tool execution:**
```python
# Model calls tool
result = search_knowledge(query="memory leak", max_results=5)

# Model receives result
# Model reasons over result
# Model generates answer
```

### Architecture

```
┌─────────────────────────────────────────────┐
│                                             │
│  Model Layer (Swappable)                    │
│  ┌─────────────┐  ┌─────────────┐          │
│  │ Ollama      │  │ Claude API  │  ...     │
│  │ llama3.2    │  │ opus-4.5    │          │
│  └─────────────┘  └─────────────┘          │
│         │                │                  │
│         └────────┬───────┘                  │
│                  │                          │
│              MCP Interface                  │
│                  │                          │
└──────────────────┼──────────────────────────┘
                   │
┌──────────────────┼──────────────────────────┐
│                  │                          │
│  Knowledge Layer (Model-agnostic)           │
│                  │                          │
│  ┌───────────────▼────────────────┐         │
│  │  MCP Tools                     │         │
│  │  ┌──────────────────────────┐  │         │
│  │  │ search_knowledge()       │  │         │
│  │  │ get_related_docs()       │  │         │
│  │  │ query_temporal()         │  │         │
│  │  │ traverse_graph()         │  │         │
│  │  │ calculate()              │  │         │
│  │  └──────────────────────────┘  │         │
│  └────────────────┬────────────────┘         │
│                   │                          │
│  ┌────────────────▼────────────────┐         │
│  │  Storage                        │         │
│  │  - Markdown files               │         │
│  │  - Frontmatter metadata         │         │
│  │  - Regenerable indexes          │         │
│  └─────────────────────────────────┘         │
│                                             │
└─────────────────────────────────────────────┘
```

### Benefits

**1. Swappable Models**

Test different models without changing knowledge layer:

```python
# Test with local model
model = OllamaModel("llama3.2:latest")
answer = model.answer_with_tools(question, mcp_tools)

# Test with cloud model
model = ClaudeModel("claude-opus-4.5")
answer = model.answer_with_tools(question, mcp_tools)

# Compare results
```

**2. Measure Model Contribution**

A/B test: Model with tools vs model without tools

```python
# Baseline: Model only (no tools)
answer_baseline = model.generate(f"Answer: {question}")

# With tools: Model + MCP tools
answer_with_tools = model.answer_with_tools(question, mcp_tools)

# Compare
baseline_accuracy = evaluate(answer_baseline)
tools_accuracy = evaluate(answer_with_tools)

contribution = tools_accuracy - baseline_accuracy
```

**This answers:** How much does the knowledge structure contribute vs raw model reasoning?

**3. Separation of Concerns**

**Knowledge layer responsibilities:**
- Storage (markdown)
- Indexing (vector, graph, fulltext)
- Retrieval (search, traverse, query)
- Structural reasoning (dates, calculations, graph queries)

**Model layer responsibilities:**
- Natural language understanding
- Semantic reasoning
- Synthesis
- Answer generation

**Clear boundary:** MCP tool interface

**4. Progressive Enhancement**

Start simple, add tools incrementally:

```python
# Phase 1: Basic search
mcp_tools = [
    search_knowledge,
]

# Phase 2: Add temporal queries
mcp_tools = [
    search_knowledge,
    query_by_date_range,
    get_events_timeline,
]

# Phase 3: Add graph traversal
mcp_tools = [
    search_knowledge,
    query_by_date_range,
    get_events_timeline,
    get_related_docs,
    traverse_causal_chain,
]

# Phase 4: Add logic
mcp_tools = [
    # ... all previous tools
    calculate,
    compare_dates,
    resolve_entity,
]
```

**Model doesn't change** - just gets more powerful tools.

### MCP Tool Design Principles

**1. Self-Contained**

Each tool does one thing well:

```python
@mcp_tool
def search_knowledge(query: str, max_results: int = 5) -> List[Document]:
    """Search knowledge base by keyword or semantic similarity.

    Args:
        query: Search query (natural language or keywords)
        max_results: Maximum number of results to return

    Returns:
        List of documents matching query, ranked by relevance
    """
    # Implementation
```

**2. Composable**

Tools can be chained:

```python
# Model can call tools in sequence:
# 1. Search for "memory leak"
docs = search_knowledge("memory leak")

# 2. Get timeline for found docs
timeline = get_events_timeline([d.id for d in docs])

# 3. Find who worked on these
people = get_entities_by_type(docs, entity_type="person")
```

**3. Deterministic (where possible)**

Logic tools should be deterministic:

```python
@mcp_tool
def compare_dates(date1: str, date2: str) -> str:
    """Compare two dates and return which is earlier.

    Deterministic: Same inputs always return same output.
    """
    d1 = parse_date(date1)
    d2 = parse_date(date2)
    if d1 < d2:
        return f"{date1} is earlier than {date2}"
    elif d1 > d2:
        return f"{date2} is earlier than {date1}"
    else:
        return f"{date1} and {date2} are the same"
```

**4. Observable**

Tools should return structured data that can be inspected:

```python
{
  "query": "memory leak",
  "results": [
    {
      "filename": "auth-memory-leak-investigation.md",
      "relevance_score": 0.95,
      "snippet": "Memory leak in TokenCache...",
      "metadata": {
        "date": "2026-01-22",
        "entities": ["Alex", "Auth Service"]
      }
    }
  ],
  "retrieval_method": "vector_search",
  "query_time_ms": 45
}
```

User can see what tool returned, verify correctness.

---

## Combined Principles: Architecture Constraints

### Constraint Matrix

| Component | Lobotomy Test | MCP Decoupling | Implication |
|-----------|---------------|----------------|-------------|
| **Source of Truth** | Must be human-readable | Model-agnostic format | → Markdown + YAML frontmatter |
| **Indexes** | Regenerable from source | Accessed via MCP tools | → SQLite/FAISS/Neo4j OK as cache |
| **Retrieval** | Fallback to basic tools (grep) | Exposed as MCP tools | → Tool interface, not direct DB access |
| **Reasoning** | Documents contain enough context | Logic in tools, not model | → Frontmatter has structured data |
| **Model** | Optional (can read without) | Swappable via MCP | → Model is consumer, not owner |

### Resulting Architecture

```
Storage Layer (Lobotomy-Safe)
├── knowledge/
│   ├── *.md           ← Human-readable source of truth
│   └── frontmatter    ← Structured metadata (YAML)
│
├── .indexes/ (Regenerable)
│   ├── vectors.faiss
│   ├── graph.db
│   └── fulltext.db
│
MCP Tool Layer (Model-Agnostic)
├── search_knowledge()
├── query_temporal()
├── traverse_graph()
├── calculate()
└── get_related()
│
Model Layer (Swappable)
└── Any model with MCP support
    ├── Ollama
    ├── Claude
    ├── GPT
    └── ...
```

### Design Decisions

**Decision 1: Primary storage format**

❌ Graph database (fails lobotomy test)
❌ Vector database (fails lobotomy test)
✓ **Markdown + YAML frontmatter** (passes both tests)

**Decision 2: Index storage**

✓ Graph database as index (regenerable)
✓ Vector database as index (regenerable)
✓ Fulltext database as index (regenerable)

**Requirement:** `rebuild_indexes.py` script must exist

**Decision 3: Tool interface**

❌ Direct database access from model
❌ Model-specific APIs
✓ **MCP tools** (standard, swappable)

**Decision 4: Reasoning location**

❌ All reasoning in model (can't measure contribution)
❌ All reasoning in tools (model becomes dumb)
✓ **Hybrid:** Structural reasoning in tools, semantic reasoning in model

---

## Testing Framework Extensions

### Test 1: Lobotomy Resilience

**Procedure:**
```bash
# Delete all tooling
rm -rf .indexes/
rm -rf venv/
pkill ollama

# Verify knowledge still accessible
cd knowledge/
cat *.md              # Can read documents? ✓
grep "memory leak" *  # Can search? ✓
git log              # Can see history? ✓
```

**Pass criteria:**
- All knowledge readable
- Basic navigation works
- No information loss

### Test 2: Model Swapping

**Procedure:**
```python
models = [
    OllamaModel("llama3.2:latest"),
    OllamaModel("qwen3:8b"),
    ClaudeAPI("claude-opus-4.5"),
]

for model in models:
    results = evaluate_model(model, questions=hard_questions, tools=mcp_tools)
    print(f"{model.name}: {results.f1_score}")
```

**Pass criteria:**
- All models can use same MCP tools
- No model-specific code in knowledge layer
- Results comparable

### Test 3: Tool Contribution

**Procedure:**
```python
# Test A: Model only (no tools)
results_no_tools = model.answer(questions, tools=[])

# Test B: Model + search tool
results_search = model.answer(questions, tools=[search_knowledge])

# Test C: Model + all tools
results_all_tools = model.answer(questions, tools=all_mcp_tools)

# Measure incremental contribution
print(f"No tools:     {results_no_tools.f1}")
print(f"Search only:  {results_search.f1}")
print(f"All tools:    {results_all_tools.f1}")

contribution_search = results_search.f1 - results_no_tools.f1
contribution_all = results_all_tools.f1 - results_no_tools.f1
```

**Pass criteria:**
- Can measure tool contribution
- Tools improve performance
- Can identify which tools help most

---

## Implementation Roadmap

### Phase 1: Lobotomy-Safe Foundation ✓ (Current)

- ✓ Markdown files
- ✓ YAML frontmatter
- ✓ Git versioning
- ✓ Human-readable

### Phase 2: Add Regenerable Indexes

```python
# Build indexes from markdown
def build_indexes():
    # Clear old indexes
    shutil.rmtree('.indexes/', ignore_errors=True)

    # Rebuild from source
    for doc in knowledge_dir.glob('*.md'):
        # Extract content and metadata
        content, metadata = parse_markdown(doc)

        # Index in vector DB
        embedding = embed(content)
        vector_db.add(doc.name, embedding)

        # Index in graph DB
        entities = metadata.get('entities', [])
        graph_db.add_doc(doc.name, entities)

        # Index in fulltext DB
        fulltext_db.add(doc.name, content)
```

### Phase 3: MCP Tool Layer

```python
@mcp_tool
def search_knowledge(query: str, max_results: int = 5):
    """Search knowledge base."""
    # Use indexes if available
    if vector_db.exists():
        results = vector_db.search(query, limit=max_results)
    else:
        # Fallback to basic search
        results = grep_search(query, limit=max_results)

    return [{"filename": r.filename, "snippet": r.snippet} for r in results]

@mcp_tool
def query_temporal(start_date: str, end_date: str):
    """Find documents in date range."""
    results = []
    for doc in knowledge_dir.glob('*.md'):
        metadata = parse_frontmatter(doc)
        doc_date = metadata.get('created_at')
        if start_date <= doc_date <= end_date:
            results.append(doc.name)
    return results

@mcp_tool
def get_related_docs(doc_name: str, max_hops: int = 1):
    """Get related documents via graph traversal."""
    if graph_db.exists():
        return graph_db.traverse(doc_name, max_hops)
    else:
        # Fallback: use frontmatter
        metadata = parse_frontmatter(doc_name)
        return metadata.get('related_docs', [])
```

### Phase 4: Model Integration

```python
# Configure model with MCP tools
model = OllamaModel("llama3.2:latest")
model.register_tools([
    search_knowledge,
    query_temporal,
    get_related_docs,
    calculate,
])

# Model can now call tools
answer = model.answer_with_tools(
    question="Which memory leak was fixed first?",
    tools=model.available_tools
)

# Model might do:
# 1. Call search_knowledge("memory leak")
# 2. Call query_temporal() on results
# 3. Synthesize answer
```

---

## Validation: Do Current Plans Satisfy Principles?

### Vector Search Baseline

**Lobotomy test:** ⚠️ Partial
- Source: Markdown ✓
- Index: Vectors (regenerable) ✓
- But: Heavy reliance on embeddings
- Fallback: grep still works ✓

**MCP decoupling:** ❌ No
- Direct model integration
- No tool interface
- Model-specific

**Recommendation:** Wrap in MCP tool

### Graph Storage Approach

**Lobotomy test:** ✓ Pass (if done right)
- Source: Markdown + YAML frontmatter ✓
- Graph: Regenerable from frontmatter ✓
- Human-readable metadata ✓

**MCP decoupling:** ✓ Pass (if done right)
- Graph queries → MCP tools
- Model-agnostic
- Swappable

**Recommendation:** This is the way

### LLM-Heavy Approach

**Lobotomy test:** ✓ Pass
- Knowledge in markdown ✓
- LLM is optional layer ✓

**MCP decoupling:** ⚠️ Depends on implementation
- If retrieval → MCP tool ✓
- If direct LLM call ❌

**Recommendation:** Use MCP tools for retrieval

---

## Conclusion

**Two new principles identified:**

1. **Lobotomy Test:** System useful without smart components
   → Forces human-readable storage

2. **MCP Decoupling:** Model separate from knowledge
   → Enables swappable models, measurable contribution

**Architectural implications:**

✓ **Storage:** Markdown + YAML frontmatter (passes lobotomy)
✓ **Indexes:** Regenerable (SQLite, vectors, graph)
✓ **Interface:** MCP tools (enables decoupling)
✓ **Models:** Swappable (Ollama, Claude, GPT)

**Enables scientific testing:**
- A/B test models
- Measure tool contribution
- Identify which tools help
- Determine if graph structure helps

**This transforms the investigation from philosophical to empirical:**
```python
# Test: Does graph storage help?
f1_flat = evaluate(model, tools=[search_markdown])
f1_graph = evaluate(model, tools=[search_markdown, traverse_graph, query_temporal])

graph_contribution = f1_graph - f1_flat
# If positive: Graph helps. If negative: Graph hurts. If zero: No difference.
```

**Want me to:**
1. **Implement MCP tool layer** for current evaluation framework?
2. **Add frontmatter to evaluation docs** to enable graph queries?
3. **Build testing harness** to measure model vs tool contribution?

This is brilliant strategic thinking - you've identified the principles that make the system sustainable and testable! 🎯
