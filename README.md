# `hela`: write your data catalog as code
![Unit Tests](https://github.com/erikmunkby/hela/actions/workflows/unit_tests.yaml/badge.svg)
![Spark](https://github.com/erikmunkby/hela/actions/workflows/test_spark.yaml/badge.svg)
![BigQuery](https://github.com/erikmunkby/hela/actions/workflows/test_bigquery.yaml/badge.svg)
![AWS Glue](https://github.com/erikmunkby/hela/actions/workflows/test_aws_glue.yaml/badge.svg)

You probably already have your data job scripts version controlled, but what about your data catalog?
The answer: **write your data catalog as code!** Storing your data catalog and data documentation as code makes your catalog searchable, referenceable, reliable, platform agnostic, sets you up for easy collaboration and much more! 
This library is built to fit small and large data landscapes, but is happiest when included from the start.

`Hela` (or Hel) is the norse mythological collector of souls, and the Swedish word for "whole" or "all of it". `Hela`
is designed to give everyone a chance to build a data catalog, with a low entry barrier: pure python code.

Links:
* [docs](https://erikmunkby.github.io/hela/)
* [pypi](https://pypi.org/project/hela/)
* [showcase catalog](https://erikmunkby.github.io/hela-showcase/)

## Installing
Using pip:

`pip install hela`

Using poetry:

`poetry add hela`

## Roadmap
These are up-coming features in no particular order, but contributions towards these milestones are highly appreciated! To read more about contributing check out `CONTRIBUTING.md`.

* Search functionality in web app
* More integrations (Snowflake, Redshift)
* More feature rich dataset classes
* Data lineage functionality (both visualized in notebooks and web app)
* Prettier docs page


## (Mega) Quick start
If you want to read more check out the [docs page](https://erikmunkby.github.io/hela/). If you do not have patience for that, the following is all you need to get started.

First of all build your own dataset class by inheriting the `BaseDataset` class. This class will hold most of your project specific functionality such as read/write, authentication etc.

```python
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
```

Now that you have a dataset class, and instantiated your first dataset, you can start populating your
data catalog.

```python
from hela import Catalog

class MyCatalog(Catalog):
    my_dataset = my_dataset
```

That's it! You now have a small catalog to keep building on. To view it as a web page you can
add the following code to a python script, and in the future add it in whichever CI/CD tool you use.
This will generate an `index.html` file that you can view in your browser or host on e.g. github pages.

```python
from hela import generate_webpage

generate_webpage(MyCatalog, output_folder='.')
```

To view what a bigger data catalog can look like check out the [showcase catalog](https://erikmunkby.github.io/hela-showcase/).