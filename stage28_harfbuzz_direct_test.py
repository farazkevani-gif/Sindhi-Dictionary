import uharfbuzz as hb

FONT = r"fonts/NotoSansArabic-Regular.ttf"

def shape_text(text):
    with open(FONT, "rb") as f:
        font_data = f.read()

    face = hb.Face(font_data)
    font = hb.Font(face)

    upem = face.upem
    font.scale = (upem, upem)

    buf = hb.Buffer()
    buf.add_str(text)

    buf.direction = "rtl"
    buf.script = "Arab"
    buf.language = "sd"

    hb.shape(font, buf)

    infos = buf.glyph_infos
    positions = buf.glyph_positions

    print("=" * 70)
    print("HARFBUZZ DIRECT SHAPING TEST")
    print("=" * 70)
    print("Input:")
    print(text)
    print()
    print("Unicode characters:", len(text))
    print("HarfBuzz glyphs:", len(infos))
    print()

    for i, (info, pos) in enumerate(zip(infos, positions)):
        print(
            f"{i:03} "
            f"glyph={info.codepoint:<5} "
            f"cluster={info.cluster:<5} "
            f"advance={pos.x_advance}"
        )

    print("=" * 70)


shape_text("تياڳڻ، ترڪ ڪرڻ، ڇڏي ڏيڻ")
shape_text("ڪرڻ")
shape_text("ڇڏي")
shape_text("سنڌي ٽيسٽ")
