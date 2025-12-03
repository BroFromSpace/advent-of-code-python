"""
Day 1: Safe Dial Password Cracker

A circular dial (0-99) starts at position 50. Each instruction rotates it:
  - 'R' = clockwise (increasing)
  - 'L' = counterclockwise (decreasing)

The dial wraps: 99 + 1 = 0, and 0 - 1 = 99

Part 1: Count when the dial lands on 0 after each rotation
Part 2: Count every time the dial passes through 0 (not just final positions)
"""

from pathlib import Path


def part_1() -> int:
    """Count how many times the dial lands on 0 after each rotation."""
    with Path("./input.txt").open() as f:
        instructions = f.readlines()

    dial_position = 50
    zero_landings = 0

    for instruction in instructions:
        turn_direction = 1 if instruction[0] == "R" else -1
        clicks = int(instruction[1:])
        dial_position = (dial_position + turn_direction * clicks) % 100

        if dial_position == 0:
            zero_landings += 1

    return zero_landings


def part_2() -> int:
    """
    Count every time the dial passes through 0 (including while rotating).

    Strategy:
    - Every 100 clicks = 1 full rotation = passes through 0 once
    - Leftover clicks might cross 0 if they wrap around the boundary

    Edge cases for the wrap check:
    1. Rotating right: new_position >= 100 means we crossed 0
       Example: pos 80 + R30 = 110 → crossed through 0 to land at 10

    2. Rotating left: new_position < 1 AND dial_position > 0 means we crossed 0
       Example: pos 20 + L30 = -10 → crossed through 0 to land at 90
       Why check dial_position > 0? If we're already at 0, rotating left goes
       straight to 99, 98, etc. without crossing 0 again.
    """
    with Path("./input.txt").open() as f:
        instructions = f.readlines()

    dial_position = 50
    zero_crossings = 0

    for instruction in instructions:
        turn_direction = 1 if instruction[0] == "R" else -1
        clicks = int(instruction[1:])

        zero_crossings += clicks // 100
        partial_clicks = clicks % 100

        if partial_clicks > 0:
            new_position = dial_position + turn_direction * partial_clicks

            if (turn_direction > 0 and new_position >= 100) or (
                turn_direction < 0 and new_position < 1 and dial_position > 0
            ):
                zero_crossings += 1

            dial_position = new_position % 100

    return zero_crossings
