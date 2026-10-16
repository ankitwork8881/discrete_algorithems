"""Permutation generators in which consecutive outputs differ by one swap.

All generators yield tuples of 1..n and produce each of the n!
permutations exactly once.

* ``heap``           - one transposition per step (Heap's algorithm).
* ``recursive_swap`` - one transposition per step, recursive scheme with
  a parity-dependent swap position.
* ``johnson_trotter`` - one *adjacent* transposition per step
  (Steinhaus-Johnson-Trotter, using directed "mobile" elements).
"""


def heap(n):
    """Heap's algorithm, iterative form."""
    perm = list(range(1, n + 1))
    counters = [0] * n
    yield tuple(perm)
    i = 1
    while i < n:
        if counters[i] < i:
            j = 0 if i % 2 == 0 else counters[i]
            perm[j], perm[i] = perm[i], perm[j]
            yield tuple(perm)
            counters[i] += 1
            i = 1
        else:
            counters[i] = 0
            i += 1


def _swap_position(m, i):
    """0-based index swapped with position m-1 after the i-th sub-pass
    (1-based i) when permuting the first m entries."""
    if m % 2 == 0 and m > 2:
        return i - 1 if i < m - 1 else m - 3
    return m - 2


def recursive_swap(n):
    """Recursive generator: permute the first m-1 entries, swap position
    m-1 with a parity-dependent position, repeat m times."""
    perm = list(range(1, n + 1))

    def generate(m):
        if m <= 1:
            yield tuple(perm)
            return
        for i in range(1, m + 1):
            yield from generate(m - 1)
            if i < m:
                j = _swap_position(m, i)
                perm[j], perm[m - 1] = perm[m - 1], perm[j]

    yield from generate(n)


def johnson_trotter(n):
    """Steinhaus-Johnson-Trotter: each step swaps two adjacent entries.

    Every element has a direction (-1 left, +1 right). An element is
    mobile if it points at a smaller neighbour. Each step moves the
    largest mobile element and reverses all larger elements.
    """
    perm = list(range(1, n + 1))
    direction = [-1] * n  # indexed by position, moves with the element
    yield tuple(perm)
    while True:
        mobile = -1
        for pos, value in enumerate(perm):
            target = pos + direction[pos]
            if 0 <= target < n and perm[target] < value:
                if mobile < 0 or value > perm[mobile]:
                    mobile = pos
        if mobile < 0:
            return
        value = perm[mobile]
        target = mobile + direction[mobile]
        perm[mobile], perm[target] = perm[target], perm[mobile]
        direction[mobile], direction[target] = direction[target], direction[mobile]
        for pos in range(n):
            if perm[pos] > value:
                direction[pos] = -direction[pos]
        yield tuple(perm)


GENERATORS = {
    "heap": heap,
    "recursive_swap": recursive_swap,
    "johnson_trotter": johnson_trotter,
}


def transposition_between(p, q):
    """Return the pair of positions where p and q differ if q is p with one
    swap applied, else None."""
    diff = [i for i, (a, b) in enumerate(zip(p, q)) if a != b]
    if len(diff) == 2 and p[diff[0]] == q[diff[1]] and p[diff[1]] == q[diff[0]]:
        return tuple(diff)
    return None
