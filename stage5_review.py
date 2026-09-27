import csv

INPUT_FILE = "dictionary_stage4_review.csv"
ADDED_FILE = "dictionary_stage5_added.csv"
REVIEW_FILE = "dictionary_stage5_source_review.csv"

# Entries judged usable from the current review.
# Row numbers refer to dictionary_stage4_review.csv as displayed.
PROMOTE_ROWS = {
    5, 16, 20, 21,
    *range(35, 61),
    *range(62, 77),
    79, 80
}

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

added = []
review = []

for i, row in enumerate(rows, 1):
    row["stage5_decision"] = ""
    row["stage5_reason"] = ""

    if i in PROMOTE_ROWS:
        row["stage5_decision"] = "ADD"
        row["stage5_reason"] = (
            "Usable dictionary definition; no obvious source truncation."
        )
        added.append(row)
    else:
        row["stage5_decision"] = "SOURCE_REVIEW"
        row["stage5_reason"] = (
            "Definition appears truncated, malformed, or is a dictionary "
            "reference fragment; verify against original source."
        )
        review.append(row)

fields = [
    "english",
    "sindhi",
    "english_definition",
    "stage5_decision",
    "stage5_reason",
]

for filename, data in [
    (ADDED_FILE, added),
    (REVIEW_FILE, review),
]:
    with open(
        filename,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()

        for row in data:
            writer.writerow({
                field: row.get(field, "")
                for field in fields
            })

print()
print("=" * 60)
print("FIFTH-STAGE CONSERVATIVE REVIEW")
print("=" * 60)
print(f"INPUT:              {len(rows):,}")
print(f"ADDED:              {len(added):,}")
print(f"SOURCE REVIEW:      {len(review):,}")
print()
print(f"Added output:       {ADDED_FILE}")
print(f"Source review:      {REVIEW_FILE}")
print("=" * 60)
