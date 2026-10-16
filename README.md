# discrete_algorithms

Combinatorial generation in pure Python 3 (no dependencies). It generates permutations and set partitions in minimal-change order, where each output differs from the previous one by the smallest possible change, and includes basic finite-set operations.

## Contents

### Permutations of {1, …, n}: `permutations`

Each generator yields all `n!` permutations exactly once, and consecutive permutations differ by a single transposition.

| Generator | Change between consecutive outputs |
|---|---|
| `heap` | one transposition (Heap's algorithm, iterative) |
| `recursive_swap` | one transposition; recursive scheme: permute the first `m−1` entries, then swap position `m` with a position chosen by the parity of `m` |
| `johnson_trotter` | one **adjacent** transposition (Steinhaus–Johnson–Trotter with directed mobile elements) |

### Set partitions of {1, …, n}: `partitions`

| Generator | Order |
|---|---|
| `restricted_growth` | lexicographic order of restricted growth strings `a₁…aₙ`, with `a₁ = 0` and `aᵢ ≤ 1 + max(a₁…aᵢ₋₁)` |
| `gray_partitions` | each partition differs from the previous one by moving one element to another block or a new block |

The Gray order is built recursively. For each partition of {1,…,n−1}, element `n` sweeps through every block and then a new block of its own. The sweep direction alternates, so consecutive sweeps meet at a shared position of `n`.

Supporting functions: `bell_numbers(n)` (Bell triangle), `stirling2(n, k)`, and `differ_by_one_move(p, q)`.

### Sets: `sets`

`union`, `intersection`, `difference`, an iterative odometer-style `cartesian_product` for any number of sets, and `power_set`. Each returns a list in a fixed order: first-seen order, or the order of the inputs.

## Usage

```bash
python -m discrete_algorithms permutations 3              # Johnson–Trotter by default
python -m discrete_algorithms permutations 4 --method heap
python -m discrete_algorithms partitions 4                # Gray order by default
python -m discrete_algorithms product 1,2 a,b,c
python -m discrete_algorithms union 1,2,3 3,4
```

```
$ python -m discrete_algorithms partitions 3
1 2 3
1 2 | 3
1 | 2 | 3
1 | 2 3
1 3 | 2
```

```python
from discrete_algorithms import partitions, permutations

list(permutations.johnson_trotter(3))
# [(1, 2, 3), (1, 3, 2), (3, 1, 2), (3, 2, 1), (2, 3, 1), (2, 1, 3)]
```

## Tests

```bash
python -m pip install -e ".[test]"
python -m pytest
```

The suite checks:

- every generator produces each object exactly once: `n!` permutations up to n = 7, and Bell-number counts of partitions up to n = 8;
- consecutive outputs differ by the stated minimal change;
- the block-count distribution matches the Stirling numbers;
- the restricted-growth order is lexicographic;
- the set operations match `itertools`.

## Credits

The set of exercises came from [Dan-Krod/discrete_math](https://github.com/Dan-Krod/discrete_math): set union and product, permutations by transpositions, and set partitions. This repository is an independent implementation with its own algorithms, tests and packaging.

## License

MIT. See `LICENSE`.
