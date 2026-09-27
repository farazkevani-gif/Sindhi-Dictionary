from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

FONT = "fonts/NotoSansArabic-Regular.ttf"

KV = r'''
#:import dp kivy.metrics.dp

BoxLayout:
    orientation: "vertical"
    padding: dp(25)
    spacing: dp(20)

    Label:
        text: "Sindhi Text Rendering Test"
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
        text: "تياڳڻ، ترڪ ڪرڻ، ڇڏي ڏيڻ"
        font_name: app.sindhi_font
        font_size: "28sp"
        halign: "right"
        text_size: self.width, None
        size_hint_y: None
        height: dp(70)

    Label:
        text: "سنڌي ٽيسٽ"
        font_name: app.sindhi_font
        font_size: "28sp"
        halign: "right"
        text_size: self.width, None
        size_hint_y: None
        height: dp(70)

    Label:
        text: "هٿ — آواز — تياڳڻ"
        font_name: app.sindhi_font
        font_size: "28sp"
        halign: "right"
        text_size: self.width, None
        size_hint_y: None
        height: dp(70)

    Label:
        text: "If these words appear connected, the font is working."
        font_size: "16sp"
'''

class TestApp(App):

    sindhi_font = FONT

    def build(self):
        return Builder.load_string(KV)


if __name__ == "__main__":
    TestApp().run()
