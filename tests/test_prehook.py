from .base import BaseTest
from .utils import prehook_resolver as resolver

class TestMapperPrehook(BaseTest):
    params = {
        'test_simple': [
            {
                "data": {'procuringEntity': {
                    'identifier': {'id': 'id'}
                }},
                "result": {"parties": [{"roles": "procuringEntity"}]}
            },
            {
                "data": {"invalid": "invalid"},
                "result": {}
            },
            {
                "data": {"bids": 
                    [{
                        "tenderers": [{
                            'identifier': {'id': 'id'}
                        }]
                    }]
                },
                "result": {"parties": [{"roles": "tenderer"}]}
            }
        ]
    }

    TEST_MAPPING = {
        "pre-hooks": [
            "if .procuringEntity then .procuringEntity.roles |= \"procuringEntity\" else . end",
            "if .bids then .bids = (.bids | map(if .tenderers then .tenderers = (.tenderers | map(.roles |= \"tenderer\")) else . end)) else . end"
        ],
        "mapping": {
            "parties": {
                "src": [
                    "procuringEntity",
                    "bids[].tenderers[]",
                ],
                "$ref": "#/definitions/organization"
            }
        },
        "definitions": {
            "organization": {
                "mapping": {
                    "roles": {
                        "src": "roles"
                    }
                }
            }
        }
    }
