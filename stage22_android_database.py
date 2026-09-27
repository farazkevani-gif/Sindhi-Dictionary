import csv
import sqlite3
import os

INPUT_FILE = "dictionary_stage14_grouped.csv"
OUTPUT_FILE = "dictionary_stage22_android.db"


# ============================================================
# REMOVE OLD DATABASE
# ============================================================

if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)


# ============================================================
# LOAD SOURCE
# ============================================================

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8-sig",
    newline=""
) as f:

    rows = list(csv.DictReader(f))


# ============================================================
# CREATE DATABASE
# ============================================================

conn = sqlite3.connect(OUTPUT_FILE)

cursor = conn.cursor()


# ============================================================
# MAIN DICTIONARY TABLE
# ============================================================

cursor.execute("""
CREATE TABLE dictionary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lookup_headword TEXT NOT NULL,
    english_headword TEXT NOT NULL,
    translation_count INTEGER NOT NULL,
    sindhi_translations TEXT NOT NULL,
    translations_json TEXT
)
""")


# ============================================================
# INSERT DATA
# ============================================================

insert_sql = """
INSERT INTO dictionary (
    lookup_headword,
    english_headword,
    translation_count,
    sindhi_translations,
    translations_json
)
VALUES (?, ?, ?, ?, ?)
"""


for row in rows:

    cursor.execute(
        insert_sql,
        (
            row.get("lookup_headword", "").strip(),
            row.get("english_headword", "").strip(),
            int(row.get("translation_count", "0") or 0),
            row.get("sindhi_translations", "").strip(),
            row.get("translations_json", "").strip()
        )
    )


# ============================================================
# ENGLISH INDEX
# ============================================================

cursor.execute("""
CREATE INDEX idx_lookup_headword
ON dictionary(lookup_headword)
""")


# ============================================================
# ENGLISH HEADWORD INDEX
# ============================================================

cursor.execute("""
CREATE INDEX idx_english_headword
ON dictionary(english_headword)
""")


# ============================================================
# SINDHI SEARCH TABLE
# ============================================================

cursor.execute("""
CREATE TABLE sindhi_index (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dictionary_id INTEGER NOT NULL,
    sindhi_term TEXT NOT NULL,
    FOREIGN KEY(dictionary_id)
        REFERENCES dictionary(id)
)
""")


# ============================================================
# BUILD SINDHI INDEX
# ============================================================

import re

sindhi_records = 0


for dictionary_id, row in enumerate(rows, 1):

    sindhi = row.get(
        "sindhi_translations",
        ""
    ).strip()

    if not sindhi:
        continue


    meanings = [
        x.strip()
        for x in sindhi.split("|")
        if x.strip()
    ]


    for meaning in meanings:

        words = re.findall(
            r"[\u0600-\u06FF]+",
            meaning
        )

        for word in words:

            word = word.strip()

            if not word:
                continue

            cursor.execute(
                """
                INSERT INTO sindhi_index (
                    dictionary_id,
                    sindhi_term
                )
                VALUES (?, ?)
                """,
                (
                    dictionary_id,
                    word
                )
            )

            sindhi_records += 1


# ============================================================
# SINDHI INDEX
# ============================================================

cursor.execute("""
CREATE INDEX idx_sindhi_term
ON sindhi_index(sindhi_term)
""")


# ============================================================
# DATABASE METADATA
# ============================================================

cursor.execute("""
CREATE TABLE metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
)
""")


metadata = {
    "dictionary_name":
        "English ↔ Sindhi Dictionary",

    "source_file":
        INPUT_FILE,

    "translation_records":
        str(len(rows)),

    "lookup_headwords":
        str(len(rows)),

    "version":
        "Stage 22",

    "android_ready":
        "yes"
}


for key, value in metadata.items():

    cursor.execute(
        """
        INSERT INTO metadata(key, value)
        VALUES (?, ?)
        """,
        (key, value)
    )


# ============================================================
# COMMIT
# ============================================================

conn.commit()


# ============================================================
# VERIFY
# ============================================================

dictionary_count = cursor.execute(
    "SELECT COUNT(*) FROM dictionary"
).fetchone()[0]

sindhi_count = cursor.execute(
    "SELECT COUNT(*) FROM sindhi_index"
).fetchone()[0]

english_count = cursor.execute(
    "SELECT COUNT(*) FROM dictionary WHERE english_headword != ''"
).fetchone()[0]


# Test English

test_abandon = cursor.execute(
    """
    SELECT english_headword, sindhi_translations
    FROM dictionary
    WHERE lookup_headword = ?
    """,
    ("abandon",)
).fetchall()


# Test Sindhi

test_sindhi = cursor.execute(
    """
    SELECT DISTINCT d.english_headword
    FROM dictionary d
    JOIN sindhi_index s
        ON d.id = s.dictionary_id
    WHERE s.sindhi_term = ?
    LIMIT 20
    """,
    ("تياڳڻ",)
).fetchall()


conn.close()


# ============================================================
# REPORT
# ============================================================

size_kb = os.path.getsize(
    OUTPUT_FILE
) / 1024


print("=" * 80)
print("STAGE 22 — ANDROID SQLITE DATABASE")
print("=" * 80)

print(
    f"SOURCE CSV ROWS:              {len(rows):,}"
)

print(
    f"DATABASE DICTIONARY ROWS:     {dictionary_count:,}"
)

print(
    f"ENGLISH HEADWORDS:            {english_count:,}"
)

print(
    f"SINDHI INDEX RECORDS:         {sindhi_count:,}"
)

print(
    f"DATABASE SIZE:                {size_kb:,.1f} KB"
)

print()
print("ENGLISH TEST — abandon")

for result in test_abandon:
    print(
        " →",
        result[0],
        "|",
        result[1]
    )

print()
print("SINDHI TEST — تياڳڻ")

for result in test_sindhi:
    print(
        " →",
        result[0]
    )

print()
print(
    f"Android database:             {OUTPUT_FILE}"
)

print()
print("SOURCE CSV MODIFIED:          NO")
print("TRANSLATIONS DELETED:         NO")
print("=" * 80)

