import csv

INPUT_FILE = "dictionary_stage8_verified.csv"
REMOVE_ENGLISH = "trouble"
REMOVE_SINDHI = "جاڳَرُ"

FINAL_FILE = "dictionary_stage9_final.csv"
REMOVED_FILE = "dictionary_stage9_removed.csv"

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

kept = []
removed = []

for row in rows:
    if (
        row.get("english", "").strip() == REMOVE_ENGLISH
        and row.get("sindhi", "").strip() == REMOVE_SINDHI
    ):
        row["stage9_status"] = "REMOVED"
        row["stage9_reason"] = (
            "Removed because the original Mewaram definition "
            "'Demand. (?) Trouble. (?)' is explicitly uncertain; "
            "the source also contains a separate sense 'A concert, a chorus.'"
        )
        removed.append(row)
    else:
        kept.append(row)

# Preserve all existing fields
fields = list(rows[0].keys()) if rows else []

if "stage9_status" not in fields:
    fields.append("stage9_status")

if "stage9_reason" not in fields:
    fields.append("stage9_reason")

# Final dictionary
with open(FINAL_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for row in kept:
        writer.writerow({
            field: row.get(field, "")
            for field in fields
        })

# Removed-entry audit
with open(REMOVED_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for row in removed:
        writer.writerow({
            field: row.get(field, "")
            for field in fields
        })

# Duplicate check
pairs = set()
duplicates = []

for row in kept:
    key = (
        row.get("english", "").strip().lower(),
        row.get("sindhi", "").strip()
    )

    if key in pairs:
        duplicates.append(row)
    else:
        pairs.add(key)

# Unique English headwords
headwords = set(
    row.get("english", "").strip().lower()
    for row in kept
    if row.get("english", "").strip()
)

print("=" * 70)
print("STAGE 9 — FINAL SOURCE CORRECTION")
print("=" * 70)
print(f"Input verified entries:       {len(rows):,}")
print(f"Removed uncertain entries:    {len(removed):,}")
print(f"Final entries:                {len(kept):,}")
print(f"Duplicate pairs:              {len(duplicates):,}")
print(f"Unique English headwords:     {len(headwords):,}")
print()
print(f"Final dictionary:              {FINAL_FILE}")
print(f"Removed-entry audit:           {REMOVED_FILE}")
print("=" * 70)

if removed:
    print()
    print("REMOVED ENTRY:")
    for row in removed:
        print(
            f'{row.get("english","")} | '
            f'{row.get("sindhi","")} | '
            f'{row.get("english_definition","")}'
        )
