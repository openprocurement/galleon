from .finder import finder
from .utils import jq_apply
from .lib import INITIALIZE, UNIQ, TAG_OCDS, TAG_ROLES

from pkg_resources import iter_entry_points


def uniq(mapping, bind, value):
    return jq_apply(UNIQ, value)


def initialize(mapping, bind, value, args=None):
    path = args.get('path')
    data = args.get('value')
    _filter = INITIALIZE.format(path=path, value=data)
    return jq_apply(_filter, value)


def tag_ocds(mapping, bind, value, args):
    default = args.get('default')
    return jq_apply(TAG_OCDS.format(default=default), value)


def tag_role(mapping, bind, value, args):
    path = args.get('path')
    role = args.get('role')
    return jq_apply(TAG_ROLES.format(path=path, role=role), value)

def count(mapping, bind, value):
    return len(value)


TRANSFORMS = {
    'uniq': uniq,
    'unique': uniq,
    'count': count,
    'tag_ocds': tag_ocds,
    'tag_role': tag_role,
    'initialize': initialize
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
