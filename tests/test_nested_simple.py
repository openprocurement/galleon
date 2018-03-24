from galleon import Mapper
from .utils import simple_resolver as resolver



class TestMapperComplexPath(object):
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
    def test_simple(self, resolver, data, result):
        mapper = Mapper(
            TestMapperComplexPath.TEST_MAPPING,
            resolver
        )
        assert mapper.apply(data) == result