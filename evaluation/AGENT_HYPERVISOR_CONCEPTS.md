# Agent Hypervisor Concepts Applied to Investigation Board

**Source:** https://github.com/sv-pro/agent-hypervisor (README.md)

**Status:** Exploring radical architectural concepts from parallel research

---

## Core Insight: Ontology-First Design

### The Radical Idea

**Traditional approach:**
```
LLM → Has access to all tools → Policy filters what it can use
```

**Ontology-first approach:**
```
Design-time → Define limited action vocabulary → LLM only sees what should exist
```

**Key quote from agent-hypervisor:**
> "Injection attacks targeting email redirection become impossible not through policy enforcement but through architectural absence—there is no tool to call, no argument to pass."

### Applied to Investigation Board

**Traditional investigation:**
```python
# LLM has access to everything, we filter/validate
tools = {
    'search_all_docs': lambda q: ...,
    'delete_doc': lambda id: ...,       # Dangerous!
    'update_doc': lambda id, content: ...,  # Dangerous!
    'search': lambda q: ...,
}

# Hope LLM doesn't misuse tools
answer = llm.use_tools(question, tools)
```

**Ontology-first investigation:**
```python
# Define ONLY the investigation-appropriate actions
investigation_ontology = {
    'find_documents_about': lambda topic: ...,     # Read-only
    'extract_date_from': lambda doc: ...,          # Pure function
    'compare_dates': lambda d1, d2: ...,           # Pure function
    'traverse_related_to': lambda doc: ...,        # Navigation only
}

# Deletion, modification don't exist in this ontology
# LLM can't even attempt to modify because the action doesn't exist
```

**Benefit:** Security/safety by construction, not by validation.

---

## Four-Layer Architecture

### Layer 0: Execution Physics (What is Physically Impossible)

**Agent-hypervisor context:** OS-level constraints, network isolation

**Investigation board context:** Storage/compute constraints

```python
# Layer 0: Physical constraints
- Knowledge files are read-only to investigation process
- Indexes are in-memory (can't corrupt disk state)
- No network access during investigation (offline-capable)
- No file system writes except to designated temp space
```

**Implication:** Even if LLM goes rogue, physical limits prevent damage.

### Layer 1: Base Ontology (What Actions Exist) [Design-Time]

**Agent-hypervisor context:** Define tool vocabulary at design time

**Investigation board context:** Investigation-specific action vocabulary

```python
# Layer 1: Base ontology for investigation
class InvestigationOntology:
    """Actions that exist in investigation world"""

    # Observation actions (read-only)
    observe_documents: (query: str) -> List[Document]
    observe_timeline: (start: Date, end: Date) -> List[Event]
    observe_entities: (doc: Document) -> List[Entity]
    observe_relationships: (entity: Entity) -> List[Relation]

    # Reasoning actions (pure functions, no side effects)
    compare_dates: (d1: Date, d2: Date) -> Comparison
    calculate: (expression: str) -> Number
    check_contradiction: (statements: List[Statement]) -> bool

    # Navigation actions (follow structure)
    traverse_related: (doc: Document, max_hops: int) -> List[Document]
    traverse_causal: (event: Event) -> List[Event]

    # Actions that DO NOT EXIST (by design):
    # - modify_document
    # - delete_document
    # - send_email
    # - execute_code
    # - access_internet
```

**Key insight:** The investigation world is **read-only by nature**. Modification actions don't exist in the ontology.

### Layer 2: Dynamic Ontology Projection (What's Visible Now) [Runtime]

**Agent-hypervisor context:** Context-dependent visibility

**Investigation board context:** Question-dependent tool visibility

```python
# Layer 2: Dynamic projection based on question type
def project_ontology(question: Question) -> Ontology:
    """Show only relevant tools for this question type"""

    base = InvestigationOntology()

    if question.type == "temporal":
        # Temporal questions only see temporal tools
        return {
            'observe_timeline': base.observe_timeline,
            'compare_dates': base.compare_dates,
            'observe_documents': base.observe_documents,
        }

    elif question.type == "causal":
        # Causal questions see causal tools
        return {
            'observe_documents': base.observe_documents,
            'traverse_causal': base.traverse_causal,
            'observe_relationships': base.observe_relationships,
        }

    elif question.type == "calculation":
        # Calculation questions see math tools
        return {
            'observe_documents': base.observe_documents,
            'calculate': base.calculate,
        }

    # LLM only sees tools relevant to question type
    # Reduces confusion, improves accuracy
```

**Benefit:** Smaller tool set → Less confusion → Better reasoning

### Layer 3: Execution Governance (What May Execute) [Enforcement]

**Agent-hypervisor context:** Runtime execution policy

**Investigation board context:** Confidence-gated execution

```python
# Layer 3: Governance - even allowed actions have constraints
class ExecutionGovernor:
    def may_execute(self, action: Action, context: Context) -> bool:
        # Governance rules:

        # 1. Confidence threshold
        if action.estimated_cost > 0.1 and context.confidence < 0.7:
            return False  # Don't execute expensive actions with low confidence

        # 2. Recursion limit
        if context.call_depth > 5:
            return False  # Prevent infinite loops

        # 3. Resource limit
        if context.documents_examined > 100:
            return False  # Prevent exhaustive searches

        # 4. Time limit
        if context.elapsed_time > 5_000:  # 5 seconds
            return False  # Keep investigation bounded

        return True
```

**Benefit:** Safety even within allowed action space.

---

## AI Aikido: LLM at Design-Time, Determinism at Runtime

### The Concept

**Agent-hypervisor quote:**
> "Use LLM generative capabilities at design-time to produce deterministic security artifacts; runtime operates only deterministically."

**Translation:** Use LLM creativity during development, but run deterministic code in production.

### Applied to Investigation Board

**Design-time (development):**
```python
# Use LLM to generate reasoning traces during development
def design_temporal_reasoner():
    # Ask LLM to solve temporal questions
    examples = [
        ("Which happened first: A or B?", "Extract dates, compare, return earlier"),
        ("What occurred between X and Y?", "Filter events by date range"),
    ]

    # LLM generates implementation
    temporal_reasoner = llm.generate_code(
        task="temporal reasoning",
        examples=examples,
        constraints="pure functions, no side effects"
    )

    # Human reviews and approves
    if human.approve(temporal_reasoner):
        return temporal_reasoner
```

**Runtime (production):**
```python
# Use deterministic code generated at design-time
def answer_temporal_question(question):
    # No LLM involved - just deterministic logic
    dates = extract_dates(question)  # Regex, deterministic
    comparison = compare_dates(dates[0], dates[1])  # Math, deterministic
    return format_answer(comparison)  # Template, deterministic
```

**Benefit:** LLM creativity when designing, but deterministic reliability when running.

### Hybrid Approach for Investigation

```python
class HybridInvestigator:
    """Use LLM for semantics, logic for structure"""

    def answer(self, question):
        # Step 1: Use logic for structure
        question_type = classify_question_deterministic(question)  # Rules
        relevant_docs = retrieve_deterministic(question)  # Index lookup

        # Step 2: Use LLM for semantics (only if needed)
        if question_type in ['trivial', 'temporal', 'calculation']:
            # Deterministic reasoning sufficient
            return answer_deterministically(question, relevant_docs)
        else:
            # Need LLM for semantic understanding
            return answer_with_llm(question, relevant_docs)
```

**Result:** Use LLM only when necessary, deterministic reasoning when possible.

---

## Tool Virtualization: Specialized Over Generic

### The Concept

**Agent-hypervisor example:**

**Bad (generic tool):**
```python
send_email(to: str, body: str)  # Can be misused
```

**Good (specialized tool):**
```python
send_report_to_security(body: str)  # Recipient fixed, can't be redirected
```

### Applied to Investigation Board

**Bad (generic tools):**
```python
# Generic, dangerous
tools = {
    'search': lambda query, filter, limit, offset: ...,  # Too flexible
    'execute_query': lambda sql: ...,  # SQL injection risk
    'call_api': lambda url, method, body: ...,  # Arbitrary API access
}
```

**Good (specialized tools):**
```python
# Specialized, safe
tools = {
    # Each tool does ONE thing, parameters are constrained
    'find_memory_leaks': lambda: search(query="memory leak", filter="issues"),
    'find_events_in_january': lambda: search_temporal(start="2026-01-01", end="2026-01-31"),
    'get_related_documents': lambda doc: traverse_graph(doc, max_hops=2),
    'compare_two_dates': lambda d1, d2: compare_dates(parse(d1), parse(d2)),
}

# Instead of:
#   search(query="memory leak", filter=<INJECTED>)
# LLM calls:
#   find_memory_leaks()
# Parameters are baked in, can't be manipulated
```

**Benefit:** Each tool has ONE job, can't be misused for other purposes.

---

## Design-Time Human-in-the-Loop

### The Concept

**Agent-hypervisor insight:**
> "Human review belongs at manifest design/approval, not individual action runtime approval."

**Translation:** Humans review the DESIGN, not every action.

### Applied to Investigation Board

**Bad (runtime HITL):**
```python
# Ask human for every action (annoying, doesn't scale)
def investigate(question):
    docs = search(question)
    if ask_human("Should I read these docs?"):  # Annoying!
        facts = extract_facts(docs)
        if ask_human("Should I compare these facts?"):  # Annoying!
            answer = reason(facts)
            if ask_human("Is this answer correct?"):  # Annoying!
                return answer
```

**Good (design-time HITL):**
```python
# Human reviews the investigation STRATEGY, then system executes
class InvestigationStrategy:
    """Human-approved investigation approach"""

    def __init__(self):
        # Design-time: Human approves this strategy
        self.approved_by_human = True

    def investigate_temporal_question(self, question):
        """
        Strategy: For temporal questions
        1. Extract dates from question
        2. Search documents mentioning those dates
        3. Compare dates deterministically
        4. Return earlier date

        Approved by: Human (at design time)
        """
        # Runtime: Execute approved strategy without asking
        dates = self.extract_dates(question)
        docs = self.search_temporal(dates)
        comparison = self.compare_dates(dates)
        return self.format_answer(comparison)

# Human reviews strategy ONCE, then it runs automatically
```

**Benefit:** Human expertise at design time, automation at runtime.

---

## Implications for Investigation Board Architecture

### 1. Ontology-First Investigation

**Redesign around what SHOULD exist, not what SHOULDN'T:**

```python
# Current thinking: "Give LLM all tools, block bad ones"
all_tools = [search, modify, delete, send_email, ...]
allowed_tools = [t for t in all_tools if not is_dangerous(t)]

# New thinking: "Define only investigation-appropriate actions"
investigation_actions = {
    'observe': [...],    # Read-only
    'reason': [...],     # Pure functions
    'navigate': [...],   # Follow structure
}
# Modification/deletion don't exist in this world
```

### 2. Deterministic Core with LLM Shell

**Architecture:**

```
┌─────────────────────────────────────┐
│  LLM Layer (Semantic Understanding) │  ← Only for semantics
│  - Parse question intent            │
│  - Understand natural language      │
│  - Synthesize final answer          │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Deterministic Core                 │  ← Most work happens here
│  - Extract dates (regex)            │
│  - Compare dates (math)             │
│  - Search index (lookup)            │
│  - Traverse graph (algorithm)       │
│  - Calculate (arithmetic)           │
└─────────────────────────────────────┘
```

**Benefit:** LLM for creativity, determinism for reliability.

### 3. Specialized Tools Over Generic

**Replace:**
```python
search(query: str, filter: Dict, limit: int, ...)
```

**With:**
```python
find_memory_leaks()
find_timeout_issues()
find_events_in_january()
find_documents_by_author(author="Alex")
```

**Each tool is single-purpose, parameters baked in.**

### 4. Layer-by-Layer Risk Elimination

**Apply 4-layer model to investigation:**

```python
# Layer 0: Physics
- Knowledge is read-only file system
- No network access
- Memory-bounded

# Layer 1: Base Ontology
- Only observation/reasoning actions exist
- No modification actions in vocabulary

# Layer 2: Dynamic Projection
- Question type determines visible tools
- Temporal questions see temporal tools only

# Layer 3: Governance
- Confidence thresholds
- Recursion limits
- Resource limits
- Time limits
```

---

## Radical Implications

### Implication 1: Inverse the Control Flow

**Current thinking:**
```
Question → Retrieve docs → LLM reasons → Answer
```

**Ontology-first thinking:**
```
Question → Classify into ontology → Execute deterministic strategy → LLM only for synthesis
```

**Change:** LLM is the LAST step, not the main step.

### Implication 2: Graph Storage is an Ontology

**Current thinking:** Graph is a retrieval optimization

**Ontology thinking:** Graph DEFINES what can be navigated

```yaml
# Graph = Ontology of navigation
entities:
  - memory_leak
  - person
  - system
  - date

relationships:  # These ARE the navigation actions
  - fixed_by:     (issue → person)
  - occurred_in:  (issue → system)
  - happened_on:  (issue → date)
  - caused_by:    (issue → issue)

# You can ONLY navigate along defined edges
# Asking "which person fixed which issue" is VALID (edge exists)
# Asking "which person deployed which infrastructure" is INVALID (no edge)
```

**Benefit:** Graph structure = Action vocabulary for navigation.

### Implication 3: Questions Have Types, Types Have Strategies

**Current thinking:** All questions go through same pipeline

**Ontology thinking:** Question type determines execution strategy

```python
question_ontology = {
    'temporal': TemporalStrategy(
        actions=['extract_dates', 'compare_dates', 'search_temporal']
    ),
    'causal': CausalStrategy(
        actions=['traverse_causal_graph', 'build_chain']
    ),
    'calculation': CalculationStrategy(
        actions=['extract_numbers', 'calculate', 'format_result']
    ),
    'semantic': SemanticStrategy(
        actions=['llm_understand', 'llm_reason', 'llm_synthesize']
    ),
}

# Route question to appropriate strategy
strategy = question_ontology[classify(question)]
answer = strategy.execute(question)
```

**Benefit:** Specialized, deterministic strategies for each question type.

---

## Connection to Existing Dimensions

### How This Relates to 16 Dimensions

**This is a META-dimension:** How to think about composing the other dimensions.

**Ontology-first is not:**
- A retrieval strategy
- A reasoning approach
- A storage format

**Ontology-first IS:**
- A design philosophy
- An architectural constraint
- A composition pattern

**It answers:** "How do we put retrieval + reasoning + storage together SAFELY?"

### Practical Next Step

**Experiment:**

1. Define investigation ontology (what actions exist for investigation)
2. Implement 3 specialized strategies (temporal, causal, calculation)
3. Test on hard questions
4. Measure: Does specialization + determinism improve accuracy?

**Hypothesis:**
```
Specialized deterministic strategies for structural questions
  +
LLM only for semantic understanding
  =
Better accuracy than "LLM does everything"
```

---

## Questions for SEMANTIC_SPACE.md

Based on the README concepts, I'm particularly curious about:

1. **How does semantic space relate to ontology layers?**
   - Is semantic space the Layer 1 (base ontology)?
   - Or a different abstraction?

2. **How is the semantic space structured?**
   - Hierarchical?
   - Graph-based?
   - Vector space?

3. **How does semantic space enable "governed world"?**
   - Does it define boundaries of what's expressible?
   - Does it map to action vocabulary?

4. **Can semantic space replace traditional knowledge graphs?**
   - Or complement them?
   - Or is it a different paradigm entirely?

**Please share SEMANTIC_SPACE.md content - it seems to contain the key architectural insight!**

---

## Immediate Actionable Ideas

**For investigation board, inspired by agent-hypervisor:**

1. **Define Investigation Ontology**
   - List ONLY actions appropriate for investigation
   - Make modification impossible by design

2. **Specialized Strategies Over Generic**
   - TemporalStrategy for date questions
   - CausalStrategy for cause-effect questions
   - CalculationStrategy for arithmetic
   - Only fall back to LLM for semantics

3. **Layer Risk Elimination**
   - Layer 0: Read-only filesystem
   - Layer 1: Investigation-only actions
   - Layer 2: Question-type specific tools
   - Layer 3: Confidence + resource limits

4. **Design-Time vs Runtime**
   - Use LLM to design strategies (once)
   - Run deterministic code (always)

**This is genuinely radical - it inverts the typical "LLM-first" approach to "ontology-first with LLM last".**
