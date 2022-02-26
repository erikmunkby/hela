import pytest
from hela.datasets.pandas_parquet_dataset import PandasParquetDataset
from hela.errors import ValidationError
from hela import column_store, Col, Catalog
from hela.data_types import String
from hela.test_suite.catalog_tests import (
    validate_dataset_variable_names,
    validate_no_duplicated_columns
)


@pytest.mark.base
def test_dataset_field_name_validations():
    @Catalog.setup(folder='.pytest_folder')
    class Cat(Catalog):
        my_dataset = PandasParquetDataset('my_dataset')

    assert validate_dataset_variable_names(Cat)

    @Catalog.setup(folder='.pytest_folder')
    class Cat(Catalog):
        wrong_name = PandasParquetDataset('my_dataset')

    with pytest.raises(ValidationError):
        validate_dataset_variable_names(Cat)


@pytest.mark.base
def test_no_column_duplicates_validations():
    @Catalog.setup(folder='.pytest_folder')
    class Cat(Catalog):
        a_dataset = PandasParquetDataset('a_dataset', columns=[
            Col('a', String()),
            Col('b', String())
        ])

        @Catalog.setup(folder='sub')
        class SubCat(Catalog):
            b_dataset = PandasParquetDataset('b_dataset', columns=[
                Col('c', String()),
                Col('d', String())
            ])

    assert validate_no_duplicated_columns(Cat)

    @Catalog.setup(folder='.pytest_folder')
    class Cat(Catalog):
        a_dataset = PandasParquetDataset('a_dataset', columns=[
            Col('a', String()),
            Col('b', String())
        ])

        @Catalog.setup(folder='sub')
        class SubCat(Catalog):
            b_dataset = PandasParquetDataset('b_dataset', columns=[
                Col('c', String()),
                Col('b', String())
            ])

    with pytest.raises(ValidationError):
        validate_no_duplicated_columns(Cat)

    @column_store()
    class Store:
        b = Col('b', String())

    @Catalog.setup(folder='.pytest_folder')
    class Cat(Catalog):
        a_dataset = PandasParquetDataset('a_dataset', columns=[
            Col('a', String()),
            Col('b', String())
        ])

        @Catalog.setup(folder='sub')
        class SubCat(Catalog):
            b_dataset = PandasParquetDataset('b_dataset', columns=[
                Col('c', String()),
                Store.b
            ])

    with pytest.raises(ValidationError):
        validate_no_duplicated_columns(Cat)

    @Catalog.setup(folder='.pytest_folder')
    class Cat(Catalog):
        a_dataset = PandasParquetDataset('a_dataset', columns=[
            Col('a', String()),
            Store.b
        ])

        @Catalog.setup(folder='sub')
        class SubCat(Catalog):
            b_dataset = PandasParquetDataset('b_dataset', columns=[
                Col('c', String()),
                Store.b
            ])

    assert validate_no_duplicated_columns(Cat)
