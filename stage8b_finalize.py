import csv

PASS_FILE = "dictionary_stage8_pass.csv"
REVIEW_FILE = "dictionary_stage8_semantic_review.csv"

DECISION_FILE = "dictionary_stage8b_decisions.csv"
VERIFIED_FILE = "dictionary_stage8_verified.csv"
REMAINING_REVIEW_FILE = "dictionary_stage8_remaining_review.csv"

# ------------------------------------------------------------
# Load files
# ------------------------------------------------------------

with open(PASS_FILE, "r", encoding="utf-8-sig", newline="") as f:
    passed = list(csv.DictReader(f))

with open(REVIEW_FILE, "r", encoding="utf-8-sig", newline="") as f:
    review = list(csv.DictReader(f))

# ------------------------------------------------------------
# Decision rules from manual semantic review
# ------------------------------------------------------------

# Entry 99 in the 112-entry semantic-review list is the only
# one we are deliberately keeping under REVIEW because the
# source definition itself contains uncertainty: "(?)".
#
# All other Stage-8 review entries were judged KEEP.
# ------------------------------------------------------------

decisions = []

for index, row in enumerate(review, 1):

    if index == 99:
        decision = "REVIEW"
        reason = "Source definition itself contains uncertain meanings: Demand. (?) Trouble. (?)"
    else:
        decision = "KEEP"
        reason = "Semantic review completed; definition provides a plausible sense of the English headword."

    new_row = dict(row)
    new_row["stage8b_decision"] = decision
    new_row["stage8b_reason"] = reason
    decisions.append(new_row)

# ------------------------------------------------------------
# Save complete decision audit
# ------------------------------------------------------------

fields = list(review[0].keys()) + [
    "stage8b_decision",
    "stage8b_reason",
]

with open(
    DECISION_FILE,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for row in decisions:
        writer.writerow({
            field: row.get(field, "")
            for field in fields
        })

# ------------------------------------------------------------
# Verified = Stage 8 PASS + manually KEEP entries
# ------------------------------------------------------------

verified_review = [
    row for row in decisions
    if row["stage8b_decision"] == "KEEP"
]

remaining_review = [
    row for row in decisions
    if row["stage8b_decision"] == "REVIEW"
]

# ------------------------------------------------------------
# Use common output fields
# ------------------------------------------------------------

base_fields = [
    "score",
    "english",
    "sindhi",
    "english_definition",
]

verified = []

for row in passed:
    verified.append({
        field: row.get(field, "")
        for field in base_fields
    })

for row in verified_review:
    verified.append({
        field: row.get(field, "")
        for field in base_fields
    })

# ------------------------------------------------------------
# Duplicate check
# ------------------------------------------------------------

seen = set()
unique_verified = []
duplicates = []

for row in verified:

    key = (
        row["english"].strip().lower(),
        row["sindhi"].strip()
    )

    if key in seen:
        duplicates.append(row)
        continue

    seen.add(key)
    unique_verified.append(row)

# ------------------------------------------------------------
# Save verified dictionary
# ------------------------------------------------------------

with open(
    VERIFIED_FILE,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.DictWriter(f, fieldnames=base_fields)
    writer.writeheader()

    for row in unique_verified:
        writer.writerow(row)

# ------------------------------------------------------------
# Save remaining review
# ------------------------------------------------------------

with open(
    REMAINING_REVIEW_FILE,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for row in remaining_review:
        writer.writerow(row)

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

unique_english = len({
    row["english"].strip().lower()
    for row in unique_verified
    if row["english"].strip()
})

print("=" * 70)
print("STAGE 8B SEMANTIC DECISION + MERGE")
print("=" * 70)

print(f"Stage 8 PASS:              {len(passed):,}")
print(f"Semantic review input:     {len(review):,}")
print(f"KEEP from semantic review: {len(verified_review):,}")
print(f"Remaining REVIEW:          {len(remaining_review):,}")
print(f"Duplicate pairs removed:  {len(duplicates):,}")
print(f"VERIFIED UNIQUE ENTRIES:  {len(unique_verified):,}")
print(f"Unique English headwords: {unique_english:,}")

print()
print(f"Decision audit:            {DECISION_FILE}")
print(f"Verified dictionary:       {VERIFIED_FILE}")
print(f"Remaining review:          {REMAINING_REVIEW_FILE}")

print("=" * 70)
