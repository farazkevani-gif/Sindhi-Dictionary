import csv
import re

KEEP_FILE = "dictionary_keep.csv"
REVIEW_FILE = "dictionary_review.csv"

FINAL_FILE = "dictionary_final.csv"
REVIEW2_FILE = "dictionary_cleanup_review.csv"
REJECT_FILE = "dictionary_rejected.csv"


def clean_definition(definition):
    d = definition.strip()

    # Remove obvious extraction punctuation at the beginning.
    d = re.sub(r'^\s*\)\s*', '', d)

    # Remove obvious extraction punctuation at the end.
    # Only remove a closing parenthesis when it is clearly unmatched.
    if d.count("(") < d.count(")"):
        d = re.sub(r'\)\s*$', '', d).strip()

    return d


def has_unbalanced_parentheses(text):
    return text.count("(") != text.count(")")


def looks_truncated(text):
    t = text.strip()

    if not t:
        return True

    # Opening parenthesis with no matching close.
    if has_unbalanced_parentheses(t):
        return True

    # Obvious unfinished ending.
    if t.endswith("("):
        return True

    return False


def read_csv(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    if not rows:
        return

    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


keep_rows = read_csv(KEEP_FILE)
review_rows = read_csv(REVIEW_FILE)

final_rows = []
cleanup_review = []
rejected = []

print("=" * 55)
print("THIRD-STAGE DICTIONARY CLEANUP")
print("=" * 55)
print(f"KEEP input:       {len(keep_rows):,}")
print(f"REVIEW input:     {len(review_rows):,}")
print()


# ---------------------------------------------------------
# Existing KEEP rows
# ---------------------------------------------------------

for row in keep_rows:
    row["stage3_decision"] = "KEEP"
    row["stage3_reason"] = "Passed second-stage quality filter."
    final_rows.append(row)


# ---------------------------------------------------------
# REVIEW rows
# ---------------------------------------------------------

for row in review_rows:

    english = row["english"].strip()
    sindhi = row["sindhi"].strip()
    definition = row["english_definition"].strip()

    cleaned = clean_definition(definition)

    # -----------------------------------------------------
    # Case 1: Obvious leading/trailing punctuation damage
    # -----------------------------------------------------

    punctuation_changed = cleaned != definition

    if punctuation_changed and not looks_truncated(cleaned):

        new_row = dict(row)
        new_row["english_definition"] = cleaned
        new_row["stage3_decision"] = "KEEP_CLEANED"
        new_row["stage3_reason"] = (
            "Obvious unmatched extraction punctuation removed; "
            "dictionary sense remains intact."
        )

        final_rows.append(new_row)
        continue


    # -----------------------------------------------------
    # Case 2: Clearly truncated / structurally damaged
    # -----------------------------------------------------

    if looks_truncated(definition):

        new_row = dict(row)
        new_row["stage3_decision"] = "REVIEW"
        new_row["stage3_reason"] = (
            "Definition appears structurally incomplete or truncated; "
            "requires source verification."
        )

        cleanup_review.append(new_row)
        continue


    # -----------------------------------------------------
    # Case 3: Short English words are NOT automatically bad.
    #
    # Examples:
    # sup, tie, tap, aim, cry, sit, etc.
    #
    # If they have a meaningful definition, retain them.
    # -----------------------------------------------------

    if len(english) <= 3 and len(definition) >= 6:

        new_row = dict(row)
        new_row["stage3_decision"] = "KEEP"
        new_row["stage3_reason"] = (
            "Short English headword has a meaningful dictionary definition."
        )

        final_rows.append(new_row)
        continue


    # -----------------------------------------------------
    # Case 4: General semantic/context review
    # -----------------------------------------------------

    new_row = dict(row)
    new_row["stage3_decision"] = "REVIEW"
    new_row["stage3_reason"] = (
        "Potentially valid dictionary entry; semantic/source "
        "verification recommended."
    )

    cleanup_review.append(new_row)


# ---------------------------------------------------------
# Write results
# ---------------------------------------------------------

write_csv(FINAL_FILE, final_rows)
write_csv(REVIEW2_FILE, cleanup_review)
write_csv(REJECT_FILE, rejected)


print("THIRD-STAGE CLEANUP COMPLETE")
print("=" * 55)
print(f"FINAL:            {len(final_rows):,}")
print(f"REVIEW:           {len(cleanup_review):,}")
print(f"REJECTED:         {len(rejected):,}")
print(f"TOTAL PROCESSED:  {len(keep_rows) + len(review_rows):,}")
print()
print(f"Final output:     {FINAL_FILE}")
print(f"Review output:    {REVIEW2_FILE}")
print(f"Rejected output:  {REJECT_FILE}")
print("=" * 55)
