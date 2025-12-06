"""
Day 6: Trash Compactor - Cephalopod Math Homework

While trapped in a garbage smasher, help a young cephalopod with her math homework.
The worksheet has problems arranged in columns, but cephalopods read them differently!

Part 1: Read worksheet normally (vertical columns, left-to-right)
Part 2: Read in cephalopod style (each column is a number read top-to-bottom, right-to-left)

Key insight: Part 2 requires transposing the grid to convert vertical digit columns
into horizontal numbers, then parsing problems in reverse order.
"""

import operator
import re
from functools import reduce
from itertools import zip_longest
from pathlib import Path

FILE_DIR = Path(__file__).parent


def part_1() -> int:
    """
    Solve the math worksheet reading normally (vertical problems, left-to-right).

    Each column contains one problem: numbers stacked vertically with the operator at bottom.
    Problems are separated by blank columns.
    """
    with (FILE_DIR / "input.txt").open() as f:
        lines = f.read().splitlines()

    worksheet_grid = [[int(num) for num in re.findall(r"\d+", line)] for line in lines[:-1]]
    operators = re.findall(r"[\*\+]", lines[-1])

    result = 0
    for problem_idx, operation in enumerate(operators):
        problem_numbers = [row[problem_idx] for row in worksheet_grid]

        if operation == "+":
            result += sum(problem_numbers)
        else:
            result += reduce(operator.mul, problem_numbers, 1)

    return result


def part_2() -> int:
    """
    Solve using cephalopod math rules (each column is a digit, read top-to-bottom).

    In cephalopod math, each column represents ONE digit of a multi-digit number,
    with the most significant digit at the top. Problems are still separated by
    blank columns, and we read right-to-left.
    """
    with (FILE_DIR / "input.txt").open() as f:
        lines = f.read().splitlines()

    vertical_digit_columns = ["".join(chars) for chars in zip_longest(*lines[:-1], fillvalue=" ")]

    problems = []
    current_problem_numbers = []
    current_operator = None

    for digit_column, operator_char in zip(vertical_digit_columns, lines[-1], strict=True):
        vertical_digits = digit_column.strip()

        if not vertical_digits:
            problems.append((current_problem_numbers, current_operator))
            current_problem_numbers = []
        else:
            number = int(vertical_digits)
            current_problem_numbers.append(number)

            if operator_char != " ":
                current_operator = operator_char

    problems.append((current_problem_numbers, current_operator))

    result = 0
    for problem_numbers, operation in problems:
        if operation == "+":
            result += sum(problem_numbers)
        else:
            result += reduce(operator.mul, problem_numbers, 1)

    return result


if __name__ == "__main__":
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")
