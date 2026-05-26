"""Genera sprite placeholder de NPC (32x48 px) — tunica verde."""

import struct, zlib, os

W, H = 32, 48

TRANSPARENT = (0, 0, 0, 0)
OUTLINE     = (20, 30, 20, 255)
SKIN        = (235, 185, 140, 255)
HAIR        = (160, 110, 50, 255)
TUNIC       = (50, 130, 80, 255)
TUNIC_DARK  = (35, 95, 55, 255)
PANTS       = (80, 60, 40, 255)
PANTS_DARK  = (55, 40, 25, 255)
BOOT        = (60, 45, 30, 255)
EYE         = (30, 50, 30, 255)


def canvas():
    return [[TRANSPARENT] * W for _ in range(H)]


def px(img, x, y, c):
    if 0 <= x < W and 0 <= y < H:
        img[y][x] = c


def rect(img, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px(img, x, y, c)


def border_rect(img, x0, y0, x1, y1, fill, border):
    rect(img, x0, y0, x1, y1, fill)
    for x in range(x0, x1 + 1):
        px(img, x, y0, border); px(img, x, y1, border)
    for y in range(y0, y1 + 1):
        px(img, x0, y, border); px(img, x1, y, border)


def draw_south(img):
    cx = 16
    border_rect(img, cx-4, 4, cx+3, 12, SKIN, OUTLINE)
    rect(img, cx-4, 4, cx+3, 7, HAIR)
    px(img, cx-2, 9, EYE); px(img, cx+1, 9, EYE)
    border_rect(img, cx-4, 13, cx+3, 26, TUNIC, OUTLINE)
    rect(img, cx-4, 22, cx+3, 26, TUNIC_DARK)
    border_rect(img, cx-6, 13, cx-5, 24, TUNIC, OUTLINE)
    border_rect(img, cx+4, 13, cx+5, 24, TUNIC, OUTLINE)
    border_rect(img, cx-6, 25, cx-5, 26, SKIN, OUTLINE)
    border_rect(img, cx+4, 25, cx+5, 26, SKIN, OUTLINE)
    border_rect(img, cx-4, 27, cx-1, 38, PANTS, OUTLINE)
    border_rect(img, cx,   27, cx+3, 38, PANTS, OUTLINE)
    rect(img, cx-4, 34, cx-1, 38, PANTS_DARK)
    rect(img, cx,   34, cx+3, 38, PANTS_DARK)
    border_rect(img, cx-4, 39, cx-1, 44, BOOT, OUTLINE)
    border_rect(img, cx,   39, cx+3, 44, BOOT, OUTLINE)


def write_png(pixels, filepath):
    def chunk(name, data):
        c = name + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    raw = b"".join(b"\x00" + bytes([v for rgba in row for v in rgba]) for row in pixels)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    with open(filepath, "wb") as f:
        f.write(png)


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites", "characters")
    img = canvas()
    draw_south(img)
    path = os.path.join(base, "npc_aldeano.png")
    write_png(img, path)
    print(f"Generado: {path}")
