from __future__ import annotations
from pandas import DataFrame


class HTMLDisplay:
    def __init__(self, html_str):
        self.html_str = html_str

    def _repr_html_(self):
        return self.html_str


class DFDisplay(DataFrame):
    def __str__(self):
        return self.to_string(index=False)

    @property
    def _constructor(self) -> DFDisplay:
        """Required property when inheriting a pandas dataframe"""
        return DFDisplay

    def __repr__(self):
        return self.__str__()

    def _repr_html_(self):
        max_chars = 50
        hover_data_df = self.copy().astype(str).applymap(
            lambda x: x.replace('"', "'")
        )
        out_pdf = self.copy().astype(str).applymap(
            lambda x: x if len(x) < max_chars else x[:max_chars - 3] + '...'
        )
        hoverbox_props = (
            'border: 2px solid #000000;'  # Box border size
            'border-radius: 0.4em;'  # Box corners smoothness
            'position:absolute;'  # Where the box should pop up
            'z-index: 1;'  # Where the object should end up (on top)
            'visibility: hidden;'  # The default visibility mode
            'background-color: white;'  # Background color of box
            'color: #000000;'  # Text color
            'font-size: 1.1em;'  # Font size
            'max-width: 80ch;'  # Maximum number of characters per row
            'overflow-wrap: break-word;'  # How to handle text overflow
            'padding: 0.8em;'  # Padding between box and text
            'transform: translate(0px, -24px);'
        )
        return (
            out_pdf
            .style
            .set_table_attributes('class="dataframe"')
            .set_tooltips(hover_data_df, props=hoverbox_props)
            .to_html()
        )
