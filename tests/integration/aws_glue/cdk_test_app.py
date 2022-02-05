import string
import random
from aws_cdk.core import App, RemovalPolicy
from aws_cdk.aws_glue import (
    Table, Database, DataFormat
)
from aws_cdk.aws_s3 import (
    Bucket
)
from catalog.schema_generators import aws_glue_schema
from catalog import Col, NestedCol
from catalog.data_types import Int, String, Date, DateTime, Float, Array, Struct, Long
from aws_cdk.core import Stack, Construct

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


class GlueStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.create_bucket()
        self.create_database()
        self.create_table()

    def create_bucket(self):
        id = bucket_name = 'test-catalog-' + ''.join(random.choices(string.ascii_lowercase, k=20))
        self.bucket = Bucket(
            self,
            id=id,
            bucket_name=bucket_name,
            removal_policy=RemovalPolicy.DESTROY,
        )

    def create_database(self):
        self.database = Database(self, id='testDB', database_name='my_test_database')

    def create_table(self):
        glue_schema = aws_glue_schema(all_types_with_desc)
        self.table = Table(
            self, id='testTable', columns=glue_schema,
            database=self.database,
            table_name='my_test_table',
            data_format=DataFormat.PARQUET,
            bucket=self.bucket,
        )


app = App()

GlueStack(app, 'glue-test-stack')

app.synth()
