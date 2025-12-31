"""Data loader module for reading transactional datasets.

Supports two CSV formats:
1. Item list format: Each row contains comma-separated item names
2. Binary matrix format: Header row with item names, subsequent rows with 0/1 values
"""

from typing import List, Optional


def load_transactions(
    filepath: str,
    limit: Optional[int] = None,
    header: Optional[bool] = None
) -> List[frozenset]:
    """Load transactions from a CSV file.

    Automatically detects the file format unless header is specified:
    - Item list format: comma/semicolon separated item names per row
    - Binary matrix format: header with item names, rows with 0/1 values

    Args:
        filepath: Path to the CSV file.
        limit: Maximum number of transactions to load. Defaults to None.
        header: If True, first row is treated as header (for item list
            format, skip it; for binary format, use it as item names).
            If False, no header row. If None (default), auto-detect.

    Returns:
        List of frozensets, where each frozenset represents a transaction.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()

    # Detect delimiter (semicolon or comma)
    delimiter = ';' if ';' in first_line else ','

    # Detect format by checking if first data line contains binary values
    is_binary_format = _detect_binary_format(filepath, delimiter)

    if is_binary_format:
        return _load_binary_matrix(filepath, delimiter, limit)
    else:
        return _load_item_list(filepath, delimiter, limit, header)


def _detect_binary_format(filepath: str, delimiter: str) -> bool:
    """Detect if the file uses binary matrix format.

    Args:
        filepath: Path to the CSV file.
        delimiter: The delimiter used in the file.

    Returns:
        True if binary matrix format, False if item list format.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        # Skip header
        f.readline()
        # Read second line
        second_line = f.readline().strip()

        if not second_line:
            return False

        values = [v.strip() for v in second_line.split(delimiter)]
        # Check if all values are 0 or 1
        return all(v in ('0', '1') for v in values if v)


def _load_binary_matrix(
    filepath: str, delimiter: str, limit: Optional[int] = None
) -> List[frozenset]:
    """Load transactions from a binary matrix format CSV.

    Args:
        filepath: Path to the CSV file.
        delimiter: The delimiter used in the file.
        limit: Maximum number of transactions to load.

    Returns:
        List of frozensets representing transactions.
    """
    transactions = []

    with open(filepath, 'r', encoding='utf-8') as f:
        # First line is the header with item names
        header_line = f.readline().strip()
        # Handle potential Windows line endings
        header_line = header_line.replace('\r', '')
        item_names = [item.strip() for item in header_line.split(delimiter)]

        for i, line in enumerate(f):
            if limit is not None and i >= limit:
                break

            line = line.strip().replace('\r', '')
            if not line:
                continue

            values = [v.strip() for v in line.split(delimiter)]

            # Build transaction from items where value is '1'
            items = []
            for idx, value in enumerate(values):
                if value == '1' and idx < len(item_names):
                    items.append(item_names[idx])

            if items:
                transactions.append(frozenset(items))

    return transactions


def _load_item_list(
    filepath: str,
    delimiter: str,
    limit: Optional[int] = None,
    header: Optional[bool] = None
) -> List[frozenset]:
    """Load transactions from an item list format CSV.

    Args:
        filepath: Path to the CSV file.
        delimiter: The delimiter used in the file.
        limit: Maximum number of transactions to load.
        header: If True, skip first row. If False or None, include all rows.

    Returns:
        List of frozensets representing transactions.
    """
    transactions = []

    with open(filepath, 'r', encoding='utf-8') as f:
        # Skip header if specified
        if header:
            f.readline()

        for i, line in enumerate(f):
            if limit is not None and i >= limit:
                break

            items = [item.strip() for item in line.strip().split(delimiter)]
            items = [item for item in items if item]

            if items:
                transactions.append(frozenset(items))

    return transactions


def get_unique_items(transactions: List[frozenset]) -> set:
    """Extract all unique items from a list of transactions.

    Args:
        transactions: List of transaction frozensets.

    Returns:
        Set of all unique items.
    """
    unique_items = set()
    for transaction in transactions:
        unique_items.update(transaction)
    return unique_items
