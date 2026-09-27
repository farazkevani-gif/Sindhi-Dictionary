import csv
from collections import Counter

INPUT_FILE = "final_dictionary_candidates.csv"
OUTPUT_FILE = "final_audit.csv"

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

WATCH_WORDS = {
    "cor",
    "liter",
    "blanco",
    "greater",
    "still",
    "sound",
    "talk",
    "pulling",
    "risen",
    "ruined",
    "transferred",
    "watching",
    "storing",
    "successful",
    "suitable",
    "arriving",
    "breaking",
    "butts",
    "flaming",
    "proving",
    "remembered",
    "tailed",
    "trouble",
}

audit = []

for row in rows:
    english = row["english"].strip().lower()
    definition = row["english_definition"].strip().lower()

    flags = []

    if english in WATCH_WORDS:
        flags.append("WATCH_WORD")

    if "cor of" in definition:
        flags.append("COR_ARTIFACT")

    if definition == english:
        flags.append("HEADWORD_ONLY")

    if len(english) <= 3:
        flags.append("VERY_SHORT_ENGLISH")

    if not row["sindhi"].strip():
        flags.append("EMPTY_SINDHI")

    row["audit_flags"] = ";".join(flags)

    if flags:
        audit.append(row)

fields = list(rows[0].keys())

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(audit)

print("=" * 55)
print("FINAL AUDIT")
print("=" * 55)
print(f"Final candidates: {len(rows):,}")
print(f"Flagged candidates: {len(audit):,}")
print(f"Output: {OUTPUT_FILE}")
print()

counts = Counter()

for row in audit:
    for flag in row["audit_flags"].split(";"):
        if flag:
            counts[flag] += 1

for flag, count in counts.most_common():
    print(f"{flag}: {count:,}")

print("=" * 55)
