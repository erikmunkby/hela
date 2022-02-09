# Refreshes data json based on example catalog and starts localhost webpage
build-local:
	cp -r ../examples examples
	python -m generate_data_json
	rm -rf examples
	npm start


# Generate a new index.html and copy it into catalog package
generate-index-html:
	npm run build
	npm run merge-to-one-file
	gzip dist/index.html
	cp dist/index.html.gz ../catalog/web_page/index.html.gz
	rm -rf dist