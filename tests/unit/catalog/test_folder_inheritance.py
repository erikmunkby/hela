import pytest
import pandas as pd
from pathlib import Path
from catalog import Catalog
from catalog.datasets.pandas_parquet_dataset import PandasParquetDataset
from catalog._utils.path_utils import join_paths


@pytest.mark.base
def test_folder_inheritance(temp_folder: Path):
    a_dataset = PandasParquetDataset('a')
    b_dataset = PandasParquetDataset('b', folder='.another_folder')
    c_dataset = PandasParquetDataset('c')

    assert a_dataset.path is None
    assert b_dataset.path == join_paths('.another_folder', 'b.parquet')

    @Catalog.setup(folder=str(temp_folder))
    class TestCatalog(Catalog):
        test_dataset = a_dataset
        with_folder = b_dataset

        @Catalog.setup(folder=str(join_paths(temp_folder, 'sub_folder')))
        class SubCatalog(Catalog):
            sub_dataset = c_dataset

    # After the catalog, a_dataset (test_dataset) should change path but not b_dataset
    assert TestCatalog.test_dataset.path == join_paths(temp_folder, 'a.parquet')
    assert TestCatalog.with_folder.path == join_paths('.another_folder', 'b.parquet')
    assert TestCatalog.test_dataset.path == a_dataset.path
    assert TestCatalog.SubCatalog.sub_dataset.path == join_paths(temp_folder, 'sub_folder', 'c.parquet')


@pytest.mark.base
def test_read_write_on_nested_folder(temp_folder: Path, simple_dataframe: pd.DataFrame):
    a_dataset = PandasParquetDataset('a')
    b_dataset = PandasParquetDataset('b', folder='.another_folder')
    c_dataset = PandasParquetDataset('c')

    @Catalog.setup(folder=str(temp_folder))
    class TestCatalog(Catalog):
        test_dataset = a_dataset
        with_folder = b_dataset

        @Catalog.setup(folder=str(join_paths(temp_folder, 'sub_folder')))
        class SubCatalog(Catalog):
            sub_dataset = c_dataset

    # Make the directory since it can't write otherwise
    join_paths(temp_folder, 'sub_folder').mkdir(parents=True)

    # Make sure the written df can be accessed via both c_dataset and the catalog
    TestCatalog.SubCatalog.sub_dataset.write(simple_dataframe)
    assert simple_dataframe.equals(c_dataset.load())

    # Make sure the written df can be accessed via the path
    TestCatalog.test_dataset.write(simple_dataframe)
    assert simple_dataframe.equals(pd.read_parquet(join_paths(temp_folder, 'a.parquet')))
