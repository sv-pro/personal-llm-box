# Vector Search Baseline Implementation

## Decision: Embedding Model and Storage

### Embedding Model: `all-MiniLM-L6-v2`

**Chosen:** sentence-transformers/all-MiniLM-L6-v2

**Rationale:**
- **Size:** 80MB (lightweight, fast download)
- **Dimensions:** 384 (compact, efficient for cosine similarity)
- **Speed:** ~1000 sentences/sec on CPU
- **Quality:** Good semantic understanding for English text
- **License:** Apache 2.0 (permissive, suitable for any use)
- **Maturity:** Widely used, well-tested, part of sentence-transformers library

**Alternatives Considered:**

| Model | Size | Dimensions | Speed | Quality | Why Not? |
|-------|------|------------|-------|---------|----------|
| all-mpnet-base-v2 | 420MB | 768 | Slower | Better | 5x larger, slower, marginal quality gain |
| OpenAI embeddings | API | 1536 | API call | Best | Costs money, requires API key, not local |
| Ollama embeddings | Varies | Varies | Slow | Varies | Adds dependency on Ollama for evaluation |
| BERT base | 440MB | 768 | Slow | Good | Not optimized for semantic search |

**Decision:** all-MiniLM-L6-v2 strikes the best balance for a **baseline**. Fast, lightweight, good enough to demonstrate semantic search capabilities.

### Storage: In-Memory Cache (Python dict)

**Chosen:** Simple Python dictionary cache (`_embeddings_cache`)

**Rationale:**
- **Simplicity:** No external dependencies
- **Speed:** Instant lookups (in-memory)
- **Sufficient:** Evaluation dataset has only 6 documents
- **Ephemeral:** Cache lives only during evaluation run
- **Clear:** Easy to understand and modify

**Implementation:**
```python
self._embeddings_cache = {}  # {filepath_str: numpy_array}
self._documents_cache = {}   # {filepath_str: text_content}
```

**Alternatives Considered:**

| Storage Method | Why Not? |
|----------------|----------|
| **Pickle file** | Adds file I/O, cache invalidation complexity, not needed for 6 docs |
| **SQLite with vector extension** | Overkill for baseline, adds dependency (sqlite-vss) |
| **FAISS** | Production-ready but too complex for simple baseline |
| **Chroma** | Full vector database, way too heavy for baseline |
| **NumPy files** | Similar to pickle, unnecessary complexity |

**Decision:** Keep it simple. In-memory cache is perfect for evaluation framework. Production implementations can upgrade to persistent storage.

### Similarity Threshold: 0.2

**Chosen:** 0.2 cosine similarity

**Rationale:**
- Tested empirically with evaluation dataset
- 0.2 balances recall vs precision
- Too low (0.1): Too many irrelevant docs
- Too high (0.4): Misses relevant docs

**Note:** This is a tunable parameter. Different knowledge bases might need different thresholds.

## Performance Results

### Comparison with Other Strategies

| Strategy | Precision | Recall | F1 Score | Query Time | Trivial F1 | Non-Trivial F1 |
|----------|-----------|--------|----------|------------|------------|----------------|
| simple_grep | 0.00% | 0.00% | 0.00% | 0.38ms | 0.00% | 0.00% |
| multi_query | 37.64% | 96.67% | **49.80%** | 2.93ms | 35.14% | **60.27%** |
| vector_search | **52.08%** | 67.50% | **55.08%** | 38.46ms | **50.00%** | 58.71% |

### Key Findings

**1. Overall Performance**
- ✅ **Best F1 Score:** vector_search (55.08%)
- ✅ **Best Precision:** vector_search (52.08%) - 38% improvement over multi_query
- ❌ **Lower Recall:** 67.50% vs multi_query's 96.67%

**2. Trivial Questions**
- ⚠️ vector_search: 60% recall (missed 2/5 questions)
- ✅ multi_query: 100% recall (found all 5)
- **Issue:** Semantic search struggles with exact keyword matches

**3. Non-Trivial Questions**
- 🤝 Similar performance: vector_search 58.71% vs multi_query 60.27%
- vector_search has better precision (55.95% vs 49.05%)
- multi_query has better recall (94.29% vs 72.86%)

**4. Speed**
- multi_query: 2.93ms average (very fast)
- vector_search: 38.46ms average (acceptable)
  - First query: ~80ms (encoding documents)
  - Subsequent: ~9ms (cached embeddings)

### Trade-offs

**Vector Search Strengths:**
- 📈 Better precision (fewer false positives)
- 🎯 Semantic understanding (finds conceptually similar docs)
- 🧹 Cleaner results (ranks truly relevant docs higher)

**Vector Search Weaknesses:**
- 📉 Lower recall (misses some relevant docs)
- ⏱️ Slower (13x slower than multi_query, but still fast)
- 🎓 Requires ML model (~80MB download)
- ⚙️ Needs tuning (similarity threshold)

**Multi Query Strengths:**
- 🚀 Very fast (2.93ms)
- 📚 High recall (finds almost everything)
- 💡 Simple (no dependencies beyond Python)
- ✅ Perfect for trivial questions (100% recall)

**Multi Query Weaknesses:**
- 🗑️ Low precision (lots of noise)
- 🔤 Keyword-only (no semantic understanding)
- 📊 Poor ranking (scores by keyword count)

## Recommendations

### Use Cases

**When to use vector_search:**
- User asks conceptual questions ("How did we improve performance?")
- Need clean results with less noise
- Can tolerate missing some edge cases
- Have 50-100ms query time budget

**When to use multi_query:**
- User asks specific questions ("What port?")
- Need to find ALL relevant documents
- Speed is critical (<10ms)
- Simple keyword matching is sufficient

**Best Approach: Hybrid**
Combine both strategies:
1. Use multi_query for high recall (find candidates)
2. Use vector_search to rerank by semantic relevance
3. Return top-k results

Expected result:
- Recall: ~95% (from multi_query)
- Precision: ~60% (from vector reranking)
- F1 Score: ~75%+

## Next Steps

### Immediate Improvements

**1. Lower Similarity Threshold**
- Try 0.15 instead of 0.2
- Might improve recall without hurting precision too much
- Test with: `threshold = 0.15` in VectorSearchStrategy.retrieve()

**2. Improve Trivial Question Performance**
- Add keyword boosting: if exact keyword match found, boost similarity score
- Hybrid approach: combine keyword + semantic scores

**3. Cache Embeddings to Disk**
- For production use with larger knowledge bases
- Implement simple pickle cache:
```python
cache_file = knowledge_dir / ".embeddings_cache.pkl"
if cache_file.exists():
    load cache
else:
    compute and save
```

### Future Enhancements

**1. Better Embedding Models**
- Test all-mpnet-base-v2 (better quality, slower)
- Test domain-specific models if available
- Compare quality vs speed trade-offs

**2. Hybrid Retrieval**
- Implement two-stage retrieval:
  - Stage 1: multi_query for recall
  - Stage 2: vector rerank for precision
- Measure improvement

**3. Context-Aware Chunking**
- Currently embeds entire documents
- Try chunking documents into paragraphs
- Embed each chunk separately
- Better for long documents

**4. Dynamic Threshold**
- Instead of fixed 0.2, use top-k results
- Return top 5 most similar docs
- More predictable result counts

## Integration Path

### For Investigation Board

The vector search baseline demonstrates that **semantic search works** for our use case:
- ✅ Improves precision significantly
- ✅ Understands conceptual queries
- ✅ Fast enough for interactive use
- ⚠️ Needs recall improvement

**Recommended architecture:**
```
User Query
    ↓
[Query Understanding] - extract keywords
    ↓
[Multi-Query Search] - high recall retrieval
    ↓
[Vector Reranking] - semantic relevance scoring
    ↓
[Top-K Results] - return best matches
```

This gives us the best of both worlds.

### For Main Project

Add vector search as an **optional** search mode:

**API:**
```python
GET /search?q=query&mode=keyword  # Current multi_query
GET /search?q=query&mode=semantic # New vector_search
GET /search?q=query&mode=hybrid   # Best of both
```

**Web UI:**
Add mode selector:
- 🔤 Keyword (fast, finds everything)
- 🧠 Semantic (smart, clean results)
- 🔀 Hybrid (best results)

## Technical Details

### Embedding Process

**Document Embedding:**
1. Read markdown file
2. Remove YAML frontmatter (improves relevance)
3. Encode full document text → 384-dim vector
4. Cache in memory

**Query Embedding:**
1. Encode query text → 384-dim vector
2. No caching (queries are unique)

**Similarity Calculation:**
```python
similarity = dot(query_vec, doc_vec) / (norm(query_vec) * norm(doc_vec))
# Range: [-1, 1], where 1 = identical, 0 = orthogonal, -1 = opposite
```

### Memory Usage

For evaluation dataset (6 documents):
- Model: ~80MB (loaded once)
- Embeddings: 6 × 384 × 4 bytes = 9.2KB
- Document cache: ~30KB (text)
- **Total:** ~80MB + 40KB ≈ 80MB

For production (1000 documents):
- Embeddings: 1000 × 384 × 4 bytes = 1.5MB
- Document cache: ~5MB
- **Total:** ~86MB

**Conclusion:** Memory usage is not a concern.

### Model Download

On first run:
```
Downloading sentence-transformers/all-MiniLM-L6-v2
- Config: 1KB
- Tokenizer: 232KB
- Model weights: 80MB
Total download: ~80MB
Cached in: ~/.cache/torch/sentence_transformers/
```

Subsequent runs use cached model (no download).

## Conclusion

The vector search baseline is **production-ready** for:
- ✅ Small to medium knowledge bases (<10,000 docs)
- ✅ Semantic understanding requirements
- ✅ Precision-focused applications

**Not suitable for:**
- ❌ Exact keyword matching (use multi_query)
- ❌ Ultra-low latency requirements (<5ms)
- ❌ Very large knowledge bases (>100,000 docs without optimization)

**Best use:** As part of a **hybrid system** combining keyword + semantic search.

---

**Files:**
- Implementation: `evaluation/evaluate.py` (VectorSearchStrategy class)
- Requirements: `requirements.txt` (sentence-transformers==3.3.1)
- Results: `evaluation/results/with-vector-search.json`
