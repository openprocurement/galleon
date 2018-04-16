import os.path
import json
import yaml
from galleon import Mapper

here = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(here, 'data/tender.json')) as _in:
    TENDER = json.load(_in)

with open(os.path.join(here, 'data/mapping.yaml')) as _in:
    MAPPING = yaml.load(_in)

with open(os.path.join(here, 'data/schema.json')) as _in:
    SCHEMA = json.load(_in)

with open(os.path.join(here, 'data/expected.json')) as _in:
    RESULT = json.load(_in)

class BaseTest(object):

    def test_simple(self, resolver, data, result):
        mapper = Mapper(
            self.__class__.TEST_MAPPING, resolver
        )
        parsed = mapper.apply(data)
        assert parsed == result
