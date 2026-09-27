import csv
import re

INPUT_FILE = "dictionary_cleanup_review.csv"

FINAL_FILE = "dictionary_stage4_final.csv"
REVIEW_FILE = "dictionary_stage4_review.csv"
REJECT_FILE = "dictionary_stage4_rejected.csv"


def norm(text):
    return re.sub(r"\s+", " ", (text or "").strip())


def balanced_parentheses(text):
    return text.count("(") == text.count(")")


def obviously_truncated(text):
    d = norm(text)

    if not d:
        return True

    # Ends with an opening parenthesis
    if d.endswith("("):
        return True

    # Common extraction/reference fragments that clearly continue
    if re.search(r"\(\s*$", d):
        return True

    if re.search(r"\(\s*(Shah|Hindi|Hindu|Jewelry|Weaving|corr|cor|e\.g)\s*$",
                 d, flags=re.IGNORECASE):
        return True

    if re.search(r"\b(corr of|cor of)\s*$", d, flags=re.IGNORECASE):
        return True

    return False


def looks_like_reference_fragment(text):
    d = norm(text).lower()

    # A definition consisting only of a bare grammatical/reference
    # fragment should be manually checked.
    if d in {
        "cor",
        "cor.",
        "corr",
        "corr.",
        "see",
        "see under",
    }:
        return True

    return False


def classify(row):

    english = norm(row.get("english", ""))
    sindhi = norm(row.get("sindhi", ""))
    definition = norm(row.get("english_definition", ""))

    # Missing essential fields
    if not english or not sindhi or not definition:
        return "REJECT", "Missing English, Sindhi, or definition field."

    # Very obvious reference fragment
    if looks_like_reference_fragment(definition):
        return "REVIEW", "Definition appears to be a dictionary reference fragment."

    # Structural damage
    if not balanced_parentheses(definition):
        return "REVIEW", "Definition has unmatched parentheses."

    # Truncated extraction
    if obviously_truncated(definition):
        return "REVIEW", "Definition appears structurally incomplete or truncated."

    # Strong direct dictionary definition
    e = english.lower()
    d = definition.lower()

    # Exact headword definition
    cleaned = re.sub(r"[^a-z0-9\s'-]", "", d).strip()

    if cleaned == e:
        return "FINAL", "Exact English headword definition."

    # Definition begins with English headword
    if d.startswith(e + "."):
        return "FINAL", "Definition directly matches English headword."

    if d.startswith(e + ","):
        return "FINAL", "Definition directly matches English headword."

    if d.startswith(e + " "):
        return "FINAL", "Definition directly matches English headword."

    # Otherwise it is still potentially valid, but retain for
    # conservative semantic review.
    return "REVIEW", "Potentially valid dictionary entry; semantic/source verification recommended."


# ------------------------------------------------------------
# LOAD
# ------------------------------------------------------------

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))


final_rows = []
review_rows = []
reject_rows = []


# ------------------------------------------------------------
# PROCESS
# ------------------------------------------------------------

for row in rows:

    decision, reason = classify(row)

    row["stage4_decision"] = decision
    row["stage4_reason"] = reason

    if decision == "FINAL":
        final_rows.append(row)

    elif decision == "REVIEW":
        review_rows.append(row)

    else:
        reject_rows.append(row)


# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------

fields = [
    "score",
    "english",
    "sindhi",
    "english_definition",
    "final_decision",
    "final_reason",
    "quality_decision",
    "quality_reason",
    "cleanup_decision",
    "cleanup_reason",
    "stage4_decision",
    "stage4_reason",
]


def write_csv(filename, data):

    with open(
        filename,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as f:

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


write_csv(FINAL_FILE, final_rows)
write_csv(REVIEW_FILE, review_rows)
write_csv(REJECT_FILE, reject_rows)


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

print()
print("=" * 60)
print("FOURTH-STAGE CONSERVATIVE DICTIONARY CLEANUP")
print("=" * 60)

print(f"INPUT:             {len(rows):,}")
print(f"FINAL:             {len(final_rows):,}")
print(f"REVIEW:            {len(review_rows):,}")
print(f"REJECTED:          {len(reject_rows):,}")
print()

print(f"Final output:      {FINAL_FILE}")
print(f"Review output:     {REVIEW_FILE}")
print(f"Rejected output:   {REJECT_FILE}")

print("=" * 60)
