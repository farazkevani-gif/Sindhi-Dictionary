import csv
import re
from collections import Counter, defaultdict

INPUT_FILE = "dictionary_core_v1.csv"

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

print("=" * 80)
print("CORE DICTIONARY V1 — FULL QUALITY AUDIT")
print("=" * 80)

print(f"TOTAL ENTRIES:             {len(rows):,}")

# ---------------------------------------------------------
# Basic field checks
# ---------------------------------------------------------

missing_english = []
missing_sindhi = []
missing_definition = []

for i, r in enumerate(rows, 1):
    english = r.get("word", "").strip()
    sindhi = (
        r.get("word_with_airab_or_variant", "").strip()
        or r.get("word", "").strip()
    )
    definition = r.get("definition", "").strip()

    if not english:
        missing_english.append(i)

    if not sindhi:
        missing_sindhi.append(i)

    if not definition:
        missing_definition.append(i)

print()
print("FIELD CHECKS")
print("-" * 80)
print(f"Missing English:            {len(missing_english):,}")
print(f"Missing Sindhi:             {len(missing_sindhi):,}")
print(f"Missing definitions:        {len(missing_definition):,}")

# ---------------------------------------------------------
# Exact duplicate check
# ---------------------------------------------------------

seen = {}
duplicates = []

for i, r in enumerate(rows, 1):
    key = (
        r.get("word", "").strip().casefold(),
        (
            r.get("word_with_airab_or_variant", "").strip()
            or r.get("word", "").strip()
        ).casefold(),
        r.get("definition", "").strip().casefold()
    )

    if key in seen:
        duplicates.append((seen[key], i))
    else:
        seen[key] = i

print()
print("DUPLICATE CHECK")
print("-" * 80)
print(f"Exact duplicate rows:       {len(duplicates):,}")

# ---------------------------------------------------------
# English headword statistics
# ---------------------------------------------------------

headwords = [
    r.get("word", "").strip()
    for r in rows
    if r.get("word", "").strip()
]

headword_counts = Counter(x.casefold() for x in headwords)

repeated = {
    word: count
    for word, count in headword_counts.items()
    if count > 1
}

print()
print("HEADWORD STATISTICS")
print("-" * 80)
print(f"Unique English headwords:   {len(headword_counts):,}")
print(f"Repeated headwords:         {len(repeated):,}")

# ---------------------------------------------------------
# Alphabet coverage
# ---------------------------------------------------------

alphabet = Counter()

for word in headwords:
    first = word[0].upper()

    if first.isalpha() and "A" <= first <= "Z":
        alphabet[first] += 1

print()
print("ALPHABET COVERAGE")
print("-" * 80)

for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    print(f"{letter}: {alphabet.get(letter, 0):,}")

# ---------------------------------------------------------
# Definition lengths
# ---------------------------------------------------------

definition_lengths = [
    len(r.get("definition", "").strip())
    for r in rows
    if r.get("definition", "").strip()
]

print()
print("DEFINITION STATISTICS")
print("-" * 80)

if definition_lengths:
    print(f"Shortest:                  {min(definition_lengths)} characters")
    print(f"Longest:                   {max(definition_lengths)} characters")
    print(f"Average:                   {sum(definition_lengths)/len(definition_lengths):.1f} characters")

# ---------------------------------------------------------
# Suspicious Unicode/control characters
# ---------------------------------------------------------

control_rows = []

for i, r in enumerate(rows, 1):
    text = " ".join([
        r.get("word", ""),
        r.get("word_with_airab_or_variant", ""),
        r.get("definition", "")
    ])

    if any(ord(ch) < 32 and ch not in "\t\n\r" for ch in text):
        control_rows.append(i)

print()
print("UNICODE / TEXT CHECK")
print("-" * 80)
print(f"Rows with control characters: {len(control_rows):,}")

# ---------------------------------------------------------
# Suspicious HTML / CSV artifacts
# ---------------------------------------------------------

artifact_patterns = [
    "<br",
    "</",
    "&nbsp;",
    "\\x",
    "�",
]

artifact_rows = []

for i, r in enumerate(rows, 1):
    text = " ".join([
        r.get("word", ""),
        r.get("word_with_airab_or_variant", ""),
        r.get("definition", "")
    ])

    if any(p.lower() in text.lower() for p in artifact_patterns):
        artifact_rows.append(i)

print()
print("ARTIFACT CHECK")
print("-" * 80)
print(f"Rows with possible artifacts: {len(artifact_rows):,}")

# ---------------------------------------------------------
# Suspicious whitespace
# ---------------------------------------------------------

whitespace_rows = []

for i, r in enumerate(rows, 1):
    for field in ["word", "word_with_airab_or_variant", "definition"]:
        value = r.get(field, "")

        if value != value.strip():
            whitespace_rows.append(i)
            break

print()
print("WHITESPACE CHECK")
print("-" * 80)
print(f"Rows with leading/trailing whitespace: {len(whitespace_rows):,}")

# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

total_issues = (
    len(missing_english)
    + len(missing_sindhi)
    + len(missing_definition)
    + len(duplicates)
    + len(control_rows)
    + len(artifact_rows)
)

print()
print("=" * 80)
print("AUDIT SUMMARY")
print("=" * 80)
print(f"Total entries:              {len(rows):,}")
print(f"Unique headwords:           {len(headword_counts):,}")
print(f"Exact duplicates:           {len(duplicates):,}")
print(f"Missing English:            {len(missing_english):,}")
print(f"Missing Sindhi:             {len(missing_sindhi):,}")
print(f"Missing definitions:        {len(missing_definition):,}")
print(f"Control-character rows:     {len(control_rows):,}")
print(f"Artifact rows:              {len(artifact_rows):,}")
print(f"Whitespace rows:            {len(whitespace_rows):,}")
print()
print("IMPORTANT: Short translations are NOT treated as errors.")
print("Legitimate multiple senses are preserved.")
print("=" * 80)
