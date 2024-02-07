import itertools

# Product or Combination genearator: Boolean default False
def cartesian_product_tuples(data, generatecomb = False):
    if generatecomb:
        return tuple((i, j) for i in data[:-1] for j in data if j > i)
    else:
        return tuple((i, j) for i in data for j in data)

def cartesian_product_loops(data, generatecomb = False):
    yield_ = []
    if generatecomb:
        for i in data[:-1]:
            yield_.extend((i, j) for j in data if j > i)
    else:
        for i in data:
            yield_.extend((i, j) for j in data)
    return yield_

def cartesian_product_nested(data, generatecomb = False):
    yield_ = []
    for i in (data[:-1] if generatecomb else data):
        for j in data:
            if generatecomb and j > i:
                yield_.append((i, j))
            elif not generatecomb:
                yield_.append((i, j))
    return yield_

def itertools_product_combinations(data, generatecomb = False):
    if generatecomb:
        return list(itertools.combinations(data, 2))
    else:
        return list(itertools.product(data, repeat=2))

