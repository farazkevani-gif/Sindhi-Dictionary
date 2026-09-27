import csv
import re
from pathlib import Path

INPUT_FILE = Path("final_dictionary_candidates.csv")

KEEP_FILE = Path("dictionary_keep.csv")
REVIEW_FILE = Path("dictionary_review.csv")
REMOVE_FILE = Path("dictionary_remove.csv")


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

SHORT_LENGTH = 3

ABBREVIATION_WORDS = {
    "ab", "abs", "adv", "art", "bot", "com", "conj", "ect",
    "fig", "gen", "gui", "inf", "lit", "mah", "mas", "med",
    "nom", "opp", "pat", "pl", "prep", "pron", "rob", "rub",
    "st", "sup", "tal", "ups", "etc"
}

WATCH_WORDS = {
    "aim",
    "breaking",
    "butts",
    "cor",
    "flaming",
    "greater",
    "liter",
    "pulling",
    "remembered",
    "risen",
    "ruined",
    "sound",
    "still",
    "storing",
    "successful",
    "suitable",
    "tailed",
    "talk",
    "transferred",
    "trouble",
    "watching",
}

BAD_EXACT = {
    "ab",
    "abs",
    "adv",
    "bot",
    "com",
    "ect",
    "gui",
    "inf",
    "lit",
    "mah",
    "mas",
    "med",
    "nom",
    "opp",
    "pat",
    "pl",
    "st",
    "tal",
    "ups",
}


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def clean(value):
    if value is None:
        return ""
    return str(value).strip()


def normalize_english(value):
    value = clean(value).lower()
    value = re.sub(r"\s+", " ", value)
    return value


def normalize_definition(value):
    value = clean(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip(" .;:")


def is_headword_only(english, definition):
    english = normalize_english(english)
    definition = normalize_definition(definition).lower()

    if not english or not definition:
        return True

    definition = re.sub(r"[^\w\s'-]", "", definition)
    english = re.sub(r"[^\w\s'-]", "", english)

    return definition == english


def is_abbreviation_like(english):
    english = normalize_english(english)

    if english in ABBREVIATION_WORDS:
        return True

    if len(english) <= SHORT_LENGTH:
        return True

    return False


def has_bad_definition(definition):
    definition = normalize_definition(definition).lower()

    if not definition:
        return True

    suspicious_patterns = [
        r"^\(?\s*of\s*$",
        r"^\(?\s*to\s*$",
        r"^\(?\s*or\s*$",
        r"^\(?\s*and\s*$",
        r"^\(?\s*idem\s*$",
        r"^\(?\s*opp\s*$",
        r"^\(?\s*pl\s*$",
        r"^\(?\s*n\s*$",
    ]

    for pattern in suspicious_patterns:
        if re.match(pattern, definition):
            return True

    return False


# ---------------------------------------------------------
# CLASSIFICATION
# ---------------------------------------------------------

def classify(row):
    english = normalize_english(row.get("english", ""))
    sindhi = clean(row.get("sindhi", ""))
    definition = clean(row.get("english_definition", ""))

    reasons = []

    if not english:
        return "REMOVE", "Missing English headword."

    if not sindhi:
        return "REMOVE", "Missing Sindhi translation."

    if english in BAD_EXACT:
        return "REMOVE", "Likely dictionary abbreviation or extraction fragment."

    if has_bad_definition(definition):
        return "REMOVE", "Definition appears incomplete or malformed."

    if is_headword_only(english, definition):
        reasons.append(
            "Definition is essentially the English headword."
        )

    if is_abbreviation_like(english):
        reasons.append(
            "Very short or abbreviation-like English entry."
        )

    if english in WATCH_WORDS:
        reasons.append(
            "English headword requires contextual/sense review."
        )

    if re.search(
        r"\(\s*(abs|bot|com|med|nom|opp|pl|lit|mas|mah)\s*\)",
        definition.lower()
    ):
        reasons.append(
            "Definition contains dictionary abbreviation marker."
        )

    if definition.endswith("("):
        reasons.append(
            "Definition appears truncated."
        )

    if definition.count("(") > definition.count(")"):
        reasons.append(
            "Definition has unmatched opening parenthesis."
        )

    if definition.count(")") > definition.count("("):
        reasons.append(
            "Definition has unmatched closing parenthesis."
        )

    if reasons:
        return "REVIEW", " ".join(reasons)

    return "KEEP", "No major rule-based quality problems detected."


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

print("=" * 55)
print("SECOND-STAGE DICTIONARY QUALITY FILTER")
print("=" * 55)

if not INPUT_FILE.exists():
    print()
    print("ERROR: Input file not found:")
    print(INPUT_FILE.resolve())
    print()
    raise SystemExit(1)

with INPUT_FILE.open(
    "r",
    encoding="utf-8-sig",
    newline=""
) as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Input candidates: {len(rows):,}")

keep_rows = []
review_rows = []
remove_rows = []

for row in rows:
    decision, reason = classify(row)

    output_row = dict(row)
    output_row["quality_decision"] = decision
    output_row["quality_reason"] = reason

    if decision == "KEEP":
        keep_rows.append(output_row)

    elif decision == "REVIEW":
        review_rows.append(output_row)

    else:
        remove_rows.append(output_row)


# ---------------------------------------------------------
# WRITE OUTPUT FILES
# ---------------------------------------------------------

if rows:
    fieldnames = list(rows[0].keys()) + [
        "quality_decision",
        "quality_reason"
    ]
else:
    fieldnames = [
        "quality_decision",
        "quality_reason"
    ]


def write_csv(path, data):
    with path.open(
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )
        writer.writeheader()
        writer.writerows(data)


write_csv(KEEP_FILE, keep_rows)
write_csv(REVIEW_FILE, review_rows)
write_csv(REMOVE_FILE, remove_rows)


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

print()
print("QUALITY FILTER COMPLETE")
print("=" * 55)
print(f"KEEP:             {len(keep_rows):,}")
print(f"REVIEW:           {len(review_rows):,}")
print(f"REMOVE:           {len(remove_rows):,}")
print(f"TOTAL:            {len(rows):,}")
print()
print(f"Keep output:      {KEEP_FILE}")
print(f"Review output:    {REVIEW_FILE}")
print(f"Remove output:    {REMOVE_FILE}")
print("=" * 55)
