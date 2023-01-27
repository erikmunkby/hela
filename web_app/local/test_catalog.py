from pathlib import Path
from hela import Catalog
from hela import BaseDataset, Col
from hela.data_types import String
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


# Now instantiate your dataset class with one example column
my_dataset = MyDatasetClass('my_dataset', 'An example dataset.', [
    Col('my_column', String(), 'An example column.')
])


class MyCatalog(Catalog):
    my_dataset = my_dataset


jg = JsonGenerator()
json_str = jg.generate_docs_jsons([MyCatalog], include_samples=False)
p = Path('./public/local_test_data.json')
if p.exists():
    p.unlink()
p.write_text(json_str)
