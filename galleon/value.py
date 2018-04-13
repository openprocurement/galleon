import jq
from jsonmapping.value import is_empty, convert_value
from .transform import apply_transformations
from .finder import finder


def _get_source(mapper, bind):
    mapping = getattr(mapper, 'mapping', mapper)
    if not mapping.get('src') and mapping.get('default'):
        return (True, mapping.get('default'))
    return (False, mapping.get(
        'src', '{}'.format(bind.name)
    ))


def extract_array(mapper, bind, data):

    def extract(iterator):
        result = []
        if not isinstance(iterator, list):
            iterator = [iterator]
        for item in iterator:
            got = mapper.apply(item)
            if isinstance(got, list):
                result.extend(got)
            else:
                result.append(got)
        return result

    default, value = _get_source(mapper, bind)
    # TODO: test for default array
    if default:
        return value
    if isinstance(value, list):
        result = []
        for source in value:
            result.extend(extract(finder(source, data)))
    else:
        result = extract(finder(value, data))
    return apply_transformations(
        mapper.mapping,
        bind,
        [item for item in result if item]
        )


def extract_value(mapping, bind, data):
    """ Given a mapping and JSON schema spec, extract a value from ``data``
    and apply certain transformations to normalize the value. """
    default, src = _get_source(mapping, bind)
    if default:
        return src
    if isinstance(data, dict):  # TODO: test me
        value = finder(src, data)
    else:
        value = data
    value = apply_transformations(mapping, bind, value)
    empty = is_empty(value)
    if empty:
        value = mapping.get('default') or bind.schema.get('default')
    return value
    # TODO: breaks json serialization
    # return convert_value(bind, value)
