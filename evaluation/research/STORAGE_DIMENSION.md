# The Storage Dimension: How Knowledge Structure Assists Question Answering

## The Third Dimension

```
     Storage Structure
           ↕
Retrieval ← → Reasoning
```

**Your hypothesis:** Hierarchical/graph networks of documents assist question answering **by themselves**, before retrieval or reasoning even happens.

This is **orthogonal** to the LLM vs Logic dimension. You could have:
- LLM reasoning + Flat storage (current baseline)
- LLM reasoning + Graph storage
- Logic reasoning + Flat storage
- Logic reasoning + Graph storage

## Current State: Flat Storage

**What we have now:**
```
knowledge/
├── 2026-01-15-architecture-overview.md
├── 2026-01-18-sprint-planning-notes.md
├── 2026-01-22-auth-memory-leak-investigation.md
└── ... (independent markdown files)
```

**Structure:** None. Each file is independent.

**Relationships:** Implicit (only in content, not formalized)

**Retrieval:** Scan all files, keyword/vector matching

**Problem for hard questions:**
- "Which memory leak was fixed first?" → Must scan all docs for "memory leak"
- Cannot pre-filter to "documents about production issues" vs "documents about test issues"
- No concept of "related documents"
- No temporal ordering
- No causal chains

## Storage Spectrum: Flat → Hierarchical → Graph

### Level 1: Flat (Current)

```
Files: [ doc1.md, doc2.md, doc3.md, ... ]
```

**Structure:** None
**Relationships:** None (implicit in text only)
**Retrieval:** Linear scan or vector search

### Level 2: Hierarchical

```
knowledge/
├── infrastructure/
│   ├── redis/
│   │   ├── migration.md
│   │   └── config.md
│   └── database/
│       └── incident.md
├── services/
│   ├── auth/
│   │   └── memory-leak.md
│   └── api-gateway/
│       └── overview.md
└── testing/
    └── test-suite-issues.md
```

**Structure:** Tree/directory hierarchy
**Relationships:** Parent-child (containment)
**Retrieval:** Navigate tree + search within subtrees

**Benefits:**
- ✓ Natural categorization
- ✓ Scope limiting ("search only in infrastructure/redis")
- ✓ Hierarchical context (doc inherits category)

**Limitations:**
- ✗ Single hierarchy (what if doc belongs to multiple categories?)
- ✗ No temporal relationships
- ✗ No causal relationships
- ✗ No entity relationships

### Level 3: Graph/Network

```
Nodes:
- Document: "auth-memory-leak-investigation.md"
- Entity: "Memory Leak (Production Auth)"
- Entity: "Memory Leak (Test Suite)"
- Person: "Alex"
- System: "Authentication Service"
- Date: "2026-01-22"

Edges:
- Document --mentions--> Entity
- Entity --fixed_by--> Person
- Entity --occurred_in--> System
- Entity --fixed_on--> Date
- Document --caused_by--> Document (causal)
- Document --related_to--> Document (semantic)
- Document --supersedes--> Document (temporal)
```

**Structure:** Graph (nodes + edges)
**Relationships:** Explicit, typed, multi-dimensional
**Retrieval:** Graph traversal + search

**Benefits:**
- ✓ Multiple categorizations (tags, types, categories)
- ✓ Explicit relationships (causal, temporal, semantic)
- ✓ Entity-centric queries ("all docs about Alex")
- ✓ Path finding ("how did A lead to B?")
- ✓ Contextual expansion ("docs related to this doc")

**Limitations:**
- ✗ Complex to build (extraction pipeline)
- ✗ Maintenance overhead (keep graph updated)
- ✗ Storage overhead (graph database)

---

## Patterns from Research

### Pattern 1: Multi-Layer Hierarchy (OpenViking)

**Structure:**
```
L0: Abstract (one-sentence summary)
 ↓
L1: Overview (2k tokens, core info)
 ↓
L2: Details (full original content)
```

**Benefit:** Retrieval can start at L0 (fast scan), drill down to L1 (planning), load L2 only if needed.

**Hypothesis validation:** ✓ Structure assists retrieval by enabling **progressive refinement**

### Pattern 2: Evolving Playbook (ACE)

**Structure:**
```
## STRATEGIES
[str-001] helpful=5 harmful=0 :: Strategy text
[str-002] helpful=2 harmful=3 :: Another strategy

## PITFALLS
[pit-001] helpful=0 harmful=8 :: Common mistake
```

**Benefit:** Tracks what works/doesn't work. Retrieval can prioritize high-scoring insights.

**Hypothesis validation:** ✓ Structure assists by **scoring relevance/quality**

### Pattern 3: Semantic Property Graph (OpenSPG)

**Structure:**
```
Nodes: Entities with types and properties
Edges: Relationships with semantics
Schema: Ontology defining valid structures
```

**Benefit:** Can query "show me all issues caused_by high_latency" → graph traversal finds answer

**Hypothesis validation:** ✓ Structure assists by **formalizing relationships**

### Pattern 4: Hybrid Vector+Graph (Cognee)

**Structure:**
```
Vector layer: Semantic similarity search
  +
Graph layer: Relationship navigation
```

**Benefit:** Vector finds "similar" docs, graph finds "related" docs. Combination is stronger.

**Hypothesis validation:** ✓ Structure assists by **combining similarity + relationships**

---

## How Structure Helps Answer Hard Questions

### Example 1: Disambiguation

**Question:** "Which memory leak was fixed first?"

**Flat storage:**
```
1. Search for "memory leak"
2. Find: auth-memory-leak-investigation.md, test-suite-issues.md
3. LLM must read both, extract dates, compare
```

**Graph storage:**
```
Graph query:
  MATCH (e:Entity {type: "memory_leak"})-[:FIXED_ON]->(d:Date)
  RETURN e.name, d.date ORDER BY d.date ASC LIMIT 1

Result: "Test Suite Memory Leak, 2026-01-12"
```

**Benefit:** Graph structure **pre-computed** the temporal relationship at ingestion time.

### Example 2: Causal Reasoning

**Question:** "Why did dashboard load times improve?"

**Flat storage:**
```
1. Search for "dashboard" + "improve"
2. Find multiple docs
3. LLM must infer causal chain
```

**Graph storage:**
```
Graph structure (built at ingestion):
  Redis Migration --causes--> Lower Latency
  Lower Latency --causes--> Faster Cache
  Faster Cache --causes--> Dashboard Improvement

Graph query:
  MATCH path = (cause)-[:CAUSES*]->(effect:Improvement {type: "dashboard"})
  RETURN path

Result: Entire causal chain returned
```

**Benefit:** Causal relationships **pre-extracted** and **queryable**.

### Example 3: Multi-Hop Reasoning

**Question:** "Who should I contact about file upload performance?"

**Flat storage:**
```
1. Search for "file upload"
2. Search for "performance"
3. LLM must connect docs and extract person
```

**Graph storage:**
```
Graph:
  FileUpload --problem_domain--> Timeout
  Timeout --owned_by--> Taylor
  Taylor --responsible_for--> Performance

Query:
  MATCH (topic {name: "file upload"})-[*]-(person:Person)-[:RESPONSIBLE_FOR]->(area {name: "performance"})
  RETURN person.name

Result: "Taylor"
```

**Benefit:** Relationship traversal finds answer **without LLM reasoning**.

---

## The Hypothesis: Structure Assists "By Itself"

**Strong form:** Graph structure can answer questions **without LLM or complex logic**

**Example: Temporal comparison**
```
Query: Which(entity_type=memory_leak, order_by=date_fixed, limit=1)
Answer: Via graph traversal, no reasoning needed
```

**Weaker form:** Graph structure makes LLM/logic reasoning **easier and more accurate**

**Example: Provide pre-structured context**
```
LLM prompt:
  Question: Why did dashboard improve?
  Causal chain: [Redis Migration → Lower Latency → Faster Cache → Dashboard Improvement]
  Documents: [migration.md, performance-monitoring.md]
  Answer:
```

LLM doesn't have to discover the causal chain (hardest part), just explain it.

---

## Trade-offs of Graph Storage

### Pros ✅

**1. Pre-computed Relationships**
- Temporal: "which happened first" → sorted by date
- Causal: "what caused X" → follow cause edges
- Hierarchical: "all Redis docs" → traverse redis subtree
- Entity-centric: "all Alex's work" → follow person edges

**2. Smarter Retrieval**
- Contextual expansion: "docs related to this doc"
- Multi-hop: "docs 2 steps away from X"
- Filtered search: "memory leaks in production (not test)"
- Path finding: "how did A lead to B"

**3. Reduces LLM Load**
- Graph answers structural queries (dates, hierarchies, relationships)
- LLM only needed for semantic understanding
- Smaller context windows (less hallucination risk)

**4. Explainable**
- "Answer came from graph traversal: node X → edge Y → node Z"
- Audit trail
- Debuggable

**5. Evolving Knowledge**
- Add nodes/edges incrementally
- Update relationships without reprocessing everything
- Track knowledge provenance

### Cons ❌

**1. Complex Ingestion Pipeline**

Must extract:
- Entities (people, systems, concepts)
- Relationships (causes, fixes, mentions, relates_to)
- Temporal markers (dates, sequences)
- Hierarchical structure (categories, topics)

**Implementation:**
```python
def ingest_document(doc):
    # 1. Extract entities (NER)
    entities = extract_entities(doc)  # "Alex", "Auth Service", "Memory Leak"

    # 2. Extract relationships
    relationships = extract_relationships(doc)  # "Alex fixed Memory Leak"

    # 3. Extract temporal info
    dates = extract_dates(doc)  # "2026-01-22"

    # 4. Build graph
    graph.add_nodes(entities)
    graph.add_edges(relationships)
    graph.add_properties(temporal=dates)

    # 5. Link to doc
    for entity in entities:
        graph.add_edge(doc_node, entity, type="mentions")
```

**Challenge:** This is hard! NER, relationship extraction, temporal parsing...

**2. Maintenance Overhead**
- Documents change → graph must update
- Relationships might be wrong → need correction mechanism
- Graph can become stale
- Schema evolution (what if new relationship types emerge?)

**3. Storage & Query Infrastructure**
- Need graph database (Neo4j, Neptune, etc.)
- Or embed graph in existing storage (SQLite with graph extension)
- Graph queries (Cypher, SPARQL) more complex than SQL
- Indexing strategies for graph traversal

**4. Extraction Accuracy**
- NER mistakes → wrong entities in graph
- Relationship extraction errors → wrong connections
- Temporal parsing failures → incorrect dates
- **Garbage in, garbage out**

**5. Upfront Complexity**
- Must decide schema (what entities? what relationships?)
- Ontology design (is "Memory Leak" an entity or a category?)
- Trade-off: specific schema (rigid but accurate) vs generic schema (flexible but fuzzy)

---

## Storage Dimension Decision Matrix

| Aspect | Flat | Hierarchical | Graph |
|--------|------|--------------|-------|
| **Ingestion complexity** | Very low | Low | High |
| **Retrieval power** | Basic | Medium | High |
| **Temporal queries** | Manual | Manual | Native |
| **Causal queries** | Manual | Manual | Native |
| **Multi-hop** | Manual | Partial | Native |
| **Maintenance** | Low | Low | Medium-High |
| **Storage overhead** | None | None | Medium |
| **Explainability** | Low | Medium | High |
| **Build time** | Hours | Days | Weeks-Months |
| **Accuracy dependency** | None | None | Extraction quality |

---

## Recommendation: Progressive Enhancement

### Phase 1: Flat + Metadata (Current)

Keep flat markdown but add structured frontmatter:

```yaml
---
title: "Auth Service Memory Leak Investigation"
entities:
  - name: "Memory Leak (Production Auth)"
    type: "issue"
  - name: "Alex"
    type: "person"
  - name: "Authentication Service"
    type: "system"
relationships:
  - type: "fixed_by"
    from: "Memory Leak (Production Auth)"
    to: "Alex"
  - type: "occurred_in"
    from: "Memory Leak (Production Auth)"
    to: "Authentication Service"
temporal:
  discovered: "2026-01-18"
  resolved: "2026-01-22"
causal:
  - "TokenCache missing cleanup caused memory growth"
tags: ["incident", "production", "memory"]
related_docs:
  - "2026-01-18-sprint-planning-notes.md"
  - "2026-01-25-infrastructure-update.md"
---
```

**Benefit:**
- ✓ Easy to add (just YAML)
- ✓ Can extract to graph later
- ✓ Enables basic filtering/queries
- ✓ Human-readable and editable
- ✓ No infrastructure change needed

**Build "poor man's graph" from frontmatter:**
```python
def build_graph_from_frontmatter():
    graph = {}
    for doc in knowledge_dir.glob("*.md"):
        fm = parse_frontmatter(doc)
        graph[doc.name] = {
            'entities': fm.get('entities', []),
            'relationships': fm.get('relationships', []),
            'temporal': fm.get('temporal', {}),
            'related': fm.get('related_docs', [])
        }
    return graph
```

Now you can query:
```python
# Find docs by entity
docs_about_alex = [d for d, meta in graph.items()
                   if any(e['name'] == 'Alex' for e in meta['entities'])]

# Find docs by date range
docs_in_january = [d for d, meta in graph.items()
                   if '2026-01' in str(meta['temporal'])]

# Follow relationships
def get_related(doc_name, depth=1):
    related = graph[doc_name]['related']
    if depth > 1:
        for r in related:
            related.extend(get_related(r, depth-1))
    return related
```

### Phase 2: Auto-Extract Entities (LLM-Assisted)

Use LLM to extract frontmatter from existing docs:

```python
def extract_metadata(doc_content):
    prompt = f"""
    Extract structured metadata from this document:

    {doc_content}

    Return JSON with:
    - entities: [{{name, type}}]
    - relationships: [{{type, from, to}}]
    - temporal: {{discovered, resolved, ...}}
    - tags: [...]

    JSON:
    """

    metadata = llm_generate(prompt)
    return json.loads(metadata)
```

**Benefit:** Automate graph construction without manual annotation.

**Risk:** LLM extraction errors → wrong graph structure.

### Phase 3: True Graph Database (If Proven Valuable)

Once you have evidence that structured queries help:

**Option A: Embed in SQLite**
```sql
CREATE TABLE entities (
    id INTEGER PRIMARY KEY,
    name TEXT,
    type TEXT
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    from_entity INTEGER,
    to_entity INTEGER,
    type TEXT,
    FOREIGN KEY(from_entity) REFERENCES entities(id),
    FOREIGN KEY(to_entity) REFERENCES entities(id)
);

CREATE TABLE doc_entities (
    doc_id INTEGER,
    entity_id INTEGER,
    FOREIGN KEY(entity_id) REFERENCES entities(id)
);
```

**Option B: Use graph database** (Neo4j, Neptune, TerminusDB, etc.)

---

## Hypothesis Testing: Does Structure Help?

### Experiment: Test on Hard Questions

**Setup:**
1. Take existing hard questions
2. Manually create graph structure for evaluation knowledge base
3. Implement graph-query answering
4. Compare accuracy

**Test questions suitable for graph querying:**

**Temporal:**
- "Which memory leak was fixed first?"
  → `MATCH (e:Issue {type: 'memory_leak'})-[:FIXED_ON]->(d:Date) RETURN e ORDER BY d`

**Causal:**
- "Why did dashboard improve?"
  → `MATCH path=(cause)-[:CAUSES*]->(effect {name: 'dashboard improvement'}) RETURN path`

**Entity-centric:**
- "What did Alex work on?"
  → `MATCH (p:Person {name: 'Alex'})-[:WORKED_ON]->(e) RETURN e`

**Multi-hop:**
- "Who handles file upload performance?"
  → `MATCH (topic {name: 'file upload'})-[*]-(person:Person)-[:RESPONSIBLE_FOR]->({name: 'performance'}) RETURN person`

**Expected result:**
- Graph queries answer structural questions **without LLM**
- LLM only needed for questions requiring semantic understanding
- Overall accuracy improves (or query speed improves)

### Metrics

| Question Type | Flat + LLM | Graph + LLM | Graph Only |
|---------------|------------|-------------|------------|
| Temporal | ? | ? | ? |
| Causal | ? | ? | ? |
| Disambiguation | ? | ? | ? |
| Multi-hop | ? | ? | ? |
| **Overall F1** | ? | ? | ? |

**Hypothesis validated if:** Graph storage improves F1 score or reduces LLM usage.

---

## The 3D Architecture Space

You now have three dimensions to explore:

```
            Storage
           (Flat ↔ Graph)
               |
               |
               |
    Retrieval--+--Reasoning
   (Simple ↔   |   (LLM ↔
    Advanced)  |    Logic)
```

**8 possible combinations:**

1. **Simple Retrieval + LLM Reasoning + Flat Storage** ← Current baseline
2. **Simple Retrieval + LLM Reasoning + Graph Storage** ← Easiest upgrade
3. **Simple Retrieval + Logic Reasoning + Graph Storage** ← Graph enables logic
4. **Advanced Retrieval + LLM Reasoning + Flat Storage**
5. **Advanced Retrieval + LLM Reasoning + Graph Storage**
6. **Advanced Retrieval + Logic Reasoning + Flat Storage**
7. **Advanced Retrieval + Logic Reasoning + Graph Storage** ← Most complex
8. **Simple Retrieval + Logic Reasoning + Flat Storage** ← Won't work well

**My recommendation:**
Start with #2 (Simple Retrieval + LLM + Graph), because:
- Graph structure makes LLM's job easier
- Can later move to logic reasoning if graph structure is proven valuable
- Lowest risk, medium effort

---

## Practical Next Steps

### Minimal Graph Prototype

**1. Add frontmatter to evaluation docs** (manual for now)

**2. Build frontmatter-based graph query**
```python
class SimpleGraph:
    def __init__(self, knowledge_dir):
        self.graph = self._build_from_frontmatter(knowledge_dir)

    def query_by_entity(self, entity_name):
        return [doc for doc, meta in self.graph.items()
                if entity_name in [e['name'] for e in meta.get('entities', [])]]

    def query_by_date_range(self, start, end):
        # ...

    def get_related(self, doc_name, max_hops=2):
        # ...
```

**3. Test on hard questions**
```python
# Question: "Which memory leak was fixed first?"

# Graph query
memory_leak_docs = graph.query_by_entity("memory leak")
sorted_by_date = sorted(memory_leak_docs, key=lambda d: graph.graph[d]['temporal']['resolved'])
answer = sorted_by_date[0]

# vs LLM query (current)
docs = multi_query_retrieve("which memory leak fixed first")
answer = llm_reason(question, docs)
```

**4. Measure: Did graph help?**
- Faster?
- More accurate?
- Less LLM usage?

### If Successful, Expand

- Auto-extract frontmatter with LLM
- Add more relationship types
- Build web UI to visualize graph
- Implement graph traversal queries
- Move to real graph database (if needed)

---

## Conclusion

**Your hypothesis is correct:** Graph/hierarchical storage **can** assist question answering by itself.

**Evidence:**
- ✓ Temporal queries: Native to graphs
- ✓ Causal chains: Graph edges
- ✓ Multi-hop reasoning: Graph traversal
- ✓ Disambiguation: Entity resolution in graph

**But:**
- ⚠️ Requires upfront extraction work
- ⚠️ Quality depends on extraction accuracy
- ⚠️ Not all questions benefit (semantic questions still need LLM)

**Best approach:** Progressive enhancement
1. Start: Flat + LLM (working baseline)
2. Add: Structured frontmatter (manual/LLM-extracted)
3. Query: Use frontmatter for structural questions
4. Measure: Does it help?
5. Expand: If yes, build more graph structure

The storage dimension is **complementary** to retrieval and reasoning, not a replacement. All three dimensions work together.

**Want me to prototype the frontmatter-based graph approach on the evaluation dataset?**
