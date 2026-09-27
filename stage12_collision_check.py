import csv
import re
from collections import Counter

INPUT_FILE = "dictionary_stage11_normalized.csv"
OUTPUT_FILE = "dictionary_stage12_clean.csv"
REVIEW_FILE = "dictionary_stage12_review.csv"

def normalize_for_lookup(word):
    w = word.strip()

    # Remove common grammatical labels only for lookup purposes.
    w = re.sub(
        r'\s*\((?:n|v|adj|adv|prep|pron|conj|interj|pl|sing|past|p\.t\.|p\.p\.|pp)\)\s*$',
        '',
        w,
        flags=re.I
    )

    # Normalize repeated whitespace.
    w = re.sub(r'\s+', ' ', w)

    return w.strip().lower()

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

review = []
seen = {}

for r in rows:
    word = r.get("word", "").strip()
    normalized = r.get("normalized_headword", "").strip()

    if not normalized:
        normalized = normalize_for_lookup(word)

    r["lookup_headword"] = normalized

    if normalized in seen:
        review.append({
            **r,
            "review_reason": "Normalized headword collision",
            "collision_with_row": seen[normalized]
        })
    else:
        seen[normalized] = r.get("row", "")

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
    if rows:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

review_fields = list(rows[0].keys()) + ["review_reason", "collision_with_row"]

with open(REVIEW_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=review_fields)
    writer.writeheader()
    writer.writerows(review)

print("=" * 80)
print("STAGE 12 — AUTOMATED HEADWORD COLLISION CHECK")
print("=" * 80)
print(f"INPUT ENTRIES:              {len(rows):,}")
print(f"UNIQUE LOOKUP HEADWORDS:    {len(seen):,}")
print(f"NORMALIZATION COLLISIONS:   {len(review):,}")
print()
print(f"Clean output:               {OUTPUT_FILE}")
print(f"Review output:              {REVIEW_FILE}")
print("=" * 80)
