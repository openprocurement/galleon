import jq
from jsonmapping.value import is_empty, convert_value


FILTER_NULL = """
with_entries(
    select(.value != null)
)
"""


def filter_null(value):
    return jq.jq(FILTER_NULL).transform(value)


def extract_array(mapper, bind, data):
    
    src = mapper.mapping.get('src', '.{}'.format(bind.name))
    src = src if src.startswith('.') else '.{}'.format(src)
    
    return [
        mapper.apply(item)
        for item in jq.jq(src).transform(data)
    ]


def extract_value(mapping, bind, data):
    """ Given a mapping and JSON schema spec, extract a value from ``data``
    and apply certain transformations to normalize the value. """
    
    if not mapping.get('src') and mapping.get('default'):
        return False, mapping.get('default')
    src = mapping.get('src', '.{}'.format(bind.name))
    src = src if src.startswith('.') else '.{}'.format(src)

    value = jq.jq(src).transform(data)
    # import ipdb; ipdb.set_trace()
    # TODO: uncoment and make multiple sources work
    # values = [data.get(src) for c in src]
    # TODO: uncoment and make transforms work
    # for transform in mapping.get('transforms', []):
    #     # any added transforms must also be added to the schema.
    #     values = list(TRANSFORMS[transform](mapping, bind, values))

    # TODO: does we really need it??
    # format_str = mapping.get('format')
    # value = values[0] if len(values) else None
    # if not is_empty(format_str):
    #     value = format_str % tuple('' if v is None else v for v in values)

    empty = is_empty(value)
    
    if empty:
        value = mapping.get('default') or bind.schema.get('default')
    value = convert_value(bind, value)
    return convert_value(bind, value)