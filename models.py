from __future__ import annotations

from dataclasses import dataclass
from typing import List, Literal


Grid = List[List[int]]
ChallengeType = Literal["row", "column"]

EXPECTED_SET = set(range(1, 10))


VALID_SUDOKU: Grid = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]


@dataclass
class OpenedCell:
    row: int
    column: int
    value: int
    salt: str


@dataclass
class Challenge:
    challenge_type: ChallengeType
    index: int  # vrednost od 0 do 8

    def display_name(self) -> str:
        label = "red" if self.challenge_type == "row" else "kolona"
        return f"{label} {self.index + 1}"


def copy_grid(grid: Grid) -> Grid:
    return [row[:] for row in grid]


def tamper_grid(grid: Grid) -> Grid:
    """
    Namerno kvari Sudoku resenje.
    Menjamo prvi red tako da ima duplikat, pa red vise nije validan.
    """
    broken = copy_grid(grid)
    broken[0][1] = broken[0][0]
    return broken
