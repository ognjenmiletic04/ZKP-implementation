"""
Sudoku Zero-Kknowledge Proof demo - struktura projekta
------------------------------------------------------

1) models.py
   - osnovni modeli podataka
   - Sudoku tabla
   - Challenge
   - OpenedCell
   - pomocne funkcije za kopiranje i kvarenje table

2) zkp.py
   - kriptografski deo demonstracije
   - SHA-256 commitment
   - Prover
   - Verifier

3) main.py
   - pokretanje programa
   - unos rezima i broja rundi
   - ispis rezultata po rundama

"""

from __future__ import annotations

from models import VALID_SUDOKU, tamper_grid
from zkp import Prover, Verifier


def print_commitment_preview(commitments: list[list[str]]) -> None:
    """Prikazuje skracene hash vrednosti, da se vidi da verifikator ne vidi resenje."""
    print("Commitment matrica koju vidi verifikator, skraceno na prvih 8 karaktera:")
    for row in commitments:
        print(" ".join(commitment[:8] for commitment in row))
    print()


def run_protocol(rounds: int = 10, use_invalid_solution: bool = False) -> None:
    print("=== Sudoku Zero-Knowledge Proof demo ===")
    print("Edukativna simulacija: SHA-256 commitment + salt + interaktivne runde")
    print()

    solution = tamper_grid(VALID_SUDOKU) if use_invalid_solution else VALID_SUDOKU

    prover = Prover(solution)
    verifier = Verifier(prover.get_commitments())

    print("Dokazivac zna Sudoku resenje.")
    print("Verifikator na pocetku dobija samo hash commitment-e, ne i vrednosti celija.")
    print_commitment_preview(verifier.commitments)

    accepted_rounds = 0

    for round_number in range(1, rounds + 1):
        challenge = verifier.choose_challenge()
        opened_cells = prover.open_challenge(challenge)
        is_valid, message = verifier.verify_opened_cells(challenge, opened_cells)
        values = [cell.value for cell in opened_cells]

        print(f"Runda {round_number}:")
        print(f"  Verifikator bira: {challenge.display_name()}")
        print(f"  Dokazivac otvara samo taj deo: {values}")
        print(f"  Provera: {message}")
        print(f"  Rezultat: {'PRIHVACENO' if is_valid else 'ODBIJENO'}")
        print()

        if is_valid:
            accepted_rounds += 1
        else:
            print("Zakljucak: protokol se zaustavlja jer je verifikator otkrio nevalidan dokaz.")
            return

    print("=== Zakljucak ===")
    print(f"Proslo je {accepted_rounds}/{rounds} rundi.")
    print("Verifikator je stekao poverenje da dokazivac poseduje validno resenje,")
    print("ali nije video celu Sudoku tablu, vec samo nasumicno trazene redove/kolone.")


def ask_int(prompt: str, default: int) -> int:
    raw = input(prompt).strip()

    if raw == "":
        return default

    try:
        value = int(raw)
        if value <= 0:
            raise ValueError
        return value
    except ValueError:
        print(f"Neispravan unos. Koristim podrazumevanu vrednost: {default}")
        return default


def main() -> None:
    print("Izaberi rezim:")
    print("1 - Validno Sudoku resenje")
    print("2 - Namerno pokvareno Sudoku resenje")

    mode = input("Unos [1/2]: ").strip()
    use_invalid_solution = mode == "2"

    rounds = ask_int("Broj rundi [podrazumevano 10]: ", default=10)
    print()

    run_protocol(rounds=rounds, use_invalid_solution=use_invalid_solution)


if __name__ == "__main__":
    main()
