import csv

INPUT_FILE = "dictionary_stage8_semantic_review.csv"

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

start = 100
end = 112

print("=" * 75)
print("STAGE 8B — SEMANTIC REVIEW BATCH 5 — FINAL")
print("=" * 75)
print(f"TOTAL REVIEW ENTRIES: {len(rows):,}")
print(f"Showing entries {start+1}–{min(end, len(rows))}")
print()

for i, r in enumerate(rows[start:end], start + 1):
    print(
        f"{i:03} | "
        f'{r.get("english","")} | '
        f'{r.get("sindhi","")} | '
        f'{r.get("english_definition","")}'
    )

print()
print("=" * 75)
