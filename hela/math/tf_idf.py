import numpy as np
from collections import Counter
from hela.math.preprocessing import clean_document, clean_corpus
from hela.math.levenshtein import replace
from hela.math.score_info import SimilarityInfo
from typing import Sequence, Tuple


def build_matrix(documents: Sequence[str]) -> Tuple[np.ndarray, Sequence[str]]:
    """Build the tf_idf matrix, returned along with the vocabulary for the matrix.

    Args:
        documents: A list of string documents

    Returns:
        A tuple (X, vocab) as the tf_idf matrix and vocabulary as list
    """
    word_count = [Counter(x.split()) for x in documents]
    vocab = list(set([w for words in word_count for w in words.keys()]))
    arrs = [[wc.get(v, 0) for v in vocab] for wc in word_count]
    X = np.array(arrs)
    idf = np.log(X.shape[1] / np.where(X > 0, 1, 0).sum(axis=0))
    return X * idf, vocab


def normalize(X: np.ndarray) -> np.ndarray:
    """Normalizes each vector in the matrix, i.e. sets vector length = 1.

    Args:
        X: A two-dimensional numpy array

    Returns:
        A normalized numpy matrix
    """
    return X / np.linalg.norm(X, axis=1).reshape(-1, 1)


def cosine_similarity(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """Calculates the cosine similarity based on two numpy matrices.

    Args:
        X: A one or two -dimensional numpy array
        Y: A two-dimensional numpy array

    Returns:
        The cosine similarity of each pair between the two matrices.
        Will have length equal to X.shape[0] * Y.shape[0]
    """
    if X.ndim == 1:
        X = X.reshape(1, -1)
    # Set the length of each vector to 1
    X, Y = normalize(X), normalize(Y)
    return (X @ Y.T).flatten()


def find_similar_occurrences(corpus: Sequence[str], min_similarity: float = .75) -> Sequence[SimilarityInfo]:
    """Finds similar occurences of documents in a corpus.

    Args:
        corpus:         A list of string documents
        min_similarity: The minimum required similarity [0 to 1]

    Returns:
        A list of similarity info objects with similarity score >= threshold
    """
    documents, tokenized_documents = clean_corpus(corpus)
    X, _ = build_matrix(tokenized_documents)
    cs = cosine_similarity(X, X).reshape(X.shape[0], -1)
    similarities, match_indices = [], []
    for i, row in enumerate(cs):
        for idx in np.argwhere(row >= min_similarity).flatten():
            # If i == idx that means it is its own match
            # if (idx, i) is in match_indices that means we found the reverse match already
            if i != idx and (idx, i) not in match_indices:
                match_indices.append((i, idx))
                similarities.append(SimilarityInfo(
                    score=round(row[idx], 3),
                    match_idx=idx,
                    match_string=documents[idx],
                    target_idx=i,
                    target_string=documents[i]
                ))
    return sorted(similarities, key=lambda x: -x.score)


def sort(query_str: str, corpus: Sequence[str], fuzzy: bool = True) -> Sequence[SimilarityInfo]:
    """Sort matches based on cosine similarity between query string and corpus.

    Args:
        query_str:  A string of one or more search terms
        corpus:     A list of documents as strings
        fuzzy:      Whether the search terms (query_str) should fuzzily adapt to vocabulary

    Returns:
        A similarity info object with the best possible matching document
    """
    query_dict = Counter(clean_document(query_str).split())
    documents, tokenized_documents = clean_corpus(corpus)
    X, vocab = build_matrix(tokenized_documents)
    if fuzzy:
        query_dict = {
            doc if doc in vocab else replace(doc, vocab): occurrences
            for doc, occurrences in query_dict.items()
        }

    query_arr = np.array([query_dict.get(x, 0) for x in vocab])
    if sum(query_arr) == 0:
        raise ValueError(f'No matching strings found between vocabulary and query string: "{query_str}"')
    sims = cosine_similarity(query_arr, X)
    return [
        SimilarityInfo(
            score=sims[idx],
            match_idx=idx,
            match_string=documents[idx]
        )
        # Argsorting on -sims to get highest similarity first
        for idx in np.argsort(-sims)
    ]
