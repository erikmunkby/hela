import pandas as pd
from datetime import datetime, date
from hela import Col, NestedCol
from hela.data_types import (
    Int,
    String,
    Date,
    DateTime,
    Struct,
    Array,
    Long,
    Float
)
from copy import deepcopy

all_types_dict_list = [
    {
        'int_col': 1, 'string_col': 'a', 'date_col': str(date(2021, 1, 2)),
        'datetime_col': str(datetime.now()),
        'struct_col': {'struct_int_col': 1, 'struct_float_col': .64113},
        'array_col': ['321', '123'],
        'sub_cols': {'sub_int_col': 6, 'sub_long_col': 351351313413415133},
    },
    {
        'int_col': 2, 'string_col': 'b', 'date_col': str(date(2021, 1, 3)),
        'datetime_col': str(datetime.now()),
        'struct_col': {'struct_int_col': 2, 'struct_float_col': .1323},
        'array_col': ['hey you', 'whats up'],
        'sub_cols': {'sub_int_col': 5, 'sub_long_col': 351351313413415133},
    }
]
all_types_dataframe = pd.DataFrame(all_types_dict_list)

all_types_with_desc = [
    Col('int_col', Int(), 'Int column'),
    Col('string_col', String(), 'String column'),
    Col('date_col', Date(), 'Date column'),
    Col('datetime_col', DateTime(), 'DateTime column'),
    Col('struct_col', Struct({'struct_int_col': Int(), 'struct_float_col': Float()}), 'Simple Struct Column.'),
    Col('array_col', Array(String()), 'This is an array'),
    NestedCol('sub_cols', [
        Col('sub_int_col', Int(), 'Nested Int'),
        Col('sub_long_col', Long(), 'Nested Long')
    ]),
]


def _remove_descriptions(col_list):
    return_list = []
    for c in col_list:
        copy_c = deepcopy(c)
        if isinstance(copy_c, Col):
            copy_c.description = None
            return_list.append(copy_c)
        elif isinstance(copy_c, NestedCol):
            copy_c.columns = _remove_descriptions(copy_c.columns)
            return_list.append(copy_c)
    return return_list


all_types_no_desc = _remove_descriptions(all_types_with_desc)
