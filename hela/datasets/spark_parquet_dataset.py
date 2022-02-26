from hela import BaseDataset
from hela._column_classes import _ColumnType
from datetime import date
from typing import Optional, Union, Sequence, Set
from pathlib import Path
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import first


def spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName('testing')
        .master('local[2]')
        .getOrCreate()
    )


class SparkParquetDataset(BaseDataset):
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

    def spark(self) -> SparkSession:
        return spark_session()

    def write(self, df: DataFrame) -> int:
        df.write.mode('overwrite').parquet(str(self.path), partitionBy=self.partition_cols)
        return df.count()

    def load(self):
        return self.spark().read.parquet(str(self.path))

    def get_dates(self) -> Set[date]:
        return set([
            date.fromisoformat(p.stem.split('=')[-1])
            for p in self.path.iterdir()
            if len(p.stem.split('=')) > 1
        ])

    def get_samples(self) -> dict:
        df = self.load().limit(1000)
        return df.select([first(x, ignorenulls=True).alias(x) for x in df.columns]).first().asDict()
