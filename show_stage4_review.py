import csv

FILE = "dictionary_stage4_review.csv"

with open(FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

print("REVIEW ENTRIES:", len(rows))
print()

for i, r in enumerate(rows, 1):
    print(
        i,
        "|", r.get("english", ""),
        "|", r.get("sindhi", ""),
        "|", r.get("english_definition", ""),
        "|", r.get("stage4_reason", "")
    )
