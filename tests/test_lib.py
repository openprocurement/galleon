from .base import BaseTest
from .utils import simple_resolver as resolver


class TestTAG_OCSD(BaseTest):
    params = {
        'test_simple': [
            {
                "data": {'dateModified': 'date'},
                "result": {"date": "date", "tags": ["tender"], }
            }
        ],
    }
    TEST_MAPPING = {
        'mapping': {
            'date': {
                'src': 'dateModified'
            },
            'tags': {
                'src': 'tags'
            }
        },
        "transforms": [
            {
                "args": {
                    "default": "tender"
                },
                'name': "tag_ocds"
            }
        ]
    }


class TestTAG_ROLE(BaseTest):
    params = {
        'test_simple': [
            {
                "data": {'dateModified': 'date'},
                "result": {"date": "date", "tags": ["tender"], "roles": ['role']}
            }
        ],
    }
    TEST_MAPPING = {
        'mapping': {
            'date': {
                'src': 'dateModified'
            },
            'tags': {
                'src': 'tags'
            },
            "roles": {
                "src": "roles"
            }
        },
        "transforms": [
            {
                "args": {
                    "default": "tender"
                },
                'name': "tag_ocds"
            },
            {
                "name": "tag_role",
                "args": {
                    "path": '',
                    "role": "role"
                }
            }
        ]
    }



