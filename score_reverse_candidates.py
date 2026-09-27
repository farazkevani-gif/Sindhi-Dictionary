import csv
import re

INPUT_FILE = "strict_reverse_candidates.csv"
OUTPUT_FILE = "scored_reverse_candidates.csv"


def clean(text):
    return " ".join(text.strip().split())


def score_candidate(english, sindhi, definition):
    score = 0

    e = english.lower()
    d = definition.lower()

    # Very strong: definition is essentially the English word itself
    if d.strip(" .;:,") == e:
        score += 5

    # Definition starts directly with the target word
    if re.match(r"^" + re.escape(e) + r"\b", d):
        score += 4

    # Definition contains exact English word
    if re.search(r"\b" + re.escape(e) + r"\b", d):
        score += 2

    # Short definition = usually more direct
    word_count = len(re.findall(r"[a-z]+", d))

    if word_count <= 3:
        score += 2
    elif word_count <= 6:
        score += 1

    # Penalize obvious contextual definitions
    bad_patterns = [
        "see under",
        "one who",
        "used for",
        "with ",
        "before ",
        "after ",
        "according to",
        "supposed to",
        "for example",
        "etc.",
    ]

    for pattern in bad_patterns:
        if pattern in d:
            score -= 2

    return score


rows = []

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        english = clean(row["english"])
        sindhi = clean(row["sindhi"])
        definition = clean(row["english_definition"])

        score = score_candidate(
            english,
            sindhi,
            definition
        )

        rows.append({
            "score": score,
            "english": english,
            "sindhi": sindhi,
            "english_definition": definition
        })


rows.sort(
    key=lambda x: (
        -x["score"],
        x["english"]
    )
)


with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:

    fields = [
        "score",
        "english",
        "sindhi",
        "english_definition"
    ]

    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)


from collections import Counter

counts = Counter(row["score"] for row in rows)

print()
print("=" * 50)
print("SCORING COMPLETE")
print("=" * 50)
print(f"Total candidates: {len(rows):,}")
print()

for score in sorted(counts, reverse=True):
    print(f"Score {score:>2}: {counts[score]:,}")

print()
print(f"Output file: {OUTPUT_FILE}")
print("=" * 50)