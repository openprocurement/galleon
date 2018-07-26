import jq


def jq_apply(filter, value, text=False):
    if text:
        return jq.jq(filter).transform(text=value, text_output=True)
    return jq.jq(filter).transform(value)


def extract_options(mapping, visitor):
    node_name = visitor.name
    def extract(mapping, visitor):
        is_array = visitor.is_array
        properties = visitor.items.properties if is_array \
            else visitor.properties
        for name in [p.name for p in properties]:
            if name not in mapping:
                if is_array:
                    mapping[name] = {'src': name}
                else:
                    mapping[name] = {
                        'src': '.'.join((node_name, name))
                    }
        return mapping

    if 'mapping' in mapping:
        options = mapping['mapping'].pop('$options', None)
        if options and options.get('$use-schema'):
            mapping['mapping'].update(extract(mapping['mapping'], visitor))
    else:
        options = mapping.pop('$options', None)
        if options and options.get('$use-schema'):
            mapping.update(extract(mapping, visitor))
    return mapping
