"""
Advent of Code 2025 - Day 7: Laboratories

Tachyon beam splitting through manifolds with splitters.

Part 1: Count how many times beams hit splitters.
Part 2: Count how many distinct timelines result from quantum splitting.
"""

from pathlib import Path

FILE_DIR = Path(__file__).parent


def part_1() -> int:
    """
    Count how many splitters get hit by tachyon beams.

    Beams travel downward from S. When a beam hits a splitter (^), it stops and
    creates two new beams - one going left and one going right from that splitter.
    We track each unique splitter position that gets hit at least once.
    """
    with (FILE_DIR / "input.txt").open() as f:
        lines = f.read().splitlines()

    manifold_width = len(lines[0])
    manifold_height = len(lines)
    beam_queue = set()

    for i, symbol in enumerate(lines[0]):
        if symbol == "S":
            beam_queue.add((i, 0))
            break

    splitter_hits = set()
    while beam_queue:
        beam_x, beam_y = beam_queue.pop()
        next_y = beam_y + 1

        if lines[next_y][beam_x] == "^":
            if (beam_x, next_y) not in splitter_hits:
                splitter_hits.add((beam_x, next_y))

            if next_y < manifold_height - 1:
                if beam_x - 1 >= 0:
                    beam_queue.add((beam_x - 1, next_y))
                if beam_x + 1 < manifold_width:
                    beam_queue.add((beam_x + 1, next_y))
        elif next_y < manifold_height - 1:
            beam_queue.add((beam_x, next_y))

    return len(splitter_hits)


def part_2() -> int:
    """
    Count how many different timelines exist after quantum splitting.

    In quantum mode, each splitter creates a timeline fork: one timeline where
    the particle went left, another where it went right. Each unique path from
    start to exit represents one timeline.

    Uses memoization to cache results: "from position (x,y), how many different
    paths reach an exit?" This prevents recalculating the same subtrees when
    multiple paths converge at the same position.

    Example: If position (5,8) can reach 7 different exits, that value gets cached.
    Any future path that reaches (5,8) instantly returns 7 instead of exploring
    all 7 paths again.
    """
    with (FILE_DIR / "input.txt").open() as f:
        lines = f.read().splitlines()

    manifold_width = len(lines[0])
    manifold_height = len(lines)
    start_position = (0, 0)

    for i, symbol in enumerate(lines[0]):
        if symbol == "S":
            start_position = (i, 0)
            break

    timeline_cache = {}

    def count_timelines(beam_x: int, beam_y: int) -> int:
        """Return how many distinct timeline paths exist from this position to any exit."""
        if (beam_x, beam_y) in timeline_cache:
            return timeline_cache[(beam_x, beam_y)]

        if beam_y >= manifold_height - 1:
            return 1

        next_y = beam_y + 1

        if lines[next_y][beam_x] == "^":
            timeline_count = 0
            if beam_x - 1 >= 0:
                timeline_count += count_timelines(beam_x - 1, next_y)
            else:
                timeline_count += 1

            if beam_x + 1 < manifold_width:
                timeline_count += count_timelines(beam_x + 1, next_y)
            else:
                timeline_count += 1
        else:
            timeline_count = count_timelines(beam_x, next_y)

        timeline_cache[(beam_x, beam_y)] = timeline_count
        return timeline_count

    return count_timelines(start_position[0], start_position[1])


if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")
