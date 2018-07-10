import arrow
from glom import glom
from .utils import jq_apply


INITIALIZE = '. as $data | $data.{path} = (if $data.{path} then $data.{path} else {value} end)'


def to_isoformat(mapping, bind, value, args=None):
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


