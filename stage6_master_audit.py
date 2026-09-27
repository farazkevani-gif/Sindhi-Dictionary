import csv
import unicodedata
from collections import Counter

FINAL4 = "dictionary_stage4_final.csv"
ADDED5 = "dictionary_stage5_added.csv"

MASTER = "dictionary_master_202.csv"
AUDIT = "dictionary_master_audit.csv"

def norm(text):
    return " ".join((text or "").strip().lower().split())

def normalize_unicode(text):
    return unicodedata.normalize("NFC", text or "")

# ------------------------------------------------------------
# Load Stage 4
# ------------------------------------------------------------

with open(FINAL4, "r", encoding="utf-8-sig", newline="") as f:
    final4 = list(csv.DictReader(f))

# ------------------------------------------------------------
# Load Stage 5 additions
# ------------------------------------------------------------

with open(ADDED5, "r", encoding="utf-8-sig", newline="") as f:
    added5 = list(csv.DictReader(f))

# ------------------------------------------------------------
# Build master dictionary
# ------------------------------------------------------------

master = []
seen = set()

for source_name, rows in [
    ("stage4", final4),
    ("stage5", added5),
]:

    for row in rows:

        english = normalize_unicode(row.get("english", "").strip())
        sindhi = normalize_unicode(row.get("sindhi", "").strip())
        definition = normalize_unicode(
            row.get("english_definition", "").strip()
        )

        key = (norm(english), norm(sindhi))

        if key in seen:
            continue

        seen.add(key)

        master.append({
            "english": english,
            "sindhi": sindhi,
            "english_definition": definition,
            "source_stage": source_name,
        })

# ------------------------------------------------------------
# Audit
# ------------------------------------------------------------

audit = []

english_counts = Counter(
    norm(row["english"])
    for row in master
)

pair_counts = Counter(
    (norm(row["english"]), norm(row["sindhi"]))
    for row in master
)

for i, row in enumerate(master, 1):

    english = row["english"]
    sindhi = row["sindhi"]
    definition = row["english_definition"]

    issues = []

    if not english:
        issues.append("Missing English headword")

    if not sindhi:
        issues.append("Missing Sindhi entry")

    if not definition:
        issues.append("Missing English definition")

    # Parentheses
    if definition.count("(") != definition.count(")"):
        issues.append("Unmatched parentheses")

    # Suspicious source fragments
    lower_def = definition.lower()

    suspicious = [
        "corr of",
        "see under",
        "page ",
        "abbrev",
        "cor of",
    ]

    for pattern in suspicious:
        if pattern in lower_def:
            issues.append(
                f"Possible source artifact: {pattern}"
            )

    # Very short definitions
    if len(definition.strip()) <= 2:
        issues.append("Extremely short definition")

    # Duplicate pair
    if pair_counts[
        (norm(english), norm(sindhi))
    ] > 1:
        issues.append("Duplicate English-Sindhi pair")

    # Multiple Sindhi senses/translations are NOT an error.
    # We only flag them for visibility.
    multiple = english_counts[norm(english)] > 1

    audit.append({
        "row": i,
        "english": english,
        "sindhi": sindhi,
        "english_definition": definition,
        "multiple_sindhi_for_headword": (
            "YES" if multiple else "NO"
        ),
        "issue": "; ".join(issues),
    })

# ------------------------------------------------------------
# Save master
# ------------------------------------------------------------

with open(
    MASTER,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    fields = [
        "english",
        "sindhi",
        "english_definition",
        "source_stage",
    ]

    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for row in master:
        writer.writerow(row)

# ------------------------------------------------------------
# Save audit
# ------------------------------------------------------------

with open(
    AUDIT,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    fields = [
        "row",
        "english",
        "sindhi",
        "english_definition",
        "multiple_sindhi_for_headword",
        "issue",
    ]

    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for row in audit:
        writer.writerow(row)

# ------------------------------------------------------------
# Statistics
# ------------------------------------------------------------

problem_rows = [
    row for row in audit
    if row["issue"]
]

multi_headwords = sum(
    1
    for count in english_counts.values()
    if count > 1
)

print()
print("=" * 65)
print("MASTER DICTIONARY + QUALITY AUDIT")
print("=" * 65)
print(f"Stage 4 entries:          {len(final4):,}")
print(f"Stage 5 entries:          {len(added5):,}")
print(f"MASTER UNIQUE ENTRIES:    {len(master):,}")
print(f"Duplicate pairs removed:  {len(final4) + len(added5) - len(master):,}")
print()
print(f"Unique English headwords: {len(english_counts):,}")
print(f"Headwords with multiple")
print(f"Sindhi entries:            {multi_headwords:,}")
print(f"Rows with audit issues:    {len(problem_rows):,}")
print()
print(f"Master file:              {MASTER}")
print(f"Audit file:               {AUDIT}")
print("=" * 65)
