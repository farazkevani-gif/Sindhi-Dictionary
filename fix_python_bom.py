from pathlib import Path

files = [
    "stage23_android_dictionary.py",
    "stage30_android_dictionary.py",
    "stage31_android_dictionary.py",
    "stage32_android_dictionary_live_search.py",
]

for name in files:
    path = Path(name)

    if not path.exists():
        print(f"SKIP  {name}")
        continue

    # Read UTF-8 with optional BOM removed
    text = path.read_text(encoding="utf-8-sig")

    # Write standard UTF-8 without BOM
    path.write_text(text, encoding="utf-8")

    print(f"FIXED {name}")

print()
print("UTF-8 BOM cleanup complete.")
