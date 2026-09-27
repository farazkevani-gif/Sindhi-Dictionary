import csv
import re
from collections import Counter

INPUT_FILE = "dictionary_core_v1.csv"

OUTPUT_FILE = "dictionary_stage11_normalized.csv"
REVIEW_FILE = "dictionary_stage11_normalization_review.csv"

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

def normalize_english(word):
    w = word.strip()

    # Normalize repeated whitespace
    w = re.sub(r"\s+", " ", w)

    # Normalize surrounding whitespace inside parentheses
    w = re.sub(r"\(\s+", "(", w)
    w = re.sub(r"\s+\)", ")", w)

    return w

def classify(word):
    w = word.strip()

    if not w:
        return "EMPTY"

    if w.startswith("(") and w.endswith(")"):
        return "PARENTHETICAL"

    if re.search(r"\([^)]*\)", w):
        return "HEADWORD_WITH_LABEL"

    if re.search(r"\s+(n|v|adj|adv|prep|conj|pron)\.?$", w, re.I):
        return "PART_OF_SPEECH_LABEL"

    if re.search(r"\bp\.?t\.?\s+of\b", w, re.I):
        return "GRAMMATICAL_LABEL"

    if re.search(r"\b(of|to|the|a|an|in|on|for)\b", w, re.I):
        return "MULTIWORD"

    return "ORDINARY_HEADWORD"

output_rows = []
review_rows = []

classification_counts = Counter()

for i, row in enumerate(rows, 1):
    original = row.get("word", "")
    normalized = normalize_english(original)
    category = classify(original)

    new_row = dict(row)
    new_row["english_original"] = original
    new_row["english_normalized"] = normalized
    new_row["headword_class"] = category

    output_rows.append(new_row)
    classification_counts[category] += 1

    # Only flag unusual forms for inspection.
    # Nothing is automatically removed.
    if (
        category in {
            "PARENTHETICAL",
            "HEADWORD_WITH_LABEL",
            "PART_OF_SPEECH_LABEL",
            "GRAMMATICAL_LABEL"
        }
        or original != normalized
    ):
        review = dict(new_row)
        review["review_reason"] = category
        review_rows.append(review)

fields = list(output_rows[0].keys())

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(output_rows)

review_fields = list(review_rows[0].keys()) if review_rows else fields

with open(REVIEW_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=review_fields)
    writer.writeheader()
    writer.writerows(review_rows)

print("=" * 80)
print("STAGE 11 — ENGLISH HEADWORD NORMALIZATION")
print("=" * 80)

print(f"INPUT ENTRIES:             {len(rows):,}")
print()

print("HEADWORD CLASSIFICATION")
print("-" * 80)

for category, count in classification_counts.most_common():
    print(f"{category:<28} {count:,}")

print()
print(f"NORMALIZATION REVIEW:      {len(review_rows):,}")
print()
print(f"Normalized dictionary:      {OUTPUT_FILE}")
print(f"Normalization review:      {REVIEW_FILE}")

print()
print("IMPORTANT:")
print("No dictionary entries were deleted.")
print("Original headwords are preserved.")
print("Normalization is stored separately from the source wording.")

print("=" * 80)
