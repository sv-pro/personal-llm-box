# Branching Guide for Retrieval Experiments

## Overview

The repository uses a structured branching strategy to keep `main` clean while experimenting with advanced retrieval techniques.

```
main (stable, simple grep search)
└── experiments/retrieval (parent for all experiments)
    ├── experiments/retrieval/vector-search (semantic search)
    ├── experiments/retrieval/fts5 (SQLite full-text)
    ├── experiments/retrieval/whoosh (indexing)
    └── ... (other experiments)
```

---

## Current Branch Structure

```
* experiments/retrieval (6e93b07)
|   Setup experiments/retrieval branch
|
* main (aa149e2) [ahead of origin/main by 1]
|   Add web UI with catalogue feature
|
* origin/main (6ccef4a)
    Add smart Ollama detection
```

---

## Working with Branches

### Check Current Branch
```bash
git branch
# * experiments/retrieval  ← you are here
#   main
```

### Switch to Main
```bash
git checkout main
```

### Switch to Experiments
```bash
git checkout experiments/retrieval
```

### Create New Experiment
```bash
# Start from experiments/retrieval
git checkout experiments/retrieval

# Create sub-branch for your experiment
git checkout -b experiments/retrieval/vector-search

# Work on your experiment
# ... edit files, test, document

# Commit changes
git add .
git commit -m "Implement vector search with sentence-transformers"

# Push to remote
git push -u origin experiments/retrieval/vector-search
```

---

## Experiment Workflow

### 1. Start Experiment

```bash
# Switch to experiment parent branch
git checkout experiments/retrieval

# Create experiment branch
git checkout -b experiments/retrieval/my-technique

# Verify you're on the right branch
git status
```

### 2. Implement & Test

```bash
# Add new files
touch app/services/my_technique.py
touch EXPERIMENT_MY_TECHNIQUE.md

# Make changes
# ... write code

# Test locally
docker-compose up -d --build backend
curl http://localhost:8000/search?q=test

# Document findings in EXPERIMENT_MY_TECHNIQUE.md
```

### 3. Commit & Document

```bash
# Stage files
git add app/services/my_technique.py
git add EXPERIMENT_MY_TECHNIQUE.md
git add requirements-experiment.txt

# Commit with descriptive message
git commit -m "Add <technique>: <brief description>

- What changed
- Performance results
- Trade-offs observed
"

# Push to remote
git push -u origin experiments/retrieval/my-technique
```

### 4. Merge to Parent (if successful)

```bash
# Switch to parent branch
git checkout experiments/retrieval

# Merge your experiment
git merge experiments/retrieval/my-technique

# Push updated parent
git push origin experiments/retrieval
```

### 5. Merge to Main (if proven)

**Only after thorough testing and approval**

```bash
# Switch to main
git checkout main

# Merge experiments/retrieval
git merge experiments/retrieval

# Push to remote
git push origin main
```

---

## Branch Protection Rules

### Main Branch
- ✅ **Always stable** - only working, tested code
- ✅ **Simple implementation** - easy to understand and maintain
- ✅ **Production-ready** - can deploy at any time
- ❌ **No experiments** - don't commit experimental code directly

### Experiments/Retrieval Branch
- ✅ **Stable experiments** - code compiles and runs
- ✅ **Documented** - has EXPERIMENT_*.md file
- ✅ **Reversible** - can revert if needed
- ⚠️  **May have unproven code** - experiments in progress
- ❌ **No broken code** - should always build

### Experiment Sub-branches
- ✅ **Work in progress** - can be broken temporarily
- ✅ **Frequent commits** - save progress often
- ✅ **Experimental** - try wild ideas
- ⚠️  **May be abandoned** - not all experiments succeed

---

## Common Scenarios

### Scenario 1: Quick Test
```bash
# Stay on experiments/retrieval
git checkout experiments/retrieval

# Make changes
vim app/routes/search.py

# Test
docker-compose up -d --build

# If it works, commit
git add app/routes/search.py
git commit -m "Quick test: XYZ"

# If it doesn't work, revert
git restore app/routes/search.py
```

### Scenario 2: Long Experiment
```bash
# Create dedicated branch
git checkout experiments/retrieval
git checkout -b experiments/retrieval/vector-search

# Work for days/weeks
# ... multiple commits

# When done, document
vim EXPERIMENT_VECTOR_SEARCH.md

# Merge back to parent
git checkout experiments/retrieval
git merge experiments/retrieval/vector-search
```

### Scenario 3: Compare Techniques
```bash
# Experiment A
git checkout -b experiments/retrieval/fts5
# ... implement, test, document

# Experiment B
git checkout experiments/retrieval
git checkout -b experiments/retrieval/vector
# ... implement, test, document

# Compare results
# Read EXPERIMENT_FTS5.md
# Read EXPERIMENT_VECTOR.md
# Choose best approach

# Merge winner to parent
git checkout experiments/retrieval
git merge experiments/retrieval/fts5  # if FTS5 won
```

### Scenario 4: Rollback Experiment
```bash
# On experiments/retrieval
git log --oneline
# abc123 Bad experiment
# def456 Good state

# Revert bad commit
git revert abc123

# Or reset to good state (careful!)
git reset --hard def456
```

---

## Naming Conventions

### Branch Names
- Use descriptive names: `experiments/retrieval/vector-search`
- Use kebab-case: `experiments/retrieval/hybrid-bm25-vector`
- Be specific: `experiments/retrieval/sqlite-fts5` not `experiments/retrieval/sql`

### Commit Messages
- Start with verb: "Add", "Implement", "Fix", "Update"
- Be specific: "Add vector search with FAISS" not "Update search"
- Include results: "Vector search: 50ms avg query time"

### File Names
- Experiments: `EXPERIMENT_<NAME>.md` (uppercase)
- Results: `BENCHMARK_<NAME>.md`
- Additional requirements: `requirements-experiment.txt`

---

## Syncing with Remote

### Push Your Branch
```bash
git push -u origin experiments/retrieval/my-technique
```

### Pull Latest Changes
```bash
# Update main
git checkout main
git pull origin main

# Update experiments/retrieval
git checkout experiments/retrieval
git pull origin experiments/retrieval
```

### Keep Experiment Updated
```bash
# On your experiment branch
git checkout experiments/retrieval/my-technique

# Merge latest from parent
git merge experiments/retrieval
```

---

## Visualization

### Current State
```
YOU ARE HERE ──┐
               ▼
* experiments/retrieval (6e93b07)
|   └─ EXPERIMENTS.md added
|   └─ CLAUDE.md updated
|
* main (aa149e2) [1 commit ahead of origin]
|   └─ Web UI + catalogue added
|
* origin/main (6ccef4a)
    └─ Smart setup + verification
```

### After Creating Experiment
```
* experiments/retrieval/vector-search (new branch)
|   └─ YOUR EXPERIMENT HERE
|
* experiments/retrieval (6e93b07)
|
* main (aa149e2)
```

### After Successful Experiment
```
* experiments/retrieval (merged)
|   └─ Vector search implemented
|   └─ EXPERIMENT_VECTOR_SEARCH.md
|
* main (aa149e2) [waiting for merge]
```

---

## Best Practices

1. **Always branch from experiments/retrieval** for new experiments
2. **Document everything** - future you will thank present you
3. **Commit frequently** - don't lose work
4. **Test thoroughly** - benchmark before merging
5. **Clean up** - delete abandoned experiment branches
6. **Communicate** - use descriptive commit messages
7. **Review code** - read your changes before committing
8. **Keep main clean** - only merge proven experiments

---

## Quick Reference

| Task | Command |
|------|---------|
| Check branch | `git branch` |
| Switch to main | `git checkout main` |
| Switch to experiments | `git checkout experiments/retrieval` |
| Create experiment | `git checkout -b experiments/retrieval/NAME` |
| Commit changes | `git add . && git commit -m "Message"` |
| Push branch | `git push -u origin BRANCH_NAME` |
| Merge to parent | `git checkout experiments/retrieval && git merge experiments/retrieval/NAME` |
| Merge to main | `git checkout main && git merge experiments/retrieval` |
| View graph | `git log --oneline --graph --all` |

---

## Need Help?

- Read `EXPERIMENTS.md` for experiment guidelines
- Read `CLAUDE.md` for branching strategy details
- Check `git status` to see what's happening
- Use `git log --oneline --graph` to visualize branches

---

**Remember:** `main` is sacred. Experiment freely in `experiments/retrieval/*` branches!
