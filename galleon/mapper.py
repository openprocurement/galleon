from jsonschema import RefResolver
from jsonmapping import Mapper as BaseMapper
from jsonmapping import SchemaVisitor
from copy import deepcopy
from jq import jq
from .value import (
    extract_array,
    extract_value,
    )


class Mapper(BaseMapper):

    def __init__(
            self,
            mapping,
            resolver,
            visitor=None,
            scope=None,
            mapping_resolver=None
            ):

        if visitor is None:
            schema = resolver.referrer
            visitor = SchemaVisitor(schema, resolver, scope=scope)

        self.visitor = visitor
        self.mapping = mapping.copy()
        if not self.visitor.parent:
            self.mapping_resolver = RefResolver.from_schema(
                self.mapping
            )
        else:
            self.mapping_resolver = mapping_resolver
        if '$ref' in self.mapping:
            with self.mapping_resolver.resolving(self.mapping.pop('$ref'))\
                    as data:
                self.mapping.update(data)
            src = self.mapping.get('src')
            if src:
                _mapping = deepcopy(self.mapping)
                if self.visitor.is_object:
                    for item, prop in _mapping.get('mapping', {}).items():
                        _src = prop.get('src')
                        if _src:
                            _mapping['mapping'][item]['src'] = "{}.{}".format(
                                src, prop['src']
                                )
                    self.mapping = _mapping

    @property
    def children(self):
        if not hasattr(self, '_children'):
            if self.visitor.is_array:
                self._children = Mapper(
                    self.mapping,
                    self.visitor.resolver,
                    visitor=self.visitor.items,
                    mapping_resolver=self.mapping_resolver
                    )
            elif self.visitor.is_object:
                self._children = []
                mp = self.mapping
                for name, mappings in mp.get('mapping', {}).items():
                    if hasattr(mappings, 'items'):
                        mappings = [mappings]
                    for mapping in mappings:

                        for prop in self.visitor.properties:
                            if prop.match(name):
                                mapper = Mapper(
                                    mapping,
                                    self.visitor.resolver,
                                    visitor=prop,
                                    mapping_resolver=self.mapping_resolver
                                    )
                                self._children.append(mapper)
            else:
                self._children = None # pragma: no cover
        return self._children

    def apply(self, data):
        """ Apply the given mapping to ``data``, recursively. The return type
        is a tuple of a boolean and the resulting data element. The boolean
        indicates whether any values were mapped in the child nodes of the
        mapping. It is used to skip optional branches of the object graph. """
        if not self.visitor.parent:
            # TODO: tests
            hooks = self.mapping.get('pre-hooks', [])
            for hook in hooks:
                data = jq(hook).transform(data)

        if self.visitor.is_object:
            obj = {}
            if self.visitor.parent is None:
                if self.visitor.path:
                    obj['$schema'] = self.visitor.path

            for child in self.children:
                value = child.apply(data)
                if not value and child.optional:
                    continue  # pragma: no cover
                if value or isinstance(value, bool):
                    if child.visitor.name in obj and child.visitor.is_array:
                        obj[child.visitor.name].extend(value)
                    else:
                        obj[child.visitor.name] = value
            return obj
        elif self.visitor.is_array:
            value = extract_array(self.children, self.visitor, data)
            return value

        elif self.visitor.is_value:
            return extract_value(self.mapping, self.visitor, data)
