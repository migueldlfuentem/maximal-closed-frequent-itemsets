"""
Main entry point for Maximal/Closed Frequent Itemsets Mining.

Usage:
    python main.py --data data/groceries.csv --min-support 0.05 --limit 200
"""
import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data_loader import load_transactions, get_unique_items
from src.apriori import get_frequent_itemsets
from src.closed_itemsets import find_closed_itemsets
from src.maximal_itemsets import find_maximal_itemsets


def format_itemset(itemset: frozenset) -> str:
    """Format an itemset for display."""
    return "{" + ", ".join(sorted(itemset)) + "}"


def main():
    parser = argparse.ArgumentParser(
        description="Find maximal and closed frequent itemsets in transactional data."
    )
    parser.add_argument(
        "--data", "-d",
        type=str,
        default="data/groceries.csv",
        help="Path to the CSV dataset (default: data/groceries.csv)"
    )
    parser.add_argument(
        "--min-support", "-s",
        type=float,
        default=0.05,
        help="Minimum support threshold (0.0 to 1.0, default: 0.05)"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=None,
        help="Maximum number of transactions to load (default: all)"
    )
    parser.add_argument(
        "--top", "-t",
        type=int,
        default=20,
        help="Number of top itemsets to display (default: 20)"
    )
    parser.add_argument(
        "--header",
        type=str,
        choices=["true", "false", "auto"],
        default="auto",
        help="Whether CSV has header row: 'true', 'false', or 'auto' (default: auto)"
    )
    
    args = parser.parse_args()
    
    if not 0 < args.min_support <= 1:
        print("Error: min-support must be between 0 and 1")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print("MAXIMAL AND CLOSED FREQUENT ITEMSETS MINING")
    print(f"{'='*60}\n")
    
    print(f"Loading transactions from: {args.data}")
    
    header = None
    if args.header == "true":
        header = True
    elif args.header == "false":
        header = False
    
    transactions = load_transactions(args.data, limit=args.limit, header=header)
    unique_items = get_unique_items(transactions)
    
    print(f"  - Transactions loaded: {len(transactions)}")
    print(f"  - Unique items: {len(unique_items)}")
    print(f"  - Min support: {args.min_support} ({int(args.min_support * len(transactions))} transactions)")
    
    print(f"\n{'-'*60}")
    print("Finding frequent itemsets (Apriori algorithm)...")
    frequent_itemsets = get_frequent_itemsets(transactions, args.min_support)
    print(f"  - Frequent itemsets found: {len(frequent_itemsets)}")
    
    print(f"\n{'-'*60}")
    print("Finding closed itemsets...")
    closed_itemsets = find_closed_itemsets(frequent_itemsets)
    print(f"  - Closed itemsets found: {len(closed_itemsets)}")
    
    print(f"\n{'-'*60}")
    print("Finding maximal itemsets...")
    maximal_itemsets = find_maximal_itemsets(frequent_itemsets)
    print(f"  - Maximal itemsets found: {len(maximal_itemsets)}")
    
    print(f"\n{'='*60}")
    print(f"TOP {args.top} FREQUENT ITEMSETS (by support)")
    print(f"{'='*60}")
    
    sorted_frequent = sorted(
        frequent_itemsets.items(), 
        key=lambda x: (-x[1], -len(x[0]))
    )[:args.top]
    
    for i, (itemset, count) in enumerate(sorted_frequent, 1):
        support_pct = count / len(transactions) * 100
        print(f"  {i:2}. {format_itemset(itemset)}")
        print(f"      Support: {count} ({support_pct:.1f}%)")
    
    print(f"\n{'='*60}")
    print(f"TOP {args.top} CLOSED ITEMSETS (by support)")
    print(f"{'='*60}")
    
    sorted_closed = sorted(
        closed_itemsets.items(), 
        key=lambda x: (-x[1], -len(x[0]))
    )[:args.top]
    
    for i, (itemset, count) in enumerate(sorted_closed, 1):
        support_pct = count / len(transactions) * 100
        print(f"  {i:2}. {format_itemset(itemset)}")
        print(f"      Support: {count} ({support_pct:.1f}%)")
    
    print(f"\n{'='*60}")
    print(f"TOP {args.top} MAXIMAL ITEMSETS (by size, then support)")
    print(f"{'='*60}")
    
    sorted_maximal = sorted(
        maximal_itemsets, 
        key=lambda x: (-len(x), -frequent_itemsets[x])
    )[:args.top]
    
    for i, itemset in enumerate(sorted_maximal, 1):
        count = frequent_itemsets[itemset]
        support_pct = count / len(transactions) * 100
        print(f"  {i:2}. {format_itemset(itemset)}")
        print(f"      Size: {len(itemset)}, Support: {count} ({support_pct:.1f}%)")
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"  - Frequent itemsets: {len(frequent_itemsets)}")
    
    if len(frequent_itemsets) > 0:
        print(f"  - Closed itemsets:   {len(closed_itemsets)} ({len(closed_itemsets)/len(frequent_itemsets)*100:.1f}% of frequent)")
        print(f"  - Maximal itemsets:  {len(maximal_itemsets)} ({len(maximal_itemsets)/len(frequent_itemsets)*100:.1f}% of frequent)")
        print(f"\n  Property verification: |maximal| ≤ |closed| ≤ |frequent|")
        print(f"  {len(maximal_itemsets)} ≤ {len(closed_itemsets)} ≤ {len(frequent_itemsets)}: {'✓' if len(maximal_itemsets) <= len(closed_itemsets) <= len(frequent_itemsets) else '✗'}")
    else:
        print(f"  - Closed itemsets:   {len(closed_itemsets)}")
        print(f"  - Maximal itemsets:  {len(maximal_itemsets)}")
        print(f"\n  No frequent itemsets found. Try lowering min-support threshold.")
    print()


if __name__ == "__main__":
    main()
