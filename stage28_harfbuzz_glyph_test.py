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


def shape_sindhi(text):

    with open(FONT, "rb") as f:
        font_data = f.read()

    face = hb.Face(font_data)
    font = hb.Font(face)

    font.scale = (face.upem, face.upem)

    buffer = hb.Buffer()
    buffer.add_str(text)

    buffer.direction = "rtl"
    buffer.script = "arab"
    buffer.language = "sd"

    hb.shape(font, buffer)

    infos = buffer.glyph_infos

    print()
    print("=" * 70)
    print("STAGE 28 — HARFBUZZ GLYPH TEST")
    print("=" * 70)
    print("Original:", text)
    print("Unicode characters:", len(text))
    print("HarfBuzz glyphs:", len(infos))
    print()

    for i, info in enumerate(infos):
        print(
            f"{i:03} "
            f"glyph_id={info.codepoint:<5} "
            f"cluster={info.cluster}"
        )

    print("=" * 70)

    return len(infos)


class TestApp(App):

    def build(self):

        root = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        root.add_widget(
            Label(
                text="Stage 28 — Sindhi Rendering",
                font_size=24,
                size_hint_y=None,
                height=60
            )
        )

        text = "ڪرڻ"

        glyph_count = shape_sindhi(text)

        root.add_widget(
            Label(
                text="Original Unicode:",
                font_size=20,
                size_hint_y=None,
                height=40
            )
        )

        root.add_widget(
            Label(
                text=text,
                font_name="SindhiFont",
                font_size=42,
                halign="right"
            )
        )

        root.add_widget(
            Label(
                text=f"HarfBuzz glyph count: {glyph_count}",
                font_size=18,
                size_hint_y=None,
                height=40
            )
        )

        return root


if __name__ == "__main__":
    TestApp().run()
