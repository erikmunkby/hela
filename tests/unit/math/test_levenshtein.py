import pytest
from catalog.math import levenshtein


@pytest.mark.base
def test_distances():
    assert levenshtein.distance('a', 'alice') == .2
    assert levenshtein.distance('alice', 'a') == .2
    assert levenshtein.distance('axxcx', 'alice') == .4


@pytest.mark.base
def test_sorting():
    matches = levenshtein.sort(
        'alice',
        ['a', 'al', 'ali', 'alic', 'alicee']
    )
    assert [m.match_string for m in matches] == ['alicee', 'alic']


@pytest.mark.base
def test_replacement():
    replacement = levenshtein.replace(
        'alice',
        ['ali', 'alic', 'alicee']
    )
    assert replacement == 'alicee'
    replacement = levenshtein.replace(
        'alice',
        ['ali', 'aliceey']
    )
    assert replacement == 'alice'
