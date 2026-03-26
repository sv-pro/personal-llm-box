# Ontology-First Implementation Roadmap for Investigation Board

**Created:** 2026-03-26
**Purpose:** Practical roadmap for applying agent-hypervisor ontology-first concepts to investigation board

---

## Executive Summary

Traditional approach: LLM has access to all tools → Policy filters what it can use
**Ontology-first approach:** Design-time defines limited action vocabulary → LLM only sees what should exist

**Key insight:** Security/safety by construction, not by validation.

This document translates the radical architectural concepts from AGENT_HYPERVISOR_CONCEPTS.md into a concrete implementation plan for the personal-llm-box investigation board.

---

## Phase 1: Define Investigation Ontology (Week 1)

### Goal
Define ONLY the actions that should exist in an investigation context. Modification/deletion don't exist by design.

### Implementation

#### Step 1.1: Core Action Categories

```python
# app/investigation/ontology.py

from typing import Protocol, List, Dict
from datetime import date
from pathlib import Path

class InvestigationAction(Protocol):
    """Base protocol for all investigation actions"""
    @property
    def name(self) -> str: ...
    @property
    def category(self) -> str: ...
    def is_read_only(self) -> bool: ...


# Layer 1: Base Ontology - What Actions Exist
class ObservationActions:
    """Read-only observation of knowledge"""

    @staticmethod
    def find_documents_about(topic: str) -> List[Path]:
        """Find documents mentioning a topic"""
        pass

    @staticmethod
    def observe_timeline(start: date, end: date) -> List[Dict]:
        """Extract events within date range"""
        pass

    @staticmethod
    def observe_entities(document: Path) -> List[str]:
        """Extract entities (people, systems, concepts) from doc"""
        pass

    @staticmethod
    def observe_relationships(entity: str) -> List[Dict]:
        """Find relationships involving an entity"""
        pass


class ReasoningActions:
    """Pure functions with no side effects"""

    @staticmethod
    def compare_dates(d1: date, d2: date) -> Dict:
        """Deterministic date comparison"""
        pass

    @staticmethod
    def calculate(expression: str) -> float:
        """Safe arithmetic evaluation"""
        pass

    @staticmethod
    def check_contradiction(statements: List[str]) -> bool:
        """Logic-based contradiction detection"""
        pass

    @staticmethod
    def extract_dates(text: str) -> List[date]:
        """Regex-based date extraction"""
        pass


class NavigationActions:
    """Follow existing structure"""

    @staticmethod
    def traverse_related(doc: Path, max_hops: int = 2) -> List[Path]:
        """Follow document references"""
        pass

    @staticmethod
    def traverse_causal(event: Dict) -> List[Dict]:
        """Follow cause-effect chains"""
        pass

    @staticmethod
    def traverse_temporal(pivot: date, direction: str) -> List[Dict]:
        """Navigate timeline forward/backward"""
        pass


# Actions that DO NOT EXIST (by design):
# - modify_document
# - delete_document
# - send_email
# - execute_code
# - access_internet
# - write_file
```

#### Step 1.2: Ontology Registry

```python
# app/investigation/registry.py

from typing import Dict, Callable, Set
from enum import Enum

class ActionCategory(Enum):
    OBSERVE = "observe"
    REASON = "reason"
    NAVIGATE = "navigate"


class InvestigationOntology:
    """Registry of allowed investigation actions"""

    def __init__(self):
        self._actions: Dict[str, Callable] = {}
        self._categories: Dict[str, ActionCategory] = {}
        self._register_base_ontology()

    def _register_base_ontology(self):
        """Register read-only investigation actions"""

        # Observation actions
        self.register(
            "find_documents_about",
            ObservationActions.find_documents_about,
            ActionCategory.OBSERVE
        )
        self.register(
            "observe_timeline",
            ObservationActions.observe_timeline,
            ActionCategory.OBSERVE
        )
        # ... register all others

    def register(self, name: str, func: Callable, category: ActionCategory):
        """Register an action in the ontology"""
        self._actions[name] = func
        self._categories[name] = category

    def get_action(self, name: str) -> Callable:
        """Get action by name. Raises KeyError if doesn't exist."""
        return self._actions[name]

    def list_actions(self, category: ActionCategory = None) -> Set[str]:
        """List available actions, optionally filtered by category"""
        if category is None:
            return set(self._actions.keys())
        return {
            name for name, cat in self._categories.items()
            if cat == category
        }

    def is_read_only(self, action_name: str) -> bool:
        """All investigation actions are read-only by design"""
        return True  # Always true in investigation ontology
```

### Success Criteria
- [ ] All investigation actions defined and categorized
- [ ] Zero write/modify/delete actions in ontology
- [ ] Registry validates that only defined actions can be called
- [ ] Attempting undefined action raises clear error

---

## Phase 2: Layer-by-Layer Architecture (Week 2)

### Goal
Implement 4-layer risk elimination model from agent-hypervisor.

### Layer 0: Execution Physics (File System Level)

```python
# docker-compose.yml additions

services:
  backend:
    volumes:
      # Mount knowledge directory as READ-ONLY
      - ./knowledge:/knowledge:ro
      # Separate temp space for indexes (in-memory or temp)
      - investigation-cache:/tmp/investigation:rw
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    # No network access during investigation
    network_mode: "host"  # Or isolated network with no internet
```

**Physical constraints:**
- Knowledge files are read-only to investigation process
- Indexes are in-memory or temp directory
- No network access during investigation
- No file system writes to knowledge directory

### Layer 1: Base Ontology (Design-Time)

Already implemented in Phase 1. This is the investigation action vocabulary.

### Layer 2: Dynamic Ontology Projection (Runtime)

```python
# app/investigation/projection.py

from typing import Dict, Callable, Set
from enum import Enum

class QuestionType(Enum):
    TEMPORAL = "temporal"  # When did X happen?
    CAUSAL = "causal"      # Why did X cause Y?
    CALCULATION = "calculation"  # Sum, count, compare numbers
    SEMANTIC = "semantic"   # Requires LLM understanding
    LOOKUP = "lookup"      # Direct fact retrieval


class OntologyProjector:
    """Projects relevant subset of ontology based on question type"""

    def __init__(self, base_ontology: InvestigationOntology):
        self.base = base_ontology

    def project(self, question_type: QuestionType) -> Set[str]:
        """Return only actions relevant to question type"""

        projections = {
            QuestionType.TEMPORAL: {
                'observe_timeline',
                'extract_dates',
                'compare_dates',
                'traverse_temporal',
                'find_documents_about',
            },
            QuestionType.CAUSAL: {
                'find_documents_about',
                'observe_relationships',
                'traverse_causal',
                'observe_entities',
            },
            QuestionType.CALCULATION: {
                'find_documents_about',
                'calculate',
                'extract_numbers',
            },
            QuestionType.LOOKUP: {
                'find_documents_about',
            },
            QuestionType.SEMANTIC: {
                # Semantic questions get full toolset
                # because they need LLM reasoning
                *self.base.list_actions()
            }
        }

        return projections[question_type]

    def classify_question(self, question: str) -> QuestionType:
        """Deterministic question classification"""

        question_lower = question.lower()

        # Temporal indicators
        temporal_keywords = ['when', 'date', 'before', 'after', 'first', 'timeline']
        if any(kw in question_lower for kw in temporal_keywords):
            return QuestionType.TEMPORAL

        # Causal indicators
        causal_keywords = ['why', 'cause', 'reason', 'because', 'led to', 'resulted in']
        if any(kw in question_lower for kw in causal_keywords):
            return QuestionType.CAUSAL

        # Calculation indicators
        calc_keywords = ['how many', 'total', 'sum', 'count', 'average']
        if any(kw in question_lower for kw in calc_keywords):
            return QuestionType.CALCULATION

        # Direct lookup indicators
        lookup_keywords = ['what is', 'what port', 'what version']
        if any(kw in question_lower for kw in lookup_keywords):
            return QuestionType.LOOKUP

        # Default to semantic (needs LLM)
        return QuestionType.SEMANTIC
```

### Layer 3: Execution Governance (Runtime Safety)

```python
# app/investigation/governance.py

from dataclasses import dataclass
from time import time
from typing import Optional

@dataclass
class ExecutionContext:
    """Runtime context for governance decisions"""
    call_depth: int
    documents_examined: int
    elapsed_time_ms: float
    estimated_cost: float
    confidence: float


class ExecutionGovernor:
    """Enforce runtime constraints on allowed actions"""

    def __init__(
        self,
        max_depth: int = 5,
        max_documents: int = 100,
        max_time_ms: float = 5000,
        min_confidence: float = 0.7,
        max_cost: float = 0.1
    ):
        self.max_depth = max_depth
        self.max_documents = max_documents
        self.max_time_ms = max_time_ms
        self.min_confidence = min_confidence
        self.max_cost = max_cost

    def may_execute(
        self,
        action_name: str,
        context: ExecutionContext
    ) -> tuple[bool, Optional[str]]:
        """
        Returns (allowed, reason) tuple.
        If not allowed, reason explains why.
        """

        # Recursion limit
        if context.call_depth > self.max_depth:
            return False, f"Exceeded max depth ({self.max_depth})"

        # Resource limit
        if context.documents_examined > self.max_documents:
            return False, f"Examined too many documents ({self.max_documents})"

        # Time limit
        if context.elapsed_time_ms > self.max_time_ms:
            return False, f"Investigation timeout ({self.max_time_ms}ms)"

        # Confidence threshold for expensive operations
        if context.estimated_cost > self.max_cost:
            if context.confidence < self.min_confidence:
                return False, (
                    f"Low confidence ({context.confidence:.2f}) "
                    f"for expensive operation"
                )

        return True, None
```

### Success Criteria
- [ ] Layer 0: Knowledge directory mounted read-only
- [ ] Layer 1: Only ontology actions callable
- [ ] Layer 2: Question type determines visible tools
- [ ] Layer 3: Runtime limits prevent runaway investigation
- [ ] All layers tested with evaluation framework

---

## Phase 3: Deterministic Core with LLM Shell (Week 3)

### Goal
Implement "AI Aikido" - use LLM only when necessary, deterministic reasoning when possible.

### Architecture

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

### Implementation

```python
# app/investigation/strategies.py

from abc import ABC, abstractmethod
from typing import Dict, List

class InvestigationStrategy(ABC):
    """Base class for question-type specific strategies"""

    @abstractmethod
    def investigate(self, question: str, context: Dict) -> str:
        """Execute investigation, return answer"""
        pass

    @abstractmethod
    def is_deterministic(self) -> bool:
        """Does this strategy use LLM?"""
        pass


class TemporalStrategy(InvestigationStrategy):
    """Deterministic temporal reasoning - NO LLM"""

    def investigate(self, question: str, context: Dict) -> str:
        # Step 1: Extract dates deterministically (regex)
        dates = ReasoningActions.extract_dates(question)

        # Step 2: Find documents in that time range
        docs = ObservationActions.observe_timeline(
            dates[0] if len(dates) > 0 else None,
            dates[1] if len(dates) > 1 else None
        )

        # Step 3: Compare dates (arithmetic)
        if len(dates) >= 2:
            comparison = ReasoningActions.compare_dates(dates[0], dates[1])

        # Step 4: Format answer (template)
        return self._format_temporal_answer(docs, comparison)

    def is_deterministic(self) -> bool:
        return True  # No LLM used

    def _format_temporal_answer(self, docs, comparison) -> str:
        """Deterministic answer formatting"""
        # Template-based response, no LLM
        pass


class CausalStrategy(InvestigationStrategy):
    """Deterministic causal chain traversal - NO LLM"""

    def investigate(self, question: str, context: Dict) -> str:
        # Step 1: Extract entities (NER, deterministic)
        entities = self._extract_entities_regex(question)

        # Step 2: Find documents mentioning entities
        docs = [
            ObservationActions.find_documents_about(entity)
            for entity in entities
        ]

        # Step 3: Traverse causal graph (algorithm)
        causal_chain = NavigationActions.traverse_causal(docs[0])

        # Step 4: Format answer (template)
        return self._format_causal_answer(causal_chain)

    def is_deterministic(self) -> bool:
        return True

    def _extract_entities_regex(self, text: str) -> List[str]:
        """Simple regex-based entity extraction"""
        # Capital words, quoted phrases, etc.
        pass


class CalculationStrategy(InvestigationStrategy):
    """Deterministic calculation - NO LLM"""

    def investigate(self, question: str, context: Dict) -> str:
        # Step 1: Extract numbers (regex)
        numbers = self._extract_numbers(question)

        # Step 2: Detect operation (keyword matching)
        operation = self._detect_operation(question)

        # Step 3: Calculate (arithmetic)
        result = ReasoningActions.calculate(
            f"{numbers[0]} {operation} {numbers[1]}"
        )

        # Step 4: Format answer
        return f"The result is {result}"

    def is_deterministic(self) -> bool:
        return True


class SemanticStrategy(InvestigationStrategy):
    """LLM-based semantic understanding - NOT deterministic"""

    def __init__(self, llm_service):
        self.llm = llm_service

    def investigate(self, question: str, context: Dict) -> str:
        # Only use LLM for truly semantic questions

        # Step 1: Retrieve documents (deterministic)
        docs = ObservationActions.find_documents_about(question)

        # Step 2: LLM synthesis (non-deterministic)
        answer = self.llm.synthesize_answer(question, docs)

        return answer

    def is_deterministic(self) -> bool:
        return False  # Uses LLM


class HybridInvestigator:
    """Route questions to appropriate strategy"""

    def __init__(self, ontology: InvestigationOntology, llm_service):
        self.projector = OntologyProjector(ontology)
        self.strategies = {
            QuestionType.TEMPORAL: TemporalStrategy(),
            QuestionType.CAUSAL: CausalStrategy(),
            QuestionType.CALCULATION: CalculationStrategy(),
            QuestionType.SEMANTIC: SemanticStrategy(llm_service),
        }

    def answer(self, question: str) -> Dict:
        # Step 1: Classify question (deterministic)
        q_type = self.projector.classify_question(question)

        # Step 2: Project relevant ontology
        available_actions = self.projector.project(q_type)

        # Step 3: Execute appropriate strategy
        strategy = self.strategies[q_type]
        answer = strategy.investigate(question, {
            'available_actions': available_actions
        })

        return {
            'answer': answer,
            'question_type': q_type.value,
            'strategy_used': strategy.__class__.__name__,
            'was_deterministic': strategy.is_deterministic(),
        }
```

### Success Criteria
- [ ] Temporal questions answered without LLM (deterministic)
- [ ] Causal questions use graph traversal (deterministic)
- [ ] Calculation questions use arithmetic (deterministic)
- [ ] Only semantic questions invoke LLM
- [ ] Evaluation shows deterministic strategies match/exceed LLM accuracy for structured questions

---

## Phase 4: Specialized Tools Over Generic (Week 4)

### Goal
Replace generic tools with single-purpose, constrained tools.

### Before (Generic, Dangerous)

```python
# BAD: Too flexible, can be misused
def search(query: str, filter: Dict, limit: int, offset: int):
    """Generic search - too many parameters"""
    pass

def execute_query(sql: str):
    """SQL injection risk"""
    pass
```

### After (Specialized, Safe)

```python
# app/investigation/specialized_tools.py

class SpecializedTools:
    """Single-purpose tools with baked-in constraints"""

    # Each tool does ONE thing
    @staticmethod
    def find_memory_leaks() -> List[Path]:
        """Find documents about memory leaks"""
        # Parameters baked in, can't be manipulated
        return ObservationActions.find_documents_about("memory leak")

    @staticmethod
    def find_timeout_issues() -> List[Path]:
        """Find documents about timeouts"""
        return ObservationActions.find_documents_about("timeout")

    @staticmethod
    def find_events_in_january() -> List[Dict]:
        """Find events in January 2026"""
        return ObservationActions.observe_timeline(
            start=date(2026, 1, 1),
            end=date(2026, 1, 31)
        )

    @staticmethod
    def find_documents_by_alex() -> List[Path]:
        """Find documents authored by Alex"""
        return ObservationActions.find_documents_about("author:Alex")

    @staticmethod
    def compare_two_dates(d1_str: str, d2_str: str) -> Dict:
        """Compare exactly two dates"""
        d1 = self._parse_date(d1_str)
        d2 = self._parse_date(d2_str)
        return ReasoningActions.compare_dates(d1, d2)

    @staticmethod
    def get_related_documents(doc: Path) -> List[Path]:
        """Get documents related to this one (max 2 hops)"""
        return NavigationActions.traverse_related(doc, max_hops=2)
```

### Tool Virtualization Pattern

```python
# Instead of LLM calling:
#   search(query="memory leak", filter={"type": <INJECTED>})
#
# LLM calls:
#   find_memory_leaks()
#
# Parameters are baked in, can't be manipulated
```

### Success Criteria
- [ ] All generic tools replaced with specialized equivalents
- [ ] Each tool has single, clear purpose
- [ ] Parameters are constrained or baked-in
- [ ] LLM cannot inject/manipulate tool parameters
- [ ] Injection attacks become architecturally impossible

---

## Phase 5: Integration with Evaluation Framework (Week 5)

### Goal
Test ontology-first architecture against evaluation questions.

### New Evaluation Strategy

```python
# evaluation/strategies/ontology_first.py

class OntologyFirstStrategy:
    """Evaluation strategy using ontology-first architecture"""

    def __init__(self):
        self.ontology = InvestigationOntology()
        self.investigator = HybridInvestigator(self.ontology, None)

    @property
    def name(self) -> str:
        return "ontology_first"

    def retrieve(self, query: str, knowledge_dir: Path) -> RetrievalResult:
        start_time = time.time()

        # Use ontology-first investigator
        result = self.investigator.answer(query)

        # Extract documents that were examined
        documents = result.get('documents_examined', [])
        snippets = result.get('snippets', [])

        query_time_ms = (time.time() - start_time) * 1000

        return RetrievalResult(
            documents=documents,
            snippets=snippets,
            query_time_ms=query_time_ms,
            strategy=self.name,
            metadata={
                'question_type': result['question_type'],
                'strategy_used': result['strategy_used'],
                'was_deterministic': result['was_deterministic'],
            }
        )
```

### Comparison Metrics

```bash
# Run evaluation comparing approaches
python evaluation/evaluate.py --strategy all --output results/ontology-comparison.json
```

Expected improvements:
- **Temporal questions:** 100% deterministic, faster than LLM
- **Causal questions:** Graph traversal more accurate than keyword search
- **Calculation questions:** Deterministic math beats LLM
- **Semantic questions:** Match baseline LLM performance
- **Security:** Zero injection attacks possible (architectural)

### Success Criteria
- [ ] Ontology-first strategy integrated into evaluation
- [ ] Non-trivial F1 score ≥ baseline
- [ ] Deterministic strategies faster than LLM
- [ ] Security guarantees validated (read-only, bounded)
- [ ] Results documented in comparison report

---

## Measuring Success

### Quantitative Metrics

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| Non-trivial F1 | ~27% | 60%+ | Evaluation framework |
| Temporal question accuracy | ~50% | 100% | Deterministic strategy |
| LLM invocations per query | 1-3 | 0-1 | Count strategy calls |
| Query time (deterministic) | ~50ms | <20ms | No LLM overhead |
| Security vulnerabilities | Unknown | 0 | Penetration testing |

### Qualitative Benefits

- **Explainability:** Deterministic strategies produce audit trails
- **Reliability:** No hallucinations for structural questions
- **Cost:** Fewer LLM calls = lower cost
- **Speed:** Deterministic computation faster than LLM
- **Safety:** Architectural constraints prevent misuse

---

## Risk Mitigation

### Risk 1: Deterministic strategies too rigid

**Mitigation:**
- Start with narrow question types (temporal, calculation)
- Fall back to LLM for edge cases
- Expand deterministic coverage incrementally

### Risk 2: Classification errors route to wrong strategy

**Mitigation:**
- Build confidence scoring for classifier
- Low-confidence questions → semantic strategy (LLM)
- Maintain audit log of classification decisions

### Risk 3: Users expect LLM for everything

**Mitigation:**
- Expose strategy selection in UI
- Show speed/accuracy benefits of deterministic
- Allow manual override to force LLM

---

## Next Steps

### Immediate (This Week)
1. [ ] Implement Phase 1: Define investigation ontology
2. [ ] Create registry of read-only actions
3. [ ] Write tests validating no write actions exist

### Short-term (Next 2 Weeks)
4. [ ] Implement Layer 2: Dynamic projection
5. [ ] Implement Layer 3: Execution governance
6. [ ] Build deterministic strategies (temporal, causal, calculation)

### Medium-term (Next Month)
7. [ ] Integrate with evaluation framework
8. [ ] Run comparative benchmarks
9. [ ] Document security guarantees

### Long-term (Next Quarter)
10. [ ] Expand to graph-based knowledge representation
11. [ ] Build interactive investigation UI
12. [ ] Production deployment

---

## Open Questions

1. **Should we build a knowledge graph explicitly?**
   - Pro: Enables deterministic causal traversal
   - Con: Adds complexity
   - Decision: Start with implicit graph (document links), evolve to explicit if needed

2. **How to handle questions that don't fit types?**
   - Answer: Semantic strategy (LLM) is catch-all
   - Measure: Track % of questions going to semantic vs deterministic

3. **Can we replace vector search with graph + deterministic?**
   - Hypothesis: Graph traversal + keyword = better than embeddings for structured questions
   - Test: Benchmark against vector search baseline

4. **What about multi-document synthesis?**
   - Deterministic: Template-based synthesis for structured formats
   - LLM: Semantic synthesis when needed
   - Hybrid: Deterministic retrieval + LLM synthesis

---

## References

- **Source concepts:** `evaluation/AGENT_HYPERVISOR_CONCEPTS.md`
- **Evaluation framework:** `evaluation/README.md`
- **Current baseline:** `evaluation/INITIAL_RESULTS.md`
- **Hard questions:** `evaluation/questions-hard.json`
- **Missing dimensions:** `evaluation/MISSING_DIMENSIONS.md`

---

**This is a radical departure from "LLM does everything" to "LLM only when necessary."**

The ontology-first approach inverts control:
- Traditional: LLM first, determinism as fallback
- Ontology-first: Determinism first, LLM as fallback

Expected outcome: Better accuracy, lower cost, architectural safety.
