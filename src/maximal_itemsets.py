"""Maximal itemsets detection module.

A frequent itemset X is MAXIMAL if there is no superset Y ⊃ X
that is also frequent.
"""

from collections import defaultdict
from typing import Dict, List


def find_maximal_itemsets(
    frequent_itemsets: Dict[frozenset, int]
) -> List[frozenset]:
    """Find all maximal itemsets from the frequent itemsets.

    An itemset is maximal if no proper superset is frequent.

    Args:
        frequent_itemsets (Dict[frozenset, int]): Dictionary mapping frequent
            itemsets to their support counts.

    Returns:
        List[frozenset]: List of maximal itemsets.
    """
    if not frequent_itemsets:
        return []

    # Group itemsets by size for efficient superset search
    itemsets_by_size: Dict[int, List[frozenset]] = defaultdict(list)
    for itemset in frequent_itemsets:
        itemsets_by_size[len(itemset)].append(itemset)

    sizes = sorted(itemsets_by_size.keys(), reverse=True)
    max_size = sizes[0]

    maximal_itemsets = []

    for size in sizes:
        for itemset in itemsets_by_size[size]:
            is_maximal = True

            # Only check itemsets of larger size (potential supersets)
            for larger_size in sizes:
                if larger_size <= size:
                    break  # sizes are sorted descending, no more larger sizes

                for other_itemset in itemsets_by_size[larger_size]:
                    if itemset < other_itemset:  # is proper subset
                        is_maximal = False
                        break

                if not is_maximal:
                    break

            if is_maximal:
                maximal_itemsets.append(itemset)

    return maximal_itemsets

