import csv

INPUT_FILE = "dictionary_stage12_clean.csv"
OUTPUT_FILE = "dictionary_stage13_lookup_ready.csv"

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

# Add stable sequential ID without changing source content
for i, r in enumerate(rows, 1):
    r["dictionary_id"] = str(i)

# Put the ID first
fields = ["dictionary_id"] + [
    k for k in rows[0].keys()
    if k != "dictionary_id"
]

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print("=" * 80)
print("STAGE 13 — LOOKUP-READY DICTIONARY")
print("=" * 80)
print(f"INPUT ENTRIES:              {len(rows):,}")
print(f"OUTPUT ENTRIES:             {len(rows):,}")
print("SOURCE ENTRIES DELETED:     0")
print("SOURCE TRANSLATIONS LOST:   0")
print()
print(f"Lookup-ready dictionary:    {OUTPUT_FILE}")
print("=" * 80)
