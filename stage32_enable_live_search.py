from pathlib import Path

path = Path(".\stage32_android_dictionary_live_search.py")

text = Path(".\stage31_android_dictionary.py").read_text(encoding="utf-8")

text = text.replace(
    'on_text_validate: root.search_dictionary()',
    'on_text: root.search_dictionary()\n            on_text_validate: root.search_dictionary()'
)

path.write_text(text, encoding="utf-8")

print("LIVE SEARCH ENABLED")
print("File:", path)
