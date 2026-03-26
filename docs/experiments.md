# Retrieval Experiments

This branch (`experiments/retrieval`) is the parent branch for experimenting with different retrieval techniques.

## Purpose

The goal is to explore and test various search/retrieval methods without cluttering the `main` branch, which maintains a simple, proven grep-based search.

## Current Baseline (main branch)

**Implementation:** Simple full-text grep search
- **File:** `app/routes/search.py` (20 lines)
- **Algorithm:** Sequential file scan with substring matching
- **Performance:** ~50ms for 100 files, ~500ms for 1000 files
- **Accuracy:** Exact substring matches only (no typos, no semantics)
- **Resource:** Negligible storage, no indexing overhead
- **User Experience:** Simple, fast for small datasets, no learning curve

## Active Experiments

### None yet

Create a new branch from `experiments/retrieval` to start:

```bash
git checkout experiments/retrieval
git checkout -b experiments/retrieval/vector-search
# ... implement your experiment
```

## Completed Experiments

None yet.

## Experiment Guidelines

### 1. Branch Naming

Use descriptive names:
- `experiments/retrieval/vector-search`
- `experiments/retrieval/fts5`
- `experiments/retrieval/whoosh`
- `experiments/retrieval/hybrid-bm25-vector`

### 2. Required Documentation

Each experiment branch must have:

**In branch root:**
- `EXPERIMENT_<NAME>.md` - Detailed findings
- `requirements-experiment.txt` - Additional dependencies
- `BENCHMARK_RESULTS.md` - Performance data

**In experiment file:**
```python
"""
Experiment: Vector Search with Sentence Transformers

Status: In Progress / Completed / Abandoned
Author: <your name>
Date: 2026-03-25

Hypothesis:
    Semantic search will improve retrieval quality for conceptually
    related documents even when exact keywords don't match.

Implementation:
    - Use sentence-transformers/all-MiniLM-L6-v2 (80MB model)
    - Embed documents on save
    - Store embeddings in vector_embeddings.db
    - Search using cosine similarity

Expected Trade-offs:
    + Better semantic matching
    + Find related concepts
    - Slower indexing (embed on save)
    - More storage (embeddings)
    - Need to load model
"""
```

### 3. Testing Checklist

Before merging to main, verify:

- [ ] Works with existing knowledge base
- [ ] Doesn't break other endpoints
- [ ] Performance is acceptable
- [ ] Memory usage is reasonable
- [ ] Dependencies are acceptable
- [ ] Code follows project conventions
- [ ] Documentation is complete
- [ ] Backward compatible or migration path provided

### 4. Benchmark Template

Test with these scenarios:

**Dataset:**
- 10 files (~1KB each)
- 100 files (~2KB each)
- 1000 files (~5KB each)

**Queries:**
- Exact keyword: `"python"`
- Phrase: `"machine learning"`
- Semantic: `"AI techniques"` (should match "neural networks", "LLMs")
- Typo: `"machne learning"` (fuzzy matching test)
- Multi-word: `"python data analysis"`

**Metrics:**
- **Precision:** Relevant results / Total results
- **Recall:** Relevant results / All relevant documents
- **Query time:** Average over 10 runs
- **Indexing time:** Time to index 1000 documents
- **Storage overhead:** Index size / Original content size
- **Memory usage:** Peak RAM during query

### 5. Decision Matrix

| Criteria | Weight | Score (1-5) | Weighted |
|----------|--------|-------------|----------|
| Query Speed | 3x | ? | ? |
| Accuracy | 3x | ? | ? |
| Easy to Use | 2x | ? | ? |
| Storage Overhead | 1x | ? | ? |
| Setup Complexity | 1x | ? | ? |
| **Total** | | | **?** |

**Threshold for merge to main:** Total score ≥ 35

## Ideas to Explore

### High Priority

1. **SQLite FTS5** (fast, built-in, proven)
   - Difficulty: Low
   - Impact: High
   - Time estimate: 2-4 hours

2. **Vector Search** (semantic matching)
   - Difficulty: Medium
   - Impact: High
   - Time estimate: 4-8 hours

### Medium Priority

3. **BM25 Ranking** (relevance scoring)
   - Difficulty: Low
   - Impact: Medium
   - Time estimate: 2-3 hours

4. **Fuzzy Matching** (typo tolerance)
   - Difficulty: Low
   - Impact: Medium
   - Time estimate: 1-2 hours

### Low Priority

5. **Knowledge Graph** (relationship discovery)
   - Difficulty: High
   - Impact: Medium
   - Time estimate: 16+ hours

6. **Hybrid Search** (combine techniques)
   - Difficulty: High
   - Impact: High
   - Time estimate: 8-12 hours

## Resources

### Vector Search
- sentence-transformers: https://www.sbert.net/
- FAISS: https://github.com/facebookresearch/faiss
- Chroma: https://www.trychroma.com/

### Full-Text Search
- SQLite FTS5: https://www.sqlite.org/fts5.html
- Whoosh: https://whoosh.readthedocs.io/
- Tantivy: https://github.com/quickwit-oss/tantivy-py

### Ranking
- BM25: https://en.wikipedia.org/wiki/Okapi_BM25
- TF-IDF: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html

### Fuzzy Matching
- python-Levenshtein: https://github.com/maxbachmann/Levenshtein
- fuzzywuzzy: https://github.com/seatgeek/fuzzywuzzy

## Notes

- Keep experiments isolated (separate files, separate routes if possible)
- Don't modify core files unless necessary
- If modifying core files, make it toggleable (feature flag or separate endpoint)
- Document all dependencies and their sizes
- Consider deployment complexity (Docker, dependencies, etc.)
- Think about user experience (setup complexity, query syntax)

## Questions to Answer

For each experiment, answer:

1. **Why this technique?** What problem does it solve?
2. **What's the trade-off?** Speed vs accuracy vs complexity?
3. **How much better?** Quantify the improvement
4. **Is it worth it?** For a personal knowledge base of <5000 files?
5. **Can we maintain it?** Long-term sustainability

## Success Criteria

An experiment is ready for merge if:

1. **Performs better** than baseline in at least 2 metrics
2. **Doesn't regress** in any critical metric
3. **Adds acceptable overhead** (<10% storage, <100MB RAM)
4. **Maintains simplicity** (documented, easy to understand)
5. **Has test coverage** for new functionality
6. **Passes code review** (follows conventions, clean code)

## Current Status

- **Branch:** `experiments/retrieval`
- **Experiments Started:** 0
- **Experiments Completed:** 0
- **Merged to Main:** 0
- **Last Updated:** 2026-03-25

---

Ready to experiment! Start by creating a sub-branch:

```bash
git checkout experiments/retrieval
git checkout -b experiments/retrieval/my-experiment
# ... code, test, document
# ... create EXPERIMENT_MY-EXPERIMENT.md
git add .
git commit -m "Add <technique> retrieval experiment"
git push -u origin experiments/retrieval/my-experiment
```

When ready to merge:

```bash
# First merge to experiments/retrieval
git checkout experiments/retrieval
git merge experiments/retrieval/my-experiment

# Then (if proven) merge to main
git checkout main
git merge experiments/retrieval
```
