import csv
from collections import Counter, defaultdict

INPUT_FILE = "dictionary_stage9_final.csv"
AUDIT_FILE = "dictionary_stage10_final_audit.csv"

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

issues = []
pairs = Counter()
exact_rows = Counter()
headwords = defaultdict(list)

for i, row in enumerate(rows, 1):
    english = row.get("english", "").strip()
    sindhi = row.get("sindhi", "").strip()
    definition = row.get("english_definition", "").strip()

    pair = (english.lower(), sindhi)
    exact = tuple(row.get(k, "") for k in row.keys())

    pairs[pair] += 1
    exact_rows[exact] += 1

    if english:
        headwords[english.lower()].append(sindhi)

    if not english:
        issues.append({
            "row": i,
            "issue": "MISSING_ENGLISH",
            "english": english,
            "sindhi": sindhi,
            "definition": definition
        })

    if not sindhi:
        issues.append({
            "row": i,
            "issue": "MISSING_SINDHI",
            "english": english,
            "sindhi": sindhi,
            "definition": definition
        })

    if not definition:
        issues.append({
            "row": i,
            "issue": "MISSING_DEFINITION",
            "english": english,
            "sindhi": sindhi,
            "definition": definition
        })

    combined = f"{english} {sindhi} {definition}".upper()

    if "REVIEW" in combined or "REJECT" in combined:
        issues.append({
            "row": i,
            "issue": "REVIEW_OR_REJECT_MARKER",
            "english": english,
            "sindhi": sindhi,
            "definition": definition
        })

    if "??" in combined or "UNKNOWN" in combined:
        issues.append({
            "row": i,
            "issue": "SUSPICIOUS_PLACEHOLDER",
            "english": english,
            "sindhi": sindhi,
            "definition": definition
        })

# Duplicate pairs
for pair, count in pairs.items():
    if count > 1:
        issues.append({
            "row": "",
            "issue": f"DUPLICATE_PAIR_x{count}",
            "english": pair[0],
            "sindhi": pair[1],
            "definition": ""
        })

# Exact duplicate rows
for exact, count in exact_rows.items():
    if count > 1:
        issues.append({
            "row": "",
            "issue": f"DUPLICATE_EXACT_ROW_x{count}",
            "english": exact[0] if len(exact) > 0 else "",
            "sindhi": exact[1] if len(exact) > 1 else "",
            "definition": exact[2] if len(exact) > 2 else ""
        })

# Audit output
audit_fields = ["row", "issue", "english", "sindhi", "definition"]

with open(AUDIT_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=audit_fields)
    writer.writeheader()
    writer.writerows(issues)

multi_headwords = {
    word: values
    for word, values in headwords.items()
    if len(set(values)) > 1
}

print("=" * 70)
print("STAGE 10 — FINAL MASTER QUALITY AUDIT")
print("=" * 70)
print(f"INPUT ENTRIES:              {len(rows):,}")
print(f"UNIQUE ENGLISH HEADWORDS:   {len(headwords):,}")
print(f"HEADWORDS WITH MULTIPLE")
print(f"SINDHI ENTRIES:             {len(multi_headwords):,}")
print(f"UNIQUE PAIRS:                {len(pairs):,}")
print(f"EXACT DUPLICATE ROW GROUPS:  {sum(1 for x in exact_rows.values() if x > 1):,}")
print(f"QUALITY ISSUES FOUND:        {len(issues):,}")
print()
print(f"Audit file:                  {AUDIT_FILE}")
print("=" * 70)

if issues:
    print()
    print("ISSUES:")
    print("-" * 70)

    for issue in issues:
        print(
            f'{issue["row"]} | '
            f'{issue["issue"]} | '
            f'{issue["english"]} | '
            f'{issue["sindhi"]} | '
            f'{issue["definition"]}'
        )
else:
    print()
    print("✓ NO QUALITY ISSUES FOUND")
    print("✓ NO DUPLICATE PAIRS")
    print("✓ NO EXACT DUPLICATE ROWS")
    print("✓ NO MISSING CORE FIELDS")
    print("✓ NO REVIEW/REJECT MARKERS")
