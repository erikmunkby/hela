"""Module consisting of all pre-built data types."""
import json
from abc import abstractmethod
from hela._base_data_type import BaseDataType
from hela._utils.bigquery_utils import BigqueryType, BigqueryMode
from typing import Dict

try:
    from aws_cdk.aws_glue import Schema as GlueSchema, Column as GlueColumn
except ModuleNotFoundError:
    pass
except json.decoder.JSONDecodeError:
    pass

try:
    from pyspark.sql import types as spark_types
except ModuleNotFoundError:
    pass

try:
    from google.cloud import bigquery
except ModuleNotFoundError:
    pass


class PrimitiveType(BaseDataType):
    """Helper class that sets up abstract methods for all other data_type classes.

    Attributes:
        name:   The name of the data type.
        description:    A description of the data type.
        json_kwargs:    Optional json key-value arguments to use for generating json schemas.
    """

    def __init__(self, name: str, description: str, json_kwargs: dict = None) -> None:
        super().__init__(name=name, description=description)
        self.json_kwargs = {} if json_kwargs is None else json_kwargs

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
    def _bigquery_type(self) -> BigqueryType:
        raise NotImplementedError


class String(PrimitiveType):
    """Regular string data type.

    Attributes:
        json_kwargs:    Optional json key-value arguments to use for generating json schemas.
    """

    def __init__(self, json_kwargs: dict = None) -> None:
        super().__init__('String', 'String object', json_kwargs=json_kwargs)

    def _spark_type(self):
        return spark_types.StringType()

    def _glue_type(self):
        return GlueSchema.STRING

    def _json_type(self):
        return {'type': 'string', **self.json_kwargs}

    def _bigquery_type(self) -> BigqueryType:
        return BigqueryType('STRING')


class Int(PrimitiveType):
    """Integer data type, represented by 32 bits.

    Attributes:
        json_kwargs:    Optional json key-value arguments to use for generating json schemas.
    """

    def __init__(self, json_kwargs: dict = None) -> None:
        super().__init__('Int', 'Integer', json_kwargs=json_kwargs)

    def _spark_type(self):
        return spark_types.IntegerType()

    def _glue_type(self):
        return GlueSchema.INTEGER

    def _json_type(self):
        return {'type': 'integer', **self.json_kwargs}

    def _bigquery_type(self) -> BigqueryType:
        return BigqueryType('INT64')


class Long(PrimitiveType):
    """Long numerical data type, represented by 64 bits.

    Attributes:
        json_kwargs:    Optional json key-value arguments to use for generating json schemas.
    """

    def __init__(self, json_kwargs: dict = None) -> None:
        super().__init__('Long', 'Long', json_kwargs=json_kwargs)

    def _spark_type(self):
        return spark_types.LongType()

    def _glue_type(self):
        return GlueSchema.BIG_INT

    def _json_type(self):
        return {'type': 'integer', **self.json_kwargs}

    def _bigquery_type(self) -> BigqueryType:
        return BigqueryType('INT64')


class Float(PrimitiveType):
    """Float decimal data type, usually represented by 32 bits.

    Attributes:
        json_kwargs:    Optional json key-value arguments to use for generating json schemas.
    """

    def __init__(self, json_kwargs: dict = None) -> None:
        super().__init__('Float', 'Float', json_kwargs=json_kwargs)

    def _spark_type(self):
        return spark_types.FloatType()

    def _glue_type(self):
        return GlueSchema.FLOAT

    def _json_type(self):
        return {'type': 'number', **self.json_kwargs}

    def _bigquery_type(self) -> BigqueryType:
        return BigqueryType('FLOAT64')


class Double(PrimitiveType):
    """Double decimal data type, usually represented by 64 bits.

    Attributes:
        json_kwargs:    Optional json key-value arguments to use for generating json schemas.
    """

    def __init__(self, json_kwargs: dict = None) -> None:
        super().__init__('Double', 'Double', json_kwargs=json_kwargs)

    def _spark_type(self):
        return spark_types.DoubleType()

    def _glue_type(self):
        return GlueSchema.DOUBLE

    def _json_type(self):
        return {'type': 'number', **self.json_kwargs}

    def _bigquery_type(self) -> BigqueryType:
        return BigqueryType('FLOAT64')


class Date(PrimitiveType):
    """Date data type e.g. YYYY-MM-dd

    Attributes:
        json_kwargs:    Optional json key-value arguments to use for generating json schemas.
    """

    def __init__(self, json_kwargs: dict = None) -> None:
        super().__init__('Date', 'Date', json_kwargs=json_kwargs)

    def _spark_type(self):
        return spark_types.DateType()

    def _glue_type(self):
        return GlueSchema.DATE

    def _json_type(self):
        return {'type': 'string', 'format': 'date', **self.json_kwargs}

    def _bigquery_type(self) -> BigqueryType:
        return BigqueryType('DATE')


class DateTime(PrimitiveType):
    """Datetime data type.

    Attributes:
        json_kwargs:    Optional json key-value arguments to use for generating json schemas.
    """

    def __init__(self, json_kwargs: dict = None) -> None:
        super().__init__('DateTime', 'DateTime', json_kwargs=json_kwargs)

    def _spark_type(self):
        return spark_types.TimestampType()

    def _glue_type(self):
        return GlueSchema.TIMESTAMP

    def _json_type(self):
        return {'type': 'string', 'format': 'date-time', **self.json_kwargs}

    def _bigquery_type(self) -> BigqueryType:
        return BigqueryType('DATETIME')


class Bool(PrimitiveType):
    """Bool data type.

    Attributes:
        json_kwargs:    Optional json key-value arguments to use for generating json schemas.
    """

    def __init__(self, json_kwargs: dict = None) -> None:
        super().__init__('Bool', 'Boolean', json_kwargs=json_kwargs)

    def _spark_type(self):
        return spark_types.BooleanType()

    def _glue_type(self):
        return GlueSchema.BOOLEAN

    def _json_type(self):
        return {'type': 'boolean', **self.json_kwargs}

    def _bigquery_type(self) -> BigqueryType:
        return BigqueryType('BOOL')


class Array(PrimitiveType):
    """Array data type, expects another primitive data type upon initialization.

    Attributes:
        item_type:  Another data type held within the array. All sub items must be of the same type.
        json_kwargs:    Optional json key-value arguments to use for generating json schemas.

    Examples:
    >>> from hela.data_types import Array, String
    >>> Array(String())
    """

    def __init__(self, item_type: PrimitiveType, json_kwargs: dict = None) -> None:
        super().__init__(f'Array({item_type.name})', 'No Description.', json_kwargs=json_kwargs)
        self.item_type = item_type

    def _spark_type(self):
        return spark_types.ArrayType(self.item_type._spark_type())

    def _glue_type(self):
        sub_type = self.item_type._glue_type()  # Returns e.g. GlueSchema.INTEGER
        return GlueSchema.array(
            input_string=sub_type.input_string,
            is_primitive=sub_type.is_primitive
        )

    def _json_type(self):
        return {'type': 'array', 'items': self.item_type._json_type(), **self.json_kwargs}

    def _bigquery_type(self) -> BigqueryType:
        array_type = self.item_type._bigquery_type()
        array_type.mode = BigqueryMode.REPEATED
        return array_type


class Struct(PrimitiveType):
    """Struct/dict/record data type, expects a dict of {str: PrimitiveType}.

    For nested columns see `hela.NestedCol`.

    Attributes:
        nested_types:   A dictionary of str: Primitive type.
        json_kwargs:    Optional json key-value arguments to use for generating json schemas.

    Examples:
    >>> from hela.data_types import Struct, String, Int
    >>> Struct({'my_string': String(), 'my_int': Int()})
    """

    def __init__(self, nested_types: Dict[str, PrimitiveType], json_kwargs: dict = None) -> None:
        desc_repr = {name: type_.name for name, type_ in nested_types.items()}
        super().__init__(f'Struct({desc_repr})', description='No Description.', json_kwargs=json_kwargs)
        self.nested_types = nested_types

    def _spark_type(self):
        return spark_types.StructType([
            spark_types.StructField(name=name, dataType=type_._spark_type())
            for name, type_ in self.nested_types.items()
        ])

    def _glue_type(self):
        return GlueSchema.struct([
            GlueColumn(name=name, type=type_._glue_type())
            for name, type_ in self.nested_types.items()
        ])

    def _json_type(self):
        nested_json_types = {name: type_._json_type() for name, type_ in self.nested_types.items()}
        return {'type': 'object', 'properties': nested_json_types, 'additionalProperties': False, **self.json_kwargs}

    def _bigquery_type(self):
        fields = (
            bigquery.SchemaField(name, **type_._bigquery_type().__dict__)
            for name, type_ in self.nested_types.items()
        )
        return BigqueryType(
            'RECORD',
            mode=BigqueryMode.NULLABLE,
            fields=fields
        )
