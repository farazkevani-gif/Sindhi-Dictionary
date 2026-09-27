from pathlib import Path

RECIPE = Path(
    "/home/faraz_baloch/sindhi_dictionary_android_stage34/"
    ".buildozer/android/platform/python-for-android/"
    "pythonforandroid/recipes/sdl2_image/__init__.py"
)

text = RECIPE.read_text(encoding="utf-8")

marker = "Skipping disabled SDL_image dependency"

if marker in text:
    print("PATCH ALREADY PRESENT")
    raise SystemExit(0)

needle = '                line_split = section.split(" = ")' + "\n"

replacement = '''                line_split = section.split(" = ")
                clone_rel_path = line_split[1].split("\\n")[0].strip()

                if clone_rel_path in {
                    "external/libjxl",
                    "external/libavif",
                    "external/dav1d",
                    "external/libwebp",
                }:
                    print(
                        f"Skipping disabled SDL_image dependency: "
                        f"{clone_rel_path}"
                    )
                    continue
'''

if needle not in text:
    raise SystemExit("PATCH ABORTED: expected insertion point not found.")

text = text.replace(needle, replacement, 1)

RECIPE.write_text(text, encoding="utf-8")

print("PATCH SUCCESSFUL")
print(RECIPE)
