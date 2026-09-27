import csv
from collections import Counter, defaultdict

INPUT_FILE = "sindhi-lexicon.csv"

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

core = [
    r for r in rows
    if r.get("domain", "").strip() == "English → Sindhi"
]

print("=" * 75)
print("CORE ENGLISH → SINDHI DATASET ANALYSIS")
print("=" * 75)

print(f"TOTAL SOURCE ROWS:       {len(core):,}")

# English words
english = [
    r.get("word", "").strip()
    for r in core
    if r.get("word", "").strip()
]

print(f"NON-EMPTY ENGLISH:        {len(english):,}")
print(f"UNIQUE ENGLISH:           {len(set(x.lower() for x in english)):,}")

# Definitions
definitions = [
    r.get("definition", "").strip()
    for r in core
]

empty_def = sum(not x for x in definitions)

print(f"EMPTY DEFINITIONS:        {empty_def:,}")

# Duplicate English headwords
counts = Counter(x.lower() for x in english)
duplicates = {
    word: count
    for word, count in counts.items()
    if count > 1
}

print(f"HEADWORDS REPEATED:       {len(duplicates):,}")
print(f"ROWS INVOLVED IN REPEATS: {sum(duplicates.values()):,}")

print()
print("REPEATED HEADWORDS:")
print("-" * 75)

for word, count in sorted(duplicates.items())[:100]:
    print(f"{count:3} | {word}")

# Missing Sindhi
missing_sindhi = []

for r in core:
    sindhi = (
        r.get("word_with_airab_or_variant", "").strip()
        or r.get("word", "").strip()
    )

    if not sindhi:
        missing_sindhi.append(r)

print()
print(f"MISSING SINDHI TRANSLATION: {len(missing_sindhi):,}")

# Definition lengths
lengths = [
    len(r.get("definition", "").strip())
    for r in core
    if r.get("definition", "").strip()
]

if lengths:
    print()
    print("DEFINITION LENGTHS")
    print(f"Shortest:                 {min(lengths)} characters")
    print(f"Longest:                  {max(lengths)} characters")
    print(f"Average:                  {sum(lengths)/len(lengths):.1f} characters")

# Show repeated examples
if duplicates:
    print()
    print("EXAMPLES OF REPEATED HEADWORDS")
    print("-" * 75)

    shown = 0

    for word in sorted(duplicates):
        matches = [
            r for r in core
            if r.get("word", "").strip().lower() == word
        ]

        print()
        print(f"[{word}]")

        for r in matches:
            print(
                "  →",
                r.get("definition", "").strip()
            )

        shown += 1

        if shown >= 20:
            break

print()
print("=" * 75)
