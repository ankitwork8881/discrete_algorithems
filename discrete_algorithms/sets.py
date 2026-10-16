"""Finite set operations on sequences, keeping first-seen order.

Inputs can be any iterables of hashable items. Results are lists, so
the output order is deterministic and easy to test.
"""


def union(*sets):
    """Elements appearing in any input, each once, in first-seen order."""
    seen = set()
    result = []
    for s in sets:
        for item in s:
            if item not in seen:
                seen.add(item)
                result.append(item)
    return result


def intersection(first, *others):
    """Elements of ``first`` that appear in every other input."""
    lookups = [set(s) for s in others]
    return [item for item in union(first) if all(item in s for s in lookups)]


def difference(first, *others):
    """Elements of ``first`` that appear in none of the other inputs."""
    excluded = set(union(*others))
    return [item for item in union(first) if item not in excluded]


def cartesian_product(*sets):
    """All tuples (a1, ..., ak) with ai from the i-th input.

    Generated iteratively like an odometer: the last coordinate changes
    fastest. The product of zero sets is [()].
    """
    pools = [union(s) for s in sets]
    if any(not pool for pool in pools):
        return []
    indices = [0] * len(pools)
    result = []
    while True:
        result.append(tuple(pool[i] for pool, i in zip(pools, indices)))
        position = len(pools) - 1
        while position >= 0:
            indices[position] += 1
            if indices[position] < len(pools[position]):
                break
            indices[position] = 0
            position -= 1
        if position < 0:
            return result


def power_set(s):
    """All subsets of ``s``, ordered by the binary counter over its elements."""
    items = union(s)
    return [
        [item for bit, item in enumerate(items) if mask >> bit & 1]
        for mask in range(1 << len(items))
    ]
