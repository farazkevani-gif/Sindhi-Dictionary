import csv
import re

INPUT_FILE = "dictionary_master_202.csv"
OUTPUT_FILE = "dictionary_stage7_semantic_audit.csv"

# ------------------------------------------------------------
# Conservative semantic audit
# ------------------------------------------------------------

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

audit = []

# Words that often indicate a definition is broad or contextual.
CONTEXT_WORDS = {
    "talk", "sound", "trouble", "still", "turn",
    "breaking", "pulling", "watching", "ruined",
    "risen", "wandering", "suitable", "successful",
}

# Definitions that contain obvious grammatical/reference
# fragments should receive human review.
REFERENCE_PATTERNS = [
    r"\bcorr\.?\b",
    r"\bcor of\b",
    r"\bsee under\b",
    r"\babbrev\b",
    r"\babbreviation\b",
    r"\bpage\b",
]

def normalize(text):
    return " ".join((text or "").strip().lower().split())

def clean_headword(word):
    return re.sub(r"[^a-z0-9\s'-]", "", normalize(word))

for i, row in enumerate(rows, 1):

    english = row.get("english", "")
    sindhi = row.get("sindhi", "")
    definition = row.get("english_definition", "")

    e = normalize(english)
    d = normalize(definition)

    issues = []
    status = "PASS"

    # --------------------------------------------------------
    # Basic field checks
    # --------------------------------------------------------

    if not e:
        issues.append("Missing English headword")

    if not sindhi.strip():
        issues.append("Missing Sindhi entry")

    if not d:
        issues.append("Missing English definition")

    # --------------------------------------------------------
    # Definition/headword relationship
    # --------------------------------------------------------

    headword = clean_headword(english)

    if headword:
        definition_words = set(
            re.findall(r"[a-z]+", d)
        )

        headword_words = set(
            re.findall(r"[a-z]+", headword)
        )

        # If the definition does not contain the headword,
        # this is NOT automatically an error.
        # Many legitimate dictionary definitions use synonyms.
        if (
            headword not in d
            and not headword_words.intersection(definition_words)
        ):
            issues.append(
                "Definition does not directly repeat headword"
            )

    # --------------------------------------------------------
    # Suspicious source/reference fragments
    # --------------------------------------------------------

    for pattern in REFERENCE_PATTERNS:
        if re.search(pattern, d, flags=re.IGNORECASE):
            issues.append(
                "Possible source/reference fragment"
            )
            break

    # --------------------------------------------------------
    # Parentheses
    # --------------------------------------------------------

    if d.count("(") != d.count(")"):
        issues.append("Unmatched parentheses")

    # --------------------------------------------------------
    # Very short definitions
    # --------------------------------------------------------

    if len(d) <= 2:
        issues.append("Very short definition")

    # --------------------------------------------------------
    # Context-sensitive headwords
    # --------------------------------------------------------

    if e in CONTEXT_WORDS:
        issues.append(
            "Context-sensitive English headword"
        )

    # --------------------------------------------------------
    # Determine status
    # --------------------------------------------------------

    if any(
        "Unmatched" in issue
        or "Missing" in issue
        or "source/reference" in issue
        for issue in issues
    ):
        status = "REVIEW"

    elif any(
        "Context-sensitive" in issue
        or "does not directly" in issue
        for issue in issues
    ):
        status = "REVIEW"

    audit.append({
        "row": i,
        "english": english,
        "sindhi": sindhi,
        "english_definition": definition,
        "semantic_status": status,
        "semantic_reason": "; ".join(issues),
    })

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

fields = [
    "row",
    "english",
    "sindhi",
    "english_definition",
    "semantic_status",
    "semantic_reason",
]

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    writer.writerows(audit)

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

from collections import Counter

counts = Counter(
    row["semantic_status"]
    for row in audit
)

print()
print("=" * 65)
print("SEVENTH-STAGE SEMANTIC CONSISTENCY AUDIT")
print("=" * 65)
print(f"INPUT ENTRIES:       {len(rows):,}")
print()
print(f"PASS:                {counts.get('PASS', 0):,}")
print(f"REVIEW:              {counts.get('REVIEW', 0):,}")
print()
print(f"Audit output:        {OUTPUT_FILE}")
print("=" * 65)

print()
print("REVIEW ENTRIES:")
print("-" * 65)

for row in audit:
    if row["semantic_status"] == "REVIEW":
        print(
            f'{row["row"]:03} | '
            f'{row["english"]} | '
            f'{row["sindhi"]} | '
            f'{row["english_definition"]} | '
            f'{row["semantic_reason"]}'
        )

