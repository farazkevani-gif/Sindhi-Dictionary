import arabic_reshaper
from bidi.algorithm import get_display

from kivy.app import App
from kivy.lang import Builder

FONT = "fonts/NotoSansArabic-Regular.ttf"


def shape_sindhi(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


KV = r"""
#:import dp kivy.metrics.dp

BoxLayout:
    orientation: "vertical"
    padding: dp(25)
    spacing: dp(20)

    Label:
        text: "Sindhi Text Shaping Test"
        font_size: "24sp"
        bold: True
        size_hint_y: None
        height: dp(55)

    Label:
        text: "English: Abandon"
        font_size: "20sp"
        size_hint_y: None
        height: dp(45)

    Label:
        text: app.shaped_abandon
        font_name: app.sindhi_font
        font_size: "28sp"
        halign: "right"
        text_size: self.width, None
        size_hint_y: None
        height: dp(70)

    Label:
        text: app.shaped_test
        font_name: app.sindhi_font
        font_size: "28sp"
        halign: "right"
        text_size: self.width, None
        size_hint_y: None
        height: dp(70)

    Label:
        text: app.shaped_words
        font_name: app.sindhi_font
        font_size: "28sp"
        halign: "right"
        text_size: self.width, None
        size_hint_y: None
        height: dp(70)

    Label:
        text: "The text above was shaped before rendering."
        font_size: "16sp"
"""


class TestApp(App):

    sindhi_font = FONT

    shaped_abandon = shape_sindhi(
        "تياڳڻ، ترڪ ڪرڻ، ڇڏي ڏيڻ"
    )

    shaped_test = shape_sindhi(
        "سنڌي ٽيسٽ"
    )

    shaped_words = shape_sindhi(
        "هٿ — آواز — تياڳڻ"
    )

    def build(self):
        return Builder.load_string(KV)


if __name__ == "__main__":
    TestApp().run()
