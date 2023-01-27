# Refreshes data json based on example catalog and starts localhost webpage
build-local:
	python local/test_catalog.py
	npm start


# Generate a new index.html and copy it into catalog package
generate-index-html:
	npm run build
	npm run merge-to-one-file
	gzip dist/index.html
	cp dist/index.html.gz ../hela/web_page/index.html.gz
	rm -rf dist