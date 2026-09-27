import csv
import json
import re
import tkinter as tk
from tkinter import ttk

DICTIONARY_FILE = "dictionary_stage14_grouped.csv"
INDEX_FILE = "dictionary_stage18_reverse_index.json"


# ============================================================
# LOAD DICTIONARY
# ============================================================

with open(DICTIONARY_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))


# ============================================================
# BUILD ENGLISH LOOKUP
# ============================================================

english_index = {}

for row in rows:
    key = row.get("lookup_headword", "").strip().lower()

    if key:
        english_index[key] = row


# ============================================================
# LOAD SINDHI REVERSE INDEX
# ============================================================

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    reverse_index = json.load(f)


# ============================================================
# BUILD ID → ROW LOOKUP
#
# Stage 18 stores English headwords as IDs.
# We therefore map the English headword back to its row.
# ============================================================

row_by_english = {}

for row in rows:
    english = row.get("english_headword", "").strip()

    if english:
        row_by_english[english] = row


# ============================================================
# SEARCH
# ============================================================

def search_dictionary(*args):

    query = search_var.get().strip().lower()

    result_box.delete("1.0", tk.END)

    if not query:
        status_var.set(
            f"{len(rows):,} translation records • "
            f"{len(english_index):,} lookup headwords"
        )
        return

    mode = search_mode.get()


    # ========================================================
    # ENGLISH → SINDHI
    # ========================================================

    if mode == "English → Sindhi":

        # Exact match first
        if query in english_index:
            results = [english_index[query]]

        else:
            # Partial English search
            results = [
                row
                for key, row in english_index.items()
                if query in key
            ]


        if not results:

            result_box.insert(
                tk.END,
                "No matching English word found.",
                "not_found"
            )

            status_var.set("No results")
            return


        for row in results[:50]:

            english = row.get(
                "english_headword", ""
            ).strip()

            sindhi = row.get(
                "sindhi_translations", ""
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


        status_var.set(
            f"{len(results):,} English matches"
        )


    # ========================================================
    # SINDHI → ENGLISH
    # ========================================================

    else:

        # ----------------------------------------------------
        # EXACT SINDHI INDEX LOOKUP
        # ----------------------------------------------------

        indexed_headwords = reverse_index.get(query, [])


        # ----------------------------------------------------
        # IF EXACT INDEX MATCH EXISTS
        # ----------------------------------------------------

        if indexed_headwords:

            english_results = []

            for english in indexed_headwords:

                row = row_by_english.get(english)

                if row:
                    english_results.append(row)


        # ----------------------------------------------------
        # OTHERWISE PARTIAL SEARCH THROUGH INDEX KEYS
        # ----------------------------------------------------

        else:

            matching_keys = [
                key
                for key in reverse_index
                if query in key
            ]

            english_names = []

            for key in matching_keys:

                for english in reverse_index[key]:

                    if english not in english_names:
                        english_names.append(english)


            english_results = [
                row_by_english[english]
                for english in english_names
                if english in row_by_english
            ]


        # ----------------------------------------------------
        # NO RESULTS
        # ----------------------------------------------------

        if not english_results:

            result_box.insert(
                tk.END,
                "No matching Sindhi entry found.",
                "not_found"
            )

            status_var.set("No results")
            return


        # ----------------------------------------------------
        # DISPLAY
        # ----------------------------------------------------

        for row in english_results[:50]:

            english = row.get(
                "english_headword", ""
            ).strip()

            sindhi = row.get(
                "sindhi_translations", ""
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


        if len(english_results) > 50:

            result_box.insert(
                tk.END,
                f"... and {len(english_results) - 50} more matches.",
                "more"
            )


        status_var.set(
            f"{len(english_results):,} Sindhi matches"
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
# WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "English ↔ Sindhi Dictionary — Stage 19"
)

root.geometry(
    "1000x720"
)

root.minsize(
    750,
    550
)


# ============================================================
# TITLE
# ============================================================

title = ttk.Label(
    root,
    text="English ↔ Sindhi Dictionary",
    font=("Segoe UI", 24, "bold")
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
# SEARCH MODE
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
# SEARCH BAR
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


search_button = ttk.Button(
    search_frame,
    text="Search",
    command=search_dictionary
)

search_button.pack(
    side="left",
    padx=(10, 5)
)


clear_button = ttk.Button(
    search_frame,
    text="Clear",
    command=clear_search
)

clear_button.pack(
    side="left"
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
    padx=18,
    pady=18
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
    "<Return>",
    lambda event: search_dictionary()
)


# ============================================================
# START
# ============================================================

search_entry.focus()

root.mainloop()

