import itertools

# Yielded Product or Combination genearator: Boolean default False
def tuplefunc(data, generatecomb = False):
    net_yield = []; len_data = len(data)
    if generatecomb:
        len_data -= 1
        yield_ = tuple((i,j) for i in data[:-1] for j in data if j > i)
    else:
        yield_ = tuple((i,j) for i in data for j in data)
    for index in range(len_data,0,-1) if generatecomb else range(len_data):
        net_yield.append(yield_[:len_data])
        yield_ = yield_[len_data:]
    return net_yield
        
def loopfunc(data, generatecomb = False):
    yield_ = []
    if generatecomb:
        for i in data[:-1]:
            yield_.append(tuple((i , j)for j in data if j > i))
    else:
        for i in data:
            yield_.append(tuple((i,j)for j in data))
    return yield_
   
def nestfunc(data, generatecomb = False):
    net_yield = []
    for i in (data[:-1] if generatecomb else data):
        yield_ = []
        for j in data:
            if generatecomb:
                if j > i:
                    yield_.append((i, j))
            else:
                yield_.append((i, j))
        net_yield.append(yield_)
    return net_yield

def iterfunc(data, generatecomb = False):
    net_yield = []; len_data = len(data)
    if generatecomb:
        len_data -= 1
        yield_ = tuple(itertools.combinations(data, 2))
    else:
        yield_ = tuple(itertools.product(data, repeat = 2))
    for index in range(len_data,0,-1) if generatecomb else range(len_data):
        net_yield.append(yield_[:len_data])
        yield_ = yield_[len_data:]
    return net_yield
    

