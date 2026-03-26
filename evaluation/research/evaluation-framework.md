# Evaluation Framework for Investigation Board

## Overview

This evaluation framework implements a **test-driven approach** to building the investigation board engine. Instead of building features and then testing them, we start with a comprehensive test dataset and build the system to pass increasingly difficult tests.

## Philosophy: Build Backwards

Traditional approach:
1. Build retrieval system
2. Test it
3. Find problems
4. Fix and repeat

**Our approach:**
1. ✅ Define success criteria (questions + expected answers)
2. ✅ Create test dataset with known complexity levels
3. ⏭️ Test baseline system
4. ⏭️ Identify gaps
5. ⏭️ Build features to close gaps
6. ⏭️ Measure improvement objectively

## Directory Structure

```
evaluation/
├── README.md                 # This file
├── questions.json            # Test questions with expected answers
├── evaluate.py              # Evaluation script
├── knowledge/               # Sample knowledge base
│   ├── 2026-01-15-architecture-overview.md
│   ├── 2026-01-18-sprint-planning-notes.md
│   ├── 2026-01-22-auth-memory-leak-investigation.md
│   ├── 2026-01-25-infrastructure-update.md
│   ├── 2026-01-28-timeout-configuration.md
│   └── 2026-02-01-api-documentation.md
└── results/                 # Evaluation results (generated)
```

## Test Dataset

### Knowledge Base
6 markdown documents about a fictional software project:
- Architecture documentation
- Sprint planning notes
- Bug investigation reports
- Infrastructure updates
- Configuration changes
- API documentation

Information is **intentionally scattered** across documents to simulate real-world knowledge bases where answers require synthesis.

### Questions (12 total)

**Trivial Questions (5):** Direct lookup, answer in single document
- Example: "What port does the API Gateway run on?" → Answer: 8000

**Non-Trivial Questions (7):** Require multi-hop reasoning across documents
- **Multi-hop reasoning** (4 questions): Connect information from 2-5 documents
- **Calculation reasoning** (1 question): Extract numbers and perform calculations
- **Synthesis** (1 question): Aggregate information across all documents
- **Temporal reasoning** (1 question): Construct timeline from dates
- **Investigative** (1 question): Infer answers from indirect evidence

### Difficulty Levels
- **Level 1** (5 questions): Single document lookup
- **Level 2** (2 questions): Simple multi-hop or calculation
- **Level 3** (3 questions): Complex multi-hop with 3-4 documents
- **Level 4** (2 questions): Synthesis or investigation requiring deep reasoning

## Running Evaluations

### Basic Usage

Test the baseline (simple grep) strategy:
```bash
python evaluation/evaluate.py --strategy simple_grep
```

Test improved multi-query strategy:
```bash
python evaluation/evaluate.py --strategy multi_query
```

Test all strategies and save results:
```bash
python evaluation/evaluate.py --strategy all --output results/comparison.json
```

### Output

The script prints a summary:
```
================================================================================
EVALUATION RESULTS: simple_grep
================================================================================

OVERALL (12 questions):
  Precision:       45.23%
  Recall:          67.89%
  F1 Score:        54.32%
  Source Coverage: 67.89%
  Avg Query Time:  12.45ms
  Found All:       3/12
  Found Any:       9/12

TRIVIAL (5 questions):
  Precision:       85.00%
  Recall:          100.00%
  F1 Score:        91.89%
  Source Coverage: 100.00%
  Avg Query Time:  8.21ms
  Found All:       5/5
  Found Any:       5/5

NON TRIVIAL (7 questions):
  Precision:       18.75%
  Recall:          45.83%
  F1 Score:        26.67%
  Source Coverage: 45.83%
  Avg Query Time:  15.32ms
  Found All:       0/7
  Found Any:       4/7
```

## Metrics Explained

### Document Retrieval Metrics

**Precision**: What % of retrieved documents are relevant?
- Formula: `relevant_retrieved / total_retrieved`
- High precision = few irrelevant results

**Recall**: What % of relevant documents were retrieved?
- Formula: `relevant_retrieved / total_relevant`
- High recall = didn't miss important documents

**F1 Score**: Harmonic mean of precision and recall
- Formula: `2 * (precision * recall) / (precision + recall)`
- Balances precision and recall

**Source Coverage**: Did we find all expected source documents?
- Same as recall for document retrieval
- Critical for multi-hop questions

**Query Time**: How fast is retrieval?
- Measured in milliseconds
- Important for interactive investigation

### Success Criteria

**Trivial Questions:**
- Target: 100% recall, 80%+ precision
- Baseline should handle these perfectly

**Non-Trivial Questions:**
- Source Coverage: Goal is 80%+ (find most relevant docs)
- F1 Score: Goal is 60%+ (balance precision/recall)
- This is where improvements are needed

## Adding New Retrieval Strategies

The evaluation framework is designed to be **pluggable**. Add new strategies by implementing the `RetrievalStrategy` protocol:

```python
class MyNewStrategy:
    @property
    def name(self) -> str:
        return "my_strategy"

    def retrieve(self, query: str, knowledge_dir: Path) -> RetrievalResult:
        # Your retrieval logic here
        documents = [...]  # List of matching filenames
        snippets = [...]   # Text snippets from each document
        query_time_ms = ...

        return RetrievalResult(
            documents=documents,
            snippets=snippets,
            query_time_ms=query_time_ms,
            strategy=self.name
        )
```

Then add it to the `strategies` dict in `main()`:

```python
strategies = {
    'simple_grep': SimpleGrepStrategy(),
    'multi_query': MultiQueryStrategy(),
    'my_strategy': MyNewStrategy()  # Add your strategy
}
```

## Planned Strategies to Test

### Phase 1: Keyword-based Improvements
- ✅ `simple_grep` - Baseline (current implementation)
- ✅ `multi_query` - Extract keywords, score by coverage
- ⏭️ `bm25` - Proper relevance ranking
- ⏭️ `fuzzy_match` - Handle typos and variations

### Phase 2: Semantic Search
- ⏭️ `vector_search` - Embedding-based similarity
- ⏭️ `hybrid` - Combine keyword + semantic

### Phase 3: Multi-Hop Reasoning
- ⏭️ `graph_retrieval` - Build knowledge graph, traverse
- ⏭️ `iterative_retrieval` - Multiple rounds of retrieval
- ⏭️ `rerank` - Two-stage: broad retrieval + reranking

### Phase 4: Investigation Engine
- ⏭️ `react_agent` - Reasoning + Action loop with LLM
- ⏭️ `decompose_query` - Break into sub-questions
- ⏭️ `synthesis` - Combine retrieved docs with LLM

## Example: Analyzing a Non-Trivial Question

**Question:** "What was the root cause of the memory leak and how was it fixed?"

**Expected Sources:**
1. `2026-01-15-architecture-overview.md` - Mentions memory leak exists
2. `2026-01-18-sprint-planning-notes.md` - Discussion and assignment
3. `2026-01-22-auth-memory-leak-investigation.md` - Root cause and fix

**Challenge for Retrieval:**
- Simple keyword search for "memory leak" finds all 3 docs ✓
- But also finds unrelated mentions in other docs ✗
- Need to identify which docs contain the ANSWER vs just mentioning the problem

**Challenge for Investigation:**
- Must synthesize information across 3 documents
- Timeline: problem identified → assigned → investigated → fixed
- Technical details only in investigation doc
- Answer requires combining all three sources

**What a good system should do:**
1. Retrieve all 3 relevant documents (100% recall)
2. Avoid irrelevant documents (high precision)
3. Rank investigation doc highest (contains answer)
4. Extract and synthesize the complete answer

## Comparing Strategies

Run multiple strategies and compare results:

```bash
python evaluation/evaluate.py --strategy all --output results/comparison.json
```

Then analyze `results/comparison.json` to see:
- Which strategy has best F1 score overall?
- Which handles non-trivial questions best?
- What's the speed vs accuracy tradeoff?
- Where does each strategy fail?

## Progressive Improvement

Use evaluation results to guide development:

1. **Establish baseline**
   ```bash
   python evaluation/evaluate.py --strategy simple_grep --output results/baseline.json
   ```

2. **Identify weakest questions**
   - Look at questions with 0% recall
   - These are high-priority improvements

3. **Implement targeted improvement**
   - Add new retrieval strategy
   - Focus on fixing specific failure modes

4. **Re-evaluate**
   ```bash
   python evaluation/evaluate.py --strategy new_strategy --output results/new.json
   ```

5. **Compare**
   - Did non-trivial F1 improve?
   - Did we maintain trivial performance?
   - What's the speed impact?

6. **Iterate**

## Integration with Main Project

This evaluation framework is **independent** of the main personal-llm-box API. It serves as:

1. **Design guide**: Shows what capabilities the investigation board needs
2. **Test harness**: Validates retrieval improvements objectively
3. **Benchmark**: Measures progress toward investigation goals
4. **Prototype**: Can be adapted into the actual investigation engine

When a retrieval strategy proves effective in evaluation:
1. Implement it as a route in `app/routes/`
2. Add it to the web UI
3. Use evaluation metrics to set user expectations

## Next Steps

### Immediate
1. Run baseline evaluation
2. Identify biggest gaps
3. Choose first improvement to implement

### Short-term
- Implement BM25 ranking
- Add fuzzy matching
- Test vector search

### Long-term
- Build multi-hop reasoning
- Implement ReAct investigation loop
- Create interactive investigation UI

## Contributing New Questions

To add more test questions:

1. Edit `evaluation/questions.json`
2. Follow the schema:
```json
{
  "id": "unique-id",
  "type": "trivial" | "non-trivial",
  "category": "direct_lookup | multi_hop_reasoning | ...",
  "question": "The question text?",
  "expected_answer": "The complete answer",
  "source_documents": ["file1.md", "file2.md"],
  "reasoning": "Why this question tests that capability",
  "difficulty": 1-4,
  "required_connections": ["Step 1", "Step 2", ...]
}
```
3. Update statistics section
4. Re-run evaluations

## Key Insights

### Why This Approach Works

**Traditional testing:**
- Tests pass/fail functionality
- Hard to measure "quality" of retrieval
- Subjective evaluation

**This approach:**
- Quantifiable metrics (precision, recall, F1)
- Objective comparison between strategies
- Clear success criteria
- Reveals exactly where system fails

### What We Learn

Each evaluation run tells us:
- ✅ What works (high precision/recall questions)
- ❌ What fails (low precision/recall questions)
- 🎯 Where to focus next (lowest scoring question types)
- 📊 Cost/benefit of improvements (speed vs accuracy)

### Limitations

This framework doesn't measure:
- **Answer quality**: We measure document retrieval, not answer generation
- **User experience**: Interactive investigation not tested
- **Edge cases**: Limited to 12 curated questions
- **Scale**: Small knowledge base (6 docs)

Future work should add:
- LLM-based answer evaluation
- User study / A/B testing
- Larger question dataset
- Scaled knowledge base (100s of docs)

---

**Ready to start?**

```bash
cd /home/dev/code/sv-pro/personal-llm-box
python evaluation/evaluate.py --strategy simple_grep
```

Let the numbers guide your development! 📊
