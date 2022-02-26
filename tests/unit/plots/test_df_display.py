from hela.plots import DFDisplay


def test_df_display():
    df = DFDisplay({
        'a': [1, 2],
        'b': ['xyz' * 30, 'lorem ipsum' * 100]
    })
    df._repr_html_()
