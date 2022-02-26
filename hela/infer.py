"""Includes functions to infer Catalog schemas on various data structures."""
from json.decoder import JSONDecodeError
import warnings
import pandas as pd
import json
from typing import List, Union
from pathlib import Path
from collections import defaultdict
from hela.data_types import PrimitiveType, String, Struct, Array
from hela._utils.maps import python_to_data_type_map
from hela import Col
from hela._column_classes import _ColumnType
from hela.errors import InferralError
from datetime import date


def _deep_string_inferral(s: pd.Series) -> PrimitiveType:
    # Attempt to parse column as date
    try:
        return _infer_pandas_column_type(s.apply(lambda x: date.fromisoformat(x)))
    except ValueError:
        pass

    # Attempt to parse column as datetime
    try:
        return _infer_pandas_column_type(pd.to_datetime(s))
    except ValueError:
        pass

    # Attempt to parse column as a json structure (list/dict)
    try:
        return _infer_pandas_column_type(s.apply(lambda x: json.loads(x.replace("'", '"'))))
    except JSONDecodeError:
        pass
    except TypeError:
        pass
    return String()


def _infer_pandas_column_type(s: pd.Series, deep: bool = True) -> PrimitiveType:
    s = s.dropna()

    type_set = set([type(x) for x in s])
    if len(type_set) > 1:
        raise InferralError(f'Could not infer data type for column {s.name}, multiple types found: {type_set}.')
    type_ = list(type_set)[0]

    if deep and type_ == str:
        return _deep_string_inferral(s)

    mapped_type = python_to_data_type_map.get(type_, None)
    if mapped_type is not None:
        return mapped_type

    if type_ == dict:
        combined_dicts = defaultdict(list)
        for d in s:
            for k, v in d.items():
                combined_dicts[k].append(v)
        return Struct({
            k: _infer_pandas_column_type(pd.Series(v, name=k), deep=deep)
            for k, v in combined_dicts.items()
        })

    if type_ == list:
        all_vals = []
        for sub_list in s:
            all_vals.extend(sub_list)
        return Array(_infer_pandas_column_type(pd.Series(sub_list, name=s.name), deep=deep))

    raise InferralError(f'Could not infer data type for column "{s.name}".')


def infer_schema_pandas(df: pd.DataFrame, raise_infer_errors=True, deep=True,
                        sample_size=10**6
                        ) -> List[_ColumnType]:
    """Attempts to infer the types of all columns in a pandas dataframe.

    Can handle nested (dict) columns.

    Args:
        df: A pandas dataframe
        raise_infer_errors: If raise_infer_errors is False, will default to String() and issue a warning
        deep: Will attempt to json load string types
        sample_size: Max number of rows to use for sampling (default 10**6)

    Returns:
        A list of Col objects

    Raises:
        InferralError: When a column or subcolumn could not be inferred

    """
    sample_df = df.sample(min(len(df), sample_size))
    cols = []
    for col, vals in sample_df.items():
        try:
            cols.append(Col(name=col, data_type=_infer_pandas_column_type(vals.copy(), deep=deep)))
        except InferralError as e:
            if raise_infer_errors:
                raise e
            warnings.warn(str(e) + ' Defaulting to String()')
            cols.append(Col(name=col, data_type=String()))
    return cols


def infer_schema_json(path_or_str: Union[Path, str],
                      raise_infer_errors=True, deep=True) -> List[_ColumnType]:
    """Attempts to infer the types of all objects in a json

    Args:
        path_or_str: JSON as string, JSON line (newline separator), Path to JSON, or string path to JSON
        raise_infer_errors: If raise_infer_errors is False, will default to String() and issue a warning
        deep: Will attempt to json load string types

    Returns:
        A list of Col objects

    Raises:
        InferralError: When a column or subcolumn could not be inferred
    """
    if isinstance(path_or_str, str) and path_or_str[-5:] == '.json':
        path_or_str = Path(path_or_str).read_text()
    elif isinstance(path_or_str, Path):
        path_or_str = path_or_str.read_text()

    try:
        dict_list = json.loads(path_or_str)
    except JSONDecodeError:
        dict_list = [json.loads(x) for x in path_or_str.split('\n')]

    try:
        df = pd.DataFrame(dict_list)
    except ValueError:
        df = pd.DataFrame([dict_list])

    return infer_schema_pandas(df, raise_infer_errors=raise_infer_errors, deep=deep)
