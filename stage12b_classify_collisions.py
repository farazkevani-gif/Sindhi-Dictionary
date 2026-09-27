import csv
from collections import defaultdict

INPUT_FILE = "dictionary_stage12_clean.csv"
REVIEW_FILE = "dictionary_stage12_review.csv"
CLASSIFIED_FILE = "dictionary_stage12_classified_review.csv"

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

groups = defaultdict(list)

for r in rows:
    key = r.get("lookup_headword", "").strip().lower()
    groups[key].append(r)

review = []

for key, matches in groups.items():
    if len(matches) <= 1:
        continue

    # Collect source headwords and Sindhi translations
    words = set(r.get("word", "").strip().lower() for r in matches)
    sindhi = set(r.get("word_with_airab_or_variant", "").strip() for r in matches)

    # Classification
    if len(words) == 1:
        classification = "SAME_SOURCE_HEADWORD_MULTIPLE_ROWS"
    elif len(sindhi) == 1:
        classification = "HEADWORD_VARIANT_SAME_SINDHI"
    else:
        classification = "GENUINE_NORMALIZATION_COLLISION"

    for r in matches:
        review.append({
            **r,
            "collision_class": classification,
            "collision_group_size": len(matches)
        })

with open(CLASSIFIED_FILE, "w", encoding="utf-8-sig", newline="") as f:
    fields = list(review[0].keys()) if review else []
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(review)

from collections import Counter
counts = Counter(r["collision_class"] for r in review)

print("=" * 80)
print("STAGE 12B — COLLISION CLASSIFICATION")
print("=" * 80)
print(f"TOTAL SOURCE ENTRIES:             {len(rows):,}")
print(f"COLLISION ROWS:                    {len(review):,}")
print()

for k, v in counts.most_common():
    print(f"{k:<40} {v:,}")

print()
print(f"Classified review:                 {CLASSIFIED_FILE}")
print("=" * 80)
