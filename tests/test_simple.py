from .base import BaseTest
from .utils import simple_resolver as resolver


class TestMapperSimple(BaseTest):
    params = {
        'test_simple': [
            {
                "data": {'dateModified': 'date'},
                "result": {'date': 'date'}
            },
            {
                "data": {'dateModified': 'date', "invalid": "invalid"},
                "result": {'date': 'date'}
            },
            {
                "data": {'dateModified': 'date', "title": "title"},
                "result": {'date': 'date', 'title': 'title'}
            }
        ],
    }

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


class TestMapperDefault(BaseTest):
    params = {
        'test_simple': [
            {
                "data": {'id': ''},
                "result": {'id': 'id'}
            },
        ],
    }

    TEST_MAPPING = {
        'mapping': {
            'id': {
                'src': 'id',
                'default': 'id'
            },
            'title': {
                'src': 'title'
            },
            'date': {
                'src': 'dateModified'
            }
        }
    }


class TestMapperDefault2(BaseTest):
    params = {
        'test_simple': [
            {
                "data": {'id': ''},
                "result": {'id': 'id', 'title': 'title'}
            },
        ],
    }

    TEST_MAPPING = {
        'mapping': {
            'id': {
                'src': 'id',
                'default': 'id'
            },
            'title': {
                'default': 'title'
            },
        }
    }


class TestMapperTransform(BaseTest):
    params = {
        'test_simple': [
            {
                "data": {'id': 'id-123321'},
                "result": {'id': 'id'}
            },
        ],
    }

    TEST_MAPPING = {
        'mapping': {
            'id': {
                'src': 'id',
                'transforms': [
                    '.|split("-")|first'
                ]
            },
        }
    }
