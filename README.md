# catalog: write your data catalog as code
![Unit Tests](https://github.com/erikmunkby/catalog/actions/workflows/unit_tests.yaml/badge.svg)
![Spark](https://github.com/erikmunkby/catalog/actions/workflows/test_spark.yaml/badge.svg)
![BigQuery](https://github.com/erikmunkby/catalog/actions/workflows/test_bigquery.yaml/badge.svg)
![AWS Glue](https://github.com/erikmunkby/catalog/actions/workflows/test_aws_glue.yaml/badge.svg)

You probably already have your data job scripts version controlled, but what about your data catalog?
The answer: **write your data catalog as code!** Storing your data catalog and data documentation as code
makes your catalog searchable, referenceable, reliable, platform agnostic, sets you up for easy collaboration
and much more! This library is built to fit small and large data landscapes, but is happiest when included
from the start.

TODO: Add link to homepage, pypi?, demo repo

# Installing
Using pip:

`pip install catalog`

Using poetry:

`poetry add catalog`

# Developing
Install [Poetry](https://python-poetry.org/), then run:

`make init`

to setup the project and add githooks. Followed by:

`make install`

## Testing
The test suite is built on pytest with test flags found in `pyproject.toml`. The available flags are:

`pytest -m base | spark | glue | bigquery`


## Versioning
The versioning follows [semantic versioning](https://semver.org/) standards, together with semantic-release python package. This means
that the version number will adjust according to the commit message.
Following commit message intros are used in this package:

| Commit message                                | Release type                  |
| -----------------------------                 | ----------------------------- |
| `fix: my small fix`                           | ~~Patch~~ Fix Release    (0.0.X)|
| `feat: my new feature`                        | ~~Minor~~ Feature Release  (0.X.0)|
| `fix: removed something`<br><br>`BREAKING CHANGE: The cool feature has been removed.` | ~~Major~~ Breaking Release (X.0.0)<br /> (Note that the `BREAKING CHANGE: ` token must be in the footer of the commit) |
| `docs: documentation updates`                 | Documentation related commit. No new version |
| `ci: New workflow`                            | Continuous integration related commit (github actions). No new version |
| `tests: always more tests`                    | Test related commit. No new version. |
| `chore: moved X to folder`                    | Other small change or refactoring. No new version. |

## Docs page
In order to write and test the docs page you need all `--extras` packages installed in poetry.
When you have made updates to the docs you can make sure everything looks good running:

`pdoc --http localhost:8080 catalog`

# Make Commands
List of make commands and when to use them:

* `make init` initializes the repo, setting up githooks
* `make install` runs poetry install
* `make lint` runs linting checks
* `make unittest` runs unit tests
* `make update-stopwords` downloads and overwrites the stopwords file
* `make testcov` runs unit tests and prints code coverage report