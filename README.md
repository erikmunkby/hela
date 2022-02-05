# catalog: write your data catalog as code
![Unit Tests](https://github.com/erikmunkby/catalog/actions/workflows/unit_tests.yaml/badge.svg)
![Spark](https://github.com/erikmunkby/catalog/actions/workflows/test_spark.yaml/badge.svg)
![BigQuery](https://github.com/erikmunkby/catalog/actions/workflows/test_bigquery.yaml/badge.svg)
![AWS Glue](https://github.com/erikmunkby/catalog/actions/workflows/test_aws_glue.yaml/badge.svg)

# Developing
Install [Poetry](https://python-poetry.org/), then run either:

`poetry install`

for base dependencies or:

`poetry install --extras "spark glue bigquery"`

depending on which package you want to further develop.

## Testing
The test suite is built on pytest with test flags found in `pyproject.toml`. The available flags are:

`pytest -m base | spark | glue | bigquery`

# Make Commands
List of make commands and when to use them:

* `make init` initializes the repo, setting up githooks
* `make install` runs poetry install
* `make lint` runs linting checks
* `make unittest` runs unit tests
* `make update-stopwords` downloads and overwrites the stopwords file
* `make testcov` runs unit tests and prints code coverage report