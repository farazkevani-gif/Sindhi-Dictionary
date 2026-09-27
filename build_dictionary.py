import csv
import re

LEXICON_FILE = "sindhi-lexicon.csv"
WORDS_FILE = "english-20k.txt"
OUTPUT_FILE = "english_sindhi_matches.csv"


def clean_word(word):
    word = word.strip().lower()
    word = re.sub(r"[^a-z'-]", "", word)
    return word


# Load 20,000 English words
with open(WORDS_FILE, "r", encoding="utf-8") as f:
    english_words = {
        clean_word(line)
        for line in f
        if clean_word(line)
    }

print(f"English words loaded: {len(english_words):,}")


# Read lexicon
matches = {}

with open(LEXICON_FILE, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:

        # The dataset uses "english" for English entries
        if row.get("language_direction", "").strip().lower() != "english":
            continue

        english = clean_word(row.get("word", ""))

        if not english:
            continue

        # Only words from our 20K frequency list
        if english not in english_words:
            continue

        sindhi = row.get("definition", "").strip()

        if not sindhi:
            continue

        # Keep the first entry for each English word
        if english not in matches:
            matches[english] = {
                "english": english,
                "sindhi": sindhi,
                "part_of_speech": row.get("part_of_speech", "").strip(),
                "definition": sindhi,
            }


# Save results
with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:

    fieldnames = [
        "english",
        "sindhi",
        "part_of_speech",
        "definition",
    ]

    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for word in sorted(matches):
        writer.writerow(matches[word])


print()
print("=" * 50)
print("DICTIONARY BUILD COMPLETE")
print("=" * 50)
print(f"20K English words:       {len(english_words):,}")
print(f"Matched words:           {len(matches):,}")
print(f"Missing translations:    {len(english_words) - len(matches):,}")
print(f"Output file:             {OUTPUT_FILE}")
print("=" * 50)