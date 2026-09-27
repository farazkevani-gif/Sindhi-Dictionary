import uharfbuzz as hb

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

FONT = "fonts/NotoSansArabic-Regular.ttf"

LabelBase.register(
    name="SindhiFont",
    fn_regular=FONT
)


def test_harfbuzz(text):

    with open(FONT, "rb") as f:
        font_data = f.read()

    face = hb.Face(font_data)
    hb_font = hb.Font(face)

    upem = face.upem
    hb_font.scale = (upem, upem)

    buffer = hb.Buffer()
    buffer.add_str(text)
    buffer.guess_segment_properties()

    hb.shape(hb_font, buffer)

    infos = buffer.glyph_infos
    positions = buffer.glyph_positions

    print()
    print("=" * 70)
    print("HARFBUZZ SHAPING TEST")
    print("=" * 70)
    print("Original:")
    print(text)
    print()
    print("Glyph count:", len(infos))
    print("Character count:", len(text))
    print()

    for i, (info, pos) in enumerate(zip(infos, positions)):
        print(
            f"{i:03} "
            f"glyph={info.codepoint:<5} "
            f"cluster={info.cluster:<5} "
            f"advance={pos.x_advance}"
        )

    print("=" * 70)


class TestApp(App):

    def build(self):

        text1 = "تياڳڻ، ترڪ ڪرڻ، ڇڏي ڏيڻ"
        text2 = "ڪرڻ"
        text3 = "ڇڏي"
        text4 = "سنڌي ٽيسٽ"

        test_harfbuzz(text1)
        test_harfbuzz(text2)
        test_harfbuzz(text3)
        test_harfbuzz(text4)

        root = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        root.add_widget(
            Label(
                text="HarfBuzz Sindhi Test",
                font_size=24,
                size_hint_y=None,
                height=50
            )
        )

        root.add_widget(
            Label(
                text=text1,
                font_name="SindhiFont",
                font_size=32,
                halign="right"
            )
        )

        root.add_widget(
            Label(
                text=text2,
                font_name="SindhiFont",
                font_size=32
            )
        )

        root.add_widget(
            Label(
                text=text3,
                font_name="SindhiFont",
                font_size=32
            )
        )

        root.add_widget(
            Label(
                text=text4,
                font_name="SindhiFont",
                font_size=32
            )
        )

        return root


if __name__ == "__main__":
    TestApp().run()
