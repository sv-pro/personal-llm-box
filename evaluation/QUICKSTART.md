# Evaluation Framework - Quick Start

## 5-Minute Guide to Test-Driven Retrieval Development

### What You Have

```
evaluation/
├── questions.json        # 12 test questions (5 trivial, 7 non-trivial)
├── knowledge/           # 6 sample documents
├── evaluate.py          # Evaluation script
└── results/             # Results from test runs
```

### Run Your First Evaluation

```bash
cd /home/dev/code/sv-pro/personal-llm-box
python evaluation/evaluate.py --strategy multi_query
```

**Output:**
```
OVERALL (12 questions):
  Precision:       37.64%
  Recall:          96.67%
  F1 Score:        49.80%
  Source Coverage: 96.67%
  Avg Query Time:  2.99ms
  Found All:       10/12
  Found Any:       12/12
```

**Interpretation:**
- ✅ 96.67% recall: Finds almost all relevant documents
- ⚠️ 37.64% precision: Lots of false positives
- ✅ 2.99ms: Fast enough for real-time use
- 🎯 Next goal: Improve precision to 60%+

### Compare Strategies

```bash
python evaluation/evaluate.py --strategy all --output results/comparison.json
```

### Look at Detailed Results

```bash
cat evaluation/results/baseline-comparison.json | jq '.evaluations[1].aggregate.non_trivial'
```

Shows performance on non-trivial (multi-hop) questions.

### Understand What You're Testing

**Trivial Questions** - Direct lookup:
```json
{
  "question": "What port does the API Gateway run on?",
  "expected_answer": "8000",
  "source_documents": ["2026-01-15-architecture-overview.md"]
}
```

**Non-Trivial Questions** - Multi-hop reasoning:
```json
{
  "question": "What was the root cause of the memory leak and how was it fixed?",
  "source_documents": [
    "2026-01-15-architecture-overview.md",   // Mentions leak exists
    "2026-01-18-sprint-planning-notes.md",  // Discussion
    "2026-01-22-auth-memory-leak-investigation.md"  // Root cause + fix
  ]
}
```

### Add Your Own Strategy

Edit `evaluation/evaluate.py`:

```python
class MyBetterStrategy:
    @property
    def name(self) -> str:
        return "my_better"

    def retrieve(self, query: str, knowledge_dir: Path) -> RetrievalResult:
        # Your improved retrieval logic here
        documents = [...]
        snippets = [...]
        query_time_ms = ...

        return RetrievalResult(
            documents=documents,
            snippets=snippets,
            query_time_ms=query_time_ms,
            strategy=self.name
        )
```

Add to strategies dict:
```python
strategies = {
    'simple_grep': SimpleGrepStrategy(),
    'multi_query': MultiQueryStrategy(),
    'my_better': MyBetterStrategy()  # Add this
}
```

Test it:
```bash
python evaluation/evaluate.py --strategy my_better
```

### Typical Development Loop

1. **Baseline** (done):
   ```bash
   python evaluation/evaluate.py --strategy multi_query --output results/baseline.json
   ```
   Result: 49.80% F1 overall, 60.27% F1 on non-trivial

2. **Improve** (your turn):
   - Implement BM25 ranking
   - Add to evaluate.py as `BM25Strategy`

3. **Test**:
   ```bash
   python evaluation/evaluate.py --strategy bm25 --output results/bm25.json
   ```

4. **Compare**:
   ```bash
   # Check if F1 improved
   cat results/baseline.json | jq '.evaluations[0].aggregate.overall.avg_f1'
   cat results/bm25.json | jq '.evaluations[0].aggregate.overall.avg_f1'
   ```

5. **Iterate**: Keep improving until you hit targets

### Success Targets

**Trivial Questions:**
- ✅ Recall: 100% (currently achieved)
- ⏭️ Precision: 80%+ (currently 21.67%)

**Non-Trivial Questions:**
- ✅ Recall: 90%+ (currently 94.29%)
- ⏭️ Precision: 60%+ (currently 49.05%)
- ⏭️ F1 Score: 70%+ (currently 60.27%)

### Quick Metrics Reference

**Precision**: How many retrieved docs are actually relevant?
- Low precision = lots of noise
- Fix: Better ranking, query understanding

**Recall**: Did we find all relevant docs?
- Low recall = missing important information
- Fix: Query expansion, semantic search

**F1 Score**: Balance of precision and recall
- Use this as your primary target metric
- Improving F1 means better overall retrieval

**Query Time**: How fast is retrieval?
- <10ms: Excellent (real-time)
- 10-50ms: Good (interactive)
- 50-200ms: Acceptable
- >200ms: Too slow for interactive use

### What to Build Next

Based on initial results, priority order:

1. **BM25 Ranking** (Highest Impact)
   - Expected: Precision 37% → 60%+
   - Difficulty: Low (100 lines of code)
   - Time: 2-3 hours

2. **Query Expansion** (High Impact)
   - Expected: Recall 96% → 99%+
   - Difficulty: Low
   - Time: 1-2 hours

3. **Vector Search** (Medium-High Impact)
   - Expected: F1 60% → 75%+
   - Difficulty: Medium
   - Time: 4-6 hours

4. **Multi-Hop Reasoning** (Transformational)
   - Expected: Can handle complex investigations
   - Difficulty: High
   - Time: 2-3 days

### Files to Read

1. **README.md** - Full documentation
2. **questions.json** - See what you're testing against
3. **INITIAL_RESULTS.md** - Baseline analysis
4. **evaluate.py** - The evaluation engine

### Common Questions

**Q: Why is simple_grep at 0%?**
A: It does literal string matching. Questions like "What port does X run on?" won't match any document text. This shows current search.py won't work for natural language queries.

**Q: Why is multi_query precision so low (37%)?**
A: It retrieves any document with keywords, even if barely relevant. Need better ranking to score true matches higher.

**Q: Can I test on my real knowledge base?**
A: Yes! Update `--knowledge-dir` parameter:
```bash
python evaluation/evaluate.py --strategy multi_query --knowledge-dir knowledge/
```

**Q: How do I add more test questions?**
A: Edit `evaluation/questions.json`, follow the schema, update statistics section.

### Next Steps

1. Read `INITIAL_RESULTS.md` to understand baseline
2. Pick an improvement strategy (recommend BM25)
3. Implement it in `evaluate.py`
4. Run evaluation and compare
5. Iterate!

---

**Start here:**
```bash
python evaluation/evaluate.py --strategy multi_query
```

Good luck! 🚀
