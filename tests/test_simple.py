from galleon import Mapper
from .utils import simple_resolver as resolver


class TestMapperSimple(object):
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

    def test_simple(self, resolver, data, result):
        mapper = Mapper(
            TestMapperSimple.TEST_MAPPING,
            resolver
        )
        assert mapper.apply(data) == result

