#!/usr/bin/env python3
"""
Evaluation framework for testing retrieval and investigation capabilities.

This script tests different retrieval strategies against a curated set of
questions (trivial and non-trivial) to measure their effectiveness.

Usage:
    python evaluate.py --strategy simple_grep
    python evaluate.py --strategy all --output results.json
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Any, Protocol
from dataclasses import dataclass, asdict
import argparse
import subprocess


@dataclass
class RetrievalResult:
    """Result from a retrieval operation"""
    documents: List[str]  # List of document filenames
    snippets: List[str]  # Relevant text snippets
    query_time_ms: float
    strategy: str


@dataclass
class EvaluationResult:
    """Result of evaluating a single question"""
    question_id: str
    question_type: str  # trivial or non-trivial
    question: str
    expected_sources: List[str]
    retrieved_sources: List[str]
    expected_answer: str
    strategy: str

    # Metrics
    precision: float  # Relevant docs / Retrieved docs
    recall: float  # Relevant docs / Total relevant docs
    f1_score: float
    source_coverage: float  # % of expected sources retrieved
    query_time_ms: float

    # Flags
    found_all_sources: bool
    found_any_sources: bool


class RetrievalStrategy(Protocol):
    """Interface for retrieval strategies"""

    def retrieve(self, query: str, knowledge_dir: Path) -> RetrievalResult:
        """Retrieve documents for a given query"""
        ...

    @property
    def name(self) -> str:
        """Strategy name"""
        ...


class SimpleGrepStrategy:
    """Current baseline: simple grep-based search"""

    @property
    def name(self) -> str:
        return "simple_grep"

    def retrieve(self, query: str, knowledge_dir: Path) -> RetrievalResult:
        start_time = time.time()

        documents = []
        snippets = []
        query_lower = query.lower()

        for md_file in knowledge_dir.glob("*.md"):
            try:
                text = md_file.read_text(encoding="utf-8")
                if query_lower in text.lower():
                    documents.append(md_file.name)
                    # Extract matching lines
                    lines = text.splitlines()
                    matching = [ln for ln in lines if query_lower in ln.lower()]
                    snippet = " … ".join(matching[:3])
                    snippets.append(snippet)
            except Exception:
                continue

        query_time_ms = (time.time() - start_time) * 1000

        return RetrievalResult(
            documents=documents,
            snippets=snippets,
            query_time_ms=query_time_ms,
            strategy=self.name
        )


class MultiQueryStrategy:
    """Improved strategy: break question into multiple search queries"""

    @property
    def name(self) -> str:
        return "multi_query"

    def _extract_keywords(self, query: str) -> List[str]:
        """Extract important keywords from query"""
        # Simple keyword extraction (can be improved with NLP)
        stopwords = {'what', 'is', 'the', 'a', 'an', 'how', 'why', 'when', 'where',
                     'who', 'was', 'were', 'are', 'and', 'or', 'for', 'to', 'in', 'on'}
        words = query.lower().split()
        keywords = [w.strip('?.,!') for w in words if w.lower() not in stopwords]
        return keywords

    def retrieve(self, query: str, knowledge_dir: Path) -> RetrievalResult:
        start_time = time.time()

        # Extract keywords and search for each
        keywords = self._extract_keywords(query)

        document_scores = {}
        all_snippets = {}

        for keyword in keywords:
            for md_file in knowledge_dir.glob("*.md"):
                try:
                    text = md_file.read_text(encoding="utf-8")
                    if keyword in text.lower():
                        # Increment score for this document
                        document_scores[md_file.name] = document_scores.get(md_file.name, 0) + 1

                        # Collect snippets
                        if md_file.name not in all_snippets:
                            lines = text.splitlines()
                            matching = [ln for ln in lines if keyword in ln.lower()]
                            all_snippets[md_file.name] = " … ".join(matching[:3])
                except Exception:
                    continue

        # Sort by score (number of keywords matched)
        sorted_docs = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)
        documents = [doc for doc, score in sorted_docs]
        snippets = [all_snippets[doc] for doc in documents]

        query_time_ms = (time.time() - start_time) * 1000

        return RetrievalResult(
            documents=documents,
            snippets=snippets,
            query_time_ms=query_time_ms,
            strategy=self.name
        )


class VectorSearchStrategy:
    """Semantic search using sentence embeddings"""

    def __init__(self):
        try:
            from sentence_transformers import SentenceTransformer
            import numpy as np
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.np = np
            self._embeddings_cache = {}
            self._documents_cache = {}
        except ImportError:
            raise ImportError("Install sentence-transformers: pip install sentence-transformers")

    @property
    def name(self) -> str:
        return "vector_search"

    def _get_document_embedding(self, filepath: Path) -> 'np.ndarray':
        """Get or compute embedding for a document"""
        cache_key = str(filepath)

        if cache_key in self._embeddings_cache:
            return self._embeddings_cache[cache_key]

        try:
            text = filepath.read_text(encoding="utf-8")
            # Remove frontmatter for better embedding
            if text.startswith('---'):
                parts = text.split('---', 2)
                if len(parts) >= 3:
                    text = parts[2].strip()

            embedding = self.model.encode(text, convert_to_numpy=True)
            self._embeddings_cache[cache_key] = embedding
            self._documents_cache[cache_key] = text
            return embedding
        except Exception:
            return self.np.zeros(384)  # all-MiniLM-L6-v2 has 384 dimensions

    def _cosine_similarity(self, vec1: 'np.ndarray', vec2: 'np.ndarray') -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = self.np.dot(vec1, vec2)
        norm1 = self.np.linalg.norm(vec1)
        norm2 = self.np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    def retrieve(self, query: str, knowledge_dir: Path) -> RetrievalResult:
        start_time = time.time()

        # Encode query
        query_embedding = self.model.encode(query, convert_to_numpy=True)

        # Calculate similarity with all documents
        similarities = []
        for md_file in knowledge_dir.glob("*.md"):
            doc_embedding = self._get_document_embedding(md_file)
            similarity = self._cosine_similarity(query_embedding, doc_embedding)
            similarities.append((md_file.name, similarity))

        # Sort by similarity (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Filter documents with similarity > threshold
        threshold = 0.2  # Adjust based on testing
        filtered_docs = [(doc, sim) for doc, sim in similarities if sim > threshold]

        documents = [doc for doc, sim in filtered_docs]

        # Generate snippets (first 200 chars of document)
        snippets = []
        for doc_name in documents:
            cache_key = str(knowledge_dir / doc_name)
            if cache_key in self._documents_cache:
                text = self._documents_cache[cache_key]
                snippet = text[:200].replace('\n', ' ') + '...'
                snippets.append(snippet)
            else:
                snippets.append('')

        query_time_ms = (time.time() - start_time) * 1000

        return RetrievalResult(
            documents=documents,
            snippets=snippets,
            query_time_ms=query_time_ms,
            strategy=self.name
        )


def calculate_metrics(expected_sources: List[str], retrieved_sources: List[str]) -> Dict[str, float]:
    """Calculate precision, recall, and F1 score"""
    expected_set = set(expected_sources)
    retrieved_set = set(retrieved_sources)

    true_positives = len(expected_set & retrieved_set)

    precision = true_positives / len(retrieved_set) if retrieved_set else 0.0
    recall = true_positives / len(expected_set) if expected_set else 0.0
    f1_score = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    source_coverage = recall  # Same as recall for document retrieval

    return {
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'source_coverage': source_coverage
    }


def evaluate_question(question: Dict[str, Any], strategy: RetrievalStrategy, knowledge_dir: Path) -> EvaluationResult:
    """Evaluate a single question using the given strategy"""

    # Retrieve documents
    result = strategy.retrieve(question['question'], knowledge_dir)

    # Calculate metrics
    expected_sources = question['source_documents']
    retrieved_sources = result.documents

    metrics = calculate_metrics(expected_sources, retrieved_sources)

    found_all = set(expected_sources).issubset(set(retrieved_sources))
    found_any = bool(set(expected_sources) & set(retrieved_sources))

    return EvaluationResult(
        question_id=question['id'],
        question_type=question['type'],
        question=question['question'],
        expected_sources=expected_sources,
        retrieved_sources=retrieved_sources,
        expected_answer=question['expected_answer'],
        strategy=strategy.name,
        precision=metrics['precision'],
        recall=metrics['recall'],
        f1_score=metrics['f1_score'],
        source_coverage=metrics['source_coverage'],
        query_time_ms=result.query_time_ms,
        found_all_sources=found_all,
        found_any_sources=found_any
    )


def run_evaluation(questions: List[Dict[str, Any]], strategy: RetrievalStrategy, knowledge_dir: Path) -> Dict[str, Any]:
    """Run evaluation for all questions using the given strategy"""

    results = []
    for question in questions:
        result = evaluate_question(question, strategy, knowledge_dir)
        results.append(result)

    # Calculate aggregate metrics
    trivial_results = [r for r in results if r.question_type == 'trivial']
    non_trivial_results = [r for r in results if r.question_type == 'non-trivial']

    def aggregate(result_list):
        if not result_list:
            return {}
        return {
            'avg_precision': sum(r.precision for r in result_list) / len(result_list),
            'avg_recall': sum(r.recall for r in result_list) / len(result_list),
            'avg_f1': sum(r.f1_score for r in result_list) / len(result_list),
            'avg_source_coverage': sum(r.source_coverage for r in result_list) / len(result_list),
            'avg_query_time_ms': sum(r.query_time_ms for r in result_list) / len(result_list),
            'found_all_count': sum(1 for r in result_list if r.found_all_sources),
            'found_any_count': sum(1 for r in result_list if r.found_any_sources),
            'total': len(result_list)
        }

    return {
        'strategy': strategy.name,
        'total_questions': len(questions),
        'results': [asdict(r) for r in results],
        'aggregate': {
            'overall': aggregate(results),
            'trivial': aggregate(trivial_results),
            'non_trivial': aggregate(non_trivial_results)
        }
    }


def print_summary(evaluation: Dict[str, Any]):
    """Print human-readable summary of evaluation results"""

    print(f"\n{'='*80}")
    print(f"EVALUATION RESULTS: {evaluation['strategy']}")
    print(f"{'='*80}\n")

    agg = evaluation['aggregate']

    for category in ['overall', 'trivial', 'non_trivial']:
        if category not in agg or not agg[category]:
            continue

        cat_data = agg[category]
        print(f"{category.upper().replace('_', ' ')} ({cat_data['total']} questions):")
        print(f"  Precision:       {cat_data['avg_precision']:.2%}")
        print(f"  Recall:          {cat_data['avg_recall']:.2%}")
        print(f"  F1 Score:        {cat_data['avg_f1']:.2%}")
        print(f"  Source Coverage: {cat_data['avg_source_coverage']:.2%}")
        print(f"  Avg Query Time:  {cat_data['avg_query_time_ms']:.2f}ms")
        print(f"  Found All:       {cat_data['found_all_count']}/{cat_data['total']}")
        print(f"  Found Any:       {cat_data['found_any_count']}/{cat_data['total']}")
        print()


def main():
    parser = argparse.ArgumentParser(description='Evaluate retrieval strategies')
    parser.add_argument('--strategy', choices=['simple_grep', 'multi_query', 'vector_search', 'all'],
                       default='simple_grep', help='Retrieval strategy to test')
    parser.add_argument('--output', type=str, help='Output JSON file for detailed results')
    parser.add_argument('--knowledge-dir', type=str, default='evaluation/data/knowledge',
                       help='Path to knowledge directory')
    parser.add_argument('--questions', type=str, default='evaluation/data/questions.json',
                       help='Path to questions JSON file')

    args = parser.parse_args()

    # Load questions
    questions_file = Path(args.questions)
    with open(questions_file) as f:
        questions_data = json.load(f)

    questions = questions_data['questions']
    knowledge_dir = Path(args.knowledge_dir)

    # Define strategies
    strategies = {
        'simple_grep': SimpleGrepStrategy(),
        'multi_query': MultiQueryStrategy()
    }

    # Add vector search if available
    try:
        strategies['vector_search'] = VectorSearchStrategy()
    except ImportError as e:
        if args.strategy == 'vector_search' or args.strategy == 'all':
            print(f"Warning: Vector search not available: {e}")
            print("Install with: pip install sentence-transformers")
            if args.strategy == 'vector_search':
                return

    # Select strategies to run
    if args.strategy == 'all':
        strategies_to_run = list(strategies.values())
    else:
        strategies_to_run = [strategies[args.strategy]]

    # Run evaluations
    all_results = []
    for strategy in strategies_to_run:
        print(f"\nRunning evaluation with strategy: {strategy.name}")
        evaluation = run_evaluation(questions, strategy, knowledge_dir)
        all_results.append(evaluation)
        print_summary(evaluation)

    # Save detailed results if output file specified
    if args.output:
        output_data = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'evaluations': all_results
        }
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"\nDetailed results saved to: {args.output}")


if __name__ == '__main__':
    main()
