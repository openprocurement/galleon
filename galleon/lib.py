import json

import arrow
import jmespath
import deep_merge
from glom import glom

from .utils import jq_apply

INITIALIZE = '. as $data | $data.{path} = (if $data.{path} then $data.{path} else {value} end)'


def raw(mapping, bind, value, args=None):
    query = args.get('query')


def to_isoformat(mapping, bind, value, args=None):
    """
    Tansforms date to isoformat
    """
    tz = None
    try:
        if args:
            for key in ('tz', 'timezone'):
                if key in args:
                    tz = args[key]
                    break

        date = arrow.get(value)
        if tz:
            date = date.replace(tzinfo=tz)

        return date.isoformat()
    except:
        return ""


def drop_if_not(mapping, bind, value, args):
    path = args.get('path', args.get('key', ''))
    if not path:
        raise ValueError("<drop_if_not: path is required>")

    if isinstance(value, list):
        return [
            item for item in value
            if jmespath.search(path, item)
        ]
    if not jmespath.search(path, value):
        return ""
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
    def check_existing(data):
        return any((
            item.get('id')
            for item in data
        ))
    default = args.get('default')
    tags = [default] if default else []
    if 'contracts' in value and\
       check_existing(value.get('contracts', [])):
        tags.append('contract')
    if 'awards' in value and\
       check_existing(value.get('awards', [])):
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
    map_with = args.get('map')
    default = args.get('default')
    replaced = map_with.get(value)
    if replaced:
        return replaced
    if default:
        return default
    return ""


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
            continue
        if id_ in roles_map:
            roles = roles_map[id_].pop('roles', [])
            roles.extend(v.get('roles', []))
            roles_map[id_] = deep_merge.merge(roles_map[id_], v)
            roles_map[id_]['roles'] = list(set(roles))
        else:
            roles_map[id_] = v
    return list(roles_map.values())


def from_json(mapping, bind, value, args):
    """
    Updates `value` with value from .json file
    """
    path = args.get('path')
    if path:
        try:
            with open(path) as f:
                json_data = json.load(f)
                updated = json_data.get(value)
                if updated:
                    return updated
                return ""
        except Exception as e:
            raise e
    raise ValueError("<from_json: path is required>")

