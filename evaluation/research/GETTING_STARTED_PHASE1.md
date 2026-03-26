# Getting Started: Phase 1 Implementation

**Date:** 2026-03-26
**Goal:** Begin ontology-first architecture implementation TODAY
**Duration:** Week 1 of 5-week Phase 1

---

## What We're Building (Week 1)

**Goal:** Define investigation ontology - the vocabulary of read-only actions that exist in our investigation world.

**Deliverable:** `app/investigation/` module with:
- Action registry (what actions are allowed)
- Typed action definitions (observe, reason, navigate)
- Zero write/modify/delete actions by design
- Tests proving architectural safety

---

## Prerequisites

### 1. Verify Evaluation Framework Works

```bash
cd /home/dev/code/sv-pro/personal-llm-box

# Run baseline evaluation
python evaluation/evaluate.py --strategy multi_query

# Expected output: 49.80% F1 on easy questions
```

If this doesn't work, stop and fix evaluation framework first.

### 2. Check Current Code Structure

```bash
tree app/ -L 2
```

Expected:
```
app/
├── main.py
├── routes/
│   ├── artifact.py
│   ├── digest.py
│   ├── knowledge.py
│   └── search.py
├── services/
│   ├── ollama.py
│   └── storage.py
└── utils/
    └── markdown.py
```

### 3. Install Additional Dependencies

```bash
# Add to requirements.txt if not already present
echo "networkx>=3.0" >> requirements.txt
echo "pydantic>=2.0" >> requirements.txt

pip install -r requirements.txt
```

---

## Step-by-Step Implementation

### Step 1: Create Investigation Module Structure

```bash
mkdir -p app/investigation
touch app/investigation/__init__.py
touch app/investigation/ontology.py
touch app/investigation/registry.py
touch app/investigation/actions.py
```

### Step 2: Define Action Types

Create `app/investigation/actions.py`:

```python
"""
Investigation action definitions.

All actions are READ-ONLY by design.
Modification actions do not exist in this ontology.
"""

from typing import Protocol, List, Dict, Set
from datetime import date
from pathlib import Path
from enum import Enum


class ActionCategory(Enum):
    """Categories of investigation actions"""
    OBSERVE = "observe"      # Read-only data access
    REASON = "reason"        # Pure functions, no side effects
    NAVIGATE = "navigate"    # Follow existing structure


class InvestigationAction(Protocol):
    """Protocol for all investigation actions"""

    @property
    def name(self) -> str:
        """Action identifier"""
        ...

    @property
    def category(self) -> ActionCategory:
        """Action category"""
        ...

    def is_read_only(self) -> bool:
        """All investigation actions are read-only"""
        ...


# ============================================================================
# OBSERVATION ACTIONS (Read-Only)
# ============================================================================

class ObservationActions:
    """
    Actions that observe knowledge without modification.
    All functions are read-only.
    """

    @staticmethod
    def find_documents_about(topic: str, knowledge_dir: Path) -> List[Path]:
        """
        Find documents mentioning a topic.

        Args:
            topic: Search term
            knowledge_dir: Path to knowledge directory

        Returns:
            List of matching document paths
        """
        matching_docs = []
        for doc_path in knowledge_dir.glob("*.md"):
            content = doc_path.read_text()
            if topic.lower() in content.lower():
                matching_docs.append(doc_path)
        return matching_docs

    @staticmethod
    def observe_timeline(
        start: date,
        end: date,
        knowledge_dir: Path
    ) -> List[Dict]:
        """
        Extract events within date range.

        Returns:
            List of {date, document, event} dicts
        """
        # TODO: Implement date extraction from documents
        raise NotImplementedError("Timeline observation not yet implemented")

    @staticmethod
    def observe_document_metadata(doc_path: Path) -> Dict:
        """
        Extract metadata from document frontmatter.

        Returns:
            Dict with title, tags, created_at, etc.
        """
        # TODO: Parse YAML frontmatter
        raise NotImplementedError("Metadata observation not yet implemented")


# ============================================================================
# REASONING ACTIONS (Pure Functions)
# ============================================================================

class ReasoningActions:
    """
    Pure functions that perform reasoning with no side effects.
    """

    @staticmethod
    def compare_dates(d1: date, d2: date) -> Dict:
        """
        Compare two dates deterministically.

        Returns:
            {
                'earlier': date,
                'later': date,
                'days_between': int,
                'same_month': bool,
                'same_year': bool
            }
        """
        if d1 < d2:
            earlier, later = d1, d2
        else:
            earlier, later = d2, d1

        delta = later - earlier

        return {
            'earlier': earlier,
            'later': later,
            'days_between': delta.days,
            'same_month': earlier.month == later.month and earlier.year == later.year,
            'same_year': earlier.year == later.year,
        }

    @staticmethod
    def calculate(expression: str) -> float:
        """
        Safe arithmetic evaluation.

        Only supports: +, -, *, /, numbers
        Raises ValueError for invalid expressions.
        """
        # Whitelist safe operations
        allowed_chars = set('0123456789+-*/(). ')
        if not all(c in allowed_chars for c in expression):
            raise ValueError(f"Invalid expression: {expression}")

        # Evaluate safely (in real impl, use ast.literal_eval or similar)
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return float(result)
        except Exception as e:
            raise ValueError(f"Cannot evaluate: {expression}") from e

    @staticmethod
    def extract_dates(text: str) -> List[date]:
        """
        Extract dates from text using regex.

        Supports formats:
        - YYYY-MM-DD
        - MM/DD/YYYY
        - Month DD, YYYY
        """
        # TODO: Implement regex date extraction
        raise NotImplementedError("Date extraction not yet implemented")


# ============================================================================
# NAVIGATION ACTIONS (Follow Structure)
# ============================================================================

class NavigationActions:
    """
    Actions that navigate existing knowledge structure.
    """

    @staticmethod
    def traverse_related(
        doc_path: Path,
        max_hops: int = 2,
        knowledge_dir: Path = None
    ) -> List[Path]:
        """
        Follow document relationships (from YAML frontmatter).

        Args:
            doc_path: Starting document
            max_hops: Maximum traversal depth
            knowledge_dir: Root knowledge directory

        Returns:
            List of related document paths
        """
        # TODO: Implement graph traversal
        raise NotImplementedError("Relation traversal not yet implemented")

    @staticmethod
    def traverse_causal(
        event: Dict,
        direction: str = "forward",
        max_depth: int = 5
    ) -> List[Dict]:
        """
        Follow causal chain (cause-effect relationships).

        Args:
            event: Starting event {doc, description, date}
            direction: "forward" (effects) or "backward" (causes)
            max_depth: Maximum chain length

        Returns:
            List of events in causal chain
        """
        # TODO: Implement causal traversal
        raise NotImplementedError("Causal traversal not yet implemented")


# ============================================================================
# FORBIDDEN ACTIONS (Do Not Exist)
# ============================================================================

# The following actions DO NOT EXIST in the investigation ontology:
# - modify_document(path, content)
# - delete_document(path)
# - send_email(to, body)
# - execute_code(code)
# - access_internet(url)
# - write_file(path, content)
#
# These actions cannot be called because they are not defined.
# This is security by architectural absence, not by policy enforcement.
```

### Step 3: Create Action Registry

Create `app/investigation/registry.py`:

```python
"""
Investigation ontology registry.

Maintains the vocabulary of allowed actions.
"""

from typing import Dict, Callable, Set, Optional
from pathlib import Path

from .actions import (
    ActionCategory,
    ObservationActions,
    ReasoningActions,
    NavigationActions,
)


class InvestigationOntology:
    """
    Registry of allowed investigation actions.

    Only actions registered here can be executed.
    Attempting to call undefined actions raises KeyError.
    """

    def __init__(self, knowledge_dir: Path):
        self.knowledge_dir = knowledge_dir
        self._actions: Dict[str, Callable] = {}
        self._categories: Dict[str, ActionCategory] = {}
        self._register_base_ontology()

    def _register_base_ontology(self):
        """Register all read-only investigation actions"""

        # Observation actions
        self.register(
            "find_documents_about",
            lambda topic: ObservationActions.find_documents_about(
                topic, self.knowledge_dir
            ),
            ActionCategory.OBSERVE
        )

        self.register(
            "observe_timeline",
            lambda start, end: ObservationActions.observe_timeline(
                start, end, self.knowledge_dir
            ),
            ActionCategory.OBSERVE
        )

        self.register(
            "observe_document_metadata",
            ObservationActions.observe_document_metadata,
            ActionCategory.OBSERVE
        )

        # Reasoning actions
        self.register(
            "compare_dates",
            ReasoningActions.compare_dates,
            ActionCategory.REASON
        )

        self.register(
            "calculate",
            ReasoningActions.calculate,
            ActionCategory.REASON
        )

        self.register(
            "extract_dates",
            ReasoningActions.extract_dates,
            ActionCategory.REASON
        )

        # Navigation actions
        self.register(
            "traverse_related",
            lambda doc: NavigationActions.traverse_related(
                doc, knowledge_dir=self.knowledge_dir
            ),
            ActionCategory.NAVIGATE
        )

        self.register(
            "traverse_causal",
            NavigationActions.traverse_causal,
            ActionCategory.NAVIGATE
        )

    def register(self, name: str, func: Callable, category: ActionCategory):
        """
        Register an action in the ontology.

        Args:
            name: Action identifier
            func: Callable function
            category: Action category
        """
        if name in self._actions:
            raise ValueError(f"Action '{name}' already registered")

        self._actions[name] = func
        self._categories[name] = category

    def get_action(self, name: str) -> Callable:
        """
        Get action by name.

        Raises:
            KeyError: If action doesn't exist in ontology
        """
        if name not in self._actions:
            raise KeyError(
                f"Action '{name}' does not exist in investigation ontology. "
                f"Available actions: {list(self._actions.keys())}"
            )
        return self._actions[name]

    def list_actions(
        self,
        category: Optional[ActionCategory] = None
    ) -> Set[str]:
        """
        List available actions, optionally filtered by category.

        Args:
            category: Filter by category (None = all actions)

        Returns:
            Set of action names
        """
        if category is None:
            return set(self._actions.keys())

        return {
            name for name, cat in self._categories.items()
            if cat == category
        }

    def is_read_only(self, action_name: str) -> bool:
        """
        Check if action is read-only.

        All investigation actions are read-only by design,
        so this always returns True.
        """
        # Verify action exists
        self.get_action(action_name)
        return True

    def get_category(self, action_name: str) -> ActionCategory:
        """Get category of an action"""
        if action_name not in self._categories:
            raise KeyError(f"Action '{action_name}' not found")
        return self._categories[action_name]
```

### Step 4: Create Package Init

Create `app/investigation/__init__.py`:

```python
"""
Investigation board ontology-first architecture.

This module implements read-only investigation actions with
security by architectural absence.
"""

from .actions import (
    ActionCategory,
    ObservationActions,
    ReasoningActions,
    NavigationActions,
)
from .registry import InvestigationOntology

__all__ = [
    'ActionCategory',
    'ObservationActions',
    'ReasoningActions',
    'NavigationActions',
    'InvestigationOntology',
]
```

### Step 5: Write Tests

Create `tests/test_investigation_ontology.py`:

```python
"""
Tests for investigation ontology.

Validates that:
1. Only defined actions can be called
2. All actions are read-only
3. Write actions do not exist
"""

import pytest
from pathlib import Path
from datetime import date

from app.investigation import InvestigationOntology, ActionCategory


def test_ontology_initialization(tmp_path):
    """Test ontology initializes with knowledge directory"""
    ontology = InvestigationOntology(tmp_path)
    assert ontology.knowledge_dir == tmp_path


def test_list_all_actions(tmp_path):
    """Test listing all registered actions"""
    ontology = InvestigationOntology(tmp_path)
    actions = ontology.list_actions()

    # Should have actions from all categories
    assert len(actions) > 0
    assert "find_documents_about" in actions
    assert "compare_dates" in actions


def test_list_actions_by_category(tmp_path):
    """Test filtering actions by category"""
    ontology = InvestigationOntology(tmp_path)

    observe_actions = ontology.list_actions(ActionCategory.OBSERVE)
    reason_actions = ontology.list_actions(ActionCategory.REASON)
    navigate_actions = ontology.list_actions(ActionCategory.NAVIGATE)

    assert "find_documents_about" in observe_actions
    assert "compare_dates" in reason_actions
    assert "traverse_related" in navigate_actions


def test_get_existing_action(tmp_path):
    """Test getting a registered action"""
    ontology = InvestigationOntology(tmp_path)
    action = ontology.get_action("compare_dates")
    assert callable(action)


def test_get_nonexistent_action_raises_error(tmp_path):
    """Test that undefined actions raise KeyError"""
    ontology = InvestigationOntology(tmp_path)

    with pytest.raises(KeyError) as exc_info:
        ontology.get_action("modify_document")

    assert "does not exist" in str(exc_info.value)
    assert "modify_document" in str(exc_info.value)


def test_all_actions_are_read_only(tmp_path):
    """Test that all actions are marked read-only"""
    ontology = InvestigationOntology(tmp_path)

    for action_name in ontology.list_actions():
        assert ontology.is_read_only(action_name) is True


def test_write_actions_do_not_exist(tmp_path):
    """Test that write/modify/delete actions are not in ontology"""
    ontology = InvestigationOntology(tmp_path)
    actions = ontology.list_actions()

    # These actions should NOT exist
    forbidden = [
        "modify_document",
        "delete_document",
        "write_file",
        "send_email",
        "execute_code",
        "access_internet",
    ]

    for forbidden_action in forbidden:
        assert forbidden_action not in actions


def test_compare_dates_action(tmp_path):
    """Test deterministic date comparison"""
    ontology = InvestigationOntology(tmp_path)
    compare_dates = ontology.get_action("compare_dates")

    d1 = date(2026, 1, 15)
    d2 = date(2026, 1, 22)

    result = compare_dates(d1, d2)

    assert result['earlier'] == d1
    assert result['later'] == d2
    assert result['days_between'] == 7
    assert result['same_month'] is True
    assert result['same_year'] is True


def test_calculate_action(tmp_path):
    """Test safe arithmetic calculation"""
    ontology = InvestigationOntology(tmp_path)
    calculate = ontology.get_action("calculate")

    assert calculate("2 + 2") == 4.0
    assert calculate("10 * 5") == 50.0
    assert calculate("100 / 4") == 25.0


def test_calculate_rejects_unsafe_expressions(tmp_path):
    """Test that calculate rejects potentially unsafe expressions"""
    ontology = InvestigationOntology(tmp_path)
    calculate = ontology.get_action("calculate")

    with pytest.raises(ValueError):
        calculate("import os")

    with pytest.raises(ValueError):
        calculate("__import__('os').system('ls')")


def test_find_documents_about(tmp_path):
    """Test document search"""
    # Create test documents
    (tmp_path / "doc1.md").write_text("Memory leak in authentication")
    (tmp_path / "doc2.md").write_text("Network timeout issues")
    (tmp_path / "doc3.md").write_text("API documentation")

    ontology = InvestigationOntology(tmp_path)
    find_docs = ontology.get_action("find_documents_about")

    results = find_docs("memory leak")
    assert len(results) == 1
    assert results[0].name == "doc1.md"


def test_action_categories(tmp_path):
    """Test that actions have correct categories"""
    ontology = InvestigationOntology(tmp_path)

    assert ontology.get_category("find_documents_about") == ActionCategory.OBSERVE
    assert ontology.get_category("compare_dates") == ActionCategory.REASON
    assert ontology.get_category("traverse_related") == ActionCategory.NAVIGATE
```

### Step 6: Run Tests

```bash
# Install pytest if not present
pip install pytest

# Create tests directory if it doesn't exist
mkdir -p tests
touch tests/__init__.py

# Run tests
pytest tests/test_investigation_ontology.py -v

# Expected: All tests pass
```

### Step 7: Verify Against Evaluation Questions

Create `scripts/test_ontology_coverage.py`:

```python
"""
Test ontology coverage against evaluation questions.

Validates that the ontology has sufficient actions to answer
test questions.
"""

import json
from pathlib import Path
from app.investigation import InvestigationOntology, ActionCategory


def analyze_question_requirements():
    """Analyze what actions are needed for evaluation questions"""

    questions_file = Path("evaluation/questions.json")
    questions = json.loads(questions_file.read_text())

    # Create ontology
    ontology = InvestigationOntology(Path("evaluation/knowledge"))

    # Analyze by question type
    for question_data in questions:
        q_type = question_data.get('category', 'unknown')
        question = question_data['question']

        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"Type: {q_type}")

        # Determine required actions
        required_actions = []

        if any(kw in question.lower() for kw in ['when', 'date', 'before', 'after']):
            required_actions.extend([
                'extract_dates',
                'compare_dates',
                'observe_timeline',
            ])

        if any(kw in question.lower() for kw in ['how many', 'total', 'count']):
            required_actions.extend([
                'calculate',
            ])

        if any(kw in question.lower() for kw in ['why', 'cause', 'led to']):
            required_actions.extend([
                'traverse_causal',
                'observe_relationships',
            ])

        # All questions need basic search
        required_actions.append('find_documents_about')

        print(f"Required actions: {required_actions}")

        # Check ontology coverage
        available = ontology.list_actions()
        missing = [a for a in required_actions if a not in available]

        if missing:
            print(f"❌ MISSING: {missing}")
        else:
            print(f"✓ All required actions available")


if __name__ == "__main__":
    analyze_question_requirements()
```

Run it:

```bash
python scripts/test_ontology_coverage.py
```

---

## Success Criteria for Week 1

### Must Have ✅

- [ ] `app/investigation/` module created
- [ ] Action types defined (observe, reason, navigate)
- [ ] Registry implemented
- [ ] All tests pass
- [ ] Zero write actions in ontology
- [ ] README documented

### Nice to Have 🎯

- [ ] Coverage analysis against evaluation questions
- [ ] Additional action implementations (dates, metadata)
- [ ] Performance benchmarks

---

## Troubleshooting

### Issue: Import errors

**Problem:** `ModuleNotFoundError: No module named 'app.investigation'`

**Solution:**
```bash
# Make sure you're in the project root
cd /home/dev/code/sv-pro/personal-llm-box

# Verify directory structure
ls -la app/investigation/

# Try running from root with python -m
python -m pytest tests/test_investigation_ontology.py
```

### Issue: Tests fail on calculate()

**Problem:** `eval()` is actually unsafe

**Solution:** Use `ast.literal_eval` or a proper expression parser:

```python
import ast
import operator

SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

def safe_eval(expr: str) -> float:
    """Safely evaluate arithmetic expression"""
    tree = ast.parse(expr, mode='eval')
    # Validate only safe operations
    # ... implement proper visitor pattern
    return float(result)
```

### Issue: Path issues in tests

**Problem:** `tmp_path` fixture not creating proper structure

**Solution:**
```python
def test_with_proper_structure(tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    knowledge_dir.mkdir()

    # Create test documents
    (knowledge_dir / "test.md").write_text("content")

    ontology = InvestigationOntology(knowledge_dir)
```

---

## What's Next (Week 2)

After Week 1 completes (ontology defined and tested), Week 2 will implement:

1. **Layer 2: Dynamic Projection**
   - Question classification
   - Action filtering by question type

2. **Layer 3: Execution Governance**
   - Runtime limits (depth, time, resources)
   - Confidence thresholds

---

## References

- **ONTOLOGY_FIRST_ROADMAP.md** - Full 5-week plan
- **SYNTHESIS_AND_DECISION.md** - Why this architecture
- **AGENT_HYPERVISOR_CONCEPTS.md** - Theoretical foundation
- **evaluation/README.md** - Evaluation framework docs

---

## Questions?

If stuck, check:
1. Are all tests passing? → Run `pytest -v`
2. Is ontology properly initialized? → Add debug prints
3. Are actions registered? → Call `ontology.list_actions()`
4. Is evaluation framework working? → Run `python evaluation/evaluate.py`

---

**Ready to start? Create that first file and begin building the ontology!** 🚀

```bash
mkdir -p app/investigation
touch app/investigation/__init__.py
# ... and so on
```
