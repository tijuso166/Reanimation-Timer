"""
Einmaliges Skript: rendert das in icon.svg definierte Motiv (Herz + Pulslinie
auf dunklem Grund) als PNG in den für die PWA benoetigten Groessen.

Kein SVG-Rasterizer (cairosvg/rsvg-convert/ImageMagick) war in dieser Umgebung
verfuegbar, daher wird dasselbe Motiv hier direkt mit Pillow (ImageDraw)
nachgezeichnet, mit denselben Koordinaten/Farben wie in icon.svg.
"""
from PIL import Image, ImageDraw

BG = (17, 24, 39, 255)       # #111827
HEART = (239, 68, 68, 255)   # #ef4444
PULSE = (249, 250, 251, 255) # #f9fafb

HEART_PATH = [
    (256, 392),
    (150, 316), (86, 260), (86, 182),
    (86, 130), (126, 94), (174, 94),
    (206, 94), (234, 112), (256, 146),
    (278, 112), (306, 94), (338, 94),
    (386, 94), (426, 130), (426, 182),
    (426, 260), (362, 316), (256, 392),
]

PULSE_POINTS = [
    (146, 262), (206, 262), (230, 206),
    (268, 322), (300, 238), (322, 262), (366, 262),
]

SUPERSAMPLE = 4
BASE_SIZE = 512


def render(size):
    scale = SUPERSAMPLE * size / BASE_SIZE
    canvas_size = int(BASE_SIZE * scale)
    img = Image.new('RGBA', (canvas_size, canvas_size), BG)
    draw = ImageDraw.Draw(img)

    heart_scaled = [(x * scale, y * scale) for x, y in HEART_PATH]
    draw.polygon(heart_scaled, fill=HEART)

    pulse_scaled = [(x * scale, y * scale) for x, y in PULSE_POINTS]
    draw.line(pulse_scaled, fill=PULSE, width=max(1, int(14 * scale)), joint='curve')
    r = max(1, int(7 * scale))
    for x, y in (pulse_scaled[0], pulse_scaled[-1]):
        draw.ellipse([x - r, y - r, x + r, y + r], fill=PULSE)

    img = img.resize((size, size), Image.LANCZOS)
    return img


if __name__ == '__main__':
    for size, name in ((180, 'icon-180.png'), (192, 'icon-192.png'), (512, 'icon-512.png')):
        render(size).save(name)
        print(f'geschrieben: {name} ({size}x{size})')
