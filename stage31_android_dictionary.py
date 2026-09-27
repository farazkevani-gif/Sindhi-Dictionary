import csv
import json
import os

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


# ============================================================
# FILES
# ============================================================

DICTIONARY_FILE = "dictionary_stage14_grouped.csv"
REVERSE_INDEX_FILE = "dictionary_stage18_reverse_index.json"
SINDHI_FONT = "fonts/NotoSansArabic-Regular.ttf"


# ============================================================
# RESULT ITEM
# ============================================================

class ResultItem(BoxLayout):

    english = StringProperty("")
    sindhi = StringProperty("")

    def __init__(self, english="", sindhi="", **kwargs):

        super().__init__(**kwargs)

        self.english = english
        self.sindhi = sindhi


# ============================================================
# KV
# ============================================================

KV = r'''
#:import dp kivy.metrics.dp

<ResultItem>:

    orientation: "vertical"
    size_hint_y: None
    height: dp(105)
    spacing: dp(4)
    padding: dp(8), dp(6)

    Label:
        text: root.english
        font_size: "20sp"
        bold: True
        halign: "left"
        valign: "middle"
        text_size: self.width, None
        size_hint_y: None
        height: dp(35)

    Label:
        text: root.sindhi
        font_name: app.sindhi_font
        font_size: "23sp"
        font_script_name: "Arab"
        font_direction: "rtl"
        halign: "right"
        valign: "middle"
        text_size: self.width, None
        size_hint_y: None
        height: dp(50)


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

        GridLayout:
            id: results_box
            cols: 1
            spacing: dp(5)
            padding: dp(5)
            size_hint_y: None
            height: self.minimum_height

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

    status_text = StringProperty("Loading dictionary...")
    rows = []
    reverse_index = {}

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.rows = []
        self.reverse_index = {}

        self.load_dictionary()


    # ========================================================
    # LOAD DATABASE
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


        # Clear previous results

        self.ids.results_box.clear_widgets()


        if not query:

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

            self.ids.results_box.add_widget(
                Label(
                    text="No matching entry found.",
                    font_size="18sp",
                    size_hint_y=None,
                    height=dp(50)
                )
            )

            self.status_text = "No results"

            return


        # ====================================================
        # RESULTS
        # ====================================================

        for r in results[:50]:

            english = r.get(
                "english_headword",
                ""
            ).strip()

            sindhi = r.get(
                "sindhi_translations",
                ""
            ).strip()


            self.ids.results_box.add_widget(
                ResultItem(
                    english=english,
                    sindhi=sindhi
                )
            )


        if len(results) > 50:

            self.ids.results_box.add_widget(
                Label(
                    text=(
                        f"... and {len(results) - 50:,} "
                        "more matches."
                    ),
                    font_size="15sp",
                    size_hint_y=None,
                    height=dp(40)
                )
            )


        self.status_text = (
            f"{len(results):,} matches"
        )


# ============================================================
# APP
# ============================================================

class EnglishSindhiDictionaryApp(App):

    sindhi_font = SINDHI_FONT

    def build(self):

        Builder.load_string(KV)

        return DictionaryRoot()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    EnglishSindhiDictionaryApp().run()
