import csv
import re

INPUT_FILE = "reverse_candidates.csv"
OUTPUT_FILE = "strict_reverse_candidates.csv"

# Words that should not be recovered from reverse definitions
BLOCKED = {
    "a", "an", "the", "and", "or", "of", "to", "in", "on",
    "at", "by", "for", "from", "with", "as", "is", "are",
    "was", "were", "be", "been", "being",
    "i", "you", "he", "she", "it", "we", "they",
    "s", "viii", "ii", "iii", "iv", "vi", "vii", "ix", "x"
}

ROMAN = re.compile(r"^(?=[ivxlcdm]+$)[ivxlcdm]+$", re.I)


def clean(text):
    return " ".join(text.strip().split())


def first_sentence(definition):
    """
    Get the first part of a dictionary definition.
    """
    text = definition.strip()

    # Stop at obvious cross-reference markers
    for marker in [
        " See ",
        " see ",
        " Page ",
        " page ",
        " Also ",
        " also "
    ]:
        pos = text.find(marker)
        if pos > 0:
            text = text[:pos]

    return text.strip(" .;:")


kept = []
seen = set()

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:

        english = clean(row.get("english", "")).lower()
        sindhi = clean(row.get("sindhi", ""))
        definition = clean(row.get("english_definition", ""))

        if not english or not sindhi or not definition:
            continue

        # Normal English word only
        if not re.fullmatch(r"[a-z]+(?:['-][a-z]+)*", english):
            continue

        if english in BLOCKED or ROMAN.fullmatch(english):
            continue

        # Ignore very long Sindhi phrases
        if len(sindhi.split()) > 6:
            continue

        first = first_sentence(definition)
        first_lower = first.lower()

        # Remove definitions that are clearly about another thing
        if "page " in definition.lower():
            continue

        # Count English words in the first definition
        words = re.findall(
            r"[a-z]+(?:['-][a-z]+)*",
            first_lower
        )

        if not words:
            continue

        # Strong signal: definition begins with the target word
        starts_with_word = (
            first_lower == english
            or first_lower.startswith(english + " ")
            or first_lower.startswith(english + ",")
            or first_lower.startswith(english + ";")
        )

        # Strong signal: definition is very short and contains the word
        short_direct = (
            len(words) <= 5
            and re.search(r"\b" + re.escape(english) + r"\b", first_lower)
        )

        # Accept only strong candidates
        if not starts_with_word and not short_direct:
            continue

        key = (english, sindhi)

        if key in seen:
            continue

        seen.add(key)

        kept.append({
            "english": english,
            "sindhi": sindhi,
            "english_definition": definition
        })


with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:

    fields = [
        "english",
        "sindhi",
        "english_definition"
    ]

    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(kept)


print()
print("=" * 50)
print("STRICT FILTER COMPLETE")
print("=" * 50)
print(f"Strict candidates: {len(kept):,}")
print(f"Output: {OUTPUT_FILE}")
print("=" * 50)