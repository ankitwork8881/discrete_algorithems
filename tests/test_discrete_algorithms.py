import itertools
import math

import pytest

from discrete_algorithms import partitions, permutations, sets
from discrete_algorithms.__main__ import main


# --- sets -------------------------------------------------------------------

def test_union_keeps_first_seen_order_without_duplicates():
    assert sets.union([3, 1, 3], [2, 1], []) == [3, 1, 2]
    assert sets.union() == []


def test_intersection_and_difference():
    assert sets.intersection([1, 2, 3, 2], [2, 3, 4], [3, 2]) == [2, 3]
    assert sets.difference([1, 2, 3, 4], [2], [4, 5]) == [1, 3]


@pytest.mark.parametrize(
    "inputs",
    [([1, 2], ["a", "b", "c"]), ([1], [2], [3]), ([0, 1],) * 4, ([1, 2], []), ()],
)
def test_cartesian_product_matches_itertools(inputs):
    assert sets.cartesian_product(*inputs) == list(itertools.product(*inputs))


def test_power_set():
    subsets = sets.power_set("abc")
    assert len(subsets) == 8
    assert sorted(map(tuple, subsets)) == sorted(
        c for r in range(4) for c in itertools.combinations("abc", r)
    )


# --- permutations ------------------------------------------------------------

@pytest.mark.parametrize("name", list(permutations.GENERATORS))
@pytest.mark.parametrize("n", range(1, 8))
def test_generators_produce_every_permutation_once(name, n):
    perms = list(permutations.GENERATORS[name](n))
    assert len(perms) == math.factorial(n)
    assert set(perms) == set(itertools.permutations(range(1, n + 1)))


@pytest.mark.parametrize("name", list(permutations.GENERATORS))
@pytest.mark.parametrize("n", range(2, 8))
def test_consecutive_permutations_differ_by_one_transposition(name, n):
    perms = list(permutations.GENERATORS[name](n))
    for p, q in zip(perms, perms[1:]):
        assert permutations.transposition_between(p, q) is not None


@pytest.mark.parametrize("n", range(2, 8))
def test_johnson_trotter_swaps_are_adjacent(n):
    perms = list(permutations.johnson_trotter(n))
    for p, q in zip(perms, perms[1:]):
        i, j = permutations.transposition_between(p, q)
        assert j == i + 1


def test_transposition_between():
    assert permutations.transposition_between((1, 2, 3), (3, 2, 1)) == (0, 2)
    assert permutations.transposition_between((1, 2, 3), (2, 3, 1)) is None
    assert permutations.transposition_between((1, 2), (1, 2)) is None


def test_zero_length():
    for gen in permutations.GENERATORS.values():
        assert list(gen(0)) == [()]


# --- partitions --------------------------------------------------------------

def canonical(partition):
    return tuple(tuple(block) for block in partition)


def is_partition_of(blocks, n):
    elements = [e for block in blocks for e in block]
    return sorted(elements) == list(range(1, n + 1)) and all(blocks)


@pytest.mark.parametrize("name", list(partitions.GENERATORS))
@pytest.mark.parametrize("n", range(0, 9))
def test_partition_generators_are_complete_and_distinct(name, n):
    parts = list(partitions.GENERATORS[name](n))
    assert len(parts) == partitions.bell_numbers(n)[n]
    assert len({canonical(p) for p in parts}) == len(parts)
    assert all(is_partition_of(p, n) for p in parts)
    for p in parts:
        assert [b[0] for b in p] == sorted(b[0] for b in p)
        assert all(b == sorted(b) for b in p)


@pytest.mark.parametrize("n", range(1, 9))
def test_block_count_distribution_matches_stirling(n):
    parts = list(partitions.restricted_growth(n))
    for k in range(n + 1):
        assert sum(len(p) == k for p in parts) == partitions.stirling2(n, k)


def test_restricted_growth_is_lexicographic():
    labels = []
    for p in partitions.restricted_growth(5):
        label = [0] * 5
        for index, block in enumerate(p):
            for e in block:
                label[e - 1] = index
        labels.append(label)
    assert labels == sorted(labels)


@pytest.mark.parametrize("n", range(2, 9))
def test_gray_partitions_move_one_element_per_step(n):
    parts = list(partitions.gray_partitions(n))
    for p, q in zip(parts, parts[1:]):
        assert partitions.differ_by_one_move(p, q), (p, q)


def test_differ_by_one_move():
    assert partitions.differ_by_one_move([[1, 2], [3]], [[1], [2, 3]])
    assert partitions.differ_by_one_move([[1, 2, 3]], [[1, 2], [3]])
    assert not partitions.differ_by_one_move([[1, 2], [3, 4]], [[1, 3], [2, 4]])
    assert not partitions.differ_by_one_move([[1], [2]], [[1], [2]])


def test_known_sequences():
    assert partitions.bell_numbers(10) == [1, 1, 2, 5, 15, 52, 203, 877, 4140, 21147, 115975]
    assert [partitions.stirling2(5, k) for k in range(6)] == [0, 1, 15, 25, 10, 1]


# --- command line -------------------------------------------------------------

def test_cli(capsys):
    main(["permutations", "3"])
    assert capsys.readouterr().out.splitlines() == [
        "1 2 3", "1 3 2", "3 1 2", "3 2 1", "2 3 1", "2 1 3",
    ]
    main(["partitions", "3", "--method", "restricted_growth"])
    assert capsys.readouterr().out.splitlines()[0] == "1 2 3"
    main(["product", "1,2", "a"])
    assert capsys.readouterr().out.splitlines() == ["(1, a)", "(2, a)"]
    main(["union", "1,2", "2,3"])
    assert capsys.readouterr().out.strip() == "1 2 3"
