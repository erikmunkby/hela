import pandas as pd
from hela import BaseDataset
from hela._column_classes import _ColumnType
from typing import Optional, Sequence, Set, Union, Dict, Any
from datetime import date
from pathlib import Path


class PandasParquetDataset(BaseDataset):
    def __init__(
        self,
        name: str,
        folder: Optional[Union[str, Path]] = None,
        description: Optional[str] = None,
        rich_description_path: Optional[str] = None,
        partition_cols: Optional[Sequence[str]] = None,
        columns: Optional[Sequence[_ColumnType]] = None
    ) -> None:
        super().__init__(
            name=name,
            data_type='parquet',
            folder=folder,
            description=description,
            rich_description_path=rich_description_path,
            columns=columns,
            partition_cols=partition_cols
        )

    def write(self, df: pd.DataFrame) -> int:
        df.to_parquet(self.path, partition_cols=self.partition_cols)
        return len(df)

    def load(self) -> pd.DataFrame:
        if self.path is None:
            raise FileNotFoundError('No path has been specified for this dataset.')
        return pd.read_parquet(self.path)

    def get_dates(self) -> Optional[Set[date]]:
        if self.path is None:
            return None
        if not self.path.exists():
            return None
        return set([
            date.fromisoformat(p.stem.split('=')[-1])
            for p in self.path.iterdir()
        ])

    def get_samples(self) -> Optional[Dict[str, Any]]:
        try:
            return self.load().apply(lambda x: x[x.first_valid_index()], axis=0).to_dict()
        except FileNotFoundError:
            return None
