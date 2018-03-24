import pytest
from jsonschema import RefResolver

SCHEMAS = {
    'simple':{
        "title": "Model",
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "title": {"type": "string"},
            "date": {"type": "string"},
        }
    },
    'array': {
        "title": "Model",
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "title": {"type": "string"},
            'items': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'string'
                        }
                    }
                }
            }
            
        }
    }
}



@pytest.fixture
def simple_resolver():
    return RefResolver.from_schema(SCHEMAS['simple'])


@pytest.fixture
def array_resolver():
    return RefResolver.from_schema(SCHEMAS['array'])