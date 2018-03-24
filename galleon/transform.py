from pkg_resources import iter_entry_points


TRANSFORMS = {
}


for entry in iter_entry_points('galeon.transforms'):
    TRANSFORMS[entry.name] = entry.load()