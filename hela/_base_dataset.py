from __future__ import annotations
import warnings
import pandas as pd
import uuid
from pathlib import Path
from abc import ABC
from typing import Optional, Set, Union, Sequence, Dict, Any, Tuple
from datetime import date
from collections import Counter
from dataclasses import dataclass
from hela._utils.date_utils import get_missing_dates
from hela._utils.dict_utils import flatten_dict
from hela._column_classes import _ColumnType
from hela._constants import _PATH_VAR
from hela._utils.path_utils import join_paths
from hela.errors import DatasetError, DuplicationError
from hela.plots.date_plots import plot_date_availability_calendar
from hela._utils.short_description import ShortDescription


@dataclass
class _DatasetInfo:
    name: str
    data_type: str
    description: str
    folder: str = None
    min_date: date = None
    max_date: date = None
    nbr_missing_dates: int = None


class Columns(Tuple[_ColumnType]):
    pass


class BaseDataset(ABC):
    """Abstract Dataset class to be used when defining building your own datasets.

    If you choose to build data interactivity through the data catalog, it is within
    your own dataset classes you would build authentication and connection logic.

    For full usage of the available catalog features implement the functions
    `BaseDataset.get_samples` and `BaseDataset.get_dates`.

    Attributes:
        name: The name of the dataset
        data_type: The data type of the dataset e.g. "parquet" or "bigquery
        description: A description of the dataset as a string
        partition_cols: A list of column names to be used for partitioning as strings
        rich_description_path:  A path to a markdown file with possibilities for longer,
                                more detailed descriptions. Primarily used for generated catalog web page.
        columns: A list of class ColumnType objects defining the columns of the dataset
        path: The path to the dataset (combination of folder and name)
    """
    _is_dataset: bool = True
    _type: str = 'Dataset'

    def __init__(
        self,
        name: str,
        data_type: str,
        folder: Optional[Union[str, Path]] = None,
        database: Optional[str] = None,
        description: Optional[str] = None,
        rich_description_path: Optional[str] = None,
        partition_cols: Optional[Sequence[str]] = None,
        columns: Optional[Sequence[_ColumnType]] = None,
    ) -> None:
        self.name = name
        self.data_type = data_type
        self.description = description
        self.rich_description_path = rich_description_path
        self.partition_cols = partition_cols
        self.database = database
        self.folder = folder
        self.path = None
        self._set_path()
        self._set_columns(columns)
        # _id used to build links in generated catalog website
        self._id: str = str(uuid.uuid4())

    def _set_columns(self, columns: Optional[Sequence[_ColumnType]] = None) -> None:
        if columns is None:
            self.columns = columns
            return
        duplicated_columns = ', '.join(
            [f'"{col.name}"' for col, count in Counter(columns).items() if count > 1]
        )
        if duplicated_columns:
            raise DuplicationError(f'Found duplication of column(s) {duplicated_columns} in dataset "{self.name}".')
        col_list = Columns(columns)
        for c in columns:
            setattr(col_list, c.name, c)
        self.columns = col_list

    def _set_path(self) -> None:
        if self.folder is None:
            return
        path = join_paths(self.folder, self.name).with_suffix(f'.{self.data_type}')
        self.path = path
        setattr(self, _PATH_VAR, path)

    def _describe(self) -> _DatasetInfo:
        info_obj = _DatasetInfo(
            name=self.name,
            data_type=self.data_type,
            description=self.description
        )
        try:
            dates = self.get_dates()
            if dates is None:
                return info_obj
            info_obj.min_date = min(dates)
            info_obj.max_date = max(dates)
            info_obj.nbr_missing_dates = len(get_missing_dates(dates))
        except NotImplementedError:
            pass
        return info_obj

    def show_columns(self, samples: bool = True) -> pd.DataFrame:
        """Returns a dataframe with information of the columns of this dataset, one column per row.

        Args:
            samples:    When true will include a sample datapoint for all columns.
                        Requires implementation of `BaseDataset.get_samples` function.

        Returns:
            A pandas dataframe with one column per row.
        """
        if self.columns is None:
            return None

        column_df = pd.DataFrame([
            cinfo.__dict__ for c in self.columns for cinfo in c._describe()
        ])
        if samples:
            try:
                fetched_samples = self.get_samples()
                if fetched_samples:
                    fetched_samples = {**fetched_samples, **flatten_dict(fetched_samples)}
                    column_df.loc[:, 'Sample'] = column_df.name.apply(lambda x: fetched_samples.get(x, None))
            except NotImplementedError:
                pass
        return column_df

    def show_dates(self) -> None:
        """
        Will generate a grid plot of all available dates for this dataset.
        Requires `BaseDataset.get_dates` implemented.
        """
        dates = self.get_dates()
        if dates is None:
            raise ValueError(f'No dates could be fetched from dataset {self}')
        return plot_date_availability_calendar(dates)

    def check_columns(
        self,
        column_list: Sequence[str],
        raise_undefined_columns: bool = False,
        raise_missing_columns: bool = False
    ) -> None:
        """
        Will compare the sent in column list against the dataset's defined columns
        and inform (warn or raise) regarding any discrepancies.

        Args:
            column_list: A list of names of columns as strings
            raise_undefined_columns: Optional; If True will raise if columns
                found in column_list not defined in dataset
            raise_missing_columns: If True will raise if columns
                defined in dataset not found in column_list

        Raises:
            DatasetError: If any of raise flags are set to True

        Examples:
        >>> my_dataset.check_columns(df.columns, raise_undefined_columns=True)
        """
        if self.columns is None:
            warnings.warn('Dataset has no columns specified.')
            return
        undefined_columns = set(column_list) - set([c.name for c in self.columns])
        msg = f'The following columns are not defined in dataset: {list(undefined_columns)}'
        if raise_undefined_columns:
            raise DatasetError(msg)
        warnings.warn(msg)

        missing_columns = set([c.name for c in self.columns]) - set(column_list)
        msg = f'The following columns are missing from column_list: {list(missing_columns)}'
        if raise_missing_columns:
            raise DatasetError(msg)
        warnings.warn(msg)

    @property
    def _prefix(self) -> str:
        """Returns the prefix as either folder, database or empty string."""
        if self.folder:
            return self.folder
        if self.database:
            return self.database
        return ''

    def __str__(self) -> str:
        prefix = self._prefix
        if prefix:
            return f'{prefix}:{self.name}'
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, o: BaseDataset) -> bool:
        return self.name == o.name and self._id == o._id

    def __hash__(self) -> int:
        return hash(self.__str__())

    def _desc_(self) -> ShortDescription:
        return ShortDescription(name=self.name, type=self._type, description=self.description)

    def get_dates(self) -> Optional[Set[date]]:
        """Implement this function for date inspection functionality such as `BaseDataset.show_dates`.

        Should return a set of dates when called or None if dates for some reason could not be fetched.
        """
        raise NotImplementedError

    def get_samples(self) -> Optional[Dict[str, Any]]:
        """Implement this function for sample inspection functionality used in e.g. `BaseDataset.show_columns`.

        Should return a dictionary of string keys for column names with samples:
        >>> {'my_column': 123}

        Nested columns should return names with dot-notation:
        >>> {'parent_column.my_column': 123}

        Or None if samples could not be fetched:
        >>> None
        """
        raise NotImplementedError
