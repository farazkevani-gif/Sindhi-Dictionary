from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

FONT = "fonts/NotoSansArabic-Regular.ttf"


class TestApp(App):

    def build(self):

        root = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        root.add_widget(
            Label(
                text="Kivy SDL2 Arabic/Sindhi Script Test",
                font_size=24,
                size_hint_y=None,
                height=60
            )
        )

        root.add_widget(
            Label(
                text="ڪرڻ",
                font_name=FONT,
                font_size=42,
                font_script_name="Arab",
                font_direction="rtl",
                text_size=(None, None)
            )
        )

        root.add_widget(
            Label(
                text="ڇڏي",
                font_name=FONT,
                font_size=42,
                font_script_name="Arab",
                font_direction="rtl",
                text_size=(None, None)
            )
        )

        root.add_widget(
            Label(
                text="تياڳڻ، ترڪ ڪرڻ، ڇڏي ڏيڻ",
                font_name=FONT,
                font_size=38,
                font_script_name="Arab",
                font_direction="rtl",
                text_size=(None, None)
            )
        )

        root.add_widget(
            Label(
                text="سنڌي ٽيسٽ",
                font_name=FONT,
                font_size=38,
                font_script_name="Arab",
                font_direction="rtl",
                text_size=(None, None)
            )
        )

        return root


if __name__ == "__main__":
    TestApp().run()
