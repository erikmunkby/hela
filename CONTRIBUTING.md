# Contributing
All contributions are welcome! If you want to know where to start, check out
issues and the road map.

## Development setup
Install [Poetry](https://python-poetry.org/), then run:

`make init`

to setup the project and add githooks. Followed by:

`make install`

## Testing
The test suite is built on pytest with test flags found in `pyproject.toml`. The available flags are:

`pytest -m base | spark | glue | bigquery`

Tests are divided into unit tests and integration tests via folder structure, run them separately via:

`pytest tests/unit | tests/integration`


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
In order to update and test the docs page you need all `--extras` packages installed in poetry.
When you have made updates to the docs you can make sure everything looks good running:

`pdoc --http localhost:8080 catalog`

This will spin up the docs page locally.

## Make Commands
List of make commands and when to use them:

* `make init` initializes the repo, setting up githooks
* `make install` runs poetry install
* `make lint` runs linting checks
* `make unittest` runs unit tests
* `make update-stopwords` downloads and overwrites the stopwords file
* `make testcov` runs unit tests and prints code coverage report

## Web App development
For web app development see `web_app/README.md`!