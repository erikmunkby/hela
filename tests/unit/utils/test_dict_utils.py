from catalog._utils.dict_utils import flatten_dict


def test_dict_utils():
    my_dict = {
        'a': {
            'b': {'c': 123},
            'd': 321
        },
        'e': 'asdf'
    }

    expected_dict = {
        'a.b.c': 123,
        'a.d': 321,
        'e': 'asdf'
    }
    assert flatten_dict(my_dict) == expected_dict
