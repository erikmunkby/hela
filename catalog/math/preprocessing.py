import re
import pkg_resources
from typing import Sequence, Tuple


# Load stopwords when module is loaded
stopwords = (
    pkg_resources
    .resource_string(__name__, "stopwords.txt")
    .decode()
    .strip()
    .split()
)


def clean_document(document: str) -> str:
    # Replace all space-like characters with spaces
    document = re.sub("[!,?._@+/-]", " ", document)
    # Remove all non-characters
    document = re.sub("[^a-z\\s]", "", document.lower())
    return ' '.join([x for x in document.split() if x not in stopwords])


def clean_corpus(corpus: Sequence[str]) -> Tuple[Sequence[str], Sequence[str]]:
    """Cleans a corpus of documents, returning original without invalid documents and cleaned corpus.

    Args:
        corpus: A sequence of string documents

    Returns:
        Tuple of:
            Original corpus, with any invalid documents removed
            Cleaned tokenized corpus
    """

    cleaned_corpus, tokenized_corpus = [], []
    for doc in corpus:
        if doc is None:
            continue
        clean_doc = clean_document(doc)
        if clean_doc:
            cleaned_corpus.append(doc)
            tokenized_corpus.append(clean_doc)
    return cleaned_corpus, tokenized_corpus
