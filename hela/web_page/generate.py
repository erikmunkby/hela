import gzip
import pkg_resources
from pathlib import Path
from typing import Union, Sequence
from hela import Catalog
from hela.web_page._json_generator import JsonGenerator


def generate_webpage(
    catalogs: Union[Catalog, Sequence[Catalog]],
    output_path: str,
    overwrite_existing: bool = False,
    include_samples: bool = False,
    web_app_title: str = 'Catalog'
) -> None:
    """Generates an index.html file that can be used as a data catalog website.

    Include a python script implementing this function in your CI/CD pipeline, outputting an index.html file
    that you can then use to share your data catalog (e.g. on github pages).
    For an example see (TODO: insert example repo link here).

    Args:
        catalogs:   One or multiple objects inheriting the Catalog class.
                    If you have a tree of catalogs, only the root catalog is required.
        output_path:  The folder where index.html file should end up.
        overwrite_existing: Flag whether and potential index.html file should be overwritten if existing.
        include_samples:    Flag whether to attempt to fetch sample datapoints from the columns in each
                            dataset. Requires `hela.BaseDataset.get_samples` function implemented.
        web_app_title:  Optional title of the web app.

    Raises:
        FileExistsError: If the index.html file already exists under `output_path` and overwrite_existing=False.

    Examples:
    >>> from my_catalog import MyCatalog
    >>> from hela import generate_webpage
    >>> generate_webpage(MyCatalog, '.', overwrite_existing=True)
    """
    if not isinstance(catalogs, Sequence):
        catalogs = [catalogs]

    jg = JsonGenerator()
    json_str = jg.generate_docs_jsons(catalogs, include_samples=include_samples)
    folder_path = Path(output_path)
    file_path = folder_path if '.html' in output_path else folder_path / 'index.html'
    if not folder_path.exists():
        folder_path.mkdir(parents=True)

    if file_path.exists():
        if not overwrite_existing:
            raise FileExistsError(f'File {file_path} already exists, delete or set overwrite_existing=True')
        file_path.unlink()

    # Replace placeholder script with actual json data
    replacement_str = f'<script>window.treeListData = {json_str}</script>'
    match_str = '<script id="tree-list-data"></script>'
    output_file = gzip.decompress(pkg_resources.resource_string(__name__, 'index.html.gz')).decode()
    if match_str not in output_file:
        raise ValueError('Could not insert data in frontend.')
    output_file = output_file.replace(match_str, replacement_str)

    if '[[ReplaceDashboard]]' not in output_file:
        raise ValueError(f'Could not replace title in frontend.')

    # Replace web app title with custom title
    output_file = output_file.replace('[[ReplaceTitleDashboard]]', f'<title>{web_app_title}</title>')
    output_file = output_file.replace('[[ReplaceDashboard]]', web_app_title)
    file_path.write_text(output_file)
