from pathlib import Path
from examples import BeerCatalog
from catalog.web_page._json_generator import JsonGenerator

jg = JsonGenerator()
json_str = jg.generate_docs_jsons([BeerCatalog], include_samples=False)
Path('./public/data.json').write_text(json_str)
