import pytest
import unittest
from galleon import Mapper
from jsonschema import RefResolver
from .base import TENDER, MAPPING, SCHEMA, RESULT


class TestBechmark(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def setupBenchmark(self, benchmark):
        self.benchmark = benchmark

    def setUp(self):
        self.data = TENDER
        self.mapper = Mapper(
            MAPPING, RefResolver.from_schema(SCHEMA)
        )

    def test_benchmark(self):
        self.assertDictEqual(
            self.benchmark(self.mapper.apply, self.data),
            RESULT
        )
