import csv
import json
import re
import tkinter as tk
from tkinter import ttk
import subprocess
import threading

DICTIONARY_FILE = "dictionary_stage14_grouped.csv"
INDEX_FILE = "dictionary_stage18_reverse_index.json"


# ============================================================
# LOAD DICTIONARY
# ============================================================

with open(DICTIONARY_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))


# ============================================================
# ENGLISH INDEX
# ============================================================

english_index = {}

for row in rows:
    key = row.get("lookup_headword", "").strip().lower()

    if key:
        english_index[key] = row


# ============================================================
# LOAD REVERSE INDEX
# ============================================================

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    reverse_index = json.load(f)


# ============================================================
# ENGLISH → ROW
# ============================================================

row_by_english = {}

for row in rows:
    english = row.get("english_headword", "").strip()

    if english:
        row_by_english[english] = row


# ============================================================
# SINDHI NORMALIZATION
# ============================================================

def normalize_sindhi(text):

    text = text.strip().lower()

    replacements = {
        "ي": "ی",
        "ى": "ی",
        "ك": "ڪ",
        "ۀ": "ه",
        "ة": "ه",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(
        r"[\u0610-\u061A\u064B-\u065F\u0670]",
        "",
        text
    )

    return text


# ============================================================
# WINDOWS SPEECH
# ============================================================

def speak_text(text, language="en"):

    text = text.strip()

    if not text:
        return

    def worker():

        try:

            if language == "en":

                voice_script = f'''
Add-Type -AssemblyName System.Speech
$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speak.SelectVoiceByHints(
    [System.Speech.Synthesis.VoiceGender]::NotSet,
    [System.Speech.Synthesis.VoiceAge]::NotSet,
    0,
    [System.Globalization.CultureInfo]::GetCultureInfo("en-US")
)
$speak.Speak({text!r})
'''

            else:

                voice_script = f'''
Add-Type -AssemblyName System.Speech
$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speak.Speak({text!r})
'''

            subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    voice_script
                ],
                creationflags=subprocess.CREATE_NO_WINDOW
            )

        except Exception as e:

            root.after(
                0,
                lambda: status_var.set(
                    f"Speech error: {e}"
                )
            )

    threading.Thread(
        target=worker,
        daemon=True
    ).start()


# ============================================================
# SPEAK SELECTED
# ============================================================

def speak_selected():

    try:
        selected = result_box.get(
            tk.SEL_FIRST,
            tk.SEL_LAST
        ).strip()

    except tk.TclError:

        status_var.set(
            "Select some text first."
        )

        return

    if not selected:

        status_var.set(
            "Select some text first."
        )

        return

    speak_text(
        selected,
        "en"
    )

    status_var.set(
        "Speaking selected text..."
    )


# ============================================================
# SEARCH ENGLISH
# ============================================================

def search_english(query):

    if query in english_index:
        return [english_index[query]]

    prefix_results = []

    for key, row in english_index.items():

        if key.startswith(query):
            prefix_results.append(row)

    contains_results = []

    for key, row in english_index.items():

        if query in key and not key.startswith(query):
            contains_results.append(row)

    return prefix_results + contains_results


# ============================================================
# SEARCH SINDHI
# ============================================================

def search_sindhi(query):

    normalized_query = normalize_sindhi(query)

    exact_results = []
    seen = set()

    possible_keys = []

    if query in reverse_index:
        possible_keys.append(query)

    if normalized_query in reverse_index:
        if normalized_query not in possible_keys:
            possible_keys.append(normalized_query)

    for key in possible_keys:

        for english in reverse_index[key]:

            if english in seen:
                continue

            row = row_by_english.get(english)

            if row:

                seen.add(english)
                exact_results.append(row)

    if exact_results:
        return exact_results


    candidates = []
    seen = set()

    for key in reverse_index:

        normalized_key = normalize_sindhi(key)

        if normalized_query in normalized_key:

            for english in reverse_index[key]:

                if english in seen:
                    continue

                row = row_by_english.get(english)

                if row:

                    seen.add(english)
                    candidates.append(row)

    return candidates


# ============================================================
# DISPLAY ENGLISH RESULTS
# ============================================================

def display_english_results(results):

    for row in results[:50]:

        english = row.get(
            "english_headword",
            ""
        ).strip()

        sindhi = row.get(
            "sindhi_translations",
            ""
        ).strip()

        result_box.insert(
            tk.END,
            english + "\n",
            "word"
        )

        meanings = [
            x.strip()
            for x in sindhi.split("|")
            if x.strip()
        ]

        for meaning in meanings:

            result_box.insert(
                tk.END,
                "• " + meaning + "\n",
                "meaning"
            )

        result_box.insert(
            tk.END,
            "\n"
        )

    if len(results) > 50:

        result_box.insert(
            tk.END,
            f"... and {len(results) - 50} more matches.",
            "more"
        )


# ============================================================
# DISPLAY SINDHI RESULTS
# ============================================================

def display_sindhi_results(results):

    for row in results[:50]:

        english = row.get(
            "english_headword",
            ""
        ).strip()

        sindhi = row.get(
            "sindhi_translations",
            ""
        ).strip()

        result_box.insert(
            tk.END,
            english + "\n",
            "word"
        )

        result_box.insert(
            tk.END,
            "Sindhi: ",
            "label"
        )

        result_box.insert(
            tk.END,
            sindhi + "\n\n",
            "meaning"
        )

    if len(results) > 50:

        result_box.insert(
            tk.END,
            f"... and {len(results) - 50} more matches.",
            "more"
        )


# ============================================================
# SEARCH
# ============================================================

def search_dictionary(*args):

    query = search_var.get().strip()

    result_box.delete(
        "1.0",
        tk.END
    )

    if not query:

        status_var.set(
            f"{len(rows):,} translation records • "
            f"{len(english_index):,} lookup headwords"
        )

        return


    mode = search_mode.get()


    if mode == "English → Sindhi":

        results = search_english(
            query.lower()
        )

        if not results:

            result_box.insert(
                tk.END,
                "No matching English word found.",
                "not_found"
            )

            status_var.set(
                "No results"
            )

            return

        display_english_results(
            results
        )

        status_var.set(
            f"{len(results):,} English matches"
        )


    else:

        results = search_sindhi(
            query
        )

        if not results:

            result_box.insert(
                tk.END,
                "No matching Sindhi entry found.",
                "not_found"
            )

            status_var.set(
                "No results"
            )

            return

        display_sindhi_results(
            results
        )

        status_var.set(
            f"{len(results):,} Sindhi matches"
        )


# ============================================================
# CLEAR
# ============================================================

def clear_search():

    search_var.set("")

    result_box.delete(
        "1.0",
        tk.END
    )

    status_var.set(
        f"{len(rows):,} translation records • "
        f"{len(english_index):,} lookup headwords"
    )

    search_entry.focus()


# ============================================================
# SPEAK CURRENT ENGLISH QUERY
# ============================================================

def speak_english_query():

    text = search_var.get().strip()

    if not text:
        status_var.set(
            "Enter an English word first."
        )
        return

    speak_text(
        text,
        "en"
    )

    status_var.set(
        "Speaking English..."
    )


# ============================================================
# SPEAK CURRENT SINDHI QUERY
# ============================================================

def speak_sindhi_query():

    text = search_var.get().strip()

    if not text:
        status_var.set(
            "Enter Sindhi text first."
        )
        return

    speak_text(
        text,
        "sd"
    )

    status_var.set(
        "Speaking Sindhi..."
    )


# ============================================================
# WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "English ↔ Sindhi Dictionary — Stage 21"
)

root.geometry(
    "1100x800"
)

root.minsize(
    850,
    650
)


# ============================================================
# TITLE
# ============================================================

title = ttk.Label(
    root,
    text="English ↔ Sindhi Dictionary",
    font=("Segoe UI", 25, "bold")
)

title.pack(
    pady=(20, 5)
)


subtitle = ttk.Label(
    root,
    text=(
        "21,726 translation records • "
        "21,419 lookup headwords • "
        "41,067 Sindhi index terms"
    ),
    font=("Segoe UI", 10)
)

subtitle.pack(
    pady=(0, 20)
)


# ============================================================
# MODE
# ============================================================

mode_frame = ttk.Frame(root)

mode_frame.pack(
    fill="x",
    padx=30
)


ttk.Label(
    mode_frame,
    text="Search direction:",
    font=("Segoe UI", 11, "bold")
).pack(
    side="left"
)


search_mode = tk.StringVar(
    value="English → Sindhi"
)


mode_box = ttk.Combobox(
    mode_frame,
    textvariable=search_mode,
    values=[
        "English → Sindhi",
        "Sindhi → English"
    ],
    state="readonly",
    width=22
)

mode_box.pack(
    side="left",
    padx=10
)

mode_box.bind(
    "<<ComboboxSelected>>",
    search_dictionary
)


# ============================================================
# SEARCH
# ============================================================

search_frame = ttk.Frame(root)

search_frame.pack(
    fill="x",
    padx=30,
    pady=15
)


search_var = tk.StringVar()


search_entry = ttk.Entry(
    search_frame,
    textvariable=search_var,
    font=("Segoe UI", 17)
)

search_entry.pack(
    side="left",
    fill="x",
    expand=True
)


ttk.Button(
    search_frame,
    text="Search",
    command=search_dictionary
).pack(
    side="left",
    padx=(10, 5)
)


ttk.Button(
    search_frame,
    text="Clear",
    command=clear_search
).pack(
    side="left"
)


# ============================================================
# SPEECH BUTTONS
# ============================================================

speech_frame = ttk.Frame(root)

speech_frame.pack(
    fill="x",
    padx=30,
    pady=(0, 10)
)


ttk.Button(
    speech_frame,
    text="🔊 Speak English",
    command=speak_english_query
).pack(
    side="left",
    padx=(0, 5)
)


ttk.Button(
    speech_frame,
    text="🔊 Speak Sindhi",
    command=speak_sindhi_query
).pack(
    side="left",
    padx=5
)


ttk.Button(
    speech_frame,
    text="🔊 Speak Selected",
    command=speak_selected
).pack(
    side="left",
    padx=5
)


# ============================================================
# LIVE SEARCH
# ============================================================

search_var.trace_add(
    "write",
    search_dictionary
)


# ============================================================
# RESULTS
# ============================================================

result_frame = ttk.Frame(root)

result_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=(5, 10)
)


scrollbar = ttk.Scrollbar(
    result_frame
)

scrollbar.pack(
    side="right",
    fill="y"
)


result_box = tk.Text(
    result_frame,
    wrap="word",
    font=("Segoe UI", 14),
    yscrollcommand=scrollbar.set,
    padx=20,
    pady=20
)

result_box.pack(
    fill="both",
    expand=True
)


scrollbar.config(
    command=result_box.yview
)


# ============================================================
# FORMATTING
# ============================================================

result_box.tag_configure(
    "word",
    font=("Segoe UI", 18, "bold")
)

result_box.tag_configure(
    "meaning",
    font=("Segoe UI", 14)
)

result_box.tag_configure(
    "label",
    font=("Segoe UI", 12, "bold")
)

result_box.tag_configure(
    "not_found",
    font=("Segoe UI", 14)
)

result_box.tag_configure(
    "more",
    font=("Segoe UI", 11)
)


# ============================================================
# STATUS
# ============================================================

status_var = tk.StringVar(
    value=(
        f"{len(rows):,} translation records • "
        f"{len(english_index):,} lookup headwords"
    )
)


status = ttk.Label(
    root,
    textvariable=status_var,
    anchor="w",
    font=("Segoe UI", 10)
)

status.pack(
    fill="x",
    padx=30,
    pady=(0, 12)
)


# ============================================================
# KEYBOARD SHORTCUTS
# ============================================================

root.bind(
    "<Control-l>",
    lambda event: clear_search()
)

root.bind(
    "<Escape>",
    lambda event: clear_search()
)

root.bind(
    "<Return>",
    lambda event: search_dictionary()
)


# ============================================================
# START
# ============================================================

search_entry.focus()

root.mainloop()

