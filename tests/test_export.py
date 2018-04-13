from galleon import Mapper
from jsonschema import RefResolver
from .base import TENDER, MAPPING, SCHEMA, RESULT


class TestBechmark(object):
    params = {
        'test_benchmark': [
            {'data': TENDER}
        ]
    }
    mapper = Mapper(
        MAPPING, RefResolver.from_schema(SCHEMA)
        )

    def test_benchmark(self, benchmark, data):
        result = benchmark(self.mapper.apply, TENDER)
        assert RESULT == result