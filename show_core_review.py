import csv

FILE = "dictionary_core_v1_review.csv"

with open(FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

print("=" * 80)
print("CORE DICTIONARY V1 — REVIEW FLAGS")
print("=" * 80)
print(f"REVIEW FLAGS: {len(rows):,}")
print()

for i, r in enumerate(rows, 1):
    print(
        f"{i:03} | "
        f"{r.get('word','')} | "
        f"{r.get('word_with_airab_or_variant','')} | "
        f"{r.get('definition','')} | "
        f"{r.get('review_reason','')}"
    )

print()
print("=" * 80)
