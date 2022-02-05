import os
import time
import pytest
import string
import random
from catalog.datasets.bigquery_dataset import BigqueryDataset
from catalog import Catalog
from tests import test_schemas
try:
    from google.cloud import bigquery
    from google.api_core.exceptions import NotFound
except ModuleNotFoundError:
    pass


@pytest.mark.bigquery
def test_building_gcp_table():
    # Set up IDs
    project_id = os.environ['CLOUDSDK_CORE_PROJECT']
    rid = ''.join(random.choices(string.ascii_letters, k=6))
    database_name = 'gcp_dataset_test_schema_' + rid
    database_id = f'{project_id}.{database_name}'

    # Instantiate client, assumes credentials are set up in environment
    client = bigquery.Client()

    # Build dataset
    dataset = bigquery.Dataset(database_id)
    dataset.location = 'europe-north1'
    client.create_dataset(dataset)

    # Create a catalog with one table in it
    @Catalog.setup(database=database_name)
    class BqCatalog(Catalog):
        test_table = BigqueryDataset(
            name='_test_table',
            columns=test_schemas.all_types_with_desc
        )

    # First create the table in bigquery
    BqCatalog.test_table.create_table()

    time.sleep(2)

    # Upload some data into it
    dict_list = test_schemas.all_types_dict_list
    BqCatalog.test_table.write_json(dict_list)

    # Query the table
    df = BqCatalog.test_table.query_table('SELECT * FROM TABLE')

    # Compare against dict_list
    assert df['string_col'].tolist() == [x['string_col'] for x in dict_list]

    # Delete the dataset when finished
    client.delete_dataset(database_id, delete_contents=True)
