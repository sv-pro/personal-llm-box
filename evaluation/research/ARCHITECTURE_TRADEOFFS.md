# Investigation Engine: Architecture Trade-offs

## The Spectrum

```
Pure Logic Engine <-----------------------------------------> Pure LLM Reasoning
        |                    |                |                      |
    Rules-Based          Hybrid          LLM-Assisted            Full LLM
```

## Edge 1: Reasoning LLM-Heavy, Dumb Retrieval

### Architecture

```
User Question
    ↓
Simple Retrieval (multi_query or vector_search)
    ↓
Retrieve top-k documents
    ↓
LLM: "Here are documents, answer the question"
    ↓
Answer
```

### Implementation

**Retrieval:** Keep it simple
- multi_query (keyword matching)
- OR vector_search (semantic similarity)
- Goal: High recall (find all potentially relevant docs)
- Don't worry about precision (LLM will filter)

**Reasoning:** Let LLM do everything
```python
prompt = f"""
Question: {user_question}

Relevant documents:
{document1}
{document2}
{document3}

Based on these documents, answer the question. If the answer requires:
- Comparing dates: extract and compare
- Calculating: perform the arithmetic
- Inferring: combine facts logically
- Disambiguating: use context to determine which entity

Answer:
"""

answer = ollama.generate(prompt)
```

### Pros ✅

**1. Fast to Build**
- Leverage existing LLM capabilities (reasoning, inference, synthesis)
- Don't need to implement temporal logic, causal reasoning, etc.
- Prototype in days, not months

**2. Flexible & Adaptive**
- Handles unexpected question types naturally
- LLM trained on diverse reasoning tasks
- Adapts to domain-specific terminology
- Can handle ambiguous/vague questions

**3. Natural Language Understanding**
- Understands paraphrases ("bottleneck" = "slow part")
- Handles synonyms automatically
- Context-aware interpretation
- Resolves pronouns and references

**4. Multi-Hop Reasoning**
- Can chain inferences across documents
- Synthesizes information naturally
- Builds coherent narratives
- Explains reasoning (if prompted)

**5. Low Code Complexity**
- Simple retrieval logic
- Simple prompt engineering
- No complex rule engines
- Easy to maintain

### Cons ❌

**1. Hallucination Risk**
- LLM might invent facts not in documents
- Confidence even when wrong
- Hard to detect fabrications
- Risk: User trusts wrong answer

**Mitigation:**
- Prompt: "Only use information from provided documents"
- Cite sources in answer
- Show retrieved documents to user
- Use retrieval-augmented generation (RAG) patterns

**2. Cost**
- Every question = LLM inference
- For local Ollama: GPU memory/compute
- For API: $ per token
- Scales linearly with usage

**Mitigation:**
- Use smaller models (llama3.2 instead of large models)
- Cache common questions
- Batch similar questions

**3. Speed**
- LLM inference: 100-500ms+ depending on model
- Longer for complex reasoning
- May not feel "instant"

**Mitigation:**
- Use faster models (quantized)
- Stream responses (show progress)
- Optimize prompt length

**4. Context Window Limits**
- Can only fit N documents in prompt
- For long documents: must chunk or summarize
- May miss relevant context

**Mitigation:**
- Iterative retrieval (multi-turn)
- Document summarization
- Hierarchical retrieval

**5. Non-Deterministic**
- Same question might get different answers
- Temperature/sampling affects output
- Hard to debug
- Hard to test

**Mitigation:**
- Set temperature=0 for deterministic output
- Use structured output (JSON)
- Extensive testing on evaluation questions

**6. Explainability**
- Black box reasoning
- Hard to audit "why this answer?"
- Compliance/legal issues in some domains

**Mitigation:**
- Prompt for chain-of-thought reasoning
- Ask LLM to show work
- Log reasoning steps

### Best For

- ✅ Rapid prototyping
- ✅ Exploratory/research questions
- ✅ Questions with unexpected patterns
- ✅ Small-medium scale (<1000 queries/day)
- ✅ Acceptable to have occasional errors
- ✅ Natural language flexibility important

### Not Suitable For

- ❌ Mission-critical systems (finance, healthcare)
- ❌ High-volume/low-latency requirements
- ❌ Strict determinism needed
- ❌ Zero tolerance for hallucinations
- ❌ Legal/compliance requirements for auditability

---

## Edge 2: LLM-Lite, Non-LLM Reasoning

### Architecture

```
User Question
    ↓
Query Understanding (NLP: parse question structure)
    ↓
Query Planner (determine what facts needed)
    ↓
Advanced Retrieval
    - Temporal index (dates)
    - Entity index (people, systems)
    - Relation index (causes, effects)
    ↓
Fact Extraction (structured parsing)
    ↓
Logic Engine
    - Temporal reasoning (date comparisons)
    - Causal reasoning (cause-effect graphs)
    - Arithmetic (calculations)
    - Inference rules (if X and Y then Z)
    ↓
Answer Synthesis (template-based)
    ↓
Answer
```

### Implementation Components

**1. Query Understanding**
```python
# Parse question into structured query
question = "Which memory leak was fixed first?"

parsed = {
    'type': 'comparison',
    'entities': ['memory leak'],
    'constraints': ['fixed'],
    'comparison_dimension': 'temporal',
    'comparison_direction': 'first'
}
```

**2. Advanced Retrieval**
```python
# Build specialized indexes
temporal_index = {
    '2026-01-12': ['test-suite-issues.md'],
    '2026-01-22': ['auth-memory-leak-investigation.md']
}

entity_index = {
    'memory_leak': [
        {'doc': 'test-suite-issues.md', 'type': 'test', 'status': 'fixed', 'date': '2026-01-12'},
        {'doc': 'auth-memory-leak-investigation.md', 'type': 'production', 'status': 'fixed', 'date': '2026-01-22'}
    ]
}

# Query: entities with 'memory_leak' tag
results = entity_index['memory_leak']
```

**3. Fact Extraction**
```python
# Extract structured facts
facts = []
for doc in results:
    facts.append({
        'entity': 'memory_leak',
        'type': extract_type(doc),  # production vs test
        'date_fixed': extract_date(doc),
        'source': doc.filename
    })
```

**4. Logic Engine**
```python
# Temporal reasoning
def which_first(facts, attribute='date_fixed'):
    sorted_facts = sorted(facts, key=lambda f: f[attribute])
    return sorted_facts[0]

answer_fact = which_first(facts)

# Template-based answer
answer = f"{answer_fact['type']} memory leak was fixed first on {answer_fact['date_fixed']}"
```

### Pros ✅

**1. Deterministic**
- Same query → same answer (always)
- Reproducible
- Testable
- Debuggable

**2. Fast**
- No LLM inference
- Index lookups: milliseconds
- Logic operations: microseconds
- Sub-10ms total latency possible

**3. Cheap**
- No GPU required
- No API costs
- Minimal compute
- Scales horizontally easily

**4. Explainable**
- Full audit trail
- "Answer came from doc X, line Y"
- "Compared dates: A < B, therefore A first"
- Regulatory compliance possible

**5. No Hallucination**
- Only states what's explicitly in documents
- Cannot invent facts
- Traceable to source
- High trust

**6. Precise Control**
- Exact behavior specified
- Fine-grained tuning
- Domain-specific optimizations
- Predictable edge cases

**7. Scalable**
- Handle millions of queries
- No rate limits
- Parallel processing
- Efficient resource usage

### Cons ❌

**1. Hard to Build**
- Implement query parser
- Build temporal reasoning engine
- Build causal reasoning engine
- Build inference engine
- Build entity extraction
- Build relation extraction
- Months of engineering

**2. Brittle**
- Fails on unexpected question formats
- "Which was fixed earlier?" vs "Which first?" need separate handling
- Lots of edge cases
- Constant patching

**3. Maintenance Heavy**
- Add rules for each question type
- Update parsers for new patterns
- Keep indexes in sync
- Debug complex rule interactions

**4. Limited Flexibility**
- Can't handle novel question types
- Requires code changes for new patterns
- Domain-specific (hard to generalize)
- Doesn't adapt automatically

**5. Natural Language Gap**
- Weak on paraphrasing
- Synonym handling requires dictionaries
- Context understanding limited
- Pronoun resolution hard

**6. Feature Engineering**
- Need to anticipate all question types
- Build specialized indexes for each
- Lots of custom code
- Hard to know when "done"

**7. Complex Codebase**
- Multiple interacting subsystems
- High cognitive load
- Hard to onboard new developers
- Testing complexity

### Best For

- ✅ Production systems with strict requirements
- ✅ High-volume, low-latency needs (>10k queries/sec)
- ✅ Deterministic behavior required
- ✅ Regulated industries (finance, medical)
- ✅ Zero tolerance for hallucinations
- ✅ Full auditability needed
- ✅ Known question patterns

### Not Suitable For

- ❌ Rapid prototyping
- ❌ Exploratory/research use cases
- ❌ Unpredictable question types
- ❌ Small teams (not enough engineering resources)
- ❌ Frequently changing requirements

---

## The Hybrid Middle Ground

### Architecture

```
User Question
    ↓
LLM: Parse into structured query
    ↓
Logic Engine: Execute structured query
    - Use indexes, logic, rules
    ↓
If simple: Return answer
If complex: Return facts
    ↓
LLM: Synthesize final answer from facts (if needed)
    ↓
Answer
```

### Hybrid Approach 1: LLM-Assisted Logic

**Use LLM for:**
- Query understanding (parse question)
- Fact extraction (extract dates, entities from text)
- Answer synthesis (make it readable)

**Use Logic for:**
- Retrieval (indexes, search)
- Reasoning (temporal, causal, arithmetic)
- Verification (check constraints)

**Example:**
```python
# Step 1: LLM parses question
parsed = llm_parse_query("Which memory leak was fixed first?")
# Returns: {'type': 'temporal_comparison', 'entity': 'memory leak'}

# Step 2: Logic retrieves candidates
candidates = entity_index['memory_leak']

# Step 3: LLM extracts facts
for doc in candidates:
    facts.append(llm_extract_facts(doc.content, entity='memory leak'))
# Returns: [{'type': 'test', 'date': '2026-01-12'}, ...]

# Step 4: Logic reasons
answer_fact = min(facts, key=lambda f: f['date'])

# Step 5: LLM synthesizes answer
answer = llm_synthesize(f"The {answer_fact['type']} leak was fixed on {answer_fact['date']}")
```

**Pros:**
- ✓ Best of both worlds
- ✓ LLM handles unstructured text
- ✓ Logic ensures correctness
- ✓ Explainable + flexible

**Cons:**
- ⚠️ More complex (two systems)
- ⚠️ Still has LLM costs
- ⚠️ Possible hallucination in fact extraction

### Hybrid Approach 2: Logic + LLM Fallback

**Default:** Use logic-based system

**Fallback:** If logic fails, use LLM

```python
try:
    # Try logic-based approach
    parsed = rule_based_parser(question)
    facts = index_retrieval(parsed)
    answer = logic_engine(facts)
except UnhandledQuestionType:
    # Fallback to LLM
    docs = simple_retrieval(question)
    answer = llm_reason(question, docs)
```

**Pros:**
- ✓ Fast/cheap for known patterns (logic)
- ✓ Flexible for new patterns (LLM)
- ✓ Gradual improvement (add rules over time)

**Cons:**
- ⚠️ Inconsistent (sometimes logic, sometimes LLM)
- ⚠️ Two codepaths to maintain

### Hybrid Approach 3: LLM + Verification

**Use LLM:** Generate answer

**Use Logic:** Verify answer

```python
# LLM generates answer
answer = llm_reason(question, docs)

# Logic verifies
facts = extract_facts_from_answer(answer)
verified = logic_verify(facts, ground_truth_docs)

if not verified:
    return "I'm not confident in this answer"
else:
    return answer
```

**Pros:**
- ✓ LLM flexibility
- ✓ Logic safety net
- ✓ Catches hallucinations

**Cons:**
- ⚠️ Verification as hard as answering
- ⚠️ False negatives (correct answer rejected)

---

## Recommendation for Personal LLM Box

### Phase 1: Start with LLM-Heavy (Rapid Validation)

**Why:**
- ✓ You have Ollama (local LLM already set up)
- ✓ Fast to build (days not months)
- ✓ Can immediately test against hard questions
- ✓ Learn what works/doesn't work
- ✓ Small scale (personal use, not production)

**Implementation:**
```python
def answer_question(question: str, knowledge_dir: Path) -> str:
    # 1. Simple retrieval
    docs = multi_query_retrieve(question, knowledge_dir, top_k=5)

    # 2. LLM reasoning
    prompt = f"""
    Question: {question}

    Documents:
    {format_docs(docs)}

    Answer the question based on the documents. If you need to:
    - Compare dates: extract and compare
    - Calculate: show your arithmetic
    - Infer: explain your reasoning

    Answer:
    """

    answer = ollama.generate(prompt)
    return answer
```

**Test immediately on hard questions:**
- See if LLM can handle temporal reasoning
- See if LLM can handle disambiguation
- Measure accuracy vs evaluation dataset

### Phase 2: Add Hybrid Elements (If Needed)

**If LLM works well:** Keep it simple

**If LLM struggles with specific patterns:**
- Add temporal index (for date questions)
- Add calculation engine (for arithmetic)
- Add entity disambiguation (for "which X" questions)

**Hybrid example:**
```python
def answer_question(question: str, knowledge_dir: Path) -> str:
    # Detect question type
    if is_calculation_question(question):
        # Use logic for arithmetic
        return logic_calculate(question, knowledge_dir)
    elif is_temporal_comparison(question):
        # Use temporal index
        return temporal_reason(question, knowledge_dir)
    else:
        # Use LLM
        return llm_reason(question, knowledge_dir)
```

### Phase 3: Move to Logic-Heavy (If Scaling)

**Only if:**
- Need to handle 1000s of queries/day
- Cost becomes significant
- Specific question patterns dominate
- Determinism required

**Then:** Build specialized logic for top patterns

---

## Decision Matrix

| Criterion | LLM-Heavy | Logic-Heavy | Hybrid |
|-----------|-----------|-------------|--------|
| **Time to build** | Days | Months | Weeks |
| **Flexibility** | High | Low | Medium |
| **Determinism** | Low | High | Medium |
| **Speed** | Medium | Very Fast | Medium |
| **Cost** | Medium | Very Low | Low |
| **Accuracy** | High* | High | Very High |
| **Explainability** | Low | High | Medium |
| **Maintenance** | Low | High | Medium |
| **Hallucination risk** | Medium | None | Low |
| **Scalability** | Medium | Very High | High |

*with good prompting and RAG patterns

---

## Concrete Recommendation

**For your personal-llm-box investigation board:**

### Start Here: LLM-Heavy
```python
# Simple MVP
1. Use multi_query for retrieval (already works)
2. Feed results to Ollama (already set up)
3. Test on hard questions
4. Measure: How many can it answer correctly?
```

**If >70% accuracy:** Ship it! LLM is good enough.

**If 40-70% accuracy:** Add hybrid logic for specific weak points

**If <40% accuracy:** Consider logic-heavy (or better LLM model)

### Bet: LLM-Heavy Will Work

**Why I think LLM will handle hard questions:**
- Modern LLMs trained on reasoning tasks
- Temporal reasoning: "2026-01-12 is before 2026-01-22" ✓
- Arithmetic: "45 / 8 = 5.625" ✓
- Disambiguation: "test suite leak vs production leak" ✓
- Inference: "leak fixed Jan 22, migration Jan 25, therefore migration didn't fix leak" ✓

**Test this hypothesis:**
```bash
# Run LLM on hard questions (build this next)
python evaluation/answer_with_llm.py --questions evaluation/questions-hard.json

# Compare with multi_query baseline
# multi_query F1: 38.13%
# Target LLM F1: >70%
```

### If You Want Maximum Control: Logic-Heavy

Build rule-based system for specific domains:
- Temporal questions → Temporal logic engine
- Calculation questions → Arithmetic engine
- Disambiguation → Entity resolution system

But this is **10x more work** for **marginal gain** at your scale.

---

## Next Step Proposal

**Build LLM-heavy answer engine and test it:**

1. Create `evaluation/answer_with_llm.py`
2. Implement LLM reasoning over retrieved docs
3. Run on hard questions dataset
4. Measure accuracy
5. **Let data guide decision:** If LLM scores >70% F1, use it. If not, add logic.

Want me to implement the LLM-heavy answer engine and test it against hard questions?
