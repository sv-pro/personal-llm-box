# Hard Questions: Results and Analysis

## Summary

Created 18 hard questions requiring reasoning beyond keyword matching. Tested against multi_query retrieval strategy.

**Results:**
- Precision: 24.91% (vs 37.64% on easy questions) ✓ **35% worse**
- Recall: 97.50% (vs 96.67% on easy questions) ~ **Same**
- F1 Score: 38.13% (vs 49.80% on easy questions) ✓ **23% worse**

## Key Insight: Retrieval ≠ Answering

**Critical finding:** multi_query can **retrieve** relevant documents (97.50% recall) but cannot **answer** the questions correctly.

###Example: Disambiguation Question

**Question:** "Which memory leak was fixed first: production or test suite?"

**multi_query behavior:**
```
Keywords extracted: ['memory', 'leak', 'fixed', 'first', 'production', 'test', 'suite']

Documents found:
1. test-suite-issues.md (score: 5/7 keywords)
2. auth-memory-leak-investigation.md (score: 4/7 keywords)
3. architecture-overview.md (score: 2/7 keywords - mentions leak)
4. sprint-planning-notes.md (score: 2/7 keywords - mentions leak)

Retrieved: 4 documents
Relevant: 2 documents (test-suite-issues, auth-memory-leak-investigation)
Precision: 2/4 = 50%
```

**Problem:** multi_query returns the right documents but with noise. More critically, it cannot:
1. Extract dates from documents (Jan 12 vs Jan 22)
2. Compare dates temporally (which is earlier?)
3. **Answer: test suite (Jan 12) was fixed first**

**Conclusion:** Finding documents is not enough. Need reasoning engine to extract answer.

## Why These Questions Are Hard

### 1. Low Precision (24.91%)

**Cause:** Keyword ambiguity

Documents share keywords across different contexts:
- "memory leak" appears in:
  - Production auth service issue (Jan 22)
  - Test suite issue (Jan 12)
  - Architecture overview (general mention)

- "timeout" appears in:
  - File upload timeout (60s → 300s)
  - Network test timeout (30s → 60s)
  - Database connection timeout

multi_query returns ALL documents matching keywords, cannot disambiguate.

### 2. Cannot Perform Reasoning

**Temporal Reasoning:**
- Question: "What was system state on Jan 20th?"
- Requires: Understanding timeline, inferring state between events
- multi_query: Finds all documents with dates, cannot infer state

**Causal Reasoning:**
- Question: "Why did dashboard load times improve?"
- Requires: Understanding cause-effect (NVMe → low latency → fast cache → fast dashboard)
- multi_query: Finds documents mentioning "dashboard" and "improve", cannot connect causality

**Inference:**
- Question: "Did Redis migration fix the memory leak?"
- Requires: Comparing dates (leak fixed Jan 22, migration Jan 25), inferring "NO"
- multi_query: Finds both documents, cannot infer temporal relationship

**Negation:**
- Question: "Which sprint goal was NOT completed?"
- Requires: Finding all goals, checking for completion evidence, identifying absence
- multi_query: Finds sprint planning doc, cannot detect missing completion

**Calculation:**
- Question: "How much faster is Redis-2 vs Redis-1?"
- Requires: Extracting numbers (45ms, 8ms), performing division (45/8 = 5.625x)
- multi_query: Finds document, cannot calculate

### 3. Comparison of Easy vs Hard Questions

| Metric | Easy Questions | Hard Questions | Change |
|--------|----------------|----------------|--------|
| **Precision** | 37.64% | 24.91% | -35% ⬇ |
| **Recall** | 96.67% | 97.50% | +1% ➡ |
| **F1 Score** | 49.80% | 38.13% | -23% ⬇ |
| **Found All** | 10/12 (83%) | 16/18 (89%) | +6% ⬆ |

**Analysis:**
- Recall stayed high: multi_query still finds relevant documents
- Precision dropped significantly: more false positives due to keyword ambiguity
- F1 score dropped 23%: harder to get clean results

### 4. What Multi_Query Cannot Do

✅ **What it CAN do:**
- Find documents containing keywords
- Score by keyword coverage
- Handle natural language questions (extract keywords)
- High recall (finds almost everything)

❌ **What it CANNOT do:**
- Disambiguate (production leak vs test leak)
- Temporal reasoning (which happened first?)
- Causal reasoning (what caused what?)
- Inference (combine facts from multiple docs)
- Negation (what didn't happen?)
- Calculation (how much faster?)
- Comparison (which is better?)
- Recognize missing information

## What This Means for Investigation Board

### Current State: Retrieval Works

multi_query (and vector_search) can retrieve relevant documents with high recall.

**Not the problem:** Finding documents
**The problem:** Answering questions from documents

### What We Need: Reasoning Engine

An investigation board needs to:

1. **Retrieve documents** (multi_query ✓)
2. **Extract facts** from documents (need LLM)
3. **Reason over facts** (need LLM)
4. **Synthesize answer** (need LLM)

### Example: Full Investigation Flow

**Question:** "Which memory leak was fixed first?"

**Step 1: Retrieve** (multi_query)
```
Found documents:
- test-suite-issues.md
- auth-memory-leak-investigation.md
- architecture-overview.md (noise)
- sprint-planning-notes.md (noise)
```

**Step 2: Extract Facts** (LLM)
```
From test-suite-issues.md:
- Issue: memory leak in integration tests
- Fixed: 2026-01-12
- Status: RESOLVED

From auth-memory-leak-investigation.md:
- Issue: memory leak in authentication service
- Fixed: 2026-01-22
- Status: RESOLVED
```

**Step 3: Reason** (LLM)
```
Question asks "which first"
Compare dates:
- Test suite: 2026-01-12
- Auth service: 2026-01-22
2026-01-12 < 2026-01-22
Therefore: Test suite was fixed first
```

**Step 4: Synthesize Answer** (LLM)
```
Answer: "The test suite memory leak was fixed first on January 12, 2026.
The production authentication service memory leak was fixed 10 days later
on January 22, 2026."
```

## Hard Questions Breakdown by Category

### Disambiguation (2 questions)
**Challenge:** Multiple entities with same keywords
**Example:** "Which timeout affected end users?" (file processing vs network tests)
**Why hard:** Keywords match both, need context understanding

### Inference (2 questions)
**Challenge:** Answer not explicitly stated
**Example:** "Did Redis migration fix the leak?" (NO - leak fixed before migration)
**Why hard:** Requires temporal reasoning + causal reasoning + stating negative

### Temporal Reasoning (2 questions)
**Challenge:** Understanding time sequences
**Example:** "What was system state on Jan 20th?" (requires inferring state between events)
**Why hard:** Need to reconstruct timeline from multiple document dates

### Causal Reasoning (2 questions)
**Challenge:** Understanding cause-effect chains
**Example:** "Why did dashboard improve?" (NVMe → latency → cache → dashboard)
**Why hard:** Requires connecting multiple causal links

### Negation (2 questions)
**Challenge:** Finding absence of evidence
**Example:** "Which sprint goal was NOT completed?" (lazy loading has no completion doc)
**Why hard:** Looking for what ISN'T there, not what IS

### Comparison (2 questions)
**Challenge:** Evaluating relative quality
**Example:** "Which sprint had better outcomes?" (December vs January)
**Why hard:** Subjective judgment based on multiple factors

### Calculation (2 questions)
**Challenge:** Arithmetic operations
**Example:** "How much faster is Redis-2?" (45ms ÷ 8ms = 5.625x)
**Why hard:** Requires extracting numbers and computing

### Synthesis (1 question)
**Challenge:** Combining information from many sources
**Example:** "Summarize all January improvements" (4+ documents)
**Why hard:** Requires filtering by date + categorizing + synthesizing

### Contradiction (1 question)
**Challenge:** Resolving conflicting information
**Example:** "What is current Redis endpoint?" (sprint: redis-1, migration: redis-2)
**Why hard:** Need temporal reasoning to resolve (use more recent)

### Multi-hop (1 question)
**Challenge:** Chaining inferences
**Example:** "Who to contact about file uploads?" (uploads → timeout → Taylor → confirm)
**Why hard:** Multiple reasoning steps

### Paraphrase (1 question)
**Challenge:** Synonym/terminology mismatch
**Example:** "What bottleneck was eliminated?" (docs say "high latency", not "bottleneck")
**Why hard:** Semantic understanding beyond keywords

## Performance by Category

Based on manual analysis of multi_query results:

| Category | Can Retrieve Docs? | Can Answer Question? | Notes |
|----------|-------------------|---------------------|-------|
| Disambiguation | ✅ Yes | ❌ No | Returns all matching contexts |
| Inference | ✅ Yes | ❌ No | Finds facts but cannot infer |
| Temporal | ✅ Yes | ❌ No | Finds docs but no timeline |
| Causal | ✅ Yes | ❌ No | Finds docs but no causality |
| Negation | ⚠️ Partial | ❌ No | Finds some docs, misses gaps |
| Comparison | ✅ Yes | ❌ No | Finds docs but cannot compare |
| Calculation | ✅ Yes | ❌ No | Finds numbers but cannot calculate |
| Synthesis | ✅ Yes | ⚠️ Partial | Finds docs, user must synthesize |
| Contradiction | ✅ Yes | ❌ No | Returns both, cannot resolve |
| Multi-hop | ⚠️ Partial | ❌ No | Finds some hops, not all |
| Paraphrase | ❌ No | ❌ No | Synonym mismatch |

**Key Pattern:** multi_query retrieves documents but cannot reason.

## Next Steps

### Phase 1: Answer Extraction (LLM Integration)

Add LLM to extract answers from retrieved documents:

```
User question → multi_query (retrieve docs) → LLM (read docs + answer question)
```

Expected improvement:
- Can handle disambiguation (LLM reads context)
- Can perform reasoning (LLM trained on reasoning)
- Can synthesize (LLM trained on summarization)

But still limited:
- No multi-hop reasoning (single LLM call)
- No iterative investigation
- Relies on retrieving ALL relevant docs upfront

### Phase 2: ReAct Agent (Iterative Reasoning)

Implement ReAct loop:

```
Question → Think (plan) → Act (search) → Observe (read) → Think → Act...
```

Can handle:
- Multi-hop reasoning (iterate until answer found)
- Missing information detection (try search, realize not enough)
- Disambiguation (search with refined query)

### Phase 3: Investigation Canvas (Human-in-Loop)

Visual investigation board:
- Show reasoning graph
- Let user correct/guide
- Track hypotheses
- Manage contradictions

## Conclusion

**Hard questions created successfully:**
- ✓ F1 score dropped 23% (49.80% → 38.13%)
- ✓ Precision dropped 35% (37.64% → 24.91%)
- ✓ Require reasoning multi_query cannot perform

**Critical insight:**
> Document retrieval is necessary but not sufficient. Investigation requires reasoning.

**These questions are the target:**
- They represent real investigative questions
- They cannot be answered by keyword matching
- They require an actual investigation engine with reasoning capabilities

**Next build:** LLM-powered answer extraction to handle these hard questions.

---

**Files:**
- Questions: `evaluation/questions-hard.json`
- Design doc: `evaluation/HARD_QUESTIONS_DESIGN.md`
- Results: `evaluation/results/hard-questions-multi-query.json`
- Knowledge base: 10 documents (6 original + 4 new with ambiguity)
