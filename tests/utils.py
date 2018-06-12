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
            "tags": {"type": "array", "items": {"type": "string"}},
            "roles": {"type": "array", "items": {"type": "string"}}
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
    },
    'prehook': {
        'title': 'Model',
        'type': 'object',
        'properties': {
            'parties': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'roles': {'type': 'string'}
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


@pytest.fixture
def prehook_resolver():
    return RefResolver.from_schema(SCHEMAS['prehook'])
