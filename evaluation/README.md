# Investigation Board Evaluation - Complete Index

**Last Updated:** 2026-03-26
**Status:** Research complete, ready for Phase 1 implementation

---

## Quick Start

**New to this project?** Read in this order:

1. **[research/evaluation-framework.md](research/evaluation-framework.md)** - Understand the test-driven evaluation framework
2. **[research/SYNTHESIS_AND_DECISION.md](research/SYNTHESIS_AND_DECISION.md)** - See the complete analysis and decisions
3. **[research/GETTING_STARTED_PHASE1.md](research/GETTING_STARTED_PHASE1.md)** - Start implementing today

**Returning to continue work?**

→ See **GETTING_STARTED_PHASE1.md** for Week 1 implementation steps

---

## Document Map

### 🎯 Strategic Documents (Read First)

| Document | Purpose | Read When |
|----------|---------|-----------|
| **[research/SYNTHESIS_AND_DECISION.md](research/SYNTHESIS_AND_DECISION.md)** | Executive summary, decision matrix, comparative analysis | Starting the project |
| **[research/ONTOLOGY_FIRST_ROADMAP.md](research/ONTOLOGY_FIRST_ROADMAP.md)** | 5-week implementation plan with code examples | Planning Phase 1 |
| **[research/GETTING_STARTED_PHASE1.md](research/GETTING_STARTED_PHASE1.md)** | Step-by-step guide for Week 1 implementation | Ready to code |

### 📊 Evaluation Framework

| Document | Purpose | Lines |
|----------|---------|-------|
| **[research/evaluation-framework.md](research/evaluation-framework.md)** | Evaluation framework overview, how to run tests | 385 |
| **[QUICKSTART.md](QUICKSTART.md)** | Fast introduction to running evaluations | 235 |
| **[evaluate.py](evaluate.py)** | Pluggable evaluation engine (Python script) | - |
| **[data/questions.json](data/questions.json)** | 12 easy test questions with expected answers | - |
| **[data/questions-hard.json](data/questions-hard.json)** | 18 hard questions testing reasoning capabilities | - |

### 🏗️ Architectural Analysis

| Document | Focus Area | Key Insight | Lines |
|----------|-----------|-------------|-------|
| **[research/ARCHITECTURAL_PRINCIPLES.md](research/ARCHITECTURAL_PRINCIPLES.md)** | Core constraints | Lobotomy Test + MCP decoupling | 737 |
| **[research/ARCHITECTURE_TRADEOFFS.md](research/ARCHITECTURE_TRADEOFFS.md)** | Retrieval × Reasoning | LLM vs Logic vs Hybrid | 651 |
| **[research/STORAGE_DIMENSION.md](research/STORAGE_DIMENSION.md)** | Storage structure | Flat vs Hierarchical vs Graph | 694 |
| **[research/AGENT_HYPERVISOR_CONCEPTS.md](research/AGENT_HYPERVISOR_CONCEPTS.md)** | Ontology-first design | Security by architectural absence | 616 |

### 📈 Results & Analysis

| Document | What It Shows | Lines |
|----------|---------------|-------|
| **[research/INITIAL_RESULTS.md](research/INITIAL_RESULTS.md)** | First baseline evaluation results | 188 |
| **[research/VECTOR_SEARCH_BASELINE.md](research/VECTOR_SEARCH_BASELINE.md)** | Vector search implementation and benchmarks | 311 |
| **[research/HARD_QUESTIONS_DESIGN.md](research/HARD_QUESTIONS_DESIGN.md)** | Rationale for hard question dataset | 273 |
| **[research/HARD_QUESTIONS_RESULTS.md](research/HARD_QUESTIONS_RESULTS.md)** | Performance on hard questions | 322 |
| **[research/COMPLETE_LANDSCAPE.md](research/COMPLETE_LANDSCAPE.md)** | Current state summary of everything | 722 |

### 🔬 Research Documents

| Document | Exploration Area | Lines |
|----------|------------------|-------|
| **[research/MISSING_DIMENSIONS.md](research/MISSING_DIMENSIONS.md)** | Unexplored experimental space (16+ dimensions) | 1140 |

### 📁 Supporting Materials

```
evaluation/
├── research/               # Architectural analysis & research documents
├── data/
│   ├── knowledge/          # 10 test documents (sample knowledge base)
│   ├── questions.json      # Easy test questions
│   └── questions-hard.json # Hard test questions
├── results/                # JSON output from evaluation runs
└── evaluate.py             # Pluggable evaluation engine
```

---

## Reading Paths by Role

### For Developers (Implementing the System)

**Day 1:**
1. README.md - Understand evaluation framework
2. SYNTHESIS_AND_DECISION.md - Understand why ontology-first
3. GETTING_STARTED_PHASE1.md - Start coding

**Week 1:**
- Follow GETTING_STARTED_PHASE1.md step-by-step
- Reference ONTOLOGY_FIRST_ROADMAP.md for context
- Run evaluation tests frequently

**Weeks 2-5:**
- Follow ONTOLOGY_FIRST_ROADMAP.md phases
- Measure against success criteria in SYNTHESIS_AND_DECISION.md

### For Architects (Understanding Design Choices)

**Core Architecture:**
1. ARCHITECTURAL_PRINCIPLES.md - Core constraints (Lobotomy Test, MCP)
2. AGENT_HYPERVISOR_CONCEPTS.md - Ontology-first inspiration
3. SYNTHESIS_AND_DECISION.md - Final decisions with rationale

**Dimension Analysis:**
1. ARCHITECTURE_TRADEOFFS.md - Retrieval × Reasoning dimensions
2. STORAGE_DIMENSION.md - Storage structure options
3. MISSING_DIMENSIONS.md - Unexplored experimental space

**Decision Validation:**
1. COMPLETE_LANDSCAPE.md - Current state
2. SYNTHESIS_AND_DECISION.md - Comparative analysis

### For Researchers (Exploring Alternatives)

**Experimental Space:**
1. MISSING_DIMENSIONS.md - 16+ unexplored dimensions
2. ARCHITECTURE_TRADEOFFS.md - Tradeoff analysis
3. STORAGE_DIMENSION.md - Alternative structures

**Empirical Data:**
1. questions.json + questions-hard.json - Test datasets
2. results/ directory - Benchmark data
3. HARD_QUESTIONS_RESULTS.md - Analysis of current limits

**Next Experiments:**
1. Graph-based retrieval
2. Symbolic AI / Prolog
3. Hybrid vector + graph
4. Multi-stage reasoning

### For Product Managers (Understanding Scope & Roadmap)

**Current State:**
1. COMPLETE_LANDSCAPE.md - What exists today
2. INITIAL_RESULTS.md - Baseline performance (49% F1)
3. HARD_QUESTIONS_RESULTS.md - Gaps (38% F1 on hard)

**Roadmap:**
1. SYNTHESIS_AND_DECISION.md - Phased approach (12 weeks)
2. ONTOLOGY_FIRST_ROADMAP.md - Detailed 5-week Phase 1 plan
3. Success metrics clearly defined

**ROI Analysis:**
1. SYNTHESIS_AND_DECISION.md § Quantitative Metrics
2. Expected: 3x faster, 70% cheaper than LLM-only
3. Target: 60-75% F1 across question types

---

## Key Metrics

### Current Performance (Baseline)

| Strategy | Easy F1 | Hard F1 | Speed | Cost |
|----------|---------|---------|-------|------|
| simple_grep | 0% | 0% | 0.4ms | Free |
| multi_query | 49.80% | 38.13% | 3ms | Free |
| vector_search | 55.08% | TBD | 38ms | Low |

### Target Performance (After Phase 1)

| Question Type | Current F1 | Target F1 | Strategy |
|---------------|------------|-----------|----------|
| Temporal | ~50% | **100%** | Deterministic (no LLM) |
| Calculation | ~40% | **100%** | Deterministic (no LLM) |
| Causal | ~30% | 50% → **80%** (Phase 2) | Graph traversal |
| Multi-hop | ~35% | 50% → **75%** (Phase 2) | Graph + LLM |
| Semantic | ~60% | **75%** | LLM synthesis |
| **Overall** | **49.80%** | **60%** → **75%** | Hybrid |

---

## Decision Summary

### Architecture: Ontology-First Hybrid

**Why?**
- Deterministic strategies for structured questions (fast, cheap, correct)
- LLM fallback for semantic questions (flexible)
- Security by architectural absence (read-only by design)

**Alternatives Considered:**
- ❌ LLM-only: Too slow, expensive, unreliable
- ❌ Logic-only: Too rigid, high complexity
- ✅ Hybrid: Best of both worlds

### Storage: Markdown + Implicit Graph

**Why?**
- Passes Lobotomy Test (human-readable)
- Git-backed (version control)
- Implicit graph via YAML frontmatter (queryable)

**Alternatives Considered:**
- ❌ Binary graph DB: Fails Lobotomy Test
- ❌ Vector-only: Not enough structure
- ✅ Markdown + YAML: Progressive enhancement

### Retrieval: Multi-Query + Vector Hybrid

**Why?**
- Multi-query: Fast, free, decent recall
- Vector search: Better semantic precision
- Hybrid: Best overall performance

**Alternatives Considered:**
- ❌ Simple grep: 0% F1 (proven inadequate)
- ⚠️ Vector-only: Expensive, slower
- ✅ Hybrid: Balance speed/cost/accuracy

---

## Implementation Status

### ✅ Complete

- [x] Evaluation framework (evaluate.py)
- [x] Test datasets (30 questions, 10 documents)
- [x] Baseline strategies (simple_grep, multi_query, vector_search)
- [x] Architectural analysis (7 major documents)
- [x] Implementation roadmap (5-week Phase 1 plan)

### 🏗️ In Progress

- [ ] Phase 1 Week 1: Define investigation ontology
- [ ] Phase 1 Week 2: Layer-by-layer architecture
- [ ] Phase 1 Week 3: Deterministic strategies
- [ ] Phase 1 Week 4: Specialized tools
- [ ] Phase 1 Week 5: Integration with evaluation

### ⏭️ Planned

- [ ] Phase 2: Graph enhancement (causal, multi-hop)
- [ ] Phase 3: Hybrid retrieval optimization
- [ ] Phase 4: Production integration

---

## Key Insights

### 1. Test-Driven Development Works

Starting with evaluation questions forces us to build what matters:
- 30 questions with known answers
- Objective metrics (precision, recall, F1)
- Incremental validation of improvements

### 2. Ontology-First Inverts Control

Traditional: LLM has power → Policy restricts → Hope for best
**Ontology-first:** Design defines vocabulary → LLM only sees defined actions → Misuse impossible

### 3. Deterministic-First Reduces Cost

~40% of questions can be answered without LLM:
- Temporal: Date extraction + arithmetic
- Calculation: Number extraction + math
- Lookup: Keyword search

**Result:** 3x faster, 70% cheaper than LLM-only.

### 4. Progressive Enhancement Manages Risk

Build in layers, each adds capability:
1. Markdown (human-readable)
2. + Keyword search (basic retrieval)
3. + Vector search (semantic)
4. + Graph (multi-hop)
5. + Deterministic strategies (structured reasoning)
6. + LLM (semantic reasoning)

Always have a working system.

### 5. Constraints Guide Design

**Lobotomy Test:** System useful without AI
**MCP Decoupling:** Model-knowledge separation

These constraints eliminate entire classes of approaches (binary DBs, proprietary formats).

---

## How to Use This Directory

### Running Evaluations

```bash
cd /home/dev/code/sv-pro/personal-llm-box

# Test baseline
python evaluation/evaluate.py --strategy multi_query

# Test vector search
python evaluation/evaluate.py --strategy vector_search

# Test on hard questions
python evaluation/evaluate.py --questions evaluation/data/questions-hard.json

# Compare all strategies
python evaluation/evaluate.py --strategy all --output results/comparison.json
```

### Adding New Strategies

1. Implement strategy in `evaluation/strategies/`
2. Register in `evaluate.py`
3. Run evaluation
4. Compare results in `results/`

### Updating Questions

1. Edit `questions.json` or `questions-hard.json`
2. Add question with expected sources
3. Re-run evaluations
4. Update metrics

---

## Research Questions (Open)

### Answered ✅

1. **Does keyword search work?** → No (0% F1 for simple_grep)
2. **Does multi-query improve?** → Yes (49.80% F1, significant improvement)
3. **Does vector search help?** → Yes (55.08% F1, better precision)
4. **What's the performance ceiling?** → Current strategies plateau at ~50% F1

### Open ❓

1. **Can deterministic strategies match LLM accuracy on structured questions?**
   - Hypothesis: Yes for temporal, calculation
   - Test in Phase 1 Week 3

2. **Does graph traversal improve multi-hop reasoning?**
   - Hypothesis: Yes, should reach 70-80% F1
   - Test in Phase 2 Week 7-8

3. **What's the optimal hybrid retrieval blend?**
   - Hypothesis: 60% keyword + 40% vector
   - Test in Phase 3 Week 9

4. **Can we reach 75% F1 overall?**
   - Hypothesis: Yes with ontology-first hybrid
   - Test throughout Phases 1-3

---

## Citation

If referencing this work:

```
Investigation Board Evaluation Framework
personal-llm-box project, 2026
https://github.com/sv-pro/personal-llm-box/tree/main/evaluation
```

Key documents:
- SYNTHESIS_AND_DECISION.md - Architectural decisions
- ONTOLOGY_FIRST_ROADMAP.md - Implementation approach
- AGENT_HYPERVISOR_CONCEPTS.md - Theoretical foundation

---

## Contact & Contribution

**Questions about the evaluation framework?**
→ See README.md for usage instructions

**Want to add new test questions?**
→ Edit questions.json or questions-hard.json following the schema

**Proposing new retrieval strategies?**
→ Implement RetrievalStrategy protocol in evaluate.py

**Exploring alternative architectures?**
→ See MISSING_DIMENSIONS.md for unexplored experimental space

---

## Version History

- **2026-03-26:** Comprehensive research phase complete
  - 7 major architectural documents
  - 30 test questions (12 easy, 18 hard)
  - 3 baseline strategies implemented and benchmarked
  - Phase 1 implementation plan created

- **2026-03-26:** Hard questions dataset added
  - 18 questions testing advanced reasoning
  - Disambiguation, inference, temporal logic, causal chains
  - Multi-query baseline: 38.13% F1 (exposes reasoning gap)

- **2026-03-26:** Vector search baseline established
  - Semantic search with sentence transformers
  - 55.08% F1 on easy questions (best so far)
  - Identifies semantic vs keyword tradeoffs

- **2026-03-26:** Ontology-first architecture designed
  - Agent-hypervisor concepts applied
  - 5-week implementation roadmap
  - Getting-started guide for immediate work

---

**Ready to build?** → Start with **GETTING_STARTED_PHASE1.md** 🚀
