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
	cp dist/index.html ../catalog/web_page/index.html
	rm -rf dist