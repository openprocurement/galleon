from galleon import Mapper

class BaseTest(object):

    def test_simple(self, resolver, data, result):
        assert Mapper(
                self.__class__.TEST_MAPPING, resolver
            ).apply(data) == result
