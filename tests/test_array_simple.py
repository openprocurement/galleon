from .utils import array_resolver as resolver
from .base import BaseTest


class TestArray(BaseTest):
    params = {
        'test_simple': [
            {
                'data': {
                    'id': 'id',
                    'title': 'title',
                    'data': {
                        'items': [
                            {'id': '1'},
                            {'id': '2'},
                            {'invalid': '3'}
                        ]
                    }
                },
                'result': {
                    'id': 'id',
                    'title': 'title',
                    'items': [
                        {'id': '1'}, 
                        {'id': '2'}
                    ]
                }
            }
        ]}
    TEST_MAPPING = {
        'mapping': {
            'id': {
                'src': 'id'
            },
            'title': {
                'src': 'title'
            },
            'items': {
                'src': 'data.items',
                '$ref': '#/definitions/item'
            },
        },
        'definitions': {
            'item': {
                'mapping': {
                'id': { 'src': 'id' }
                }
            }
        }
    }


class TestArrayMultipleSources(BaseTest):
    params = {
        'test_simple': [
            {
                'data': {
                    'id': 'id',
                    'title': 'title',
                    'data': {
                        'items': [
                            {'id': '1'},
                            {'id': '2'},
                            {'invalid': '3'}
                        ],
                        'values': [
                            {'id': '3'},
                            {'id': '1'}
                        ]
                    }
                },
                'result': {
                    'id': 'id',
                    'title': 'title',
                    'items': [
                        {'id': '1'}, 
                        {'id': '2'},
                        {'id': '3'}
                    ]
                }
            }
        ]}
    TEST_MAPPING = {
        'mapping': {
            'id': {
                'src': 'id'
            },
            'title': {
                'src': 'title'
            },
            'items': {
                'src': [
                    'data.items',
                    'data.values'
                ],
                'transforms': ['uniq'],
                '$ref': '#/definitions/item'
            },
        },
        'definitions': {
            'item': {
                'mapping': {
                'id': { 'src': 'id' }
                }
            }
        }
    }


# class TestArrayNested(object):
