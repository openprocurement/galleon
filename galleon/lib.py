import arrow
from glom import glom
from .utils import jq_apply


INITIALIZE = '. as $data | $data.{path} = (if $data.{path} then $data.{path} else {value} end)'


def to_isoformat(mapping, bind, value, args=None):
    """
    Tansforms date to isoformat
    """
    tz = None
    try:
        for key in ('tz', 'timezone'):
            if key in args:
                tz = args[key]
                break

        date = arrow.get(value)
        if tz:
            date = date.replace(tzinfo=tz)

        return date.isoformat()
    except:
        return value


def to_number(mapping, bind, value):
    """
    Transforms value to number
    """
    if value:
        return float(value)
    return None


def merge_by_key(mapping, bind, value, args={}):
    """
    Merges list of objects by provided key (default is `id`).
    """
    if not isinstance(value, list):
        return value
    key = args.get('key', 'id')
    result = {}
    for obj in value:
        result.setdefault(key, {}).update(obj)
    return list(result.values())


def uniq(mapping, bind, value):
    """
    Makes elements unique
    """
    result = []
    for v in value:
        if v not in result:
            result.append(v)
    return result


def initialize(mapping, bind, value, args=None):
    """
    Initializes provided path with provided value
    """
    path = args.get('path')
    data = args.get('value')
    _filter = INITIALIZE.format(path=path, value=data)
    return jq_apply(_filter, value)


def tag_ocds(mapping, bind, value, args):
    """
    Makes tags array according to OCDS specification
    """
    default = args.get('default')
    tags = [default] if default else []
    if 'contracts' in value:
        tags.append('contract')
    if 'awards' in value:
        tags.append('award')
    value.setdefault('tags', [])
    value['tags'].extend(tags)
    return value


def tag_role(mapping, bind, value, args):
    """
    Tag object with roles
    """
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
    """
    Counts elements
    """
    return len(value)


def replace(mapping, bind, value, args=None):
    """
    Replaces elements in one object by elements from provided
    """
    replaced = args.get(value)
    if replaced:
        return replaced
    return value


def uniq_roles(mapping, bind, value):
    """
    Makes roles unique
    """
    roles_map = dict()
    for v in value:
        id_ = v.get('id', '')
        if not id_:
            id_ = v.get('name')
        if not id_:
            return value
        if id_ in roles_map:
            roles_map[id_].setdefault('roles', []).extend(v.get('roles', []))
            roles_map[id_]['roles'] = list(set(roles_map[id_]['roles']))
        else:
            roles_map[id_] = v
    return list(roles_map.values())
