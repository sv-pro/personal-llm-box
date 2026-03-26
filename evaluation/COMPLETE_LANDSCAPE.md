# Complete Landscape: Investigation Board System

**Date:** 2026-03-26
**Branch:** experiments/retrieval
**Status:** Research & design phase, test-driven framework established

---

## What We Have Built

### 1. Test-Driven Evaluation Framework ✅

**Core infrastructure for empirical testing:**

```
evaluation/
├── evaluate.py                    # Pluggable evaluation engine
├── questions.json                 # 12 easy questions (5 trivial, 7 non-trivial)
├── questions-hard.json            # 18 hard questions (reasoning-heavy)
├── knowledge/                     # 10 sample documents
│   ├── 2025-12-20-december-sprint-retrospective.md
│   ├── 2026-01-12-test-suite-issues.md
│   ├── 2026-01-15-architecture-overview.md
│   ├── 2026-01-18-sprint-planning-notes.md
│   ├── 2026-01-22-auth-memory-leak-investigation.md
│   ├── 2026-01-25-infrastructure-update.md
│   ├── 2026-01-28-timeout-configuration.md
│   ├── 2026-01-30-incident-report-database.md
│   ├── 2026-02-01-api-documentation.md
│   └── 2026-02-05-performance-monitoring.md
└── results/
    ├── baseline-comparison.json
    ├── with-vector-search.json
    └── hard-questions-multi-query.json
```

**Capabilities:**
- Pluggable retrieval strategies (protocol-based interface)
- Automated metrics calculation (precision, recall, F1, query time)
- Question difficulty levels (trivial, easy non-trivial, hard)
- Separate scoring for different question types
- JSON output for analysis

**Usage:**
```bash
python evaluate.py --strategy simple_grep
python evaluate.py --strategy multi_query
python evaluate.py --strategy vector_search
python evaluate.py --questions questions-hard.json
python evaluate.py --strategy all --output results.json
```

### 2. Baseline Retrieval Strategies ✅

**Implemented and tested:**

**simple_grep:**
- Literal substring matching
- Current: 0% F1 (fails on natural language questions)
- Speed: 0.4ms average
- Status: Proves current search.py won't work

**multi_query:**
- Keyword extraction + scoring by coverage
- Easy questions: 49.80% F1
- Hard questions: 38.13% F1
- Speed: 3ms average
- Status: Best current baseline

**vector_search:**
- Sentence transformers (all-MiniLM-L6-v2)
- In-memory embedding cache
- Easy questions: 55.08% F1 (better precision)
- Hard questions: Not tested yet
- Speed: 38ms average
- Status: Semantic baseline established

**Key insight:** All strategies can retrieve documents, but cannot reason over them.

### 3. Knowledge Base (Evaluation Dataset) ✅

**10 documents with intentional complexity:**

**Decoy documents** (overlapping keywords):
- Test suite memory leak vs production memory leak
- File upload timeout vs network test timeout
- Multiple performance improvement docs

**Scattered information:**
- Timeline spans Dec 2025 - Feb 2026
- Causal chains across documents
- Entity relationships (people, systems, issues)
- Temporal dependencies

**Design:** Forces multi-hop reasoning, disambiguation, temporal logic

### 4. Question Datasets ✅

**questions.json (12 easy questions):**
- 5 trivial: Direct lookup, single document
- 7 easy non-trivial: Multi-document, explicit answers
- Purpose: Test basic retrieval
- multi_query performance: 49.80% F1

**questions-hard.json (18 hard questions):**
- Disambiguation (2): Which X? (multiple entities with same keywords)
- Inference (2): Requires combining facts not explicitly stated
- Temporal reasoning (2): Timeline reconstruction, date comparisons
- Causal reasoning (2): Understanding cause-effect chains
- Negation (2): What DIDN'T happen?
- Comparison (2): Which is better/faster?
- Calculation (2): Arithmetic operations
- Synthesis (1): Aggregate across all documents
- Contradiction (1): Resolve conflicting information
- Multi-hop (1): Chain multiple inferences
- Paraphrase (1): Synonym mismatch (bottleneck vs slow)
- Purpose: Test reasoning capabilities
- multi_query performance: 38.13% F1 (finds docs, can't reason)

---

## What We Have Documented

### 1. Architecture Analysis Documents

**ARCHITECTURE_TRADEOFFS.md**
- **Retrieval × Reasoning dimension analysis**
- LLM-heavy vs Logic-heavy comparison
- Pros/cons matrices
- Decision criteria
- Hybrid approaches
- Recommendation: Start LLM-heavy, add logic if needed

**STORAGE_DIMENSION.md**
- **Storage structure dimension analysis**
- Flat vs Hierarchical vs Graph
- Research: OpenViking, ACE, OpenSPG, Cognee patterns
- Multi-layer hierarchy (L0/L1/L2 abstractions)
- Hybrid vector + graph approaches
- Poor man's graph via YAML frontmatter
- Recommendation: Progressive enhancement from flat

**ARCHITECTURAL_PRINCIPLES.md**
- **Two fundamental constraints:**
  - Lobotomy Test: System useful without smart components
  - MCP Decoupling: Model-knowledge separation via tools
- Design implications for all choices
- Regenerable indexes pattern
- Source of truth = markdown, indexes = cache
- MCP tool interface for swappable models
- Empirical testing framework

**MISSING_DIMENSIONS.md**
- **12 additional experimental dimensions identified:**
  1. Logical languages (Lean, Lojban, Prolog, Datalog)
  2. Special models (LoRA, BERT, T5, MoE, SLM)
  3. Investigation tracing & self-improvement
  4. Uncertainty & confidence handling
  5. Query understanding & clarification
  6. Multi-modal knowledge (code, diagrams, images)
  7. Contradiction detection & resolution
  8. Answer presentation & visualization
  9. Human-in-the-loop patterns
  10. Privacy & security
  11. Cost & performance optimization
  12. Domain adaptation
- Priority recommendations (Tier 1/2/3)
- Comprehensive experimental matrix (16 dimensions, 65,536 combinations)

### 2. Evaluation & Results Documents

**INITIAL_RESULTS.md**
- Baseline evaluation analysis
- Why multi_query works (keyword extraction critical)
- Why simple_grep fails (literal matching)
- Performance comparison tables
- Precision/recall trade-offs
- Recommendation: Hybrid approach needed

**VECTOR_SEARCH_BASELINE.md**
- Embedding model decision (all-MiniLM-L6-v2)
- Storage decision (in-memory cache)
- Performance vs multi_query
- Better precision (52% vs 38%), lower recall (68% vs 97%)
- Trade-off analysis
- Recommendation: Use for precision, multi_query for recall

**HARD_QUESTIONS_DESIGN.md**
- Why current "non-trivial" questions are too easy
- 8 patterns that make questions genuinely hard
- Design strategies (decoys, synonyms, inference, temporal)
- Success criteria for hard questions

**HARD_QUESTIONS_RESULTS.md**
- multi_query on hard questions: 38.13% F1 (vs 49.80% on easy)
- Critical insight: Retrieval ≠ Answering
- Example breakdowns showing where multi_query fails
- Proof that reasoning is needed, not just better retrieval

### 3. Implementation Guides

**README.md** (in evaluation/)
- Complete framework documentation
- Test-driven development philosophy
- Question dataset structure
- Metrics explanation
- Adding new strategies guide
- Progressive improvement workflow

**QUICKSTART.md**
- 5-minute getting started
- Running evaluations
- Understanding output
- Common questions
- Typical development loop

**BRANCHING_GUIDE.md** (project root)
- Experiment workflow
- Branch naming conventions
- Merge path to main
- Rollback procedures
- Quick reference

**EXPERIMENTS.md** (project root)
- Experiment guidelines
- Baseline metrics (grep search: 20 lines, ~50ms for 100 files)
- Benchmark template
- Decision matrix for merge criteria
- Ideas to explore (FTS5, vector, BM25, fuzzy, hybrid, knowledge graph)

---

## The Complete Experimental Space

### Primary Dimensions (3D Space)

**Dimension 1: Retrieval**
```
Simple ────────────────────────────────────> Advanced
  │                                              │
  ├─ Keyword matching (grep, multi_query)       ├─ Semantic (vector search)
  ├─ Full-text search (SQLite FTS5)             ├─ Graph traversal
  └─ BM25 ranking                               └─ Hybrid (keyword + semantic + graph)
```

**Dimension 2: Reasoning**
```
LLM-Heavy ─────────────────────────────────> Logic-Heavy
     │                                              │
     ├─ Pure LLM (Ollama generates answer)         ├─ Rule engine
     ├─ LLM with tools (MCP interface)             ├─ Temporal logic
     ├─ Hybrid (LLM + verification)                ├─ Prolog/Datalog
     └─ Ensemble (multiple LLMs vote)              └─ Formal verification (Lean)
```

**Dimension 3: Storage**
```
Flat ──────────────────────────────────────> Graph
  │                                              │
  ├─ Markdown files                              ├─ YAML frontmatter (entities, relations)
  ├─ Directory hierarchy                         ├─ SQLite graph tables
  └─ Tags                                        ├─ Neo4j property graph
                                                 └─ RDF/SPARQL semantic web
```

### Secondary Dimensions (13 More)

**4. Logical Languages**
- None (natural language only)
- Prolog (logic programming)
- Datalog (guaranteed termination)
- Lean (theorem proving)
- Lojban (constructed logical language)
- ASP (answer set programming)

**5. Model Architectures**
- Generative: GPT, LLaMA, Qwen (text generation)
- Encoder: BERT, sentence-transformers (embeddings)
- Encoder-decoder: T5, BART (text-to-text)
- Mixture of Experts (MoE)
- Small Language Models (SLM <1B params)
- LoRA-adapted (domain-specific fine-tuning)
- Ensemble (multiple models voting)

**6. Investigation Tracing**
- None (answer only)
- Basic logging (actions taken)
- Full trace (action + reasoning + intermediate results)
- Trace visualization (graph of investigation steps)
- Trace-based learning (analyze failures)

**7. Self-Improvement**
- Static (no learning)
- Failure analysis (log and review failures)
- RLHF (reinforcement learning from human feedback)
- Active learning (ask human about uncertain cases)
- Meta-learning (learn which strategies work when)
- Curriculum learning (easy → hard progression)

**8. Uncertainty Handling**
- None (always answer)
- Confidence scores (0-1)
- "I don't know" detection
- Confidence thresholds (only answer if conf > 0.7)
- Uncertainty propagation (track through reasoning chain)

**9. Query Understanding**
- As-is (use query verbatim)
- Spell correction
- Ambiguity detection + clarification
- Query expansion (synonyms, related terms)
- Intent classification (fact lookup, comparison, explanation, etc.)
- Query rewriting (reformulate for better retrieval)

**10. Multi-Modal**
- Text only
- Code (syntax-aware search)
- Diagrams (Mermaid, PlantUML)
- Images (OCR, vision models)
- Tables (structured data extraction)
- Audio/video transcripts

**11. Contradiction Handling**
- Ignore (return first found)
- Detect (flag contradictions)
- Resolve - temporal (use most recent)
- Resolve - authority (trust official sources)
- Resolve - ask user
- Resolve - track multiple versions

**12. Answer Presentation**
- Plain text
- Markdown formatted
- Timeline visualization
- Graph/tree visualization
- Citations with links
- Interactive drill-down
- Confidence indicators
- Source highlighting

**13. Human-in-the-Loop**
- Fully automated
- Verification (human confirms answer)
- Guided investigation (human steers)
- Active learning (system asks for labels)
- Collaborative (human + AI explore together)

**14. Privacy/Security**
- No controls
- PII detection + warning
- Redaction (auto-remove sensitive info)
- Encryption at rest
- Access level controls (private/work/public)
- Audit logging

**15. Performance Optimization**
- No optimization
- Answer caching
- Adaptive model selection (small for easy, large for hard)
- Batch processing
- Lazy loading (load docs on-demand)
- Precomputed indexes

**16. Domain Adaptation**
- Generic (works for any domain)
- Configurable schema (define entities/relations)
- Domain-specific tools (code search, paper search, etc.)
- Domain-specific prompts
- Domain-specific fine-tuning

---

## Current Repository State

### File Structure

```
personal-llm-box/
├── app/                           # FastAPI backend (WORKING)
│   ├── main.py
│   ├── routes/
│   │   ├── artifact.py
│   │   ├── catalogue.py
│   │   ├── digest.py
│   │   ├── knowledge.py
│   │   └── search.py
│   ├── services/
│   │   ├── ollama.py
│   │   └── storage.py
│   └── utils/
│       └── markdown.py
├── web-ui/                        # Web interface (WORKING)
│   └── index.html                 # 5 tabs: Catalogue, Search, Save, Ingest, Digest
├── knowledge/                     # Production knowledge store
│   └── *.md                       # User's actual notes
├── evaluation/                    # Test-driven framework (NEW)
│   ├── evaluate.py                ✅ Evaluation engine
│   ├── questions.json             ✅ 12 easy questions
│   ├── questions-hard.json        ✅ 18 hard questions
│   ├── knowledge/                 ✅ 10 test documents
│   ├── results/                   ✅ Test results
│   ├── README.md                  ✅ Framework docs
│   ├── QUICKSTART.md              ✅ Getting started
│   ├── INITIAL_RESULTS.md         ✅ Baseline analysis
│   ├── VECTOR_SEARCH_BASELINE.md  ✅ Vector search analysis
│   ├── HARD_QUESTIONS_DESIGN.md   ✅ Hard question rationale
│   ├── HARD_QUESTIONS_RESULTS.md  ✅ Hard question results
│   ├── ARCHITECTURE_TRADEOFFS.md  ✅ LLM vs Logic analysis
│   ├── STORAGE_DIMENSION.md       ✅ Storage structure analysis
│   ├── ARCHITECTURAL_PRINCIPLES.md ✅ Lobotomy test & MCP
│   ├── MISSING_DIMENSIONS.md      ✅ 12 additional dimensions
│   └── COMPLETE_LANDSCAPE.md      ← THIS FILE
├── docker-compose.yml             # Service orchestration
├── Dockerfile                     # Backend container
├── requirements.txt               # Python dependencies
├── CLAUDE.md                      # AI assistant guide
├── BRANCHING_GUIDE.md             # Experiment workflow
├── EXPERIMENTS.md                 # Experiment guidelines
├── CATALOGUE_FEATURE.md           # Catalogue documentation
└── README.md                      # User documentation
```

### Git Branches

```
main
  └── experiments/retrieval
      ├── (commits)
      │   ├── 958fcb0 Add test-driven evaluation framework
      │   ├── eecd13a Add vector search baseline
      │   ├── d2c6d86 Add hard questions requiring reasoning
      │   ├── 9bf98a3 Document 3D architectural space
      │   ├── be184d9 Add architectural principles
      │   └── 784b0b2 Identify missing experimental dimensions
      │
      └── (potential future branches)
          ├── experiments/retrieval/vector-search
          ├── experiments/retrieval/fts5
          ├── experiments/retrieval/graph-storage
          ├── experiments/retrieval/llm-reasoning
          ├── experiments/retrieval/logical-languages
          ├── experiments/retrieval/hybrid
          └── ...
```

### Dependencies

**Current (requirements.txt):**
```
fastapi==0.115.6
uvicorn[standard]==0.34.0
requests==2.32.3
pydantic==2.10.6
sentence-transformers==3.3.1
numpy==2.2.1
```

**System:**
- Ollama (llama3.2:latest, 2GB model)
- Docker & Docker Compose
- Git
- Python 3.13

---

## Decision Points (Conscious Choices Available)

### Immediate Decisions

**1. Next Implementation Direction**

**Option A: Test LLM-Heavy Approach**
- Build answer_with_llm.py
- Test on hard questions
- Measure: Can Ollama reason over retrieved docs?
- Effort: 1-2 days
- Risk: Low (just testing)

**Option B: Implement Graph Storage**
- Add YAML frontmatter to evaluation docs
- Build graph query tools
- Test: Does graph structure help?
- Effort: 3-5 days
- Risk: Medium (more complex)

**Option C: Add Confidence Scoring**
- Implement uncertainty detection
- Test: Are high-confidence answers more accurate?
- Effort: 1 day
- Risk: Low

**Option D: Explore Logical Languages**
- Represent questions in Prolog/Datalog
- Test: Can logic programming answer hard questions?
- Effort: 1 week+
- Risk: High (steep learning curve)

**Option E: Something Radical** (you mentioned this)
- ???
- Waiting for your input...

**2. Architectural Philosophy**

**Philosophy A: Pragmatic MVP**
- Start LLM-heavy (fast to build)
- Add complexity only if proven necessary
- Ship working system quickly
- Iterate based on real usage

**Philosophy B: Research-Driven**
- Explore all dimensions systematically
- Build comprehensive comparison
- Publish findings
- Choose optimal approach with evidence

**Philosophy C: Hybrid Experimental**
- Build multiple approaches in parallel branches
- Run tournaments (which wins?)
- Keep winner, archive losers
- Scientific exploration

**3. Scope Decision**

**Scope A: Personal Tool**
- Keep it simple
- Just needs to work for you
- Optimize for your use case
- Fast iteration, no polish

**Scope B: Research Project**
- Comprehensive evaluation
- Academic rigor
- Publishable results
- Broader applicability

**Scope C: Production System**
- Full feature set
- Polish & UX
- Scalability
- Documentation
- Support multiple users

**4. Measurement Focus**

**Focus A: Accuracy**
- Maximize F1 score
- Get correct answers
- Doesn't matter if slow/complex

**Focus B: Speed**
- Sub-10ms queries
- Real-time feel
- Sacrifice accuracy if needed

**Focus C: Explainability**
- Trace all reasoning
- Show sources
- Audit trail
- Trust > accuracy

**Focus D: Cost**
- Minimize LLM calls
- Maximize caching
- Efficient models

---

## What Works Right Now

**Production System (main branch):**
- ✅ FastAPI backend running
- ✅ Ollama integration working
- ✅ Web UI functional (5 tabs)
- ✅ Git-backed storage
- ✅ Search endpoint (basic grep)
- ✅ Artifact saving with frontmatter
- ✅ Text ingestion with chunking
- ✅ LLM digest/analysis
- ✅ Catalogue view

**Evaluation Framework (experiments/retrieval):**
- ✅ Three strategies implemented and tested
- ✅ 30 questions (12 easy, 18 hard)
- ✅ 10 test documents
- ✅ Automated metrics calculation
- ✅ Baseline performance established
- ✅ Proof that reasoning is needed

**Documentation:**
- ✅ Complete architectural analysis
- ✅ All dimensions mapped
- ✅ Decision frameworks
- ✅ Experimental guidelines
- ✅ Trade-off matrices

---

## What's Missing (Opportunities)

**Core Gaps:**
- ❌ No LLM-based reasoning (just retrieval)
- ❌ No graph structure (flat files only)
- ❌ No confidence scoring
- ❌ No query understanding
- ❌ No investigation tracing
- ❌ No self-improvement loops

**Quality Gaps:**
- ❌ No contradiction detection
- ❌ No answer visualization
- ❌ No human-in-the-loop
- ❌ No multi-modal support

**Optimization Gaps:**
- ❌ No caching
- ❌ No model selection
- ❌ No batching

**Polish Gaps:**
- ❌ No spell checking
- ❌ No ambiguity handling
- ❌ No privacy controls
- ❌ No domain adaptation

---

## Success Criteria (Defined)

### For Easy Questions (questions.json)

**Target metrics:**
- Trivial questions: 100% F1 (must get all basic lookups right)
- Non-trivial questions: 80% F1 (strong performance on multi-doc)
- Query time: <100ms (interactive feel)

**Current baseline:**
- multi_query: 49.80% F1 overall
- Trivial: 35.14% F1 (needs work)
- Non-trivial: 60.27% F1 (decent)

**Gap:** Need 30-40% improvement

### For Hard Questions (questions-hard.json)

**Target metrics:**
- Overall F1: 70%+ (most questions answered correctly)
- Temporal questions: 90%+ (should be deterministic)
- Causal questions: 70%+ (harder, requires understanding)
- Calculation questions: 95%+ (math should be perfect)

**Current baseline:**
- multi_query: 38.13% F1
- Cannot reason, only retrieves

**Gap:** Need reasoning capability, not just better retrieval

### For Production Use

**User-facing criteria:**
- Can answer 80% of real questions correctly
- Response time feels instant (<1s)
- Explanations are clear
- Rare hallucinations (< 5% of answers)
- Can say "I don't know" when uncertain

---

## The Landscape Summary

**You have:**

1. ✅ **Working system** (personal-llm-box with web UI)
2. ✅ **Test-driven framework** (evaluation/ with 30 questions)
3. ✅ **Baseline measurements** (multi_query: 49.80% F1 easy, 38.13% F1 hard)
4. ✅ **Complete architectural analysis** (16 dimensions documented)
5. ✅ **Clear gaps identified** (reasoning, not retrieval, is the bottleneck)
6. ✅ **Decision frameworks** (principles, trade-offs, priorities)
7. ✅ **Experimental infrastructure** (branches, evaluation, metrics)

**You can:**

1. Test any retrieval strategy objectively
2. Measure any reasoning approach empirically
3. Compare models/architectures with data
4. Explore 65,536 combinations systematically
5. Make evidence-based decisions
6. Iterate rapidly with confidence

**You're at:**
- A fork in the road with multiple viable paths
- Full visibility into the decision space
- Solid foundation for any direction
- Ready for "something radical"

---

## Visual Decision Tree

```
                    START HERE
                        │
        ┌───────────────┼───────────────┐
        │               │               │
    Fast MVP      Comprehensive     Radical New
    (1 week)      Research          Approach
                  (1-3 months)      (???)
        │               │               │
        │               │               │
    LLM-Heavy    Test Everything    [WAITING FOR
        │         Systematically     YOUR INPUT]
        │               │
        ├─> Ship    Publish
        │           Paper
        │
    Iterate
    Based on
    Real Use
```

---

**Ready for the radical idea. Show me what you've got! 🚀**
