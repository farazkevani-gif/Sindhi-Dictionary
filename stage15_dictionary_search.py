import csv

INPUT_FILE = "dictionary_stage14_grouped.csv"

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

print("=" * 80)
print("STAGE 15 — DICTIONARY SEARCH TEST")
print("=" * 80)
print(f"DICTIONARY HEADWORDS: {len(rows):,}")
print()
print("Type an English word to search.")
print("Partial searches are supported.")
print("Type EXIT to quit.")
print("=" * 80)

while True:
    query = input("\nSearch: ").strip().lower()

    if query == "exit":
        break

    if not query:
        continue

    exact = [
        r for r in rows
        if r.get("lookup_headword", "").lower() == query
    ]

    if exact:
        results = exact
    else:
        results = [
            r for r in rows
            if query in r.get("lookup_headword", "").lower()
        ]

    if not results:
        print("No matching English word found.")
        continue

    print()
    print("-" * 80)

    for r in results[:20]:
        print(f"English: {r.get('english_headword', '')}")
        print(f"Sindhi:  {r.get('sindhi_translations', '')}")
        print()

    if len(results) > 20:
        print(f"... and {len(results) - 20} more matches.")

    print("-" * 80)

print()
print("Dictionary search ended.")
