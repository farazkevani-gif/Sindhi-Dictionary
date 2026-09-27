import csv
import tkinter as tk
from tkinter import ttk

INPUT_FILE = "dictionary_stage14_grouped.csv"

# Load dictionary
with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

# ------------------------------------------------------------
# SEARCH
# ------------------------------------------------------------

def search_dictionary(*args):
    query = search_var.get().strip().lower()

    result_box.delete("1.0", tk.END)

    if not query:
        return

    exact = [
        r for r in rows
        if r.get("lookup_headword", "").lower() == query
    ]

    if exact:
        results = exact
    else:
        results = [
            r for r in rows
            if query in r.get("lookup_headword", "").lower()
        ]

    if not results:
        result_box.insert(tk.END, "No matching English word found.")
        return

    for r in results[:50]:
        english = r.get("english_headword", "").strip()
        sindhi = r.get("sindhi_translations", "").strip()

        result_box.insert(tk.END, english + "\n", "word")
        result_box.insert(tk.END, sindhi + "\n\n", "meaning")

    if len(results) > 50:
        result_box.insert(
            tk.END,
            f"... {len(results) - 50} additional matches not shown.\n"
        )


# ------------------------------------------------------------
# WINDOW
# ------------------------------------------------------------

root = tk.Tk()
root.title("English → Sindhi Dictionary")
root.geometry("900x650")
root.minsize(700, 500)

# Title
title = ttk.Label(
    root,
    text="English → Sindhi Dictionary",
    font=("Segoe UI", 22, "bold")
)
title.pack(pady=(20, 10))

# Statistics
stats = ttk.Label(
    root,
    text=f"{len(rows):,} translation records",
    font=("Segoe UI", 10)
)
stats.pack(pady=(0, 15))

# Search frame
search_frame = ttk.Frame(root)
search_frame.pack(fill="x", padx=30)

search_var = tk.StringVar()

search_entry = ttk.Entry(
    search_frame,
    textvariable=search_var,
    font=("Segoe UI", 16)
)
search_entry.pack(side="left", fill="x", expand=True)

search_button = ttk.Button(
    search_frame,
    text="Search",
    command=search_dictionary
)
search_button.pack(side="left", padx=(10, 0))

# Search whenever text changes
search_var.trace_add("write", search_dictionary)

# Results frame
result_frame = ttk.Frame(root)
result_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=20
)

scrollbar = ttk.Scrollbar(result_frame)
scrollbar.pack(side="right", fill="y")

result_box = tk.Text(
    result_frame,
    wrap="word",
    font=("Segoe UI", 14),
    yscrollcommand=scrollbar.set,
    padx=15,
    pady=15
)

result_box.pack(fill="both", expand=True)

scrollbar.config(command=result_box.yview)

# Text formatting
result_box.tag_configure(
    "word",
    font=("Segoe UI", 16, "bold")
)

result_box.tag_configure(
    "meaning",
    font=("Segoe UI", 14)
)

# Start with search box focused
search_entry.focus()

root.mainloop()
