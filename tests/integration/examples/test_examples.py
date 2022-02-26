import pytest
import shutil
from examples import BeerCatalog
from hela._utils.path_utils import join_paths
from examples import _data_generators


@pytest.mark.spark
def test_write_to_catalog():
    # First store the movies dataset, using Pandas Dataset
    df = _data_generators.generate_orders_dataframe()
    BeerCatalog.Sales.orders.write(df)

    # Then store the housing dataset using SparkParquetDataset
    df = _data_generators.generate_user_interaction_dataframe()
    dataset = BeerCatalog.Web.user_interactions
    dataset.write(df)

    # Test loading the data
    BeerCatalog.Sales.orders.load()
    BeerCatalog.Web.user_interactions.load()

    f = join_paths(BeerCatalog.Sales._folder)
    if f.exists():
        shutil.rmtree(str(f))

    f = join_paths(BeerCatalog.Web._folder)
    if f.exists():
        shutil.rmtree(str(f))
