import csv
import json
import os
import time
from google import genai

INPUT_FILE = "scored_reverse_candidates.csv"
OUTPUT_FILE = "ai_verified_candidates.csv"
BATCH_SIZE = 50

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise SystemExit("ERROR: GEMINI_API_KEY is not set.")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.8-flash"

# ------------------------------------------------------------
# Load candidates
# ------------------------------------------------------------

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

# Give every candidate a stable ID FIRST.
for i, row in enumerate(rows):
    row["id"] = str(i + 1)

print(f"Candidates loaded: {len(rows):,}")

# ------------------------------------------------------------
# Resume support
# ------------------------------------------------------------

processed = {}

if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("id"):
                processed[row["id"]] = row

    print(f"Already processed: {len(processed):,}")

remaining = [r for r in rows if r["id"] not in processed]

print(f"Remaining: {len(remaining):,}")
print()

# ------------------------------------------------------------
# Instructions
# ------------------------------------------------------------

SYSTEM_INSTRUCTION = """
You are a bilingual Sindhi-English dictionary verification system.

Your job is NOT to invent translations.

For every candidate, determine whether the Sindhi word or phrase
is a valid translation or lexical equivalent of the supplied
English word, using the supplied English dictionary definition.

MATCH:
The Sindhi entry clearly corresponds to the English word or meaning.

REJECT:
The candidate is clearly unrelated, merely contextual, an example,
page/reference artifact, grammatical label, abbreviation, fragment,
or the English word appears only incidentally.

UNCERTAIN:
There is some evidence of a relationship but it is not sufficiently
clear to accept automatically.

Rules:
- Prefer dictionary meaning over superficial word overlap.
- Do not invent translations.
- Keep multiple genuine Sindhi equivalents when valid.
- "etc", page references, grammatical abbreviations and fragments
  should normally be rejected.
- A definition such as "A cork, plug." is strong evidence for "cork".
- Judge the actual English word, not merely a word appearing somewhere
  inside the definition.
- Return exactly one result for every supplied ID.
"""

# ------------------------------------------------------------
# Process batches
# ------------------------------------------------------------

results = list(processed.values())

total_batches = (len(remaining) + BATCH_SIZE - 1) // BATCH_SIZE

for batch_number, start in enumerate(
    range(0, len(remaining), BATCH_SIZE),
    start=1
):
    batch = remaining[start:start + BATCH_SIZE]

    print(
        f"Batch {batch_number}/{total_batches} "
        f"({len(batch)} candidates)..."
    )

    candidates = []

    for r in batch:
        candidates.append({
            "id": r["id"],
            "score": r.get("score", ""),
            "english": r["english"],
            "sindhi": r["sindhi"],
            "definition": r["english_definition"]
        })

    prompt = f"""
Verify these English-Sindhi dictionary candidates.

Return ONLY a JSON array.

Each item MUST contain:

{{
  "id": "...",
  "decision": "MATCH",
  "confidence": 0.0,
  "reason": "short explanation"
}}

The decision MUST be exactly one of:
MATCH
REJECT
UNCERTAIN

Candidates:

{json.dumps(candidates, ensure_ascii=False)}
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=SYSTEM_INSTRUCTION + "\n\n" + prompt,
            config={
                "temperature": 0
            }
        )

        text = response.text.strip()

        # Remove Markdown code fences if present.
        if text.startswith("```"):
            lines = text.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            text = "\n".join(lines).strip()

        ai_results = json.loads(text)

        result_by_id = {
            str(x["id"]): x
            for x in ai_results
        }

        for r in batch:

            ai = result_by_id.get(r["id"])

            if not ai:
                ai = {
                    "decision": "UNCERTAIN",
                    "confidence": 0,
                    "reason": "AI did not return a result."
                }

            results.append({
                "id": r["id"],
                "score": r.get("score", ""),
                "english": r["english"],
                "sindhi": r["sindhi"],
                "english_definition": r["english_definition"],
                "decision": ai.get(
                    "decision",
                    "UNCERTAIN"
                ),
                "confidence": ai.get(
                    "confidence",
                    0
                ),
                "reason": ai.get(
                    "reason",
                    ""
                )
            })

        # Save after EVERY batch.
        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8-sig",
            newline=""
        ) as f:

            fields = [
                "id",
                "score",
                "english",
                "sindhi",
                "english_definition",
                "decision",
                "confidence",
                "reason"
            ]

            writer = csv.DictWriter(
                f,
                fieldnames=fields
            )

            writer.writeheader()
            writer.writerows(results)

        print(
            f"Saved {len(results):,} results."
        )

        time.sleep(1)

    except Exception as e:

        print()
        print("ERROR IN THIS BATCH:")
        print(e)
        print()
        print(
            "Everything processed before this batch has been saved."
        )
        print(
            "Run the script again to resume."
        )
        break

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

counts = {
    "MATCH": 0,
    "REJECT": 0,
    "UNCERTAIN": 0
}

for r in results:
    decision = r.get("decision", "")

    if decision in counts:
        counts[decision] += 1

print()
print("=" * 55)
print("AI VERIFICATION COMPLETE")
print("=" * 55)
print(f"Total processed: {len(results):,}")
print(f"MATCH:           {counts['MATCH']:,}")
print(f"REJECT:          {counts['REJECT']:,}")
print(f"UNCERTAIN:       {counts['UNCERTAIN']:,}")
print()
print(f"Output: {OUTPUT_FILE}")
print("=" * 55)