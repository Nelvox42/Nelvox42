"""Build the restrained three-line GIF used by the profile README.

Run with Python 3 and Pillow. The output is assets/archive-loop.gif.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "archive-loop.gif"
WIDTH, HEIGHT = 1200, 210
SCALE = 2
LINES = (
    "Building small things.",
    "Learning how things work.",
    "Documenting the process.",
)

BG = "#181714"
PAPER = "#F0EADF"
MUTED = "#C9C2B5"
OCHRE = "#D0AA62"
RUST = "#B9513D"

SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"
MONO = "/System/Library/Fonts/Menlo.ttc"


def mark(draw):
    draw.line([(56 * SCALE, 154 * SCALE), (90 * SCALE, 76 * SCALE), (124 * SCALE, 154 * SCALE)], fill=RUST, width=5 * SCALE)
    draw.line([(72 * SCALE, 128 * SCALE), (114 * SCALE, 128 * SCALE)], fill=RUST, width=5 * SCALE)
    draw.ellipse((137 * SCALE, 81 * SCALE, 148 * SCALE, 92 * SCALE), fill=RUST)


def frame(index, reveal=1.0):
    image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), BG)
    draw = ImageDraw.Draw(image)
    serif = ImageFont.truetype(SERIF, 54 * SCALE)
    mono = ImageFont.truetype(MONO, 16 * SCALE)

    draw.rectangle((26 * SCALE, 24 * SCALE, 1174 * SCALE, 186 * SCALE), outline="#514B40", width=SCALE)
    draw.line((26 * SCALE, 24 * SCALE, 155 * SCALE, 24 * SCALE), fill=RUST, width=3 * SCALE)
    mark(draw)

    draw.text((192 * SCALE, 55 * SCALE), "WORKBENCH / NOTE", font=mono, fill=OCHRE)
    draw.text((1070 * SCALE, 55 * SCALE), f"0{index + 1} / 03", font=mono, fill=MUTED)

    line = LINES[index]
    x, y = 190 * SCALE, 96 * SCALE
    max_width = int(draw.textlength(line, font=serif) * reveal)
    text_layer = Image.new("RGB", image.size, BG)
    ImageDraw.Draw(text_layer).text((x, y), line, font=serif, fill=PAPER)
    image.paste(text_layer.crop((x, y, x + max_width, y + 78 * SCALE)), (x, y))

    draw.line((190 * SCALE, 178 * SCALE, (240 + index * 35) * SCALE, 178 * SCALE), fill=OCHRE, width=2 * SCALE)
    return image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def main():
    # The first frame is a complete, readable still for paused previews.
    images = [frame(0)]
    durations = [2200]
    for index in (1, 2, 0):
        for reveal in (0.22, 0.43, 0.66, 0.84, 1.0):
            images.append(frame(index, reveal))
            durations.append(110)
        images.append(frame(index))
        durations.append(2200 if index != 0 else 900)

    images[0].save(
        OUTPUT,
        save_all=True,
        append_images=images[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()
