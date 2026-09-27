import csv

with open("dictionary_cleanup_review.csv", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

print("TOTAL:", len(rows))
print()

for i, r in enumerate(rows, 1):
    print(
        i,
        "|", r.get("english", ""),
        "|", r.get("sindhi", ""),
        "|", r.get("english_definition", ""),
        "|", r.get("cleanup_reason", "")
    )
