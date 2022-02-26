import pytest
from hela import Catalog
from hela.datasets.pandas_parquet_dataset import PandasParquetDataset


@pytest.mark.base
def test_instantiating_catalog():
    d1 = PandasParquetDataset('dataset')

    class TestCat(Catalog):
        my_dataset = d1

    assert TestCat.get_datasets() == [d1]

    with pytest.raises(ValueError):
        # Decorating class that is not a catalog should raise ValueError
        @Catalog.setup(folder='.my_testfolder')
        class TestCat:
            my_dataset = d1

    # Decorating catalog class should work
    @Catalog.setup(folder='.my_testfolder')
    class TestCat(Catalog):
        my_dataset = d1


@pytest.mark.base
def test_nested_catalogs():
    d1 = PandasParquetDataset('dataset')
    d2 = PandasParquetDataset('sub_dataset')

    class TestCat(Catalog):
        my_dataset = d1

        @Catalog.setup(folder='.pytest_folder')
        class SubCat(Catalog):
            sub_dataset = d2

    assert TestCat.get_datasets() == [d1, d2]
    assert TestCat.get_datasets() != [d2, d1]
    assert TestCat.get_catalogs()[0]._desc_().name == 'SubCat'
