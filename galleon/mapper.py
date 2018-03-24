from jsonmapping import Mapper as BaseMapper, SchemaVisitor
from .value import extract_array, extract_value, filter_null


class Mapper(BaseMapper):

    def __init__(self, mapping, resolver, visitor=None, scope=None):
        self.mapping = mapping.copy()
        if visitor is None:
            schema = resolver.referrer
            visitor = SchemaVisitor(schema, resolver, scope=scope)
        # TODO: uncoment and make work
        # if '$ref' in self.mapping:
        #     with resolver.resolving(self.mapp):
        #         uri, data = resolver.resolve(self.mapping.pop('$ref'))
        #         self.mapping.update(data)
        self.visitor = visitor

    @property
    def children(self):
        if not hasattr(self, '_children'):
            if self.visitor.is_array:
                self._children = Mapper(
                    self.mapping,
                    self.visitor.resolver,
                    visitor=self.visitor.items
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
                                    visitor=prop
                                    )
                                self._children.append(mapper)
            else:
                self._children = None
        return self._children

    def apply(self, data):
        """ Apply the given mapping to ``data``, recursively. The return type
        is a tuple of a boolean and the resulting data element. The boolean
        indicates whether any values were mapped in the child nodes of the
        mapping. It is used to skip optional branches of the object graph. """
        
        if self.visitor.is_object:
            obj = {}
            if self.visitor.parent is None:
                obj['$schema'] = self.visitor.path
            obj_empty = True
            for child in self.children:
                value = child.apply(data)
                if not value and child.optional:
                    continue
                obj_empty = False if value else obj_empty

                if child.visitor.name in obj and child.visitor.is_array:
                    obj[child.visitor.name].extend(value)
                else:
                    obj[child.visitor.name] = value
            return filter_null(obj)
        elif self.visitor.is_array:
            value = extract_array(self.children, self.visitor, data)
            return value
            
        elif self.visitor.is_value:
            return extract_value(self.mapping, self.visitor, data)