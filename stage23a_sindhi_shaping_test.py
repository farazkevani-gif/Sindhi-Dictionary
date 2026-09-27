import os
import arabic_reshaper
from bidi.algorithm import get_display

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FONT = os.path.join(
    BASE_DIR,
    "fonts",
    "NotoSansArabic-Regular.ttf"
)

LabelBase.register(
    name="SindhiFont",
    fn_regular=FONT
)

def sindhi_text(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


class TestApp(App):

    def build(self):

        box = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=30
        )

        box.add_widget(
            Label(
                text="English Test",
                font_size=30
            )
        )

        box.add_widget(
            Label(
                text=sindhi_text("سنڌي ٽيسٽ"),
                font_name="SindhiFont",
                font_size=35
            )
        )

        box.add_widget(
            Label(
                text=sindhi_text(
                    "تياڳڻ، ترڪ ڪرڻ، ڇڏي ڏيڻ"
                ),
                font_name="SindhiFont",
                font_size=32
            )
        )

        return box


if __name__ == "__main__":
    TestApp().run()

