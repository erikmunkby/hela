import numpy as np
from typing import Sequence
from hela.math.preprocessing import clean_corpus, clean_document
from hela.math.score_info import SimilarityInfo


def distance(s1: str, s2: str) -> float:
    size_x, size_y = len(s1) + 1, len(s2) + 1

    matrix = np.zeros((size_x, size_y), dtype=int)

    # Populate the top row, and leftmost column in the matrix
    for x in range(1, size_x):
        matrix[x, 0] = x
    for y in range(1, size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            # If the characters equal eachother we have 0 cost
            cost = 0 if s1[x - 1] == s2[y - 1] else 1

            matrix[x, y] = min(
                matrix[x - 1, y] + 1,  # Deletions
                matrix[x, y - 1] + 1,  # Insertions
                matrix[x - 1, y - 1] + cost  # Substitutions
            )
    return round(1 - matrix[-1, -1] / max(len(s1), len(s2)), 3)


def sort(query_str: str, corpus: Sequence[str], min_similarity: float = .75) -> Sequence[SimilarityInfo]:
    """Sorts a corpus of documents based on levenshtein distance similarity.

    Args:
        query_str:      The string to compare against the corpus
        corpus:         A sequence of documents as strings
        min_similarity: The minimum required similarity [0 to 1]

    Returns:
        A list of SimilarityInfo Objects
    """
    documents, tokenized_documents = clean_corpus(corpus)
    query_str = clean_document(query_str)

    matches = [
        SimilarityInfo(
            score=distance(query_str, document),
            match_idx=i,
            match_string=documents[i],
            target_string=query_str
        )
        for i, document in enumerate(tokenized_documents)
    ]
    matches = [m for m in matches if m.score >= min_similarity]
    return sorted(matches, key=lambda x: -x.score)


def replace(query_str: str, corpus: Sequence[str], min_similarity: float = .75) -> str:
    # Create boundaries for length of replacement string
    boundary_length = round(len(query_str) * (1 - min_similarity))
    min_len, max_len = len(query_str) - boundary_length, len(query_str) + boundary_length
    # Slim down corpus based on string length
    slimmed_corpus = [doc for doc in corpus if len(doc) >= min_len and len(doc) <= max_len]
    results = sort(query_str, slimmed_corpus, min_similarity=min_similarity)
    if len(results) > 0:
        return results[0].match_string
    return query_str
