from __future__ import annotations
from abc import abstractmethod, ABC
from copy import copy
from dataclasses import dataclass
from hela._base_data_type import BaseDataType
from hela.data_types import Struct, PrimitiveType
from hela._utils.bigquery_utils import BigqueryMode
from typing import Optional, Sequence

from hela._utils.short_description import ShortDescription

try:
    from aws_cdk.aws_glue import Column as GlueColumn
except ModuleNotFoundError:
    pass

try:
    from pyspark.sql.types import StructField
except ModuleNotFoundError:
    pass

try:
    from google.cloud import bigquery
except ModuleNotFoundError:
    pass


@dataclass
class _ColInfo:
    name: str
    data_type: str
    description: str
    from_store: bool


class _ColumnType(BaseDataType, ABC):
    _type: str = 'Column'
    data_type: BaseDataType
    label: Optional[str] = None
    from_store: bool = False

    def __init__(self, name: str, data_type: BaseDataType, description: str) -> None:
        super().__init__(name=name, description=description)
        self.data_type = data_type

    def __eq__(self, o: _ColumnType) -> bool:
        return self.__hash__() == o.__hash__()

    def __hash__(self) -> int:
        return hash(str(self.name) + str(self.data_type))

    def __str__(self) -> str:
        return f'Col:{self.name}'

    def __repr__(self) -> str:
        return self.__str__()

    @abstractmethod
    def _describe(self) -> Sequence[_ColInfo]:
        raise NotImplementedError

    @abstractmethod
    def _spark_type(self):
        raise NotImplementedError

    @abstractmethod
    def _glue_type(self):
        raise NotImplementedError

    @abstractmethod
    def _json_type(self):
        raise NotImplementedError

    @abstractmethod
    def _bigquery_type(self):
        raise NotImplementedError

    def _desc_(self) -> ShortDescription:
        return ShortDescription(name=self.name, type=self._type, description=self.description)


class Col(_ColumnType):
    """A basic column object, for nested columns see `hela.NestedCol`.

    This class is used to define columns within a `hela.BaseDataset` or `hela.column_store`.
    Each defined column will be searchable, testable and referenceable.

    If you want to give further functionality to your columns, please this class.

    Attributes:
        name:   The name of the column.
        data_type:  The data type of the column, should be one of types found in `hela.data_types`
        description: A description of this column as a string, better descriptions yield a more secure catalog.

    Examples:
    >>> from hela import Col
    >>> from hela.data_types import String
    >>> my_col = Col('my_col', String(), 'This is an example column')
    """

    def __init__(
        self,
        name: str,
        data_type: PrimitiveType,
        description: str = None,
    ) -> None:
        super().__init__(name=name, data_type=data_type, description=description)

    def _describe(self) -> Sequence[_ColInfo]:
        return [_ColInfo(
            name=self.name,
            data_type=str(self.data_type),
            description=self.description,
            from_store=self.from_store
        )]

    def _spark_type(self):
        return StructField(name=self.name, dataType=self.data_type._spark_type())

    def _glue_type(self):
        return GlueColumn(name=self.name, type=self.data_type._glue_type(), comment=self.description)

    def _json_type(self):
        return {self.name: self.data_type._json_type()}

    def _bigquery_type(self):
        return bigquery.SchemaField(
            name=self.name,
            description=self.description,
            **self.data_type._bigquery_type().__dict__
        )

    def __str__(self) -> str:
        return f'Col(name="{self.name}", data_type={self.data_type}, description={self.description})'

    def __repr__(self) -> str:
        return self.__str__()


class NestedCol(_ColumnType):
    """A nested style column object, should be instantiated with sub columns.

    Most data stores support nested style columns, these can be built using this column class.
    These columns will be referenced with dot-notation when shown in the **catalog**.
    For dict/struct style columns see `hela.data_types.Struct`.

    Attributes:
        name:   The name of the column.
        columns:    A sequence of columns nested within this column. Can be Col or NestedCol objects.

    Examples:
    >>> from hela import NestedCol, Col
    >>> from hela.data_types import String, Int
    >>> my_col = NestedCol('my_nested_col', [
    ...     Col('nested_string', String(), 'Nested string column'),
    ...     Col('nested_int', Int(), 'Nested int column')
    ... ])
    """

    def __init__(self, name: str, columns: Sequence[_ColumnType]) -> None:
        self.columns = columns
        data_type = Struct({c.name: c.data_type for c in columns})
        super().__init__(name=name, data_type=data_type, description='A subset of columns.')

    def _describe(self) -> Sequence[_ColInfo]:
        col_info_list = []
        for c in self.columns:
            for c_desc in c._describe():
                desc = copy(c_desc)
                desc.name = f'{self.name}.{desc.name}'
                col_info_list.append(desc)
        return col_info_list

    def _spark_type(self):
        return StructField(name=self.name, dataType=self.data_type._spark_type())

    def _glue_type(self):
        return GlueColumn(name=self.name, type=self.data_type._glue_type())

    def _json_type(self):
        return {self.name: self.data_type._json_type()}

    def _bigquery_type(self):
        return bigquery.SchemaField(
            name=self.name,
            field_type='RECORD',
            mode=BigqueryMode.NULLABLE,
            fields=[c._bigquery_type() for c in self.columns]
        )

    def __str__(self) -> str:
        subs = [str(c) for c in self.columns]
        return f'NestedCol(name="{self.name}", subcols={subs})'

    def _desc_(self) -> Sequence[ShortDescription]:
        desc_list = []
        for c_desc in self.columns:
            desc = copy(c_desc._desc_())
            desc.name = f'{self.name}.{c_desc.name}'
            desc_list.append(desc)
        return desc_list

    def __repr__(self) -> str:
        return self.__str__()
