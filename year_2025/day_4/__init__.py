"""
Day 4: Printing Department

Part 1: Count accessible paper rolls (< 4 adjacent rolls).
Part 2: Remove accessible rolls iteratively until none remain.
"""

from collections import deque
from collections.abc import Iterator
from pathlib import Path

FILE_DIR = Path(__file__).parent


def get_adjacent_positions(x: int, y: int, width: int, height: int) -> Iterator[tuple[int, int]]:
    """Return all 8 adjacent positions within grid bounds."""
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            neighbor_x, neighbor_y = x + dx, y + dy
            if 0 <= neighbor_x < width and 0 <= neighbor_y < height:
                yield (neighbor_x, neighbor_y)


def part_1() -> int:
    """Count accessible paper rolls in warehouse."""
    with (FILE_DIR / "input.txt").open() as f:
        warehouse = f.read().splitlines()

    warehouse_width = len(warehouse[0])
    warehouse_height = len(warehouse)
    accessible_rolls = 0

    for row_idx, row in enumerate(warehouse):
        for col_idx, cell in enumerate(row):
            if cell != "@":
                continue

            adjacent_rolls = sum(
                1
                for neighbor_x, neighbor_y in get_adjacent_positions(
                    col_idx, row_idx, warehouse_width, warehouse_height
                )
                if warehouse[neighbor_y][neighbor_x] == "@"
            )

            if adjacent_rolls < 4:
                accessible_rolls += 1

    return accessible_rolls


def part_2() -> int:
    """
    Remove accessible rolls iteratively using queue-based adjacency tracking.

    Maintains neighbor counts to avoid rescanning the entire grid after each removal.
    """
    with (FILE_DIR / "input.txt").open() as f:
        lines = f.read().splitlines()

    warehouse = [list(row) for row in lines]
    warehouse_width = len(warehouse[0])
    warehouse_height = len(warehouse)

    neighbor_counts = {}
    forklift_queue = deque()

    for row_idx in range(warehouse_height):
        for col_idx in range(warehouse_width):
            if warehouse[row_idx][col_idx] != "@":
                continue

            adjacent_rolls = sum(
                1
                for neighbor_x, neighbor_y in get_adjacent_positions(
                    col_idx, row_idx, warehouse_width, warehouse_height
                )
                if warehouse[neighbor_y][neighbor_x] == "@"
            )
            neighbor_counts[(col_idx, row_idx)] = adjacent_rolls

            if adjacent_rolls < 4:
                forklift_queue.append((col_idx, row_idx))

    total_removed = 0

    while forklift_queue:
        col_idx, row_idx = forklift_queue.popleft()

        if warehouse[row_idx][col_idx] != "@":
            continue

        warehouse[row_idx][col_idx] = "."
        total_removed += 1

        for neighbor_x, neighbor_y in get_adjacent_positions(
            col_idx, row_idx, warehouse_width, warehouse_height
        ):
            if warehouse[neighbor_y][neighbor_x] != "@":
                continue

            neighbor_counts[(neighbor_x, neighbor_y)] -= 1

            if neighbor_counts[(neighbor_x, neighbor_y)] == 3:
                forklift_queue.append((neighbor_x, neighbor_y))

    return total_removed


if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")
