import jmespath


class Finder:

    def __init__(self):
        self._cache = {}

    def __call__(self, path, data):
        if path not in self._cache:
            self._cache[path] = self._compile(path)
        return self._cache[path].search(data)

    def _compile(self, path):
        return jmespath.compile(path)


finder = Finder()