import arabic_reshaper
from bidi.algorithm import get_display

from kivy.app import App
from kivy.lang import Builder

FONT = "fonts/NotoSansArabic-Regular.ttf"


# ------------------------------------------------------------
# SINDHI SHAPING
# ------------------------------------------------------------

RESHAPER_CONFIG = {
    "delete_harakat": False,
    "support_ligatures": True,

    # Sindhi-specific Arabic characters
    "use_unshaped_instead_of_isolated": False,
}

reshaper = arabic_reshaper.ArabicReshaper(
    configuration=RESHAPER_CONFIG
)


def shape_sindhi(text):
    shaped = reshaper.reshape(text)
    return get_display(shaped)


# ------------------------------------------------------------
# TEST TEXT
# ------------------------------------------------------------

ABANDON = shape_sindhi(
    "تياڳڻ، ترڪ ڪرڻ، ڇڏي ڏيڻ"
)

TEST = shape_sindhi(
    "سنڌي ٽيسٽ"
)

WORDS = shape_sindhi(
    "هٿ — آواز — تياڳڻ — ڪرڻ — ڇڏي"
)


# ------------------------------------------------------------
# UI
# ------------------------------------------------------------

KV = r"""
#:import dp kivy.metrics.dp

BoxLayout:
    orientation: "vertical"
    padding: dp(25)
    spacing: dp(20)

    Label:
        text: "Sindhi Shaping Test"
        font_size: "24sp"
        bold: True
        size_hint_y: None
        height: dp(55)

    Label:
        text: "Abandon"
        font_size: "20sp"
        size_hint_y: None
        height: dp(40)

    Label:
        text: app.abandon
        font_name: app.sindhi_font
        font_size: "30sp"
        halign: "right"
        text_size: self.width, None
        size_hint_y: None
        height: dp(70)

    Label:
        text: app.test
        font_name: app.sindhi_font
        font_size: "30sp"
        halign: "right"
        text_size: self.width, None
        size_hint_y: None
        height: dp(70)

    Label:
        text: app.words
        font_name: app.sindhi_font
        font_size: "30sp"
        halign: "right"
        text_size: self.width, None
        size_hint_y: None
        height: dp(100)
"""


class TestApp(App):

    sindhi_font = FONT

    abandon = ABANDON
    test = TEST
    words = WORDS

    def build(self):
        return Builder.load_string(KV)


if __name__ == "__main__":
    TestApp().run()
