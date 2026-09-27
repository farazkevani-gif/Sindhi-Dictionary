import csv
from collections import defaultdict

INPUT_FILE = "sindhi-lexicon.csv"

OUTPUT_FILE = "dictionary_core_v1.csv"
DUPLICATES_FILE = "dictionary_core_v1_duplicates.csv"
REVIEW_FILE = "dictionary_core_v1_review.csv"

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

# Only the dedicated English → Sindhi domain
core = [
    r for r in rows
    if r.get("domain", "").strip() == "English → Sindhi"
]

# Normalize only for comparison; preserve original text in output
def norm(value):
    return " ".join((value or "").strip().split()).casefold()

seen = set()
unique_rows = []
duplicates = []

for row in core:
    english = row.get("word", "").strip()
    sindhi = (
        row.get("word_with_airab_or_variant", "").strip()
        or row.get("word", "").strip()
    )
    definition = row.get("definition", "").strip()

    key = (
        norm(english),
        norm(sindhi),
        norm(definition)
    )

    if key in seen:
        duplicates.append(row)
    else:
        seen.add(key)
        unique_rows.append(row)

# Flag unusual but NOT automatically rejectable entries
review = []

for row in unique_rows:
    english = row.get("word", "").strip()
    sindhi = (
        row.get("word_with_airab_or_variant", "").strip()
        or row.get("word", "").strip()
    )
    definition = row.get("definition", "").strip()

    reasons = []

    if len(english) <= 1:
        reasons.append("Very short English headword")

    if len(definition) <= 2:
        reasons.append("Very short definition")

    if not sindhi:
        reasons.append("Missing Sindhi translation")

    if reasons:
        r = dict(row)
        r["review_reason"] = "; ".join(reasons)
        review.append(r)

# Fields
fields = list(core[0].keys())

if "review_reason" not in fields:
    review_fields = fields + ["review_reason"]
else:
    review_fields = fields

# Write core dictionary
with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(unique_rows)

# Write duplicates
with open(DUPLICATES_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(duplicates)

# Write review
with open(REVIEW_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=review_fields)
    writer.writeheader()
    writer.writerows(review)

print("=" * 75)
print("CORE DICTIONARY V1 — DEDUPLICATION")
print("=" * 75)
print(f"Source English → Sindhi:   {len(core):,}")
print(f"Unique entries:            {len(unique_rows):,}")
print(f"Exact duplicates removed:  {len(duplicates):,}")
print(f"Review flags:              {len(review):,}")
print()
print(f"Core dictionary:            {OUTPUT_FILE}")
print(f"Duplicates:                 {DUPLICATES_FILE}")
print(f"Review file:                {REVIEW_FILE}")
print("=" * 75)
