import csv
import json
import re
from collections import defaultdict

INPUT_FILE = "dictionary_stage14_grouped.csv"
OUTPUT_FILE = "dictionary_stage18_reverse_index.json"

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

reverse_index = defaultdict(list)

for row in rows:

    english = row.get("english_headword", "").strip()
    sindhi = row.get("sindhi_translations", "").strip()

    if not english or not sindhi:
        continue

    # Split grouped Sindhi translations
    meanings = [
        x.strip()
        for x in sindhi.split("|")
        if x.strip()
    ]

    for meaning in meanings:

        # ----------------------------------------------------
        # INDEX COMPLETE SINDHI MEANING
        # ----------------------------------------------------

        key = meaning.lower().strip()

        if english not in reverse_index[key]:
            reverse_index[key].append(english)

        # ----------------------------------------------------
        # INDEX INDIVIDUAL SINDHI WORDS
        # ----------------------------------------------------

        words = re.findall(r'[\u0600-\u06FF]+', meaning)

        for word in words:

            word_key = word.lower().strip()

            if word_key and english not in reverse_index[word_key]:
                reverse_index[word_key].append(english)


reverse_index = dict(reverse_index)


with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    json.dump(
        reverse_index,
        f,
        ensure_ascii=False,
        indent=2
    )


indexed_relationships = sum(
    len(v)
    for v in reverse_index.values()
)


print("=" * 80)
print("STAGE 18 — SINDHI REVERSE SEARCH INDEX")
print("=" * 80)

print(f"SOURCE DICTIONARY ROWS:       {len(rows):,}")
print(f"REVERSE INDEX TERMS:          {len(reverse_index):,}")
print(f"INDEXED RELATIONSHIPS:        {indexed_relationships:,}")

print()
print(f"Reverse index:                {OUTPUT_FILE}")

print()
print("SOURCE DICTIONARY MODIFIED:   NO")
print("SOURCE TRANSLATIONS DELETED:  NO")

print("=" * 80)

