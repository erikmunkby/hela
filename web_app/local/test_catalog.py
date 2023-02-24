from pathlib import Path
from hela import Catalog, column_store, BaseDataset, Col
from hela.data_types import String, Long
from hela.web_page._json_generator import JsonGenerator


class MyDatasetClass(BaseDataset):
    def __init__(
        self,
        name: str,  # Required
        description: str,  # Optional but recommended
        columns: list,  # Optional but recommended
        rich_description_path: str = None,  # Optional, used for web app
        partition_cols: list = None,  # Optional but recommended
        # folder: str = None, # Only do one of either folder or database
        database: str = None,  # Optional, can also be enriched via Catalog
    ) -> None:
        super().__init__(
            name,
            data_type='bigquery',
            folder=None,
            database=database,
            description=description,
            rich_description_path=rich_description_path,
            partition_cols=partition_cols,
            columns=columns
        )
        # Do more of your own init stuff

    def my_func(self) -> None:
        # Your own dataset function
        pass

    def get_samples(self):
        return {
            c.name: f'{c.name} SAMPLE' if str(c.data_type) == 'String' else 123
            for c in self.columns
        }


@column_store(label='shared')
class Cols:
    shared_col = Col('shared_col', String(), 'A shared column.')


if __name__ == '__main__':
    # Now instantiate your dataset class with one example column

    foo = MyDatasetClass('foo', 'A foo-lish dataset.', [
        Col('foo_col', Long(), 'Foo column only.'),
        Cols.shared_col
    ])

    bar = MyDatasetClass('bar', 'A dataset made by Bar-tholomew', columns=[
        Col('bar_col', String(), 'A bar column only.'),
        Cols.shared_col
    ])

    class MyCatalog(Catalog):
        foo = foo
        bar = bar

    jg = JsonGenerator()
    json_str = jg.generate_docs_jsons([MyCatalog], include_samples=True)
    p = Path('./public/local_test_data.json')
    if p.exists():
        p.unlink()
    p.write_text(json_str)
