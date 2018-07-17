from pkg_resources import iter_entry_points
from .lib import uniq, uniq_roles, count,\
    tag_ocds, tag_role, initialize, replace,\
    to_isoformat, to_number, merge_by_key, drop_if_not
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
}


def apply_transformations(mapping, bind, value):
    if not value:
        return ""
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
            value = jq_apply(transform, value)
    return value


for entry in iter_entry_points('galleon.transforms'):
    TRANSFORMS[entry.name] = entry.load()
