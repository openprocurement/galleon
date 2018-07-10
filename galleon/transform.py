from pkg_resources import iter_entry_points
from .lib import uniq, uniq_roles, count,\
    tag_ocds, tag_role, initialize, replace,\
    to_isoformat


TRANSFORMS = {
    'uniq': uniq,
    'unique': uniq,
    'uniq_roles': uniq_roles,
    'count': count,
    'tag_ocds': tag_ocds,
    'tag_role': tag_role,
    'initialize': initialize,
    'replace': replace,
    'to_isoformat': to_isoformat
}


def apply_transformations(mapping, bind, value):
    for transform in mapping.get('transforms', []):
        args = {}
        if isinstance(transform, dict):
            args = transform.get('args')
            transform = transform.get('name')
        if transform in TRANSFORMS:
            if args:
                value = TRANSFORMS[transform](mapping, bind, value, args=args)
            else:
                value = TRANSFORMS[transform](mapping, bind, value)
        else:
            try:
                value = jq_apply(transform, value)
            except:
                continue
    return value


for entry in iter_entry_points('galleon.transforms'):
    TRANSFORMS[entry.name] = entry.load()
