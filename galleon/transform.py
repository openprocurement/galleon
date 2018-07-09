from .finder import finder
from .utils import jq_apply
from .lib import INITIALIZE

from pkg_resources import iter_entry_points
from glom import glom


def uniq(mapping, bind, value):
    result = []
    for v in value:
        if v not in result:
            result.append(v)
    return result


def initialize(mapping, bind, value, args=None):
    path = args.get('path')
    data = args.get('value')
    _filter = INITIALIZE.format(path=path, value=data)
    return jq_apply(_filter, value)


def tag_ocds(mapping, bind, value, args):
    default = args.get('default')
    tags = [default] if default else []
    if 'contracts' in value:
        tags.append('contract')
    if 'awards' in value:
        tags.append('award')
    if 'tags' in value:
        value['tags'].extend(tags)
    else:
        value['tags'] = tags
    return value


def tag_role(mapping, bind, value, args):
    path = args.get('path')
    role = args.get('role')
    if path:
        field = glom(value, path)
    else:
        field = value
    if isinstance(field, list):
        for f in field:
            if 'roles' in f:
                f['roles'].append(role)
            else:
                f['roles'] = [role]
    elif 'roles' in field:
        field['roles'].append(role)
    else:
        field['roles'] = [role]
    return value


def count(mapping, bind, value):
    return len(value)


def replace(mapping, bind, value, args=None):
    replaced = args.get(value)
    if replaced:
        return replaced
    return value


def uniq_roles(mapping, bind, value):
    roles_map = dict()
    for v in value:
        id_ = v.get('id', '')
        if not id_:
            id_ = v.get('name')
        if not id_:
            return value
        if id_ in roles_map:
            roles_map[id_].setdefault('roles', []).extend(v.get('roles',[]))
            roles_map[id_]['roles'] = list(set(roles_map[id_]['roles']))
        else:
            roles_map[id_] = v
    return list(roles_map.values())


TRANSFORMS = {
    'uniq': uniq,
    'unique': uniq,
    'uniq_roles': uniq_roles,
    'count': count,
    'tag_ocds': tag_ocds,
    'tag_role': tag_role,
    'initialize': initialize,
    'replace': replace
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
