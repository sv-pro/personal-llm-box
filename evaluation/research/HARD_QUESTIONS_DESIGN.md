# Designing Hard Questions for Multi-Query Failure

## Problem: Current "Non-Trivial" Questions Are Too Easy

**Why multi_query succeeds (96.67% recall, 60.27% F1 on non-trivial):**

1. **Keywords overlap with answers** - Questions contain the same words as the answer documents
2. **Explicit answers** - Answers are stated directly in documents
3. **Single-hop retrieval sufficient** - Finding documents with keywords = finding the answer

**Example of "easy non-trivial":**
```
Question: "What was the root cause of the memory leak and how was it fixed?"
Keywords: ['root', 'cause', 'memory', 'leak', 'fixed']

Document: auth-memory-leak-investigation.md contains:
- "root cause"
- "memory leak"
- "fixed"
- Literally all keywords!

multi_query: Finds it easily ✓
```

## What Makes Questions Actually Hard?

### 1. Keyword Mismatch (Paraphrase Problem)

**Question uses different terminology than documents:**

```
Question: "What performance improvements were implemented?"
Documents mention: "latency reduction", "speed optimization", "faster response times"
Documents never use: "performance improvements"

multi_query: Searches for ['performance', 'improvements', 'implemented']
Result: Misses documents that use synonyms ✗
```

### 2. Inference Required (No Explicit Answer)

**Answer must be inferred from combining facts:**

```
Question: "Did the Redis migration solve the memory leak problem?"

Facts scattered across documents:
- Doc A: "Memory leak occurs during token renewals"
- Doc B: "TokenCache uses Redis for storage"
- Doc C: "Redis migration completed on Jan 25"
- Doc D: "Memory leak fixed on Jan 22" (BEFORE migration)

Answer: NO (leak was fixed before migration)
But no document says "migration did not solve leak"

multi_query: Finds all 4 documents (keyword matches) ✓
But cannot infer the answer ✗
Needs: Temporal reasoning + causal reasoning
```

### 3. Negation Questions (What Did NOT Happen?)

**Questions about absence of information:**

```
Question: "What sprint tasks were NOT completed?"

Documents mention:
- Memory leak: COMPLETED
- Timeout config: COMPLETED
- API docs: COMPLETED
- Lazy loading: ASSIGNED to Jordan (no completion doc)

Answer: Lazy loading was not completed
But no document says "lazy loading not completed"

multi_query: Finds sprint planning doc (mentions all tasks) ✓
Cannot determine which lack completion status ✗
```

### 4. Causal Chain Reasoning

**A causes B, B causes C, therefore A causes C:**

```
Question: "Why did dashboard load times improve?"

Causal chain:
- Redis-1 had SATA SSD → high latency (45ms)
- High latency → slow cache access
- Slow cache → dashboard loads in 2.1s
- Migration to Redis-2 (NVMe SSD) → low latency (8ms)
- Low latency → fast cache
- Fast cache → dashboard loads in 0.8s

Answer: "Because NVMe SSD is faster than SATA SSD"
But no single document states this complete chain

multi_query: Finds docs mentioning "dashboard", "load", "time" ✓
Cannot connect the causal chain ✗
```

### 5. Comparison Questions

**Requires understanding quality/trade-offs:**

```
Question: "Which would be faster: increasing timeout or optimizing processing?"

Documents mention:
- Timeout increased from 60s to 300s
- Processing rate: 1.2s per MB

Answer: Optimizing processing (timeout just avoids failure, doesn't improve speed)
But requires understanding difference between "avoiding timeout" vs "actual speed"

multi_query: Finds both timeout and processing docs ✓
Cannot compare approaches ✗
```

### 6. Contradiction Detection

**Multiple documents say conflicting things:**

```
Question: "What is the current Redis endpoint?"

- Sprint planning (Jan 18): "Redis at redis-1.internal.local"
- Infrastructure update (Jan 25): "Migrated to redis-2.internal.local"

Answer: redis-2.internal.local (more recent)
Requires: Temporal reasoning to resolve conflict

multi_query: Finds both documents ✓
Returns both conflicting answers ✗
```

### 7. Missing Information Detection

**Question cannot be answered with available information:**

```
Question: "How much memory did the authentication service use after the fix?"

Documents mention:
- Memory grew to 1.5GB before fix
- "Memory usage remained stable at ~250MB" in testing
- But no production deployment confirmation

Answer: "Unknown - only test environment metrics available"
Requires: Recognizing information gap

multi_query: Finds investigation doc ✓
Returns incomplete answer without caveat ✗
```

### 8. Multi-Hop with Disambiguation

**Same keywords in multiple unrelated contexts:**

```
Question: "What was the deadline for fixing the timeout issue?"

Documents mention:
- "Memory leak deadline: end of sprint" (deadline + fix)
- "Timeout increased to 300s" (timeout + fix)
- "Sprint goals" (has deadlines)

Which timeout? Which deadline? Which fix?

multi_query: Finds all docs mentioning timeouts and deadlines ✓
Cannot disambiguate which specific timeout issue ✗
```

## Strategy: Create Truly Hard Questions

### Approach 1: Add Decoy Documents

Add documents with similar keywords but different contexts:

```
New document: performance-testing.md
- Mentions "memory leak in test suite" (different leak!)
- Mentions "timeout in network tests" (different timeout!)

Now multi_query finds WRONG documents with same keywords
```

### Approach 2: Use Synonyms/Paraphrases

```
Question: "What bottleneck was eliminated?"
Answer: "High cache latency"
Documents use: "slow Redis", "cache performance issue"
Never use: "bottleneck", "eliminated"
```

### Approach 3: Require Inference

```
Question: "Could the memory leak have been prevented with better testing?"

Evidence:
- "Memory leak occurs under load (1000+ renewals in 5 min)"
- "Load testing revealed the issue"

Inference needed: Yes, load testing revealed it, so earlier load testing could have prevented it
But no document explicitly says this
```

### Approach 4: Temporal Reasoning

```
Question: "What problems existed between Jan 18 and Jan 22?"

Requires:
1. Identify date range
2. Find issues mentioned during that period
3. Exclude issues fixed before Jan 18
4. Exclude issues reported after Jan 22

multi_query cannot do temporal filtering
```

### Approach 5: Quantitative Reasoning

```
Question: "How many times faster is Redis-2 than Redis-1?"

Facts:
- Redis-1: 45ms latency
- Redis-2: 8ms latency

Answer: 45/8 = 5.625x faster
Requires: Extracting numbers and calculating

multi_query: Finds both facts ✓
Cannot calculate ✗
```

## Proposed Hard Questions

I'll create questions in these categories:

1. **Inference** (5 questions) - Answer not explicitly stated
2. **Temporal reasoning** (3 questions) - Requires understanding time sequence
3. **Causal reasoning** (3 questions) - Understanding cause-effect chains
4. **Negation** (2 questions) - What did NOT happen
5. **Comparison** (2 questions) - Which is better/faster/more effective
6. **Disambiguation** (3 questions) - Multiple things with same keywords
7. **Calculation** (2 questions) - Requires arithmetic

Total: 20 hard questions

These should cause multi_query to fail because:
- Keywords match multiple unrelated documents (low precision)
- Correct documents don't contain question keywords (low recall)
- Finding documents ≠ answering question (requires reasoning)

## Success Criteria

A question is "hard enough" if:
- multi_query F1 score < 30%
- Requires actual reasoning, not just document retrieval
- Cannot be answered by keyword matching alone

## Next Steps

1. Expand knowledge base (6 → 15 documents)
2. Add decoy documents with overlapping keywords
3. Write 20 hard questions
4. Test multi_query (expect poor performance)
5. This becomes the target for investigation board engine
