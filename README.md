# ZKP-implementation

Edukativna implementacija interaktivnog dokaza nultog znanja (Zero-Knowledge Proof) za proveru validnosti Sudoku resenja bez otkrivanja kompletnog resenja.

## Opis projekta

Cilj projekta je demonstracija osnovnih principa dokaza nultog znanja kroz pojednostavljeni Sudoku primer.

Dokazivac (Prover) poseduje validno Sudoku resenje i zeli da dokaze verifikatoru (Verifier) da je resenje ispravno, ali bez prikazivanja cele Sudoku table.

Implementacija koristi:

- SHA-256 hash funkciju
- salt vrednosti
- commitment mehanizam
- interaktivne runde izmedju dokazivaca i verifikatora

Projekat predstavlja edukativnu simulaciju ZKP principa i nije pun industrijski kriptografski ZKP sistem.

---

# Struktura projekta

```text
ZKP-implementation/
│
├── models.py
├── zkp.py
├── main.py
└── README.md