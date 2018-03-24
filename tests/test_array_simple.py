from .utils import array_resolver as resolver
from galleon import Mapper


class TestArray(object):
    params = {'test_simple': [
            {
                'data': {
                    'id': 'id',
                    'title': 'title',
                    'data': {
                        'items': [
                            {'id': '1'},
                            {'id': '2'}
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
                'mapping': {
                    'id': {
                        'src': 'id'
                    }
                }
            }
        }
    }

    def test_simple(self, resolver, data, result):
        assert Mapper(
                TestArray.TEST_MAPPING, resolver
            ).apply(data) == result