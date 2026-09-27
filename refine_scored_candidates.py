import csv
import re

INPUT_FILE = "scored_reverse_candidates.csv"

HIGH_OUTPUT = "high_confidence_candidates.csv"
POSSIBLE_OUTPUT = "possible_candidates.csv"
REJECT_OUTPUT = "local_rejected_candidates.csv"


# ------------------------------------------------------------
# Junk English entries / dictionary artifacts
# ------------------------------------------------------------

JUNK_WORDS = {
    "etc",
    "abs",
    "adv",
    "cor",
    "n",
    "v",
    "adj",
    "prep",
    "pron",
    "conj",
    "interj",
}


# ------------------------------------------------------------
# Obvious artifact patterns
# ------------------------------------------------------------

BAD_PATTERNS = [
    r"\bsee\b",
    r"\bpage\b",
    r"\bchapter\b",
    r"\btable\b",
    r"\bplate\b",
    r"\bappendix\b",
    r"\babbreviation\b",
    r"\babbrev\b",
    r"\bof\s*$",
    r"^\s*etc\.?\s*$",
]


# ------------------------------------------------------------
# Clean text
# ------------------------------------------------------------

def clean(text):
    return re.sub(r"\s+", " ", text.strip())


# ------------------------------------------------------------
# Local scoring
# ------------------------------------------------------------

def classify(row):

    score = int(row["score"])
    english = clean(row["english"]).lower()
    definition = clean(row["english_definition"]).lower()

    # --------------------------------------------
    # Obvious junk
    # --------------------------------------------

    if english in JUNK_WORDS:
        return "REJECT"

    for pattern in BAD_PATTERNS:
        if re.search(pattern, definition, re.IGNORECASE):
            return "REJECT"

    # --------------------------------------------
    # Very strong direct dictionary match
    # --------------------------------------------

    if score >= 13:
        return "HIGH"

    # Definition exactly equals English word
    if definition.strip(" .;:,") == english:
        return "HIGH"

    # Definition starts with the English word
    if re.match(
        r"^" + re.escape(english) + r"\b",
        definition,
        re.IGNORECASE
    ):
        return "HIGH"

    # --------------------------------------------
    # Strong score
    # --------------------------------------------

    if score >= 8:
        return "POSSIBLE"

    # --------------------------------------------
    # Medium score
    # --------------------------------------------

    if score >= 5:
        return "POSSIBLE"

    # --------------------------------------------
    # Everything else
    # --------------------------------------------

    return "REJECT"


# ------------------------------------------------------------
# Load
# ------------------------------------------------------------

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8-sig",
    newline=""
) as f:

    rows = list(csv.DictReader(f))


print("=" * 55)
print("REFINING SCORED CANDIDATES")
print("=" * 55)

print(f"Input candidates: {len(rows):,}")


high = []
possible = []
rejected = []


# ------------------------------------------------------------
# Classify
# ------------------------------------------------------------

for row in rows:

    category = classify(row)

    if category == "HIGH":
        high.append(row)

    elif category == "POSSIBLE":
        possible.append(row)

    else:
        rejected.append(row)


# ------------------------------------------------------------
# Save helper
# ------------------------------------------------------------

FIELDS = [
    "score",
    "english",
    "sindhi",
    "english_definition"
]


def save_file(filename, data):

    with open(
        filename,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=FIELDS
        )

        writer.writeheader()
        writer.writerows(data)


save_file(HIGH_OUTPUT, high)
save_file(POSSIBLE_OUTPUT, possible)
save_file(REJECT_OUTPUT, rejected)


# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

print()
print("REFINEMENT COMPLETE")
print("=" * 55)

print(f"HIGH CONFIDENCE: {len(high):,}")
print(f"POSSIBLE:        {len(possible):,}")
print(f"REJECTED:        {len(rejected):,}")
print()

print(f"High output:     {HIGH_OUTPUT}")
print(f"Possible output: {POSSIBLE_OUTPUT}")
print(f"Rejected output: {REJECT_OUTPUT}")

print("=" * 55)