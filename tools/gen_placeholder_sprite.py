"""
Genera un sprite placeholder de personaje en pixel art (32x48 px, 4 direcciones).
Salida: assets/sprites/characters/player_placeholder.png
"""

import struct
import zlib
import os

W, H = 32, 48

# Paleta de colores RGBA
TRANSPARENT = (0, 0, 0, 0)
OUTLINE     = (30, 20, 40, 255)
SKIN        = (240, 195, 150, 255)
HAIR        = (80, 50, 30, 255)
SHIRT       = (70, 100, 180, 255)
SHIRT_DARK  = (50, 75, 140, 255)
PANTS       = (55, 60, 90, 255)
PANTS_DARK  = (40, 44, 68, 255)
BOOT        = (70, 50, 35, 255)
EYE         = (40, 40, 80, 255)
BLUSH       = (220, 150, 130, 255)


def canvas():
    return [[TRANSPARENT] * W for _ in range(H)]


def px(img, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        img[y][x] = color


def rect(img, x0, y0, x1, y1, color):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px(img, x, y, color)


def outline_rect(img, x0, y0, x1, y1, fill, border):
    rect(img, x0, y0, x1, y1, fill)
    for x in range(x0, x1 + 1):
        px(img, x, y0, border)
        px(img, x, y1, border)
    for y in range(y0, y1 + 1):
        px(img, x0, y, border)
        px(img, x1, y, border)


def draw_south(img):
    cx = 16

    # Cabeza
    outline_rect(img, cx-4, 4, cx+3, 12, SKIN, OUTLINE)
    # Cabello
    rect(img, cx-4, 4, cx+3, 6, HAIR)
    rect(img, cx-4, 7, cx-4, 9, HAIR)
    rect(img, cx+3, 7, cx+3, 9, HAIR)
    # Ojos
    px(img, cx-2, 9, EYE)
    px(img, cx+1, 9, EYE)
    # Boca / blush
    px(img, cx-1, 11, BLUSH)
    px(img, cx+0, 11, BLUSH)

    # Cuerpo
    outline_rect(img, cx-4, 13, cx+3, 24, SHIRT, OUTLINE)
    rect(img, cx-4, 20, cx+3, 24, SHIRT_DARK)

    # Brazos
    outline_rect(img, cx-6, 13, cx-5, 22, SHIRT, OUTLINE)
    outline_rect(img, cx+4, 13, cx+5, 22, SHIRT, OUTLINE)
    # Manos
    outline_rect(img, cx-6, 23, cx-5, 24, SKIN, OUTLINE)
    outline_rect(img, cx+4, 23, cx+5, 24, SKIN, OUTLINE)

    # Piernas
    outline_rect(img, cx-4, 25, cx-1, 38, PANTS, OUTLINE)
    outline_rect(img, cx,   25, cx+3, 38, PANTS, OUTLINE)
    rect(img, cx-4, 34, cx-1, 38, PANTS_DARK)
    rect(img, cx,   34, cx+3, 38, PANTS_DARK)

    # Botas
    outline_rect(img, cx-4, 39, cx-1, 44, BOOT, OUTLINE)
    outline_rect(img, cx,   39, cx+3, 44, BOOT, OUTLINE)


def draw_north(img):
    cx = 16
    # Cabeza (vista espalda)
    outline_rect(img, cx-4, 4, cx+3, 12, SKIN, OUTLINE)
    rect(img, cx-4, 4, cx+3, 9, HAIR)

    # Cuerpo
    outline_rect(img, cx-4, 13, cx+3, 24, SHIRT, OUTLINE)
    rect(img, cx-4, 20, cx+3, 24, SHIRT_DARK)

    # Brazos
    outline_rect(img, cx-6, 13, cx-5, 22, SHIRT, OUTLINE)
    outline_rect(img, cx+4, 13, cx+5, 22, SHIRT, OUTLINE)
    outline_rect(img, cx-6, 23, cx-5, 24, SKIN, OUTLINE)
    outline_rect(img, cx+4, 23, cx+5, 24, SKIN, OUTLINE)

    # Piernas
    outline_rect(img, cx-4, 25, cx-1, 38, PANTS, OUTLINE)
    outline_rect(img, cx,   25, cx+3, 38, PANTS, OUTLINE)
    rect(img, cx-4, 34, cx-1, 38, PANTS_DARK)
    rect(img, cx,   34, cx+3, 38, PANTS_DARK)

    # Botas
    outline_rect(img, cx-4, 39, cx-1, 44, BOOT, OUTLINE)
    outline_rect(img, cx,   39, cx+3, 44, BOOT, OUTLINE)


def draw_west(img):
    cx = 16
    # Cabeza perfil izquierda
    outline_rect(img, cx-3, 4, cx+3, 12, SKIN, OUTLINE)
    rect(img, cx-3, 4, cx+3, 7, HAIR)
    rect(img, cx+3, 5, cx+3, 10, HAIR)
    px(img, cx-1, 9, EYE)

    # Cuerpo
    outline_rect(img, cx-3, 13, cx+3, 24, SHIRT, OUTLINE)
    rect(img, cx-3, 20, cx+3, 24, SHIRT_DARK)

    # Brazo visible (derecho en pantalla)
    outline_rect(img, cx+4, 13, cx+5, 22, SHIRT, OUTLINE)
    outline_rect(img, cx+4, 23, cx+5, 24, SKIN, OUTLINE)

    # Piernas
    outline_rect(img, cx-3, 25, cx,   38, PANTS, OUTLINE)
    outline_rect(img, cx+1, 25, cx+3, 38, PANTS, OUTLINE)
    rect(img, cx-3, 34, cx,   38, PANTS_DARK)
    rect(img, cx+1, 34, cx+3, 38, PANTS_DARK)

    # Botas
    outline_rect(img, cx-3, 39, cx,   44, BOOT, OUTLINE)
    outline_rect(img, cx+1, 39, cx+3, 44, BOOT, OUTLINE)


def draw_east(img):
    # Imagen de west con flip horizontal
    west = canvas()
    draw_west(west)
    for y in range(H):
        for x in range(W):
            img[y][x] = west[y][W - 1 - x]


# --- PNG writer minimalista ---

def write_png(pixels, filepath):
    def chunk(name, data):
        c = name + data
        crc = zlib.crc32(c) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + c + struct.pack(">I", crc)

    raw = b""
    for row in pixels:
        raw += b"\x00"
        for r, g, b, a in row:
            raw += bytes([r, g, b, a])

    compressed = zlib.compress(raw, 9)

    png  = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", compressed)
    png += chunk(b"IEND", b"")

    with open(filepath, "wb") as f:
        f.write(png)


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites", "characters")
    os.makedirs(base, exist_ok=True)

    directions = {
        "south": draw_south,
        "north": draw_north,
        "west":  draw_west,
        "east":  draw_east,
    }

    for name, fn in directions.items():
        img = canvas()
        fn(img)
        path = os.path.join(base, f"player_{name}.png")
        write_png(img, path)
        print(f"Generado: {path}")

    print("\nListo. Importa los PNG en Godot con filtro 'Nearest'.")
