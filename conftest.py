import pytest
import pandas as pd
import shutil
from pathlib import Path
from catalog import Col, NestedCol
from catalog._column_classes import _ColumnType
from catalog.data_types import Int, String, Date, DateTime, Struct, Float, Long, Array
from typing import List, Tuple
from datetime import datetime, date


@pytest.fixture(scope='function')
def dataframe_with_schema() -> Tuple[pd.DataFrame, List[_ColumnType]]:
    df = pd.DataFrame([
        {
            'a': 1, 'b': 'a', 'date': date(2021, 1, 2), 'time': datetime.now(),
            'c': {'d': 1, 'f': .64113},
            'arrays': [321, 123],
            'col_list': {'x': 6, 'y': 351351313413415133},
        },
        {
            'a': 2, 'b': 'b', 'date': date(2021, 1, 3), 'time': datetime.now(),
            'c': {'d': 2, 'f': .1323},
            'arrays': [444, 555],
            'col_list': {'x': 5, 'y': 351351313413415133},
        },
        {
            'a': 3, 'b': 'c', 'date': date(2021, 1, 7), 'time': datetime.now(),
            'c': {'d': 3, 'f': .531},
            'arrays': [765, 999],
            'col_list': {'x': 6, 'y': 351351313413415133},
        }
    ])
    col_list = [
        Col('a', Int()),
        Col('b', String()),
        Col('date', Date()),
        Col('time', DateTime()),
        Col('c', Struct({'d': Int(), 'f': Float()})),
        Col('arrays', Array(Int())),
        NestedCol('col_list', [
            Col('x', Int()),
            Col('y', Long())
        ])
    ]
    return df, col_list


@pytest.fixture(scope='function')
def simple_dataframe() -> pd.DataFrame:
    df = pd.DataFrame({
        'a': [1, 2, 3],
        'b': [.1, .2, .3],
        'c': ['a', 'b', 'c']
    })
    return df


@pytest.fixture(scope='function')
def temp_folder() -> Path:
    temp_folder = Path('.pytest_folder')
    if not temp_folder.exists():
        temp_folder.mkdir(parents=True)
    yield temp_folder
    shutil.rmtree(str(temp_folder))


@pytest.fixture(scope='function')
def temp_path(temp_folder: Path) -> Path:
    temp_path = temp_folder / 'a_temp_path'
    yield temp_path
