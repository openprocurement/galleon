import jq
from pkg_resources import iter_entry_points
from .finder import finder


FILTER_NULL = """
with_entries(
    select(.value != null)
)
"""

def merge_roles(mapping, bind, value):
    ids = {}

    for i, v in enumerate(value):
        id = v['identifier']['id']
        roles = v['roles']
        if id not in ids:
            ids[id] = [[i], roles]
        else:
            ids[id][0].append(i)
            ids[id][1].extend(roles)

    for _, pair in ids.items():
        for v in value:
            indexes = pair[0]
            roles = pair[1]
            for index in indexes:
                value[index]['roles'] = roles
    return value

def uniq(mapping, bind, value):
    return jq.jq('.|unique').transform(value)

def count(mapping, bind, value):
    return len(value)


TRANSFORMS = {
    'uniq': uniq,
    'unique': uniq,
    'count': count,
    'merge_roles': merge_roles
}


def apply_transformations(mapping, bind, value):
    for transform in mapping.get('transforms', []):
        if transform in TRANSFORMS:
            value = TRANSFORMS[transform](mapping, bind, value)
        else:
            try:
                value = jq.jq(transform).transform(value)
            except:
                continue
    return value


for entry in iter_entry_points('galleon.transforms'):
    TRANSFORMS[entry.name] = entry.load()
