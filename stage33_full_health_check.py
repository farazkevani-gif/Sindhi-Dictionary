import ast
import csv
import json
import os
import re
import sqlite3
import importlib.util
from collections import defaultdict

BASE = "."

CSV_FILE = "dictionary_stage14_grouped.csv"
INDEX_FILE = "dictionary_stage18_reverse_index.json"
FONT_FILE = os.path.join("fonts", "NotoSansArabic-Regular.ttf")
DB_FILE = "dictionary_stage22_android.db"

APP_FILES = [
    "stage23_android_dictionary.py",
    "stage30_android_dictionary.py",
    "stage31_android_dictionary.py",
    "stage32_android_dictionary_live_search.py",
]

issues = []
warnings = []

def issue(msg):
    issues.append(msg)

def warning(msg):
    warnings.append(msg)

print("=" * 90)
print("DICTIONARY PROJECT — FULL HEALTH CHECK")
print("=" * 90)

# ============================================================
# FILE EXISTENCE
# ============================================================

required_files = [
    CSV_FILE,
    INDEX_FILE,
    FONT_FILE,
]

print()
print("1. REQUIRED FILES")
print("-" * 90)

for filename in required_files:

    exists = os.path.exists(filename)

    print(
        f"{'OK   ' if exists else 'FAIL '}"
        f"{filename}"
    )

    if not exists:
        issue(f"Missing required file: {filename}")


# ============================================================
# CURRENT APP FILES
# ============================================================

print()
print("2. CURRENT APP SCRIPTS")
print("-" * 90)

for filename in APP_FILES:

    if os.path.exists(filename):

        size = os.path.getsize(filename)

        print(
            f"OK    {filename:<45} {size:,} bytes"
        )

    else:

        print(
            f"INFO  {filename:<45} not present"
        )


# ============================================================
# KIVY / HARFBUZZ DEPENDENCIES
# ============================================================

print()
print("3. PYTHON DEPENDENCIES")
print("-" * 90)

for module_name in [
    "kivy",
    "uharfbuzz",
]:

    spec = importlib.util.find_spec(module_name)

    if spec:
        print(f"OK    {module_name}")
    else:
        print(f"FAIL  {module_name}")
        issue(f"Missing Python dependency: {module_name}")


# ============================================================
# CSV
# ============================================================

print()
print("4. GROUPED DICTIONARY CSV")
print("-" * 90)

rows = []

if os.path.exists(CSV_FILE):

    try:

        with open(
            CSV_FILE,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as f:

            rows = list(csv.DictReader(f))


        expected_columns = [
            "lookup_headword",
            "english_headword",
            "translation_count",
            "sindhi_translations",
            "translations_json",
        ]

        actual_columns = list(rows[0].keys()) if rows else []

        print(
            f"Rows:                    {len(rows):,}"
        )

        print(
            f"Columns:                 {len(actual_columns)}"
        )

        if actual_columns != expected_columns:

            issue(
                "Stage 14 CSV columns do not exactly match "
                "the expected structure."
            )

            print("FAIL  Column structure differs")

        else:

            print("OK    Column structure")


        # ----------------------------------------------------
        # Basic field validation
        # ----------------------------------------------------

        empty_lookup = 0
        empty_english = 0
        empty_sindhi = 0
        bad_counts = 0
        json_errors = 0
        json_count_mismatch = 0

        lookup_seen = set()

        translation_sum = 0

        for r in rows:

            lookup = r["lookup_headword"].strip()
            english = r["english_headword"].strip()
            sindhi = r["sindhi_translations"].strip()

            if not lookup:
                empty_lookup += 1

            if not english:
                empty_english += 1

            if not sindhi:
                empty_sindhi += 1

            lookup_seen.add(lookup.lower())

            try:
                count = int(r["translation_count"])
                translation_sum += count

            except Exception:
                bad_counts += 1
                continue


            try:

                data = json.loads(
                    r["translations_json"]
                )

                if not isinstance(data, list):
                    json_errors += 1

                elif len(data) != count:
                    json_count_mismatch += 1

            except Exception:
                json_errors += 1


        print(
            f"Unique lookup headwords: {len(lookup_seen):,}"
        )

        print(
            f"Translation records:     {translation_sum:,}"
        )

        print(
            f"Empty lookup fields:      {empty_lookup}"
        )

        print(
            f"Empty English fields:     {empty_english}"
        )

        print(
            f"Empty Sindhi fields:      {empty_sindhi}"
        )

        print(
            f"Bad translation counts:   {bad_counts}"
        )

        print(
            f"Bad translations JSON:    {json_errors}"
        )

        print(
            f"JSON count mismatches:    {json_count_mismatch}"
        )


        if empty_lookup:
            issue(f"CSV has {empty_lookup} empty lookup headwords.")

        if empty_english:
            issue(f"CSV has {empty_english} empty English headwords.")

        if empty_sindhi:
            issue(f"CSV has {empty_sindhi} empty Sindhi translations.")

        if bad_counts:
            issue(f"CSV has {bad_counts} invalid translation counts.")

        if json_errors:
            issue(f"CSV has {json_errors} invalid translations_json values.")

        if json_count_mismatch:
            issue(
                f"CSV has {json_count_mismatch} "
                "translations_json/count mismatches."
            )


    except Exception as e:

        issue(f"Could not read grouped CSV: {e}")

else:

    print("SKIPPED — file missing")


# ============================================================
# REVERSE INDEX
# ============================================================

print()
print("5. REVERSE INDEX CONSISTENCY")
print("-" * 90)

reverse_index = {}

if os.path.exists(INDEX_FILE):

    try:

        with open(
            INDEX_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            reverse_index = json.load(f)


        if not isinstance(reverse_index, dict):

            issue("Reverse index is not a JSON object.")

        else:

            print(
                f"Index terms:             {len(reverse_index):,}"
            )

            relationships = sum(
                len(v)
                for v in reverse_index.values()
                if isinstance(v, list)
            )

            print(
                f"Indexed relationships:   {relationships:,}"
            )


            # ------------------------------------------------
            # Verify every English result exists
            # ------------------------------------------------

            valid_english = {
                r["english_headword"].strip()
                for r in rows
            }

            dangling = []

            for term, english_list in reverse_index.items():

                if not isinstance(english_list, list):
                    issue(
                        f"Reverse index term '{term}' "
                        "does not contain a list."
                    )
                    continue

                for english in english_list:

                    if english not in valid_english:

                        dangling.append(
                            (term, english)
                        )


            print(
                f"Dangling English references: {len(dangling):,}"
            )

            if dangling:

                issue(
                    f"Reverse index contains "
                    f"{len(dangling)} dangling references."
                )


            # ------------------------------------------------
            # Rebuild expected relationships from CSV
            # ------------------------------------------------

            expected = defaultdict(set)

            for r in rows:

                english = r[
                    "english_headword"
                ].strip()

                sindhi = r[
                    "sindhi_translations"
                ].strip()

                for meaning in [
                    x.strip()
                    for x in sindhi.split("|")
                    if x.strip()
                ]:

                    # Complete meaning
                    expected[
                        meaning.lower()
                    ].add(english)

                    # Individual Sindhi tokens
                    words = re.findall(
                        r"[\u0600-\u06FF]+",
                        meaning
                    )

                    for word in words:

                        expected[
                            word.lower()
                        ].add(english)


            # ------------------------------------------------
            # Compare expected → actual
            # ------------------------------------------------

            missing_relationships = []

            for term, english_set in expected.items():

                actual_set = set(
                    reverse_index.get(
                        term,
                        []
                    )
                )

                missing = english_set - actual_set

                for english in missing:

                    missing_relationships.append(
                        (term, english)
                    )


            # Extra relationships are also worth checking

            extra_relationships = []

            for term, english_list in reverse_index.items():

                actual_set = set(english_list)

                expected_set = expected.get(
                    term,
                    set()
                )

                for english in actual_set - expected_set:

                    extra_relationships.append(
                        (term, english)
                    )


            print(
                f"Missing relationships:   "
                f"{len(missing_relationships):,}"
            )

            print(
                f"Extra relationships:     "
                f"{len(extra_relationships):,}"
            )


            if missing_relationships:

                issue(
                    "Reverse index is missing "
                    f"{len(missing_relationships):,} "
                    "relationships present in the dictionary."
                )

                print()
                print("First 20 missing relationships:")

                for term, english in missing_relationships[:20]:

                    print(
                        f"  {term} → {english}"
                    )


            if extra_relationships:

                warning(
                    "Reverse index contains "
                    f"{len(extra_relationships):,} "
                    "relationships not reconstructed from the "
                    "current grouped CSV."
                )


    except Exception as e:

        issue(
            f"Could not validate reverse index: {e}"
        )


# ============================================================
# FONT / HARFBUZZ
# ============================================================

print()
print("6. SINDHI FONT / HARFBUZZ")
print("-" * 90)

if os.path.exists(FONT_FILE):

    size = os.path.getsize(FONT_FILE)

    print(
        f"Font size:               {size:,} bytes"
    )

    if size < 100_000:
        warning(
            "Font file is unusually small."
        )

    try:

        import uharfbuzz as hb

        with open(
            FONT_FILE,
            "rb"
        ) as f:

            font_data = f.read()


        face = hb.Face(font_data)
        font = hb.Font(face)

        font.scale = (
            face.upem,
            face.upem
        )


        sample_words = [
            "ڪرڻ",
            "ڇڏي",
            "تياڳڻ، ترڪ ڪرڻ، ڇڏي ڏيڻ",
        ]


        for sample in sample_words:

            buf = hb.Buffer()

            buf.add_str(sample)

            buf.direction = "rtl"
            buf.script = "Arab"
            buf.language = "sd"

            hb.shape(
                font,
                buf
            )

            glyphs = buf.glyph_infos

            zero_glyphs = [
                g for g in glyphs
                if g.codepoint == 0
            ]

            print(
                f"{sample} | "
                f"characters={len(sample)} | "
                f"glyphs={len(glyphs)} | "
                f"missing_glyphs={len(zero_glyphs)}"
            )

            if zero_glyphs:

                issue(
                    f"Font has missing glyphs for sample: "
                    f"{sample}"
                )


    except Exception as e:

        issue(
            f"HarfBuzz/font test failed: {e}"
        )

else:

    issue(
        "Sindhi font file is missing."
    )


# ============================================================
# PYTHON SCRIPT SYNTAX
# ============================================================

print()
print("7. PYTHON SCRIPT SYNTAX")
print("-" * 90)

for filename in APP_FILES:

    if not os.path.exists(filename):
        continue

    try:

        source = open(
            filename,
            "r",
            encoding="utf-8"
        ).read()

        ast.parse(
            source,
            filename=filename
        )

        print(
            f"OK    {filename}"
        )

    except Exception as e:

        print(
            f"FAIL  {filename}: {e}"
        )

        issue(
            f"Syntax error in {filename}: {e}"
        )


# ============================================================
# STAGE 32 LIVE SEARCH CHECK
# ============================================================

print()
print("8. LIVE SEARCH / RTL CONFIGURATION")
print("-" * 90)

stage32 = "stage32_android_dictionary_live_search.py"

if os.path.exists(stage32):

    text = open(
        stage32,
        "r",
        encoding="utf-8"
    ).read()

    checks = {
        "live on_text search":
            "on_text: root.search_dictionary()" in text,

        "Arabic script setting":
            'font_script_name: "Arab"' in text,

        "RTL setting":
            'font_direction: "rtl"' in text,

        "separate ResultItem":
            "class ResultItem" in text,

        "Noto Arabic font":
            "NotoSansArabic-Regular.ttf" in text,

        "Sindhi pronunciation removed":
            "Speak Sindhi" not in text
            and "speak_sindhi" not in text,
    }

    for name, passed in checks.items():

        print(
            f"{'OK   ' if passed else 'FAIL '}"
            f"{name}"
        )

        if not passed:

            issue(
                f"Stage 32 check failed: {name}"
            )

else:

    warning(
        f"{stage32} is not present; "
        "Stage 31 can still be the current app."
    )


# ============================================================
# SQLITE DATABASE
# ============================================================

print()
print("9. ANDROID SQLITE DATABASE")
print("-" * 90)

if os.path.exists(DB_FILE):

    try:

        conn = sqlite3.connect(DB_FILE)

        cur = conn.cursor()

        dictionary_count = cur.execute(
            "SELECT COUNT(*) FROM dictionary"
        ).fetchone()[0]

        sindhi_count = cur.execute(
            "SELECT COUNT(*) FROM sindhi_index"
        ).fetchone()[0]

        print(
            f"Dictionary rows:         {dictionary_count:,}"
        )

        print(
            f"Sindhi index rows:       {sindhi_count:,}"
        )

        if rows and dictionary_count != len(rows):

            issue(
                "SQLite dictionary row count does not "
                "match Stage 14 grouped CSV."
            )

        metadata = dict(
            cur.execute(
                "SELECT key, value FROM metadata"
            ).fetchall()
        )

        print(
            f"Metadata version:        "
            f"{metadata.get('version', 'missing')}"
        )

        conn.close()

    except Exception as e:

        issue(
            f"SQLite database check failed: {e}"
        )

else:

    warning(
        "dictionary_stage22_android.db not found. "
        "It is not currently required by Stage 32."
    )


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 90)
print("FINAL HEALTH CHECK")
print("=" * 90)

if not issues:

    print("PASS — no blocking structural problems found.")

else:

    print(
        f"FAIL — {len(issues):,} issue(s) found."
    )

    print()
    print("BLOCKING ISSUES:")

    for item in issues:

        print(
            f"  ❌ {item}"
        )


if warnings:

    print()
    print(
        f"WARNINGS: {len(warnings):,}"
    )

    for item in warnings:

        print(
            f"  ⚠ {item}"
        )


print()
print("No dictionary source files were modified.")
print("=" * 90)
