import pytest
import jsonschema
from jsonschema import ValidationError
from catalog.schema_generators import json_schema
from catalog import Col
from catalog.data_types import String


@pytest.mark.base
def test_json_schema_generation(dataframe_with_schema):
    df, schema = dataframe_with_schema
    expected_schema = {
        '$schema': 'http://json-schema.org/draft-07/schema',
        'type': 'object',
        'properties': {
            'a': {'type': 'integer'},
            'b': {'type': 'string'},
            'date': {'type': 'string', 'format': 'date'},
            'time': {'type': 'string', 'format': 'date-time'},
            'c': {
                'type': 'object',
                'properties': {'d': {'type': 'integer'}, 'f': {'type': 'number'}},
                'additionalProperties': False
            },
            'arrays': {
                'type': 'array',
                'items': {'type': 'integer'}
            },
            'col_list': {
                'type': 'object',
                'properties': {'x': {'type': 'integer'}, 'y': {'type': 'integer'}},
                'additionalProperties': False
            }
        }
    }

    assert expected_schema == json_schema(schema)


@pytest.mark.base
def test_json_validation_using_schema(dataframe_with_schema):
    df, schema = dataframe_with_schema
    val_schema = json_schema(schema)

    # Have to convert date/timestamp to string since that's what the jsonschema expects. Otherwise store as Long
    df.loc[:, 'date'] = df.date.astype(str)
    df.loc[:, 'time'] = df.time.astype(str)

    obj = df.to_dict(orient='records')[0]

    # Should raise no error
    jsonschema.validate(obj, schema=val_schema)

    obj.pop('col_list')
    jsonschema.validate(obj, schema=val_schema)

    # Should raise error since b is marked as a string
    obj['b'] = 123
    with pytest.raises(ValidationError):
        jsonschema.validate(obj, schema=val_schema)


@pytest.mark.base
def test_additional_json_properties():
    col_schema = [
        Col('len_string', String(json_kwargs={'maxLength': 5})),
        Col('reg_string', String(json_kwargs={'pattern': "^(\\([0-9]{3}\\))?[0-9]{3}-[0-9]{4}$"}))
    ]

    schema = json_schema(col_schema)

    with pytest.raises(ValidationError):
        jsonschema.validate({'len_string': 'too long'}, schema)
    jsonschema.validate({'len_string': 'short'}, schema)

    # Example from:
    # https://json-schema.org/understanding-json-schema/reference/string.html#regular-expressions
    with pytest.raises(ValidationError):
        jsonschema.validate({'reg_string': '(123)Something'}, schema)
    jsonschema.validate({'reg_string': '(888)555-1212'}, schema)
