from __future__ import annotations

import hashlib
import random
import secrets
from typing import List, Tuple

from models import Challenge, ChallengeType, EXPECTED_SET, Grid, OpenedCell, copy_grid


def make_commitment(value: int, salt: str) -> str:
    """
    Pravi SHA-256 commitment za jednu Sudoku celiju.

    Commitment je kao zakljucana kutija:
    - sakriva vrednost celije;
    - ali kasnije omogucava proveru da vrednost nije promenjena.
    """
    payload = f"{value}:{salt}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


class Prover:
    """Dokazivac: zna tajno Sudoku resenje i otvara samo trazeni deo."""

    def __init__(self, solution: Grid):
        self.solution = copy_grid(solution)
        self.salts = self._generate_salts()
        self.commitments = self._generate_commitments()

    def _generate_salts(self) -> List[List[str]]:
        return [[secrets.token_hex(16) for _ in range(9)] for _ in range(9)]

    def _generate_commitments(self) -> List[List[str]]:
        return [
            [make_commitment(self.solution[r][c], self.salts[r][c]) for c in range(9)]
            for r in range(9)
        ]

    def get_commitments(self) -> List[List[str]]:
        """Verifikator dobija samo commitment matricu, ne i Sudoku vrednosti."""
        return [row[:] for row in self.commitments]

    def open_challenge(self, challenge: Challenge) -> List[OpenedCell]:
        """Otvara samo izabrani red ili kolonu."""
        opened: List[OpenedCell] = []

        if challenge.challenge_type == "row":
            r = challenge.index
            for c in range(9):
                opened.append(
                    OpenedCell(
                        row=r,
                        column=c,
                        value=self.solution[r][c],
                        salt=self.salts[r][c],
                    )
                )
        else:
            c = challenge.index
            for r in range(9):
                opened.append(
                    OpenedCell(
                        row=r,
                        column=c,
                        value=self.solution[r][c],
                        salt=self.salts[r][c],
                    )
                )

        return opened


class Verifier:
    """Verifikator: bira izazove i proverava otvoreni dokaz."""

    def __init__(self, commitments: List[List[str]]):
        self.commitments = commitments

    def choose_challenge(self) -> Challenge:
        challenge_type: ChallengeType = random.choice(["row", "column"])
        index = random.randint(0, 8)
        return Challenge(challenge_type=challenge_type, index=index)

    def verify_opened_cells(
        self,
        challenge: Challenge,
        opened_cells: List[OpenedCell],
    ) -> Tuple[bool, str]:
        if len(opened_cells) != 9:
            return False, "Dokaz ne sadrzi tacno 9 celija."

        if not self._cells_match_challenge(challenge, opened_cells):
            return False, "Otvorene celije ne pripadaju trazenom redu/koloni."

        if not self._commitments_are_valid(opened_cells):
            return False, "Commitment provera nije uspesna. Vrednost ili salt su promenjeni."

        values = [cell.value for cell in opened_cells]
        if set(values) != EXPECTED_SET:
            return False, f"Sudoku pravilo nije ispostovano. Dobijene vrednosti: {values}"

        return True, "Commitment-i su validni i vrednosti su brojevi 1-9 bez ponavljanja."

    def _cells_match_challenge(self, challenge: Challenge, opened_cells: List[OpenedCell]) -> bool:
        if challenge.challenge_type == "row":
            return all(cell.row == challenge.index for cell in opened_cells)
        return all(cell.column == challenge.index for cell in opened_cells)

    def _commitments_are_valid(self, opened_cells: List[OpenedCell]) -> bool:
        for cell in opened_cells:
            expected_commitment = self.commitments[cell.row][cell.column]
            actual_commitment = make_commitment(cell.value, cell.salt)

            if actual_commitment != expected_commitment:
                return False

        return True
