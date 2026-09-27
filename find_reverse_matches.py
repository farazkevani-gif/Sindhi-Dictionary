import csv
import re
from collections import defaultdict

LEXICON_FILE = "sindhi-lexicon.csv"
WORDS_FILE = "english-20k.txt"
EXISTING_FILE = "english_sindhi_matches.csv"
OUTPUT_FILE = "reverse_candidates.csv"


def normalize(word):
    return word.strip().lower()


# --------------------------------------------------
# 1. Load the 20K English words
# --------------------------------------------------

with open(WORDS_FILE, "r", encoding="utf-8") as f:
    english_words = {
        normalize(line)
        for line in f
        if normalize(line)
    }

# --------------------------------------------------
# 2. Load words already matched
# --------------------------------------------------

with open(EXISTING_FILE, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)

    existing = {
        normalize(row["english"])
        for row in reader
        if row.get("english")
    }

missing = english_words - existing

print(f"Total English words: {len(english_words):,}")
print(f"Already matched:     {len(existing):,}")
print(f"Still missing:       {len(missing):,}")
print()
print("Building reverse index...")


# --------------------------------------------------
# 3. Build an index from English definitions
# --------------------------------------------------

index = defaultdict(list)

with open(LEXICON_FILE, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:

        if row.get("language_direction", "").strip().lower() != "sindhi-english":
            continue

        sindhi_word = row.get("word", "").strip()
        definition = row.get("definition", "").strip()

        if not sindhi_word or not definition:
            continue

        # Extract English words from the definition
        english_terms = re.findall(r"[a-z]+(?:['-][a-z]+)*", definition.lower())

        for term in set(english_terms):

            if term in missing:
                index[term].append({
                    "sindhi": sindhi_word,
                    "definition": definition
                })


print("Reverse index built.")
print("Finding candidates...")


# --------------------------------------------------
# 4. Find candidates
# --------------------------------------------------

candidates = []

for english in missing:

    if english not in index:
        continue

    for item in index[english]:

        candidates.append({
            "english": english,
            "sindhi": item["sindhi"],
            "english_definition": item["definition"]
        })


# --------------------------------------------------
# 5. Remove duplicates
# --------------------------------------------------

unique = {}

for item in candidates:

    key = (
        item["english"],
        item["sindhi"]
    )

    if key not in unique:
        unique[key] = item


# --------------------------------------------------
# 6. Save candidates
# --------------------------------------------------

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:

    fieldnames = [
        "english",
        "sindhi",
        "english_definition"
    ]

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(unique.values())


# --------------------------------------------------
# 7. Results
# --------------------------------------------------

print()
print("=" * 50)
print("REVERSE SEARCH COMPLETE")
print("=" * 50)
print(f"Missing words checked: {len(missing):,}")
print(f"Candidate matches:     {len(unique):,}")
print(f"Output file:           {OUTPUT_FILE}")
print("=" * 50)