import csv
import tkinter as tk
from tkinter import ttk

INPUT_FILE = "dictionary_stage14_grouped.csv"

# ============================================================
# LOAD DICTIONARY
# ============================================================

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))


# ============================================================
# BUILD INDEXES
# ============================================================

english_index = {}
sindhi_index = {}

for r in rows:

    english = r.get("lookup_headword", "").strip().lower()

    sindhi = r.get("sindhi_translations", "").strip().lower()

    if english:
        english_index.setdefault(english, []).append(r)

    if sindhi:
        for meaning in sindhi.split("|"):
            meaning = meaning.strip()

            if meaning:
                sindhi_index.setdefault(meaning, []).append(r)


# ============================================================
# SEARCH
# ============================================================

def search_dictionary(*args):

    query = search_var.get().strip().lower()

    result_box.delete("1.0", tk.END)

    if not query:
        status_var.set(
            f"{len(rows):,} translation records • "
            f"{len(english_index):,} English lookup headwords"
        )
        return

    mode = search_mode.get()

    # ========================================================
    # ENGLISH → SINDHI
    # ========================================================

    if mode == "English → Sindhi":

        # Exact indexed search
        results = english_index.get(query, [])

        # Partial search only if exact search fails
        if not results:
            results = [
                r for key in english_index
                if query in key
                for r in english_index[key]
            ]

        if not results:
            result_box.insert(
                tk.END,
                "No matching English word found."
            )

            status_var.set("No results")
            return

        shown = set()

        for r in results:

            dictionary_id = r.get("dictionary_id", "")

            if dictionary_id in shown:
                continue

            shown.add(dictionary_id)

            english = r.get(
                "english_headword", ""
            ).strip()

            meanings = [
                x.strip()
                for x in r.get(
                    "sindhi_translations", ""
                ).split("|")
                if x.strip()
            ]

            result_box.insert(
                tk.END,
                english + "\n",
                "word"
            )

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

            if len(shown) >= 50:
                break

        status_var.set(
            f"{len(results):,} English matches"
        )

        if len(results) > 50:

            result_box.insert(
                tk.END,
                f"... and {len(results) - 50} more matches."
            )

    # ========================================================
    # SINDHI → ENGLISH
    # ========================================================

    else:

        # Exact Sindhi meaning search
        results = []

        for key, indexed_rows in sindhi_index.items():

            if query == key:

                results.extend(indexed_rows)

        # Partial Sindhi search
        if not results:

            for key, indexed_rows in sindhi_index.items():

                if query in key:

                    results.extend(indexed_rows)

        if not results:

            result_box.insert(
                tk.END,
                "No matching Sindhi entry found."
            )

            status_var.set("No results")
            return

        shown = set()

        for r in results:

            dictionary_id = r.get(
                "dictionary_id",
                ""
            )

            if dictionary_id in shown:
                continue

            shown.add(dictionary_id)

            english = r.get(
                "english_headword",
                ""
            ).strip()

            meanings = [
                x.strip()
                for x in r.get(
                    "sindhi_translations",
                    ""
                ).split("|")
                if x.strip()
            ]

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
                " | ".join(meanings) + "\n\n",
                "meaning"
            )

            if len(shown) >= 50:
                break

        status_var.set(
            f"{len(results):,} Sindhi matches"
        )

        if len(results) > 50:

            result_box.insert(
                tk.END,
                f"... and {len(results) - 50} more matches."
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
        f"{len(english_index):,} English lookup headwords"
    )

    search_entry.focus()


# ============================================================
# WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "English ↔ Sindhi Dictionary"
)

root.geometry(
    "950x700"
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
        f"{len(rows):,} translation records • "
        f"{len(english_index):,} lookup headwords"
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
    font=("Segoe UI", 17, "bold")
)

result_box.tag_configure(
    "meaning",
    font=("Segoe UI", 14)
)

result_box.tag_configure(
    "label",
    font=("Segoe UI", 12, "bold")
)


# ============================================================
# STATUS
# ============================================================

status_var = tk.StringVar(
    value=(
        f"{len(rows):,} translation records • "
        f"{len(english_index):,} English lookup headwords"
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
# KEYBOARD
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

