"""Module containing the Catalog class and helper functions."""
from __future__ import annotations
from typing import Optional, Sequence, Dict, Union
from collections import defaultdict
from hela._constants import _PATH_VAR
from hela.plots.html_displays import DFDisplay
from hela._utils.path_utils import join_paths
from hela.math import levenshtein, tf_idf
from hela._base_dataset import BaseDataset
from hela._column_classes import _ColumnType
from hela._utils.short_description import ShortDescription


def is_catalog(obj: object) -> Union[Catalog, None]:
    if getattr(obj, '_is_catalog', False):
        return obj
    return None


def is_dataset(obj: object) -> Union[BaseDataset, None]:
    if getattr(obj, '_is_dataset', False):
        return obj
    return None


class Catalog:
    """Inheritable Catalog class, used when building your own data catalog.

    The namesake of the python package, this class will turn your code from just being code into a data catalog.
    This class will make your datasets iterable, testable, referenceable and more.
    You can also decorate the catalog with the `Catalog.setup` function, giving your catalog a description and
    enriching datasets within it.

    Examples:
    >>> # Without decorator
    >>> from catalog import Catalog
    >>> class MyCatalog(Catalog):
    ...     my_dataset = Dataset(...)

    >>> # With decorator
    >>> from catalog import Catalog
    >>> @Catalog.setup(folder='sales', description='Datasets related to sales.')
    >>> class SalesCatalog(Catalog):
    ...     my_dales_dataset = Dataset(...)
    """
    _is_catalog: bool = True
    _type: str = 'Catalog'
    _folder: str = None
    _database: str = None
    _description: str = None
    _rich_description_path: str = None

    @staticmethod
    def setup(
        cls: Catalog = None,
        folder: Optional[str] = None,
        database: Optional[str] = None,
        description: Optional[str] = None,
        rich_description_path: Optional[str] = None
    ) -> Catalog:
        """Decorator enriching the catalog with a description, and optionally binding
        a folder or database to all datasets within it.

        Args:
            folder: Used for filestore style datasets (e.g. spark),
                    build the catalogs folder structure.
            database:   Used for database style datasets (e.g. bigquery,
                        aws glue) builds the catalogs database structure.
            description:    A description of this catalog.
            rich_description_path: Path to markdown file with richer descriptions of this catalog.
        """

        def wrap(cls: Catalog):
            if not getattr(cls, '_is_catalog', False):
                raise ValueError(f'Class {cls} must inherit Catalog class.')
            cls._folder = folder
            cls._database = database
            cls._description = description
            cls._rich_description_path = rich_description_path
            _enrich_datasets(cls, folder=folder, database=database)
            return cls

        # When called with pathentheses "@catalog()"
        if cls is None:
            return wrap

        # When called without pathentheses "@catalog"
        return wrap(cls)

    @classmethod
    def get_catalogs(cls, recursive: bool = True) -> Sequence[Catalog]:
        """Get a list of all sub-catalogs of this catalog, not including self.

        Args:
            recursive:  Flag whether to search for sub-catalog in this catalog's sub-catalogs.

        Returns:
            A list of objects inheriting the Catalog class.
        """
        catalog_list = []
        for obj in cls.__dict__.values():
            catalog = is_catalog(obj)
            if catalog:
                catalog_list.append(catalog)
                if recursive:
                    catalog_list.extend(catalog.get_catalogs())
        return catalog_list

    @classmethod
    def get_datasets(cls, recursive: bool = True) -> Sequence[BaseDataset]:
        """Returns a list of all datasets within this catalog, recursively if flag is set.

        Args:
            recursive: When set to true this function will fetch datasets from sub-catalogs of this catalog.

        Returns:
            A list of dataset objects.
        """
        dataset_list = []
        for obj in cls.__dict__.values():
            dataset = is_dataset(obj)
            if dataset:
                dataset_list.append(obj)
            elif recursive:
                catalog = is_catalog(obj)
                if catalog:
                    dataset_list.extend(catalog.get_datasets())
        return dataset_list

    @classmethod
    def get_columns_datasets(cls, recursive: bool = True) -> Dict[_ColumnType, Sequence[BaseDataset]]:
        column_dict = defaultdict(list)
        for dataset in cls.get_datasets(recursive=recursive):
            if dataset.columns is None:
                continue

            for column in dataset.columns:
                column_dict[column].append(dataset)
        return column_dict

    @classmethod
    def show_datasets(cls, recursive: bool = True) -> DFDisplay:
        """Returns a DFDisplay with a description of all datasets in this catalog, one dataset per row.

        Args:
            recursive: Whether to show dataset recursively in subcatalogs.

        Returns:
            DFDisplay (pandas dataframe)
        """
        return DFDisplay([
            d._describe().__dict__
            for d in cls.get_datasets(recursive=recursive)
        ])

    @classmethod
    def show_columns(cls, recursive: bool = True) -> DFDisplay:
        """Returns a pandas dataframe with a description of all columns in this catalog, one column per row.

        Args:
            recursive: Whether to show dataset recursively in subcatalogs.

        Returns:
            DFDisplay (pandas dataframe)
        """
        df = DFDisplay([
            {
                **col.__dict__,
                'datasets': datasets
            }
            for col_obj, datasets in cls.get_columns_datasets(recursive=recursive).items()
            for col in col_obj._describe()
        ])
        return df.sort_values('name').reset_index(drop=True)

    @classmethod
    def _all_descriptions(cls, recursive=True) -> Sequence[ShortDescription]:
        """Collect descriptions for all Catalogs, Datasets and Columns.

        Args:
            recursive:  Whether to search recursively through sub-catalogs.

        Returns:
            A sequence of ShortDescription objects
        """
        column_descriptions = []
        for c in cls.get_columns_datasets(recursive=recursive).keys():
            desc = c._desc_()
            # Columns will sometimes give a sequence if it is a nested column
            if isinstance(desc, Sequence):
                column_descriptions.extend(desc)
            else:
                column_descriptions.append(desc)
        return [
            *column_descriptions,
            *[d._desc_() for d in cls.get_datasets(recursive=recursive)],
            *[c._desc_() for c in cls.get_catalogs(recursive=recursive)],
            cls._desc_()
        ]

    @classmethod
    def search(cls, query_str: str, recursive: bool = True, max_hits: int = 5, min_relevance: float = .1) -> DFDisplay:
        """Searches across names and descriptions of Catalogs, Datasets and Columns.

        * Search on name is based on Levenshtein distance (fuzzy search).
        * Search on description is based on cosine similarity of TF-IDF matrix.

        Args:
            query_str:  The string to base the search on.
            recursive:  Whether to search recursively through sub-catalogs.
            max_hits:   Maximum number of hits to return.
            min_relevance: Minimum required relevance score to return a hit.

        Returns:
            A DFDisplay (pandas) dataframe with hits sorted on relevance.
        """

        # Create dictionaries to collect into unique name/desc keys
        name_dict, desc_dict = defaultdict(list), defaultdict(list)
        for short_desc in cls._all_descriptions(recursive=recursive):
            name = short_desc.name
            if name is not None:
                name_dict[name].append(short_desc)
                # Take both original and split version if we're dealing with nested columns
                # E.g. ratings.taste
                if '.' in name:
                    name_dict[name.split('.')[-1]].append(short_desc)
            if short_desc.description is not None:
                desc_dict[short_desc.description].append(short_desc)

        l_search = levenshtein.sort(query_str, list(name_dict.keys()), min_similarity=.5)
        try:
            tf_idf_search = tf_idf.sort(query_str, list(desc_dict.keys()))
        except ValueError:
            # Raised when we get no vocabulary matches at all
            tf_idf_search = []

        relevance_col = 'relevance'

        hit_df = DFDisplay([
            *[
                {
                    **short_desc.__dict__,
                    relevance_col: hit.score,
                    'hit_on': 'name'
                }
                for hit in l_search
                for short_desc in name_dict[hit.match_string]
            ],
            *[
                {
                    **short_desc.__dict__,
                    relevance_col: hit.score,
                    'hit_on': 'description'
                }
                for hit in tf_idf_search
                for short_desc in desc_dict[hit.match_string]
            ]
        ])
        error_msg = f'No hits good enough found on query string: "{query_str}"'
        if len(hit_df) == 0:
            raise ValueError(error_msg)
        hit_df = hit_df[hit_df[relevance_col] > min_relevance]

        if len(hit_df) == 0:
            raise ValueError(error_msg)

        hit_df.loc[:, relevance_col] = hit_df[relevance_col].round(2)
        return (
            hit_df
            .sort_values(relevance_col, ascending=False)
            .drop_duplicates(subset=['name', 'type'])
            [:max_hits]
        )

    @classmethod
    def _desc_(self) -> ShortDescription:
        return ShortDescription(name=self.__name__, type=self._type, description=self._description)


def _enrich_datasets(
        catalog: Catalog,
        folder: Optional[str] = None,
        database: Optional[str] = None) -> None:
    """Perform various enrichments such as extending with path, database and adding its own catalog.

    Args:
        folder:     If folder is set on catalog, add it
        database:   If database is set on catalog, add it
    """
    # Loop through all datasets in the catalog, non-recursive
    for dataset in catalog.get_datasets(recursive=False):
        # If folder input is not None and dataset has no folder already
        if folder and dataset.folder is None:
            dataset_path = join_paths(folder, dataset.name).with_suffix('.' + dataset.data_type)
            setattr(dataset, 'folder', folder)
            setattr(dataset, _PATH_VAR, dataset_path)

        # If database is not None, and dataset has no database already
        if database and dataset.database is None:
            setattr(dataset, 'database', database)
