import ujson
from pkg_resources import iter_entry_points
from .lib import uniq, uniq_roles, count, \
    tag_ocds, tag_role, initialize, replace, \
    to_isoformat, to_number, merge_by_key, drop_if_not, from_json
from .utils import jq_apply


TRANSFORMS = {
    'uniq': uniq,
    'unique': uniq,
    'uniq_roles': uniq_roles,
    'count': count,
    'tag_ocds': tag_ocds,
    'tag_role': tag_role,
    'initialize': initialize,
    'replace': replace,
    'to_isoformat': to_isoformat,
    'to_number': to_number,
    'merge_by_key': merge_by_key,
    'drop_if_not': drop_if_not,
    'from_json': from_json,
}


def apply_transformations(mapping, bind, value):
    if not value:
        return ""
    raw = []
    for transform in mapping.get('transforms', []):
        arguments = {}
        if isinstance(transform, dict):
            arguments = transform.get('args')
            transform = transform.get('name')
        if transform in TRANSFORMS:
            if arguments:
                value = TRANSFORMS[transform](mapping, bind, value, args=arguments)
            else:
                value = TRANSFORMS[transform](mapping, bind, value)
        else:
            raw.append(transform)
    if raw:
        transform = '|'.join(raw)
        value = ujson.loads(jq_apply(transform, ujson.dumps(value), text=True))
    return value


for entry in iter_entry_points('galleon.transforms'):
    TRANSFORMS[entry.name] = entry.load()
