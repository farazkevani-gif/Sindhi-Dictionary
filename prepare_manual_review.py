import csv

INPUT_FILE = "scored_reverse_candidates.csv"
OUTPUT_FILE = "manual_review_candidates.csv"

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

# Keep score >= 4 for human review.
# We are deliberately NOT deleting lower-confidence candidates yet.
review = [
    r for r in rows
    if int(r["score"]) >= 4
]

# Highest scores first, then alphabetically.
review.sort(
    key=lambda r: (
        -int(r["score"]),
        r["english"].lower()
    )
)

fields = [
    "score",
    "english",
    "sindhi",
    "english_definition"
]

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=fields
    )

    writer.writeheader()
    writer.writerows(review)

print("=" * 55)
print("MANUAL REVIEW FILE CREATED")
print("=" * 55)
print(f"Original candidates: {len(rows):,}")
print(f"Review candidates:   {len(review):,}")
print()
print(f"Output: {OUTPUT_FILE}")
print("=" * 55)