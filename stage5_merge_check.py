import csv

FINAL4 = "dictionary_stage4_final.csv"
ADDED5 = "dictionary_stage5_added.csv"

with open(FINAL4, "r", encoding="utf-8-sig", newline="") as f:
    final4 = list(csv.DictReader(f))

with open(ADDED5, "r", encoding="utf-8-sig", newline="") as f:
    added5 = list(csv.DictReader(f))

def norm(text):
    return " ".join((text or "").strip().lower().split())

existing = {
    (norm(r.get("english")), norm(r.get("sindhi")))
    for r in final4
}

new_entries = []
duplicates = []

for row in added5:
    key = (norm(row.get("english")), norm(row.get("sindhi")))

    if key in existing:
        duplicates.append(row)
    else:
        new_entries.append(row)
        existing.add(key)

print()
print("=" * 60)
print("STAGE 5 MERGE / DUPLICATE CHECK")
print("=" * 60)
print(f"Stage 4 final:       {len(final4):,}")
print(f"Stage 5 added:       {len(added5):,}")
print(f"New unique entries:  {len(new_entries):,}")
print(f"Duplicates:          {len(duplicates):,}")
print(f"Provisional total:   {len(final4) + len(new_entries):,}")
print("=" * 60)
