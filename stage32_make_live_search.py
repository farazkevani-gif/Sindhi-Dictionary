from pathlib import Path

source = Path(".\stage31_android_dictionary.py")
target = Path(".\stage32_android_dictionary_live_search.py")

text = source.read_text(encoding="utf-8")

old = '''        TextInput:
            id: search_input
            hint_text: "Search English word..."
            multiline: False
            font_size: "18sp"
            on_text_validate: root.search_dictionary()
'''

new = '''        TextInput:
            id: search_input
            hint_text: "Search English word..."
            multiline: False
            font_size: "18sp"
            on_text: root.search_dictionary()
'''

if old not in text:
    raise SystemExit("Could not find the search input section.")

text = text.replace(old, new)

target.write_text(text, encoding="utf-8")

print("Stage 32 created:")
print(target)
