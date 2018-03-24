import jq
from pkg_resources import iter_entry_points


FILTER_NULL = """
with_entries(
    select(.value != null)
)
"""


def uniq(mapping, bind, value):
    return jq.jq('.|unique').transform(value)


TRANSFORMS = {
    'uniq': uniq,
    'unique': uniq
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
