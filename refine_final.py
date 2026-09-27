import csv
import re

INPUT_FILE = "manual_review_candidates.csv"
OUTPUT_FILE = "final_dictionary_candidates.csv"
REJECTED_FILE = "final_rejected_candidates.csv"

# ------------------------------------------------------------
# Rules for obvious dictionary artifacts / bad reverse matches
# ------------------------------------------------------------

BAD_DEFINITION_PATTERNS = [
    r"\bsee under\b",
    r"\bsee\b",
    r"\bpage\b",
    r"\betc\.?\b",
    r"\babbreviation\b",
    r"\babbrev\b",
    r"\bplural of\b",
    r"\bpast tense of\b",
    r"\bparticiple of\b",
    r"\bcor of\b",
    r"\bn\. cor\b",
    r"\( cor\b",
]

# Definitions that clearly describe the requested English word
# are retained even if the score is lower.
STRONG_DEFINITION_PATTERNS = [
    r"^\s*{WORD}\s*[\.,;:]?$",
    r"^\s*{WORD}\b",
]

# ------------------------------------------------------------
# Load
# ------------------------------------------------------------

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

print("=" * 55)
print("FINAL DICTIONARY REFINEMENT")
print("=" * 55)
print(f"Input candidates: {len(rows):,}")
print()

accepted = []
rejected = []

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def normalize(text):
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def looks_like_artifact(english, definition):
    e = normalize(english)
    d = normalize(definition)

    # Empty fields
    if not e or not d:
        return True

    # Explicit dictionary/reference artifacts
    for pattern in BAD_DEFINITION_PATTERNS:
        if re.search(pattern, d, flags=re.IGNORECASE):
            return True

    # "cor of ..." entries are generally fragments rather than
    # translations of the English headword.
    if re.search(r"\bcor of\b", d, flags=re.IGNORECASE):
        return True

    # Definition consisting only of the English headword is useful.
    # It was already selected by the previous scoring stage.
    return False


def is_direct_match(english, definition):
    e = normalize(english)
    d = normalize(definition)

    # Exact definition: "England."
    d_clean = re.sub(r"[^a-z0-9\s'-]", "", d).strip()

    if d_clean == e:
        return True

    # "Crooked, zigzag." / "Curse, imprecation."
    if d.startswith(e + ","):
        return True

    if d.startswith(e + " "):
        return True

    return False


# ------------------------------------------------------------
# Process
# ------------------------------------------------------------

for row in rows:

    english = row.get("english", "")
    sindhi = row.get("sindhi", "")
    definition = row.get("english_definition", "")
    score = row.get("score", "")

    if looks_like_artifact(english, definition):
        row["final_decision"] = "REJECT"
        row["final_reason"] = "Dictionary/reference artifact or unrelated fragment."
        rejected.append(row)
        continue

    # Strong direct dictionary evidence
    if is_direct_match(english, definition):
        row["final_decision"] = "ACCEPT"
        row["final_reason"] = "Definition directly matches the English headword."
        accepted.append(row)
        continue

    # Reject suspiciously weak entries
    try:
        numeric_score = int(score)
    except ValueError:
        numeric_score = 0

    if numeric_score < 4:
        row["final_decision"] = "REJECT"
        row["final_reason"] = "Low candidate score without strong direct definition."
        rejected.append(row)
        continue

    # Otherwise retain for dictionary output.
    row["final_decision"] = "ACCEPT"
    row["final_reason"] = "Candidate retained after final rule-based refinement."
    accepted.append(row)


# ------------------------------------------------------------
# Save accepted
# ------------------------------------------------------------

fields = [
    "score",
    "english",
    "sindhi",
    "english_definition",
    "final_decision",
    "final_reason",
]

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for row in accepted:
        writer.writerow({
            field: row.get(field, "")
            for field in fields
        })


# ------------------------------------------------------------
# Save rejected
# ------------------------------------------------------------

with open(
    REJECTED_FILE,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for row in rejected:
        writer.writerow({
            field: row.get(field, "")
            for field in fields
        })


# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

unique_english = len({
    normalize(r["english"])
    for r in accepted
    if normalize(r["english"])
})

print("FINAL REFINEMENT COMPLETE")
print("=" * 55)
print(f"ACCEPTED:         {len(accepted):,}")
print(f"REJECTED:         {len(rejected):,}")
print(f"UNIQUE ENGLISH:   {unique_english:,}")
print()
print(f"Final output:     {OUTPUT_FILE}")
print(f"Rejected output:  {REJECTED_FILE}")
print("=" * 55)