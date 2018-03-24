from .utils import simple_resolver as resolver
from .base import BaseTest



class TestMapperComplexPath(BaseTest):
    params = {
        'test_simple': [
            {
                "data": {
                    "object":{
                        'dateModified': 'date'
                    },
                    "data": {
                        "id": "id",
                        "title": "title"
                    }
                },
                "result": {
                    'date': 'date',
                    'id': "id",
                    "title": "title"
                }
            },
        ],
    }

    TEST_MAPPING = {
        'mapping': {
            'id': {
                'src': 'data.id'
            },
            'title': {
                'src': 'data.title'
            },
            'date': {
                'src': 'object.dateModified'
            }
        }
    }
