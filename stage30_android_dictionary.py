import csv
import json
import os

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout


# ============================================================
# FILES
# ============================================================

DICTIONARY_FILE = "dictionary_stage14_grouped.csv"
REVERSE_INDEX_FILE = "dictionary_stage18_reverse_index.json"
SINDHI_FONT = "fonts/NotoSansArabic-Regular.ttf"


# ============================================================
# KV LAYOUT
# ============================================================

KV = r'''
#:import dp kivy.metrics.dp

<DictionaryRoot>:

    orientation: "vertical"
    padding: dp(16)
    spacing: dp(10)

    Label:
        text: "English ↔ Sindhi Dictionary"
        font_size: "25sp"
        bold: True
        size_hint_y: None
        height: dp(55)

    Label:
        text: "21,419 lookup headwords"
        font_size: "13sp"
        size_hint_y: None
        height: dp(25)

    Spinner:
        id: search_mode
        text: "English → Sindhi"
        values: ["English → Sindhi", "Sindhi → English"]
        size_hint_y: None
        height: dp(48)
        font_size: "16sp"
        on_text: root.change_mode(self.text)

    BoxLayout:
        size_hint_y: None
        height: dp(52)
        spacing: dp(8)

        TextInput:
            id: search_input
            hint_text: "Search English word..."
            multiline: False
            font_size: "18sp"
            on_text_validate: root.search_dictionary()

        Button:
            text: "Search"
            size_hint_x: None
            width: dp(100)
            on_release: root.search_dictionary()

    ScrollView:

        Label:
            id: results
            text: root.result_text
            markup: True
            font_size: "18sp"
            font_name: root.sindhi_font
            font_script_name: "Arab"
            font_direction: "rtl"
            text_size: self.width, None
            halign: "right"
            valign: "top"
            size_hint_y: None
            height: self.texture_size[1] + dp(30)
            padding: dp(10), dp(10)

    Label:
        id: status
        text: root.status_text
        font_size: "13sp"
        size_hint_y: None
        height: dp(30)
'''


# ============================================================
# ROOT
# ============================================================

class DictionaryRoot(BoxLayout):

    result_text = StringProperty("")
    status_text = StringProperty("Loading dictionary...")
    sindhi_font = StringProperty(SINDHI_FONT)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.rows = []
        self.reverse_index = {}

        self.load_dictionary()


    # ========================================================
    # LOAD
    # ========================================================

    def load_dictionary(self):

        try:

            with open(
                DICTIONARY_FILE,
                "r",
                encoding="utf-8-sig",
                newline=""
            ) as f:

                self.rows = list(csv.DictReader(f))


            if os.path.exists(REVERSE_INDEX_FILE):

                with open(
                    REVERSE_INDEX_FILE,
                    "r",
                    encoding="utf-8"
                ) as f:

                    self.reverse_index = json.load(f)


            self.status_text = (
                f"{len(self.rows):,} dictionary headwords loaded"
            )


        except Exception as e:

            self.status_text = f"Database error: {e}"


    # ========================================================
    # MODE
    # ========================================================

    def change_mode(self, mode):

        if mode == "English → Sindhi":

            self.ids.search_input.hint_text = (
                "Search English word..."
            )

        else:

            self.ids.search_input.hint_text = (
                "سنڌي لفظ ڳوليو..."
            )

        self.search_dictionary()


    # ========================================================
    # ENGLISH SEARCH
    # ========================================================

    def search_english(self, query):

        exact = [
            r for r in self.rows
            if r.get(
                "lookup_headword",
                ""
            ).lower() == query
        ]

        if exact:
            return exact


        return [
            r for r in self.rows
            if query in r.get(
                "lookup_headword",
                ""
            ).lower()
        ]


    # ========================================================
    # SINDHI SEARCH
    # ========================================================

    def search_sindhi(self, query):

        results = []

        if self.reverse_index:

            ids = self.reverse_index.get(query, [])

            if ids:

                english_words = set(ids)

                for r in self.rows:

                    english = r.get(
                        "english_headword",
                        ""
                    ).strip()

                    if english in english_words:

                        results.append(r)


                if results:
                    return results


        # Partial fallback

        for r in self.rows:

            sindhi = r.get(
                "sindhi_translations",
                ""
            )

            if query in sindhi:

                results.append(r)


        return results


    # ========================================================
    # SEARCH
    # ========================================================

    def search_dictionary(self):

        query = (
            self.ids.search_input.text
            .strip()
            .lower()
        )


        if not query:

            self.result_text = ""

            self.status_text = (
                f"{len(self.rows):,} dictionary headwords"
            )

            return


        mode = self.ids.search_mode.text


        if mode == "English → Sindhi":

            results = self.search_english(query)

        else:

            results = self.search_sindhi(query)


        # ====================================================
        # NO RESULTS
        # ====================================================

        if not results:

            self.result_text = (
                "[b]No matching entry found.[/b]"
            )

            self.status_text = "No results"

            return


        # ====================================================
        # DISPLAY
        # ====================================================

        output = []


        for r in results[:50]:

            english = r.get(
                "english_headword",
                ""
            ).strip()

            sindhi = r.get(
                "sindhi_translations",
                ""
            ).strip()


            output.append(
                f"[b]{english}[/b]"
            )

            output.append(
                sindhi
            )

            output.append("")


        if len(results) > 50:

            output.append(
                f"... and {len(results) - 50:,} more matches."
            )


        self.result_text = "\n".join(output)

        self.status_text = (
            f"{len(results):,} matches"
        )


# ============================================================
# APP
# ============================================================

class EnglishSindhiDictionaryApp(App):

    def build(self):

        Builder.load_string(KV)

        return DictionaryRoot()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    EnglishSindhiDictionaryApp().run()
