import jq

def jq_apply(filter, value):
    return jq.jq(filter).transform(value)
