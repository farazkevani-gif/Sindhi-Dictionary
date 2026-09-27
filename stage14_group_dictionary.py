import csv
import json
from collections import OrderedDict

INPUT_FILE = "dictionary_stage13_lookup_ready.csv"
OUTPUT_FILE = "dictionary_stage14_grouped.csv"

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

groups = OrderedDict()

for r in rows:
    key = r.get("lookup_headword", "").strip().lower()

    if not key:
        continue

    if key not in groups:
        groups[key] = {
            "lookup_headword": key,
            "english_headword": r.get("english_original", "").strip(),
            "translations": []
        }

    translation = {
        "sindhi": r.get("definition", "").strip(),
        "source_word": r.get("word", "").strip(),
        "source_dictionary": r.get("source_dictionary", "").strip(),
        "part_of_speech": r.get("part_of_speech", "").strip(),
        "domain": r.get("domain", "").strip(),
        "lexical_id": r.get("lexical_id", "").strip()
    }

    groups[key]["translations"].append(translation)

output_rows = []

for key, item in groups.items():
    output_rows.append({
        "lookup_headword": item["lookup_headword"],
        "english_headword": item["english_headword"],
        "translation_count": len(item["translations"]),
        "sindhi_translations": " | ".join(
            t["sindhi"]
            for t in item["translations"]
            if t["sindhi"]
        ),
        "translations_json": json.dumps(
            item["translations"],
            ensure_ascii=False
        )
    })

fields = [
    "lookup_headword",
    "english_headword",
    "translation_count",
    "sindhi_translations",
    "translations_json"
]

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(output_rows)

print("=" * 80)
print("STAGE 14 — GROUPED ENGLISH → SINDHI DICTIONARY")
print("=" * 80)
print(f"SOURCE ROWS:                 {len(rows):,}")
print(f"UNIQUE LOOKUP HEADWORDS:     {len(output_rows):,}")
print(f"TRANSLATION RECORDS:         {len(rows):,}")
print()
print("No source rows deleted.")
print("Multiple meanings preserved.")
print()
print(f"Grouped dictionary:          {OUTPUT_FILE}")
print("=" * 80)
