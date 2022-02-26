import pytest
from hela.math import tf_idf

corpus = [
    'dummy string query',
    'What does string-beans consist of',
    'In google you can write a search query',
    'this should always get zero relevance'
]


@pytest.mark.base
def test_sort():
    matches = tf_idf.sort('query string', corpus)
    assert [m.match_string for m in matches] == corpus[:4]

    # Should still work as well due to fuzzy vocabulary matching
    matches = tf_idf.sort('quer strin', corpus)
    assert [m.match_string for m in matches] == corpus[:4]

    # Should raise errors due to no matches in vocabulary
    with pytest.raises(ValueError):
        matches = tf_idf.sort('que stri', corpus)
