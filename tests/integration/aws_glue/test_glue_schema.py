import pytest
from hela.schema_generators import aws_glue_schema
from tests import test_schemas
try:
    from aws_cdk.aws_glue import Schema, Column
except ModuleNotFoundError:
    pass


@pytest.mark.glue
def test_aws_glue_schema():
    expected_schema = [
        Column(name='int_col', type=Schema.INTEGER),
        Column(name='string_col', type=Schema.STRING),
        Column(name='date_col', type=Schema.DATE),
        Column(name='datetime_col', type=Schema.TIMESTAMP),
        Column(name='struct_col', type=Schema.struct([
            Column(name='struct_int_col', type=Schema.INTEGER),
            Column(name='struct_float_col', type=Schema.FLOAT),
        ])),
        Column(name='array_col', type=Schema.array(
            input_string=Schema.STRING.input_string,
            is_primitive=Schema.STRING.is_primitive
        )),
        Column(name='sub_cols', type=Schema.struct([
            Column(name='sub_int_col', type=Schema.INTEGER),
            Column(name='sub_long_col', type=Schema.BIG_INT)
        ]))
    ]
    assert expected_schema == aws_glue_schema(test_schemas.all_types_no_desc)
