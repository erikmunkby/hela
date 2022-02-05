from pathlib import Path
from typing import Union, Sequence
from catalog import Catalog
from catalog.web_page._json_generator import JsonGenerator


def generate_webpage(
    catalogs: Union[Catalog, Sequence[Catalog]],
    output_folder: str,
    overwrite_existing: bool = False,
    include_samples: bool = False
) -> None:
    """Generates an index.html file that can be used as a data catalog website.

    Include a python script implementing this function in your CI/CD pipeline, outputting an index.html file
    that you can then use to share your data catalog (e.g. on github pages).
    For an example see (TODO: insert example repo link here).

    Args:
        catalogs:   One or multiple objects inheriting the Catalog class.
                    If you have a tree of catalogs, only the root catalog is required.
        output_folder:  The folder where index.html file should end up.
        overwrite_existing: Flag whether and potential index.html file should be overwritten if existing.
        include_samples:    Flag whether to attempt to fetch sample datapoints from the columns in each
                            dataset. Requires `catalog.BaseDataset.get_samples` function implemented.

    Raises:
        FileExistsError: If the index.html file already exists under `output_folder` and overwrite_existing=False.

    Examples:
    >>> from my_catalog import MyCatalog
    >>> from catalog import generate_webpage
    >>> generate_webpage(MyCatalog, '.', overwrite_existing=True)
    """
    if not isinstance(catalogs, Sequence):
        catalogs = [catalogs]

    jg = JsonGenerator()
    json_str = jg.generate_docs_jsons(catalogs, include_samples=include_samples)
    folder_path = Path(output_folder)
    file_path = folder_path / 'index.html'
    if not folder_path.exists():
        folder_path.mkdir(parents=True)

    if file_path.exists():
        if not overwrite_existing:
            raise FileExistsError(f'File {file_path} already exists, delete or set overwrite_existing=True')
        file_path.unlink()

    # TODO: Pipe the json_str into an index.html file
    file_path.write_text(json_str)
