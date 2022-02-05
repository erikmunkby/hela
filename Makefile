.DEFAULT_GOAL: all

# Do init stuff
.phony: init
init:
	chmod +x .github/.githooks/pre-push
	git config core.hooksPath .github/.githooks
	git config commit.template .github/commit_template.txt

# Install poetry
.PHONY: install
install:
	poetry install

# Linting
.PHONY: lint
lint:
	poetry run flake8

# Run all unit tests
.PHONY: unittest
unittest:
	poetry run pytest tests/unit

# Update NLTK list of stopwords
.phony: update-stopwords
update-stopwords:
	poetry run python -m nltk.downloader -d ./temp-nltk stopwords
	cp temp-nltk/corpora/stopwords/english catalog/math/stopwords.txt
	rm -rf temp-nltk

# Run code coverage and get report
.phony: testcov
testcov:
	poetry run coverage run -m pytest tests/unit
	poetry run coverage report -m