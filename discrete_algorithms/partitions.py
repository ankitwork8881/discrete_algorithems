"""Set partitions of {1, ..., n}.

A partition is returned as a list of blocks, each block a sorted list,
with blocks ordered by their smallest element, e.g. [[1, 3], [2], [4]].

* ``restricted_growth`` - lexicographic order of restricted growth strings.
* ``gray_partitions``   - consecutive partitions differ by moving one
  element to another (or a new) block.

Counts are checked against Bell and Stirling numbers of the second kind.
"""


def blocks_from_labels(labels):
    """Convert a block label per element (labels[i] for element i+1) into
    a list of blocks ordered by smallest element."""
    order = {}
    for element, label in enumerate(labels, start=1):
        order.setdefault(label, []).append(element)
    return sorted(order.values(), key=lambda block: block[0])


def restricted_growth(n):
    """All partitions in lexicographic order of restricted growth strings.

    A restricted growth string a_1..a_n has a_1 = 0 and
    a_i <= 1 + max(a_1..a_{i-1}); a_i is the block of element i.
    """
    if n == 0:
        yield []
        return
    a = [0] * n
    peak = [0] * n  # peak[i] = max(a[0..i])
    while True:
        yield blocks_from_labels(a)
        # Rightmost position that can still be incremented.
        i = n - 1
        while i > 0 and a[i] > peak[i - 1]:
            i -= 1
        if i == 0:
            return
        a[i] += 1
        peak[i] = max(peak[i - 1], a[i])
        for j in range(i + 1, n):
            a[j] = 0
            peak[j] = peak[i]


def gray_partitions(n):
    """All partitions, each obtained from the previous by moving one element.

    Built recursively: for each partition of {1..n-1} (in this same
    order), element n visits every existing block and then a new block of
    its own, sweeping forwards (first block .. new block) and backwards
    alternately. Consecutive sweeps meet with n either alone or in the
    block of 1, and the partitions of {1..n-1} differ by one move, so the
    property also holds across sweep boundaries.
    """
    if n == 0:
        yield []
        return
    labels = [0] * n
    forward = True
    for blocks in gray_partitions(n - 1):
        for index, block in enumerate(blocks):
            for element in block:
                labels[element - 1] = index
        k = len(blocks)
        for label in range(k + 1) if forward else range(k, -1, -1):
            labels[n - 1] = label
            yield blocks_from_labels(labels)
        forward = not forward


def _without(partition, element):
    """The partition with ``element`` deleted (empty blocks dropped)."""
    return frozenset(
        frozenset(block) - {element} for block in partition if list(block) != [element]
    )


def differ_by_one_move(p, q):
    """True if q is obtained from p by moving one element to another
    (possibly new) block."""
    if _without(p, None) == _without(q, None):
        return False
    return any(_without(p, e) == _without(q, e) for block in p for e in block)


def bell_numbers(n):
    """[B_0, ..., B_n] via the Bell triangle."""
    bells = [1]
    row = [1]
    for _ in range(n):
        nxt = [row[-1]]
        for value in row:
            nxt.append(nxt[-1] + value)
        row = nxt
        bells.append(row[0])
    return bells


def stirling2(n, k):
    """Stirling number of the second kind S(n, k) by the standard recurrence."""
    table = [[0] * (k + 1) for _ in range(n + 1)]
    table[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            table[i][j] = j * table[i - 1][j] + table[i - 1][j - 1]
    return table[n][k]


GENERATORS = {"restricted_growth": restricted_growth, "gray": gray_partitions}
