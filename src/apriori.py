"""Apriori algorithm implementation for finding frequent itemsets.

This is a pure Python implementation without external libraries.
"""

from itertools import combinations
from typing import Dict, List, Set


def count_support(
    transactions: List[frozenset], itemsets: Set[frozenset]
) -> Dict[frozenset, int]:
    """Count the support (occurrence count) for each itemset in the transactions.

    Args:
        transactions (List[frozenset]): List of transaction frozensets.
        itemsets (Set[frozenset]): Set of itemsets to count support for.

    Returns:
        Dict[frozenset, int]: Dictionary mapping each itemset to its support count.
    """
    support_counts = {itemset: 0 for itemset in itemsets}

    for transaction in transactions:
        for itemset in itemsets:
            if itemset.issubset(transaction):
                support_counts[itemset] += 1

    return support_counts


def generate_candidates(frequent_itemsets: Set[frozenset], k: int) -> Set[frozenset]:
    """Generate candidate itemsets of size k from frequent itemsets of size k-1.

    Uses the Apriori principle: candidates are formed by joining itemsets
    that share k-2 items. Only generates candidates whose k-1 subsets are
    all frequent (downward closure property).

    Args:
        frequent_itemsets (Set[frozenset]): Set of frequent itemsets of size k-1.
        k (int): Size of candidates to generate.

    Returns:
        Set[frozenset]: Set of candidate itemsets of size k.
    """
    candidates = set()
    itemsets_list = list(frequent_itemsets)

    for i in range(len(itemsets_list)):
        for j in range(i + 1, len(itemsets_list)):
            union = itemsets_list[i] | itemsets_list[j]
            if len(union) == k:
                all_subsets_frequent = True
                for subset in combinations(union, k - 1):
                    if frozenset(subset) not in frequent_itemsets:
                        all_subsets_frequent = False
                        break

                if all_subsets_frequent:
                    candidates.add(union)

    return candidates


def get_frequent_itemsets(
    transactions: List[frozenset], min_support: float
) -> Dict[frozenset, int]:
    """Find all frequent itemsets using the Apriori algorithm.

    Args:
        transactions (List[frozenset]): List of transaction frozensets.
        min_support (float): Minimum support threshold (0.0 to 1.0).

    Returns:
        Dict[frozenset, int]: Dictionary mapping each frequent itemset to its
            support count.
    """
    n_transactions = len(transactions)
    min_support_count = int(min_support * n_transactions)

    frequent_itemsets: Dict[frozenset, int] = {}

    all_items = set()
    for transaction in transactions:
        all_items.update(transaction)

    single_itemsets = {frozenset([item]) for item in all_items}
    support_counts = count_support(transactions, single_itemsets)

    current_frequent = {
        itemset
        for itemset, count in support_counts.items()
        if count >= min_support_count
    }

    for itemset in current_frequent:
        frequent_itemsets[itemset] = support_counts[itemset]

    k = 2
    while current_frequent:
        candidates = generate_candidates(current_frequent, k)

        if not candidates:
            break

        support_counts = count_support(transactions, candidates)

        current_frequent = {
            itemset
            for itemset, count in support_counts.items()
            if count >= min_support_count
        }

        for itemset in current_frequent:
            frequent_itemsets[itemset] = support_counts[itemset]

        k += 1

    return frequent_itemsets

