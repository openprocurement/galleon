import pytest
from jsonschema import RefResolver
from galleon import Mapper


TEST_SCHEMA = {
    "title": "Model",
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "title": {"type": "string"},
        "date": {"type": "string"},
    }
}

@pytest.fixture
def resolver():
    return RefResolver.from_schema(TEST_SCHEMA)

TEST_MAPPING = {
    'mapping': {
        'id': {
           'src': 'id'
        },
        'title': {
            'src': 'title'
        },
        'date': {
            'src': 'dateModified'
        }
    }
}

@pytest.mark.parametrize("data,result", [
    ({'dateModified': 'date'}, {'date': 'date'}),
])
def test_mapper(resolver, data, result):
    mapper = Mapper(TEST_MAPPING, resolver)
    assert mapper.apply(data) == result