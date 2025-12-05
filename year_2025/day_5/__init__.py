"""
Day 5: Cafeteria

Part 1: Count how many available ingredients are fresh.
Part 2: Count total unique fresh ingredient IDs across all ranges.
"""

import bisect
from pathlib import Path

FILE_DIR = Path(__file__).parent


def merge_freshness_ranges(freshness_ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Merge overlapping or adjacent freshness ranges into non-overlapping ranges.

    Examples:
        >>> merge_freshness_ranges([(3, 5), (10, 14), (12, 18)])
        [(3, 5), (10, 18)]  # (10, 14) and (12, 18) overlap, merged into (10, 18)

        >>> merge_freshness_ranges([(1, 5), (6, 10)])
        [(1, 10)]  # Adjacent ranges (5 and 6) are merged

        >>> merge_freshness_ranges([(1, 10), (3, 5)])
        [(1, 10)]  # (3, 5) is fully contained in (1, 10)

    """
    if not freshness_ranges:
        return []

    freshness_ranges.sort()
    merged = []

    for range_start, range_end in freshness_ranges:
        if merged and range_start <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], range_end))
        else:
            merged.append((range_start, range_end))

    return merged


def part_1() -> int:
    """
    Count available ingredient IDs that are fresh using binary search on merged ranges.

    Binary search approach:
        Given merged ranges [(3, 5), (10, 18)] and ingredient_id=12:
        1. Extract range starts: [3, 10]
        2. bisect_right([3, 10], 12) = 2, so idx = 2 - 1 = 1
        3. Check if 12 is in merged_ranges[1] = (10, 18): 10 <= 12 <= 18 ✓ Fresh!

        For ingredient_id=8:
        1. bisect_right([3, 10], 8) = 1, so idx = 1 - 1 = 0
        2. Check if 8 is in merged_ranges[0] = (3, 5): 3 <= 8 <= 5 ✗ Spoiled!
    """
    with (FILE_DIR / "input.txt").open() as f:
        database = f.read().split("\n\n")

    fresh_ranges = []
    for line in database[0].strip().split("\n"):
        range_start, range_end = line.split("-")
        fresh_ranges.append((int(range_start), int(range_end)))

    merged_fresh_ranges = merge_freshness_ranges(fresh_ranges)
    range_starts = [r[0] for r in merged_fresh_ranges]

    fresh_count = 0
    for id_str in database[1].strip().split("\n"):
        ingredient_id = int(id_str)
        idx = bisect.bisect_right(range_starts, ingredient_id) - 1
        if (
            idx >= 0
            and merged_fresh_ranges[idx][0] <= ingredient_id <= merged_fresh_ranges[idx][1]
        ):
            fresh_count += 1

    return fresh_count


def part_2() -> int:
    """Count total unique fresh ingredient IDs by merging overlapping ranges."""
    with (FILE_DIR / "input.txt").open() as f:
        database = f.read().split("\n\n")

    fresh_ranges = []
    for line in database[0].strip().split("\n"):
        range_start, range_end = line.split("-")
        fresh_ranges.append((int(range_start), int(range_end)))

    merged_fresh_ranges = merge_freshness_ranges(fresh_ranges)
    return sum(range_end - range_start + 1 for range_start, range_end in merged_fresh_ranges)


if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")
