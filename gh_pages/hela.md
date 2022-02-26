You probably already have your data job scripts version controlled, but what about your data catalog?
The answer: **write your data catalog as code!** Storing your data catalog and data documentation as code makes your catalog searchable, referenceable, reliable, platform agnostic, sets you up for easy collaboration and much more! 
This library is built to fit small and large data landscapes, but is happiest when included from the start.

`Hela` (or Hel) is the norse mythological collector of souls, and the Swedish word for "whole" or "all of it". `Hela`
is designed to give everyone a chance to build a data catalog, with a low entry barrier: pure python code.

TODO: Add link to github for contributions.
TODO: Add link to repo with example catalog.

# Overview
The catalog package consists of four primary components:

* `hela.Catalog`: The eponymous class of this package. This inheritable class holds your entire catalog together,
and you can build trees of datasets in catalogs in catalogs.
* `hela.BaseDataset`: An inheritable dataset class, the second cornerstone of the package. Depending on how much
time you want to invest in this data **catalog**, it is within your own datasets you would write the most code.
See `hela.datasets.pandas_parquet_dataset.PandasParquetDataset` for examples.
* `hela.Col` & `hela.NestedCol`: The leaves of your beautiful **catalog** tree. These are referenceable,
reusable and (preferably) well documented column objects.
* `hela.column_store`: The most generous store filled with columns used in multiple datasets of your **catalog** landscape.

And let's not forget the crown of this beautiful tree:

* `hela.generate_webpage` Giving you the possibility to democratize and share your **catalog** with all recipients you want to.
Serve the site wherever you can host a static _index.html_ file such [github pages](https://pages.github.com/).


# One schema to rule them all
With high probability you have at some point have stumbled upon a situation where you have the same type of data,
represented in multiple locations of different formats. Be it JSON, a database, Parquet files or BigQuery, usually a
datapoint called e.g. _weekday_ will mean the same no matter where you are. With **catalog** you can make sure these
datapoints are of the same type, and described the same no matter the source.

Let's say you have an API that dumps JSON into some kind of blob storage. You want to dump this data into your BigQuery
table and ensure that you have the correct schema end-to-end. Using the same dataset (or list of columns) you can generate
a schema for both BigQuery and JSON:
```python
from hela import Col, schema_generators
from hela.data_types import String, Int
columns = [
    Col('product_name', String(), 'The name of the product.'),
    NestedCol('ratings', [
        Col('taste', Int(), 'A taste rating of 1-5'),
        Col('design', Int(), 'A design rating of 1-5')
    ])
]
# Generates BigQuery schema (using BigQuery SDK)
bigquery_schema = schema_generators.bigquery_schema(columns)
# Generates JSON schema (according to json-schema.org)
json_schema = schema_generators.json_schema(columns)
```

Or if you have some data stored in parquet read by spark, with overlapping columns stored in S3 managed by AWS Glue:
```python
from hela import Col, NestedCol, schema_generators, column_store
from hela.data_types import String, Int

@column_store()
class MyStore:
    product_name = Col('product_name', String(), 'The name of the product.')
    
glue_columns = [
    MyStore.product_name,
    Col('nbr_sold', Int(), 'Number sold of a specific product.')
]
spark_columns = [
    MyStore.product_name,
    Col('product_id', Int(), 'Integer identificator of a specific product.')
]
# Generates glue schema (using AWS CDK)
schema_generators.aws_glue_schema(glue_columns)
# Generate spark schema (using pyspark)
schema_generators.spark_schema(spark_columns)
```

# Getting Started
Setting up, reference the infer module here?

When building your data **catalog** it is recommended to keep the folder structure
in line with how the data will be structure in your data lake/warehouse as the example below
(for a complete example see the [showcase repo](TODO: link to showcase repo)).

```
my_catalog/
├── rich_descriptions/
│   ├── orders.md
│   └── ...
├── MyDatasets/
│   ├── best_dataset.py
│   └── ...
├── MyOtherDatasets/
│   ├── decent_dataset.py
│   └── ...
├── my_catalog.py
└── my_column_store.py
```

The next step is to build your own dataset, this is where you can put most of your code when it comes
functionality such as:

* Authentication and permissions
* Connections and configs
* Write & Load functionality
* Various partitioning and optimization logic

Important is to inherit the `hela.BaseDataset` class and shadow/hard-code any of the init fields
required.

```python
from hela import BaseDataset, Col
from hela.data_types import String

class MyDatasetClass(BaseDataset):
    def __init__(
        self,
        name: str, # Required
        description: str, # Optional but recommended
        columns: list, # Optional but recommended
        rich_description_path: str = None, # Optional, used for web app
        partition_cols: list = None,  # Optional but recommended
        # folder: str = None, # Only do one of either folder or database
        database: str, # Optional, can also be enriched via Catalog
    ) -> None:
        super().__init__(
            name,
            data_type='bigquery',
            folder=None,
            database=database,
            description=description,
            rich_description_path=rich_description_path,
            partition_cols=partition_cols,
            dependencies=None,
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
add the following code to a python script, and in the future add it in whichever CI/CD tool you use:

```python
from hela import generate_webpage

generate_webpage(MyCatalog, output_folder='.')
```

For further reading check out:

* `hela.Catalog.search` Smart search across your catalog!
* `hela.test_suite` Quality assurance and smart validations for your testing pipeline.
* [Catalog Showcase Repo](TODO: link to showcase repo) See a bigger catalog in action.


# Highlights
In the sections below you will find some important highlights of quality-of-life improvements given
by the catalog package!

## Iterate through datasets
Let's say you want to change the type of your column `best_column` from a string to an integer 
everywhere the column is used, you can do that by fetching all datasets that 
includes `best_column` using `hela.Catalog.get_columns_datasets`, then execute your query
on these datasets:

```python
from my_package import MyCatalog
columns_datasets_dict = MyCatalog.get_columns_datasets()
for dataset in columns_datasets_dict['best_column']:
    dataset.query('your schema changing spark query')
```

## Anticipate errors before they happen
Everyone knows how difficult it is to name things, especially when managing multiple datasets
across many similar domains. **Catalog** helps you keep your standards in check by making sure
no column is unknowingly duplicated between different datasets.

To combat this there is a pre-built `hela.test_suite` module filled with helper functions. The best
way to use these functions is to include them in your package test setup (e.g. pytest). For example
make sure no column name is duplicated using `hela.test_suite.catalog_tests.validate_no_duplicated_columns`.

On the other hand, sometimes as you build your catalog you find columns you would want to have the same name,
as they might include the same type of information. In these cases we can only rely on that the descriptions are
similar enough to get a hit using `hela.test_suite.description_tests.validate_description_similarity`.

## Notebook interactivity
![Date availability grid from show_dates function](TODO: Add url to image here when repo public)
![Show Columns functionality](TODO: Add url to image here when repo public)


# Advanced
**[Page under construction]**

Sometimes things work almost, but not exactly, the way you want. Here is a brief guide on how to modify the behaviour among a variety of topics.
If you improve something that you believe could be useful for other people as well, please consider contributing.

Coming soon:

* Build your own schema generators
* Build your own data types

