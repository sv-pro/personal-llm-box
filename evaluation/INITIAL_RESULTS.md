# Initial Evaluation Results

**Date:** 2026-03-26
**Purpose:** Baseline evaluation of retrieval strategies for investigation board

## Summary

Built a test-driven evaluation framework with 12 questions (5 trivial, 7 non-trivial) and 6 sample knowledge documents. Tested two initial strategies.

## Results

### Strategy Comparison

| Metric | simple_grep | multi_query |
|--------|-------------|-------------|
| **Overall Recall** | 0.00% | **96.67%** |
| **Overall Precision** | 0.00% | 37.64% |
| **Overall F1** | 0.00% | 49.80% |
| **Avg Query Time** | 0.34ms | 2.99ms |
| **Found All Sources** | 0/12 | 10/12 |

### By Question Type

**Trivial Questions (5 total):**
- multi_query: 100% recall, 21.67% precision, 35.14% F1
- Found all relevant sources for all trivial questions ✓

**Non-Trivial Questions (7 total):**
- multi_query: 94.29% recall, 49.05% precision, **60.27% F1**
- Found all relevant sources for 5/7 non-trivial questions
- Missed complete source set on 2 questions

## Key Insights

### 1. Current Search Won't Work for Natural Language Questions

The `simple_grep` strategy (which mirrors `app/routes/search.py`) performs literal substring matching. When given a full question like "What port does the API Gateway run on?", it searches for that entire string in documents.

**Result:** 0% recall - finds nothing

**Why:** Current search is designed for keyword queries ("API Gateway port"), not natural language questions.

### 2. Keyword Extraction is Critical

The `multi_query` strategy extracts keywords from questions (removing stopwords like "what", "is", "the"). This simple improvement:

- ✅ Achieves 96.67% recall overall
- ✅ Finds all sources for 10/12 questions
- ✅ Works for both trivial and non-trivial questions
- ❌ Low precision (37.64%) - too many false positives

### 3. Non-Trivial Questions Need Better Ranking

multi_query finds almost all relevant documents (94.29% recall) but also retrieves many irrelevant ones (49.05% precision).

**Problem:** Documents are scored only by keyword count. A document mentioning "memory" and "leak" scores the same whether it contains the answer or just mentions the problem.

**Solution needed:** Better relevance ranking (BM25, TF-IDF, or semantic similarity)

### 4. Speed is Not the Bottleneck

Even with naive implementation:
- multi_query: 2.99ms average
- Processes 6 documents in <4ms
- Fast enough for real-time use

**Insight:** We can afford more sophisticated retrieval methods without hurting UX.

## Questions Where We Failed

### simple_grep: All 12 questions (0/12)
Complete failure due to literal string matching.

### multi_query: 2 questions failed to find all sources

**non-trivial-5:** "What were all the tasks completed in the January sprint?"
- Expected: 5 sources
- Retrieved: Found most but missed some connections
- Reason: Very broad question requiring synthesis across all docs

**non-trivial-6:** "In what order were the sprint tasks completed?"
- Expected: 5 sources with temporal reasoning
- Retrieved: Found some but incomplete
- Reason: Needs date extraction and timeline construction

## What This Tells Us

### For Investigation Board Development:

1. **Phase 1: Query Understanding** (CRITICAL)
   - Implement keyword extraction
   - Handle natural language questions
   - Without this, nothing else matters

2. **Phase 2: Relevance Ranking** (HIGH)
   - BM25 or TF-IDF scoring
   - Current keyword-count scoring is too naive
   - Will improve precision dramatically

3. **Phase 3: Multi-Document Synthesis** (MEDIUM)
   - For questions requiring 4-5 documents
   - Current approach finds docs but doesn't synthesize
   - Needs LLM integration

4. **Phase 4: Temporal/Calculation Reasoning** (FUTURE)
   - Extract dates, numbers
   - Perform calculations
   - Construct timelines

### Success Path

**Quick Win:** Implement BM25 ranking
- Expected impact: Precision improves from 37% to 60%+
- Maintains high recall
- Small implementation effort

**Medium Win:** Add query expansion
- Synonyms and related terms
- Expected impact: Recall improves to 99%+
- Catches edge cases

**Big Win:** Semantic search (vector embeddings)
- Understand concepts, not just keywords
- Expected impact: Find documents even with different terminology
- Higher implementation cost

## Next Steps

### Immediate
1. ✅ Baseline established - we have numbers to beat
2. ⏭️ Implement BM25 strategy in evaluate.py
3. ⏭️ Re-run evaluation and compare
4. ⏭️ If BM25 shows improvement, integrate into main API

### Short-term
- Add fuzzy matching for typos
- Implement query expansion with synonyms
- Test vector search (sentence-transformers)

### Long-term
- Multi-hop reasoning engine
- LLM-based answer synthesis
- Interactive investigation UI

## Validation

This evaluation proves the test-driven approach works:

✅ **Objective metrics** - Not subjective "it seems better"
✅ **Clear gaps identified** - Know exactly what to fix
✅ **Quantifiable progress** - Can measure improvement
✅ **Fast iteration** - 3ms evaluations enable rapid testing

## Recommendations

### For Current Project

Update `app/routes/search.py` to:
1. Extract keywords from natural language queries
2. Implement BM25 ranking
3. Return documents sorted by relevance

This alone would make the search much more useful for investigation.

### For Investigation Board

Don't build the full investigation engine yet. Instead:

1. **Sprint 1:** Improve retrieval to 80% F1 on non-trivial questions
   - Implement BM25
   - Add query understanding
   - Test with evaluation framework

2. **Sprint 2:** Add multi-hop reasoning
   - Implement iterative retrieval
   - Create new test questions for multi-hop
   - Measure improvement

3. **Sprint 3:** Build interactive UI
   - Visual investigation canvas
   - Human-in-the-loop feedback
   - Guided exploration

Each sprint validated by the evaluation framework.

---

**Conclusion:** The evaluation framework works. We have a clear path forward with measurable goals. Build incrementally, measure objectively, improve systematically.
