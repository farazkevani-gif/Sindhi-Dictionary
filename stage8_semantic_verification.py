import csv
import re

INPUT_FILE = "dictionary_stage7_semantic_audit.csv"

OUTPUT_FILE = "dictionary_stage8_semantic_review.csv"
PASS_FILE = "dictionary_stage8_pass.csv"
REJECT_FILE = "dictionary_stage8_rejected.csv"

# ------------------------------------------------------------
# STAGE 8
# Conservative semantic verification
#
# Goal:
#   - Keep entries that have clear semantic evidence.
#   - Keep context-sensitive entries for manual/source review.
#   - Reject only obvious mismatches.
#
# IMPORTANT:
# This stage does NOT try to determine whether a Sindhi word
# is the "best" translation. It only identifies obvious problems.
# ------------------------------------------------------------

def norm(text):
    return re.sub(r"\s+", " ", (text or "").strip().lower())


# English headwords whose meanings are especially broad or
# context-dependent. These should NOT be automatically rejected.
CONTEXT_WORDS = {
    "breaking",
    "pulling",
    "risen",
    "ruined",
    "sound",
    "still",
    "successful",
    "suitable",
    "talk",
    "trouble",
    "wandering",
    "watching",
    "weaving",
    "turn",
    "falling",
    "working",
    "transferred",
    "thunder",
    "swallowing",
    "shaking",
    "drinking",
    "giving",
    "proving",
    "storing",
    "travelling",
    "twist",
}

# ------------------------------------------------------------
# Obvious bad semantic patterns
# ------------------------------------------------------------

OBVIOUS_BAD = [
    r"^\s*$",
]

# These are not automatically rejected merely because they
# contain unusual punctuation or dictionary-source fragments.
# We only reject when there is strong evidence of a completely
# unrelated English meaning.

# ------------------------------------------------------------
# Load
# ------------------------------------------------------------

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

print("=" * 65)
print("EIGHTH-STAGE SEMANTIC VERIFICATION")
print("=" * 65)
print(f"INPUT ENTRIES:       {len(rows):,}")
print()

pass_rows = []
review_rows = []
reject_rows = []

# ------------------------------------------------------------
# Process
# ------------------------------------------------------------

for row in rows:

    english = norm(row.get("english", ""))
    sindhi = row.get("sindhi", "").strip()
    definition = row.get("english_definition", "").strip()
    old_status = row.get("semantic_status", "").strip()

    # Missing core data
    if not english or not sindhi:
        row["stage8_status"] = "REJECT"
        row["stage8_reason"] = "Missing English or Sindhi headword."
        reject_rows.append(row)
        continue

    # Empty definition
    if not definition:
        row["stage8_status"] = "REVIEW"
        row["stage8_reason"] = "Missing English definition; source verification required."
        review_rows.append(row)
        continue

    # If Stage 7 already passed it, retain it.
    if old_status == "PASS":
        row["stage8_status"] = "PASS"
        row["stage8_reason"] = "Passed previous semantic audit."
        pass_rows.append(row)
        continue

    # Context-sensitive English words are retained for review,
    # not rejected.
    if english in CONTEXT_WORDS:
        row["stage8_status"] = "REVIEW"
        row["stage8_reason"] = (
            "Context-sensitive English headword; "
            "retain pending source/sense verification."
        )
        review_rows.append(row)
        continue

    # Otherwise retain conservatively for human/source review.
    row["stage8_status"] = "REVIEW"
    row["stage8_reason"] = (
        "Potentially valid dictionary entry; "
        "source/sense verification recommended."
    )
    review_rows.append(row)


# ------------------------------------------------------------
# Fields
# ------------------------------------------------------------

fields = [
    "row",
    "english",
    "sindhi",
    "english_definition",
    "semantic_status",
    "semantic_reason",
    "stage8_status",
    "stage8_reason",
]


def save_file(filename, data):
    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fields,
            extrasaction="ignore"
        )
        writer.writeheader()

        for row in data:
            writer.writerow({
                field: row.get(field, "")
                for field in fields
            })


save_file(PASS_FILE, pass_rows)
save_file(OUTPUT_FILE, review_rows)
save_file(REJECT_FILE, reject_rows)

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

print("STAGE 8 COMPLETE")
print("=" * 65)
print(f"INPUT:               {len(rows):,}")
print(f"PASS:                {len(pass_rows):,}")
print(f"REVIEW:              {len(review_rows):,}")
print(f"REJECTED:            {len(reject_rows):,}")
print()
print(f"Pass output:         {PASS_FILE}")
print(f"Review output:       {OUTPUT_FILE}")
print(f"Rejected output:     {REJECT_FILE}")
print("=" * 65)
