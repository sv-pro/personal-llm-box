# Synthesis and Decision Matrix

**Date:** 2026-03-26
**Purpose:** Synthesize all architectural research into actionable decisions
**Status:** Decision framework for Phase 1 implementation

---

## Executive Summary

After comprehensive analysis of 16+ architectural dimensions, 3 retrieval strategies, and 30 test questions, we have a clear path forward for building an investigation board system that is:

1. **Empirically tested** (test-driven evaluation framework)
2. **Architecturally safe** (ontology-first, read-only by design)
3. **Incrementally buildable** (graceful degradation, progressive enhancement)
4. **Provably correct** (deterministic reasoning for structured questions)

**Core insight:** Invert the traditional "LLM does everything" approach to "deterministic first, LLM as fallback."

---

## Current State

### What Works ✅

| Component | Status | Metrics |
|-----------|--------|---------|
| Evaluation framework | ✅ Production ready | 12+18 test questions |
| Simple grep baseline | ✅ Tested | 0% F1 (proves inadequacy) |
| Multi-query keyword | ✅ Tested | 49.80% F1 (easy), 38.13% F1 (hard) |
| Vector search | ✅ Tested | 55.08% F1 (easy), untested hard |
| Knowledge structure | ✅ Valid | Passes Lobotomy Test |
| Git-backed storage | ✅ Production | Read-only safe |

### What's Missing ❌

| Capability | Current Gap | Impact on Questions |
|------------|-------------|---------------------|
| Multi-hop reasoning | Retrieval only | 38% F1 on hard questions |
| Temporal logic | No date extraction | Fails "which happened first" |
| Causal traversal | No graph | Fails "root cause" |
| Calculation | No arithmetic | Fails "how many total" |
| Disambiguation | No context | Fails "which memory leak" |
| Contradiction resolution | No validation | Fails conflicting info |

**Critical insight:** All strategies retrieve documents, but cannot reason over them.

---

## Architectural Dimensions Analyzed

### 1. Retrieval Dimension (COMPLETE_LANDSCAPE.md, VECTOR_SEARCH_BASELINE.md)

| Strategy | F1 Score (Easy) | F1 Score (Hard) | Speed | Cost |
|----------|-----------------|-----------------|-------|------|
| simple_grep | 0% | 0% | 0.4ms | Free |
| multi_query | 49.80% | 38.13% | 3ms | Free |
| vector_search | 55.08% | TBD | 38ms | Embedding compute |
| **hybrid** (planned) | TBD | TBD | TBD | Embedding + |

**Decision:** Start with multi_query (free, fast, decent), add vector_search for semantic queries.

### 2. Reasoning Dimension (ARCHITECTURE_TRADEOFFS.md)

| Approach | Accuracy | Speed | Cost | Explainability |
|----------|----------|-------|------|----------------|
| LLM-only | Unknown | Slow (seconds) | High | Low (black box) |
| Logic-only | High (for formal) | Fast (ms) | Low | Perfect |
| **Hybrid** | Best of both | Mixed | Medium | Mixed |

**Decision:** Deterministic reasoning for structured questions (temporal, causal, calculation), LLM for semantic.

### 3. Storage Dimension (STORAGE_DIMENSION.md)

| Structure | Lobotomy Test | Queryability | Complexity |
|-----------|---------------|--------------|------------|
| Flat files | ✅ PASS | Limited | Low |
| Hierarchy | ✅ PASS | Better | Medium |
| Graph DB | ❌ FAIL | Best | High |
| **Implicit graph** | ✅ PASS | Good | Low |

**Decision:** Keep flat markdown (passes Lobotomy Test), add implicit graph via YAML frontmatter links.

### 4. Ontology Dimension (AGENT_HYPERVISOR_CONCEPTS.md, ONTOLOGY_FIRST_ROADMAP.md)

| Approach | Security | Flexibility | Explainability |
|----------|----------|-------------|----------------|
| Policy-based | Runtime check | High | Low |
| **Ontology-first** | Design-time guarantee | Medium | High |

**Decision:** Ontology-first architecture - define read-only investigation actions, modification impossible by design.

### 5. Architectural Constraints (ARCHITECTURAL_PRINCIPLES.md)

**Non-negotiable:**

1. **Lobotomy Test:** System must be useful without AI components
   - ✅ Markdown files readable by humans
   - ✅ Git history preserves knowledge
   - ✅ No binary databases required

2. **MCP Decoupling:** Model-knowledge separation
   - ✅ Knowledge in markdown
   - ✅ Models as interchangeable tools
   - ✅ No model-specific formats

**Decision:** All designs must satisfy both constraints.

### 6. Unexplored Dimensions (MISSING_DIMENSIONS.md - 1140 lines!)

**High-value experiments identified but not yet tested:**

| Dimension | Potential Benefit | Complexity | Priority |
|-----------|-------------------|------------|----------|
| Logical languages (Prolog) | Provably correct reasoning | High | Medium |
| Theorem provers (Lean) | Zero hallucination | Very high | Low |
| Graph algorithms | Better multi-hop | Medium | **HIGH** |
| Symbolic AI | Deterministic rules | Medium | **HIGH** |
| Hybrid retrieval | Best recall/precision | Low | **HIGH** |
| Multi-stage reasoning | Better hard questions | Medium | **HIGH** |

**Decision:** Focus on high-priority, medium-complexity experiments first (graph, symbolic, hybrid).

---

## Decision Matrix: Which Approach for Which Question Type?

### Question Type Classification

Based on `questions.json` and `questions-hard.json` analysis:

| Question Type | % of Dataset | Best Strategy | Why |
|---------------|--------------|---------------|-----|
| **Trivial (lookup)** | 17% (5/30) | Keyword search | Direct match sufficient |
| **Temporal** | 13% (4/30) | Deterministic | Date extraction + arithmetic |
| **Causal** | 10% (3/30) | Graph traversal | Follow cause-effect edges |
| **Calculation** | 10% (3/30) | Deterministic | Number extraction + arithmetic |
| **Disambiguation** | 7% (2/30) | Context + LLM | Requires semantic understanding |
| **Multi-hop** | 17% (5/30) | Graph + LLM | Traverse then synthesize |
| **Semantic** | 27% (8/30) | LLM | Requires natural language understanding |

### Strategy Routing Decision Tree

```
Question Input
    │
    ├─ Contains "when", "date", "before", "after"?
    │   └─ YES → TemporalStrategy (deterministic)
    │       └─ Extract dates → Compare → Format answer
    │
    ├─ Contains "why", "cause", "led to"?
    │   └─ YES → CausalStrategy (graph traversal)
    │       └─ Extract entities → Traverse causal edges → Build chain
    │
    ├─ Contains "how many", "total", "sum", "count"?
    │   └─ YES → CalculationStrategy (deterministic)
    │       └─ Extract numbers → Arithmetic → Format result
    │
    ├─ Single-document direct lookup?
    │   └─ YES → SimpleRetrievalStrategy (keyword)
    │       └─ Find document → Extract snippet
    │
    ├─ Multiple entities with ambiguity?
    │   └─ YES → DisambiguationStrategy (LLM)
    │       └─ Retrieve candidates → LLM picks correct one
    │
    └─ DEFAULT → SemanticStrategy (LLM)
        └─ Retrieve documents → LLM synthesis
```

**Key insight:** ~40% of questions can use deterministic strategies (faster, cheaper, explainable).

---

## Implementation Strategy

### Phase 0: Foundation (COMPLETE - evaluation framework exists)

✅ Evaluation framework
✅ Test questions (12 easy + 18 hard)
✅ Baseline strategies (simple_grep, multi_query, vector_search)
✅ Metrics collection (precision, recall, F1)

### Phase 1: Ontology-First Architecture (ONTOLOGY_FIRST_ROADMAP.md)

**Week 1: Define Investigation Ontology**
- [ ] Create `app/investigation/ontology.py`
- [ ] Define read-only action categories (observe, reason, navigate)
- [ ] Build action registry
- [ ] Test: Attempting write action raises error

**Week 2: Layer-by-Layer Risk Elimination**
- [ ] Layer 0: Mount knowledge directory read-only
- [ ] Layer 1: Implement base ontology
- [ ] Layer 2: Dynamic projection by question type
- [ ] Layer 3: Execution governance (limits)

**Week 3: Deterministic Strategies**
- [ ] TemporalStrategy (no LLM)
- [ ] CausalStrategy (graph traversal)
- [ ] CalculationStrategy (arithmetic)
- [ ] Test: Match/exceed LLM accuracy on structured questions

**Week 4: Specialized Tools**
- [ ] Replace generic search with specialized tools
- [ ] `find_memory_leaks()`, `find_events_in_january()`, etc.
- [ ] Baked-in parameters prevent injection

**Week 5: Integration**
- [ ] Add ontology_first strategy to evaluation
- [ ] Run benchmarks vs baseline
- [ ] Document security guarantees

**Success metric:** Non-trivial F1 ≥ 60% (vs current 38-49%).

### Phase 2: Graph Enhancement (Weeks 6-8)

**Goal:** Enable causal and multi-hop reasoning.

**Week 6: Implicit Graph via YAML**
```yaml
---
title: "Memory Leak Investigation"
related_to:
  - 2026-01-15-architecture-overview.md
  - 2026-01-18-sprint-planning-notes.md
caused_by:
  - TokenCache not clearing expired sessions
fixes:
  - Implement cleanup timer
---
```

**Week 7: Graph Extraction**
- [ ] Parse frontmatter relationships
- [ ] Build in-memory graph (NetworkX)
- [ ] Implement traversal functions

**Week 8: Graph-Based Strategies**
- [ ] Causal chain traversal
- [ ] Multi-hop relation following
- [ ] Test on hard questions

**Success metric:** Causal and multi-hop question F1 ≥ 70%.

### Phase 3: Hybrid Retrieval (Weeks 9-10)

**Goal:** Best of keyword + semantic search.

**Week 9: Hybrid Strategy**
- [ ] Keyword search (broad recall)
- [ ] Vector search (semantic precision)
- [ ] Score fusion (RRF or weighted)

**Week 10: Optimization**
- [ ] Caching layer
- [ ] Query expansion
- [ ] Benchmark all strategies

**Success metric:** Overall F1 ≥ 70% across all question types.

### Phase 4: Production Integration (Weeks 11-12)

**Goal:** Integrate into main API and UI.

**Week 11: API Endpoints**
- [ ] POST `/investigate` - full investigation pipeline
- [ ] GET `/investigate/explain` - reasoning trace
- [ ] GET `/investigate/strategy` - strategy used

**Week 12: UI**
- [ ] Investigation interface in Open WebUI
- [ ] Show reasoning steps
- [ ] Display source documents with highlights

**Success metric:** End-to-end investigation working in production.

---

## Comparative Analysis: Approaches

### Approach A: LLM-Only (Traditional)

**Architecture:**
```
Question → Retrieve all documents → LLM reasons over all → Answer
```

**Pros:**
- ✓ Simple to implement
- ✓ Flexible (handles any question)
- ✓ Natural language output

**Cons:**
- ✗ Slow (LLM inference)
- ✗ Expensive (API costs)
- ✗ Hallucination risk
- ✗ Not explainable
- ✗ No correctness guarantee

**When to use:** Semantic questions requiring natural language understanding.

### Approach B: Logic-Only (Pure Symbolic)

**Architecture:**
```
Question → Parse to logic → Prove theorem → Format answer
```

**Pros:**
- ✓ Provably correct
- ✓ Fast (deterministic)
- ✓ Explainable (proof trace)
- ✓ No hallucination

**Cons:**
- ✗ Requires formal knowledge representation
- ✗ Can't handle ambiguity
- ✗ Limited to formalizable knowledge
- ✗ High complexity

**When to use:** High-stakes domains requiring correctness guarantees (medical, legal).

### Approach C: Ontology-First Hybrid (RECOMMENDED)

**Architecture:**
```
Question → Classify type → Route to strategy
    ├─ Temporal → Deterministic (no LLM)
    ├─ Causal → Graph traversal → Template synthesis
    ├─ Calculation → Arithmetic (no LLM)
    └─ Semantic → LLM reasoning
```

**Pros:**
- ✓ Fast for structured questions (no LLM)
- ✓ Cheap (fewer LLM calls)
- ✓ Explainable (deterministic strategies)
- ✓ Flexible (LLM fallback for hard cases)
- ✓ Architecturally safe (read-only ontology)
- ✓ Incrementally buildable

**Cons:**
- ⚠ Moderate complexity (multiple strategies)
- ⚠ Requires question classification
- ⚠ Strategy development cost

**When to use:** Knowledge-intensive investigation with mix of structured and semantic questions (our use case).

**Performance estimate:**
- 40% of questions: Deterministic (no LLM) → <20ms, $0
- 30% of questions: Graph + template → <50ms, $0
- 30% of questions: LLM synthesis → 500ms+, $0.01/query

**Total: ~3x faster, ~70% cheaper than LLM-only.**

---

## Risk Assessment

### Risk 1: Deterministic strategies too brittle

**Scenario:** Real questions don't fit clean categories.

**Mitigation:**
- Confidence scoring for classification
- Low confidence → route to LLM (safe fallback)
- Track classification accuracy
- Expand deterministic coverage incrementally

**Measurement:** Track % questions routed to LLM. Target: <40%.

### Risk 2: Graph extraction inaccurate

**Scenario:** YAML frontmatter relationships incomplete/wrong.

**Mitigation:**
- Start with human-curated links
- Add LLM-assisted link suggestion (review before commit)
- Validate graph integrity (no dangling refs)
- Graceful degradation (if no graph, fallback to retrieval)

**Measurement:** Graph coverage (% documents with links). Target: >60%.

### Risk 3: Classification errors

**Scenario:** Question misclassified → wrong strategy → wrong answer.

**Mitigation:**
- Multi-label classification (question can be multiple types)
- Run multiple strategies in parallel for ambiguous questions
- Strategy voting (consensus answer)
- User feedback on strategy selection

**Measurement:** Classification accuracy. Target: >80%.

### Risk 4: Development complexity

**Scenario:** Maintaining multiple strategies increases code complexity.

**Mitigation:**
- Shared ontology interface (all strategies use same actions)
- Strategy isolation (no cross-dependencies)
- Comprehensive testing (evaluation framework catches regressions)
- Documentation (reasoning traces show strategy behavior)

**Measurement:** Test coverage. Target: >80%.

### Risk 5: User expectations

**Scenario:** Users expect magic LLM, don't understand deterministic strategies.

**Mitigation:**
- Show strategy used in UI ("This was answered using temporal reasoning")
- Explain speed/accuracy benefits
- Allow manual override ("Force LLM mode")
- Progressive disclosure (start simple, show advanced options)

**Measurement:** User satisfaction surveys.

---

## Success Criteria

### Quantitative Metrics

| Metric | Baseline | Phase 1 Target | Phase 2 Target | Phase 3 Target |
|--------|----------|----------------|----------------|----------------|
| **Overall F1** | 49.80% | 60% | 70% | 75% |
| **Temporal F1** | ~50% | **100%** | 100% | 100% |
| **Causal F1** | ~30% | 50% | **80%** | 85% |
| **Calculation F1** | ~40% | **100%** | 100% | 100% |
| **Multi-hop F1** | ~35% | 50% | **75%** | 80% |
| **Semantic F1** | ~60% | 65% | 70% | **75%** |
| **Avg Query Time** | 38ms (vector) | <50ms | <50ms | <30ms |
| **LLM Calls/Query** | 1-3 | 0.6 | 0.4 | 0.3 |

### Qualitative Goals

- [ ] **Explainability:** Every answer includes reasoning trace
- [ ] **Reliability:** Deterministic strategies never hallucinate
- [ ] **Cost:** 70% reduction in LLM API costs
- [ ] **Speed:** Sub-second response for 90% of questions
- [ ] **Safety:** Architectural guarantee of read-only investigation
- [ ] **Auditability:** Git history + reasoning traces = full audit log

---

## Decision Summary

### Immediate Decisions (This Week)

1. **Architecture:** Ontology-first hybrid (deterministic + LLM fallback)
2. **Storage:** Keep markdown, add implicit graph via YAML
3. **Retrieval:** Multi-query keyword baseline, add vector for semantic
4. **Reasoning:** Route by question type to specialized strategies
5. **Safety:** Read-only ontology, layer-by-layer risk elimination

### Implementation Order

1. **Phase 1 (Weeks 1-5):** Ontology-first architecture + deterministic strategies
2. **Phase 2 (Weeks 6-8):** Graph enhancement for causal/multi-hop
3. **Phase 3 (Weeks 9-10):** Hybrid retrieval optimization
4. **Phase 4 (Weeks 11-12):** Production integration

### Deferred Decisions (Revisit After Phase 1)

- Formal logic (Prolog, Lean) - high complexity, uncertain ROI
- Binary graph database - fails Lobotomy Test
- Reranking models - wait for retrieval bottleneck evidence
- Multi-turn conversation - start with single-shot investigation

### Abandoned Approaches

- ❌ Simple grep only - proven inadequate (0% F1)
- ❌ LLM-only - too slow, expensive, not explainable
- ❌ Binary storage - fails Lobotomy Test
- ❌ Policy-based security - prefer architectural guarantees

---

## Next Actions

### This Week (Week 1 of Phase 1)

**Monday-Tuesday:**
- [ ] Create `app/investigation/` directory
- [ ] Implement `ontology.py` (action registry)
- [ ] Write tests for ontology

**Wednesday-Thursday:**
- [ ] Implement `projection.py` (question classification)
- [ ] Test classifier on 30 evaluation questions
- [ ] Measure classification accuracy

**Friday:**
- [ ] Document ontology architecture
- [ ] Demo to team: "Watch deterministic temporal strategy"
- [ ] Plan Week 2 (governance layer)

### Checkpoints

**End of Week 2:** All 4 layers implemented and tested
**End of Week 3:** First deterministic strategy passing evaluation
**End of Week 5:** Ontology-first strategy integrated, benchmarked vs baseline
**End of Week 12:** Production deployment

---

## Theoretical Foundation

### Why Ontology-First Works

**Traditional approach:**
```
LLM has power → Policy restricts power → Hope LLM obeys
```
**Problem:** Security by policy (runtime check, can fail).

**Ontology-first approach:**
```
Design defines vocabulary → LLM only sees defined actions → Misuse impossible
```
**Benefit:** Security by construction (design-time guarantee).

**Key quote from agent-hypervisor:**
> "Injection attacks targeting email redirection become impossible not through policy enforcement but through architectural absence—there is no tool to call, no argument to pass."

### Why Deterministic-First Works

**Traditional approach:**
```
All questions → LLM → Hope for best
```
**Problem:** LLM overkill for structured questions, slow, expensive, unreliable.

**Deterministic-first approach:**
```
Classify question type → Route to appropriate tool → LLM only when needed
```
**Benefit:** Use the right tool for each job.

**Analogy:** You wouldn't use a neural network to add 2+2. You use arithmetic. Similarly, don't use LLM to compare dates—use date arithmetic.

### Why Progressive Enhancement Works

**Traditional approach:**
```
Build complete system → Test at end → Discover problems
```
**Problem:** Big bang integration, late discovery of failures.

**Progressive enhancement approach:**
```
Start simple (passes Lobotomy Test) → Add capabilities → Measure improvement
```
**Benefit:** Always have working system, empirically validate improvements.

**Layers:**
1. Markdown files (human-readable)
2. + Keyword search (basic retrieval)
3. + Vector search (semantic retrieval)
4. + Graph traversal (multi-hop reasoning)
5. + Deterministic strategies (structured reasoning)
6. + LLM synthesis (semantic reasoning)

Each layer adds capability without breaking previous layers.

---

## References

### Core Documents

- **ONTOLOGY_FIRST_ROADMAP.md** - Implementation plan
- **COMPLETE_LANDSCAPE.md** - Current state overview
- **ARCHITECTURAL_PRINCIPLES.md** - Lobotomy Test + MCP constraints
- **ARCHITECTURE_TRADEOFFS.md** - Retrieval × Reasoning dimensions
- **STORAGE_DIMENSION.md** - Storage structure options
- **MISSING_DIMENSIONS.md** - Unexplored experimental space
- **AGENT_HYPERVISOR_CONCEPTS.md** - Ontology-first inspiration

### Evaluation Data

- **evaluation/questions.json** - 12 easy test questions
- **evaluation/questions-hard.json** - 18 hard test questions
- **evaluation/results/** - Baseline performance data

### Code

- **evaluation/evaluate.py** - Evaluation framework
- **app/routes/search.py** - Current search endpoint (to be replaced)
- **app/services/storage.py** - Git-backed markdown storage

---

## Conclusion

We have a clear, empirically-validated path forward:

1. **Test-driven:** 30 questions with known answers guide development
2. **Architecturally safe:** Ontology-first, read-only by design
3. **Incrementally buildable:** Progressive enhancement from simple to complex
4. **Empirically measured:** Evaluation framework validates improvements

**The radical insight:**
> Don't ask "How can we make the LLM do everything?"
> Ask "What can we solve deterministically, and use LLM only when necessary?"

**Result:** Faster, cheaper, more reliable, and architecturally safer than LLM-only approaches.

**Status:** Ready to begin Phase 1 implementation.

---

**Let's build it.** 🚀
