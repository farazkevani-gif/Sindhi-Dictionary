import csv
from collections import defaultdict

INPUT_FILE = "manual_review_candidates.csv"
OUTPUT_FILE = "grouped_review_candidates.txt"

groups = defaultdict(list)

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8-sig",
    newline=""
) as f:

    reader = csv.DictReader(f)

    for row in reader:
        english = row["english"].strip().lower()

        groups[english].append({
            "score": row["score"],
            "sindhi": row["sindhi"],
            "definition": row["english_definition"]
        })


# Highest scoring English words first
ordered_words = sorted(
    groups,
    key=lambda word: (
        -max(int(x["score"]) for x in groups[word]),
        word
    )
)


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write("SINDHI-ENGLISH REVERSE DICTIONARY REVIEW\n")
    f.write("=" * 70 + "\n\n")

    for english in ordered_words:

        candidates = sorted(
            groups[english],
            key=lambda x: -int(x["score"])
        )

        f.write(f"ENGLISH: {english}\n")
        f.write("-" * 70 + "\n")

        for item in candidates:

            f.write(
                f"  [{item['score']}] "
                f"{item['sindhi']}  |  "
                f"{item['definition']}\n"
            )

        f.write("\n")


print("=" * 55)
print("GROUPED REVIEW CREATED")
print("=" * 55)
print(f"Unique English words: {len(groups):,}")
print(f"Total candidates:     {sum(len(x) for x in groups.values()):,}")
print(f"Output:               {OUTPUT_FILE}")
print("=" * 55)