"""Closed itemsets detection module.

A frequent itemset X is CLOSED if there is no superset Y ⊃ X
with the same support as X.
"""

from collections import defaultdict
from typing import Dict, List


def find_closed_itemsets(
    frequent_itemsets: Dict[frozenset, int]
) -> Dict[frozenset, int]:
    """Find all closed itemsets from the frequent itemsets.

    An itemset is closed if no proper superset has the same support.

    Args:
        frequent_itemsets (Dict[frozenset, int]): Dictionary mapping frequent
            itemsets to their support counts.

    Returns:
        Dict[frozenset, int]: Dictionary mapping closed itemsets to their
            support counts.
    """
    if not frequent_itemsets:
        return {}

    itemsets_by_size: Dict[int, List[frozenset]] = defaultdict(list)
    for itemset in frequent_itemsets:
        itemsets_by_size[len(itemset)].append(itemset)

    sizes = sorted(itemsets_by_size.keys(), reverse=True)

    closed_itemsets = {}

    for size in sizes:
        for itemset in itemsets_by_size[size]:
            support = frequent_itemsets[itemset]
            is_closed = True

            for larger_size in sizes:
                if larger_size <= size:
                    break  # sizes are sorted descending, no more larger sizes

                for other_itemset in itemsets_by_size[larger_size]:
                    if itemset < other_itemset:
                        if frequent_itemsets[other_itemset] == support:
                            is_closed = False
                            break

                if not is_closed:
                    break

            if is_closed:
                closed_itemsets[itemset] = support

    return closed_itemsets


