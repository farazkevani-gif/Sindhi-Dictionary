from pathlib import Path

path = Path(".\stage23_android_dictionary.py")
text = path.read_text(encoding="utf-8")

# Force English text to use LTR direction.
text = text.replace(
    'output.append(\n                f"[b]{english}[/b]"\n            )',
    'output.append(\n                f"[b]\\u200e{english}\\u200e[/b]"\n            )'
)

path.write_text(text, encoding="utf-8")

print("Stage 29 English LTR fix applied.")
