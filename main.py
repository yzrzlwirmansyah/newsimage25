#!/usr/bin/env python3
"""news-image-20261125 -- "THE WORLD TODAY" newspaper front page.

Sums up 25 November 2026 world news in one 1024x1024 image.

Pure Python 3.13 standard library only (math, os, struct, sys, zlib).
No PIL, no network, no external files, no fonts beyond the hand-rolled
5x7 bitmap font below. Fully deterministic: fixed geometry, fixed
palette, fixed zlib level, no time, no randomness. Every number on the
page comes from PLAN.md or is a date.

Writes $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
"""

import math
import os
import struct
import sys
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- palette
PAPER = (245, 239, 224)   # newsprint cream
INK = (26, 26, 26)        # near-black ink
RED = (158, 43, 37)       # kicker / label red
NAVY = (31, 58, 95)       # deep sea blue
SEA = (38, 84, 124)       # mid sea
SKY = (191, 212, 230)     # pale sky
LIGHT = (232, 226, 210)   # light panel fill
GREY = (120, 120, 115)    # smoke grey
DARKGREY = (70, 70, 70)
WHITE = (255, 255, 255)
ORANGE = (230, 120, 30)   # flame
YELLOW = (240, 200, 60)   # flame core / sun
GREEN = (60, 110, 70)     # land
BROWN = (120, 84, 50)
STEEL = (90, 100, 110)    # ship hull
CONTAINER_RED = (180, 60, 50)
CONTAINER_BLUE = (50, 90, 160)
CONTAINER_YELLOW = (210, 170, 40)
CONTAINER_GREEN = (70, 140, 80)

# ------------------------------------------------------- 5x7 bitmap font
# Each glyph: 7 rows of 5 bits, '#' = on, '.' = off.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
}
BLANK = ("00000", "00000", "00000", "00000", "00000", "00000", "00000")

# ------------------------------------------------------------------ canvas
class Canvas:
    """Flat RGB bytearray, 1024x1024."""

    def __init__(self, w=W, h=H, bg=PAPER):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set_pixel(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def fill_rect(self, x0, y0, x1, y1, color):
        x0 = max(0, x0)
        y0 = max(0, y0)
        x1 = min(self.w, x1)
        y1 = min(self.h, y1)
        r, g, b = color
        for y in range(y0, y1):
            base = (y * self.w + x0) * 3
            for x in range(x0, x1):
                i = base + (x - x0) * 3
                self.px[i] = r
                self.px[i + 1] = g
                self.px[i + 2] = b

    def rect(self, x0, y0, x1, y1, color, thickness=1):
        for t in range(thickness):
            self.hline(x0, y0 + t, x1, color)
            self.hline(x0, y1 - 1 - t, x1, color)
            self.vline(x0 + t, y0, y1, color)
            self.vline(x1 - 1 - t, y0, y1, color)

    def hline(self, x0, y, x1, color):
        if x0 > x1:
            x0, x1 = x1, x0
        for x in range(x0, x1):
            self.set_pixel(x, y, color)

    def vline(self, x, y0, y1, color):
        if y0 > y1:
            y0, y1 = y1, y0
        for y in range(y0, y1):
            self.set_pixel(x, y, color)

    def line(self, x0, y0, x1, y1, color):
        """Bresenham line."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def dashed_line(self, x0, y0, x1, y1, color, dash=6, gap=4):
        length = int(math.hypot(x1 - x0, y1 - y0))
        if length == 0:
            return
        ux = (x1 - x0) / length
        uy = (y1 - y0) / length
        d = 0
        while d < length:
            end = min(d + dash, length)
            self.line(int(x0 + ux * d), int(y0 + uy * d),
                      int(x0 + ux * end), int(y0 + uy * end), color)
            d = end + gap

    def filled_circle(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            self.hline(cx - dx, cy + dy, cx + dx + 1, color)

    def circle(self, cx, cy, r, color):
        for a in range(0, 360, 2):
            rad = math.radians(a)
            self.set_pixel(cx + int(r * math.cos(rad)),
                           cy + int(r * math.sin(rad)), color)

    def fill_triangle(self, p0, p1, p2, color):
        """Scanline filled triangle."""
        pts = sorted([p0, p1, p2], key=lambda p: p[1])
        (x0, y0), (x1, y1), (x2, y2) = pts
        if y0 == y2:
            return
        def interp(xa, ya, xb, yb, y):
            if yb == ya:
                return xa
            return xa + (xb - xa) * (y - ya) / (yb - ya)
        for y in range(y0, y2 + 1):
            if y < y1:
                xa = interp(x0, y0, x2, y2, y)
                xb = interp(x0, y0, x1, y1, y)
            else:
                xa = interp(x0, y0, x2, y2, y)
                xb = interp(x1, y1, x2, y2, y)
            if xa > xb:
                xa, xb = xb, xa
            self.hline(int(xa), y, int(xb) + 1, color)

    def fill_poly(self, points, color):
        """Convex polygon fill via triangle fan."""
        if len(points) < 3:
            return
        for i in range(1, len(points) - 1):
            self.fill_triangle(points[0], points[i], points[i + 1], color)

# -------------------------------------------------------------------- text
def char_advance(scale, tracking=0):
    return 6 * scale + tracking

def text_width(text, scale, tracking=0):
    if not text:
        return 0
    return len(text) * char_advance(scale, tracking) - tracking

def draw_text(c, x, y, text, scale, color, tracking=0):
    """Draw uppercased text; returns width drawn."""
    text = text.upper()
    adv = char_advance(scale, tracking)
    cx = x
    for ch in text:
        glyph = FONT.get(ch, BLANK)
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == '1':
                    c.fill_rect(cx + col * scale, y + row * scale,
                                cx + col * scale + scale,
                                y + row * scale + scale, color)
        cx += adv
    return cx - x - tracking if text else 0

def draw_text_centered(c, cx, y, text, scale, color, tracking=0):
    w = text_width(text, scale, tracking)
    draw_text(c, cx - w // 2, y, text, scale, color, tracking)

def wrap_text(text, scale, max_w, tracking=0):
    """Break text into lines that fit max_w pixels."""
    adv = char_advance(scale, tracking)
    per_line = max(1, max_w // adv)
    lines = []
    for para in text.split('\n'):
        words = para.split(' ')
        cur = ''
        for word in words:
            if len(word) > per_line:
                # hard-split a very long word
                if cur:
                    lines.append(cur)
                    cur = ''
                while len(word) > per_line:
                    lines.append(word[:per_line])
                    word = word[per_line:]
                cur = word
                continue
            trial = word if not cur else cur + ' ' + word
            if len(trial) <= per_line:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines

def draw_wrapped(c, x, y, text, scale, color, max_w, line_h=None, tracking=0):
    lines = wrap_text(text, scale, max_w, tracking)
    if line_h is None:
        line_h = 7 * scale + 2
    for i, ln in enumerate(lines):
        draw_text(c, x, y + i * line_h, ln, scale, color, tracking)
    return len(lines)

# ------------------------------------------------------------------- scenes
def draw_lead_scene(c, x0, y0, x1, y1):
    """Gulf of Finland: sky, distant shore, sea, burning cargo ship, drone."""
    # sky bands
    c.fill_rect(x0, y0, x1, y0 + 60, SKY)
    c.fill_rect(x0, y0 + 60, x1, y0 + 110, (168, 196, 220))
    # sun
    c.filled_circle(x1 - 70, y0 + 42, 18, YELLOW)
    c.circle(x1 - 70, y0 + 42, 22, (220, 190, 90))
    # clouds
    for cx, cy, r in ((x0 + 60, y0 + 30, 16), (x0 + 84, y0 + 26, 12),
                      (x0 + 250, y0 + 48, 14), (x0 + 272, y0 + 44, 10)):
        c.filled_circle(cx, cy, r, WHITE)
    # birds
    for bx, by in ((x0 + 150, y0 + 70), (x0 + 170, y0 + 62), (x0 + 330, y0 + 80)):
        c.line(bx - 6, by, bx, by - 4, INK)
        c.line(bx, by - 4, bx + 6, by, INK)
    # distant shore (Finland coast)
    shore_y = y0 + 118
    c.fill_rect(x0, shore_y, x1, shore_y + 14, GREEN)
    c.fill_rect(x0, shore_y + 14, x1, shore_y + 18, (48, 88, 58))
    # pine trees on the shore
    for tx in range(x0 + 12, x1 - 12, 26):
        c.fill_triangle((tx, shore_y + 2), (tx + 5, shore_y - 12),
                        (tx + 10, shore_y + 2), (40, 80, 50))
    # sea
    sea_y = shore_y + 18
    c.fill_rect(x0, sea_y, x1, y1, SEA)
    c.fill_rect(x0, sea_y, x1, sea_y + 30, NAVY)
    # waves
    for wy in range(sea_y + 44, y1 - 8, 22):
        for wx in range(x0 + 8, x1 - 30, 64):
            c.hline(wx, wy, wx + 34, (120, 170, 205))
            c.hline(wx + 8, wy + 3, wx + 26, (120, 170, 205))
    # ---- cargo ship SPARTA II ----
    hx0, hx1 = x0 + 70, x1 - 70
    deck_y = sea_y + 78
    hull_top = deck_y
    hull_bot = deck_y + 34
    c.fill_poly([(hx0, hull_top), (hx1, hull_top),
                 (hx1 - 26, hull_bot), (hx0 + 26, hull_bot)], STEEL)
    c.fill_rect(hx0, hull_top, hx1, hull_top + 6, DARKGREY)
    # bow waterline stripe
    c.hline(hx0 + 10, hull_bot - 6, hx1 - 10, WHITE)
    # containers on deck
    conts = [(hx0 + 18, CONTAINER_RED), (hx0 + 62, CONTAINER_BLUE),
             (hx0 + 106, CONTAINER_YELLOW), (hx0 + 150, CONTAINER_GREEN)]
    for cx, col in conts:
        c.fill_rect(cx, deck_y - 26, cx + 40, deck_y - 2, col)
        c.rect(cx, deck_y - 26, cx + 40, deck_y - 2, INK, 1)
        c.vline(cx + 13, deck_y - 26, deck_y - 2, INK)
        c.vline(cx + 27, deck_y - 26, deck_y - 2, INK)
    # bridge tower (starboard)
    c.fill_rect(hx1 - 58, deck_y - 52, hx1 - 18, deck_y - 2, WHITE)
    c.rect(hx1 - 58, deck_y - 52, hx1 - 18, deck_y - 2, INK, 1)
    c.fill_rect(hx1 - 54, deck_y - 46, hx1 - 22, deck_y - 38, NAVY)
    c.fill_rect(hx1 - 54, deck_y - 34, hx1 - 22, deck_y - 26, NAVY)
    # funnel with smoke
    c.fill_rect(hx0 + 200, deck_y - 44, hx0 + 216, deck_y - 2, INK)
    # flames over the mid containers
    fx = hx0 + 96
    c.fill_triangle((fx, deck_y - 26), (fx + 14, deck_y - 62),
                    (fx + 28, deck_y - 26), ORANGE)
    c.fill_triangle((fx + 10, deck_y - 26), (fx + 20, deck_y - 50),
                    (fx + 32, deck_y - 26), YELLOW)
    c.fill_triangle((fx + 34, deck_y - 26), (fx + 44, deck_y - 46),
                    (fx + 54, deck_y - 26), ORANGE)
    # smoke puffs rising
    for sx, sy, r in ((fx + 22, deck_y - 74, 12), (fx + 34, deck_y - 92, 15),
                      (fx + 18, deck_y - 110, 18), (fx + 40, deck_y - 128, 14)):
        c.filled_circle(sx, sy, r, GREY)
        c.filled_circle(sx + 4, sy - 3, r - 4, (150, 150, 145))
    # ---- drone, top right, with dashed attack path ----
    dx, dy = x1 - 120, y0 + 74
    c.dashed_line(dx, dy + 8, fx + 30, deck_y - 60, INK, 7, 5)
    c.fill_rect(dx - 10, dy - 3, dx + 10, dy + 5, INK)
    c.fill_rect(dx - 3, dy - 8, dx + 3, dy + 10, INK)
    for rx, ry in ((dx - 16, dy - 8), (dx + 16, dy - 8),
                   (dx - 16, dy + 10), (dx + 16, dy + 10)):
        c.hline(rx - 8, ry, rx + 8, INK)
        c.filled_circle(rx, ry, 2, DARKGREY)
    c.line(dx - 10, dy, dx - 16, dy - 8, INK)
    c.line(dx + 10, dy, dx + 16, dy - 8, INK)
    c.line(dx - 10, dy + 4, dx - 16, dy + 10, INK)
    c.line(dx + 10, dy + 4, dx + 16, dy + 10, INK)
    # caption
    draw_text_centered(c, (x0 + x1) // 2, y1 + 8,
                       "THE SPARTA II AFLAME IN THE GULF OF FINLAND",
                       1, DARKGREY)

def scene_benghazi(c, x0, y0, x1, y1):
    """Sinking warship off Benghazi: tilted hull, sea, smoke.

    All art is kept inside the strip (top >= y0) so nothing can
    paint over the story body text above the strip.
    """
    mid = (y0 + y1) // 2
    c.fill_rect(x0, y0, x1, mid, SKY)
    c.fill_rect(x0, mid, x1, y1, SEA)
    for wx in range(x0 + 6, x1 - 20, 44):
        c.hline(wx, mid + 12, wx + 24, (120, 170, 205))
    # tilted sinking hull (bow up, stern down), top at mid-16
    c.fill_poly([(x0 + 40, mid - 4), (x0 + 250, mid - 16),
                 (x0 + 250, mid - 6), (x0 + 40, mid + 8)], STEEL)
    c.fill_rect(x0 + 60, mid - 14, x0 + 90, mid - 4, WHITE)
    # flame
    c.fill_triangle((x0 + 150, mid - 10), (x0 + 158, mid - 18),
                    (x0 + 168, mid - 10), ORANGE)
    # smoke, kept below the strip top
    for sx, sy, r in ((x0 + 130, mid - 14, 4), (x0 + 142, mid - 16, 4),
                      (x0 + 124, mid - 17, 3)):
        c.filled_circle(sx, sy, r, GREY)
    # listing mast
    c.line(x0 + 96, mid - 4, x0 + 84, mid - 16, INK)

def scene_riyadh(c, x0, y0, x1, y1):
    """Riyadh skyline with the tall PIF Tower and a blast star."""
    c.fill_rect(x0, y0, x1, y1, (232, 222, 196))
    base = y1 - 4
    # background blocks
    for bx, bh in ((x0 + 8, 22), (x0 + 46, 30), (x0 + 210, 26),
                   (x0 + 248, 20), (x0 + 120, 16)):
        c.fill_rect(bx, base - bh, bx + 30, base, DARKGREY)
    # PIF Tower: tall, slanted top
    tx0, tx1 = x0 + 128, x0 + 168
    c.fill_poly([(tx0, base), (tx0, y0 + 8), (tx1, y0 + 2),
                 (tx1, base)], NAVY)
    c.fill_rect(tx0 + 6, y0 + 12, tx1 - 6, y0 + 20, (140, 180, 220))
    for wy in range(y0 + 28, base - 6, 8):
        c.hline(tx0 + 4, wy, tx1 - 4, (120, 160, 200))
    # blast star at the tower crown
    sx, sy = (tx0 + tx1) // 2, y0 + 6
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        c.line(sx, sy, sx + int(12 * math.cos(rad)),
               sy + int(12 * math.sin(rad)), ORANGE)
    c.filled_circle(sx, sy, 4, YELLOW)

def scene_huawei(c, x0, y0, x1, y1):
    """Courthouse: pediment and columns, gavel block."""
    c.fill_rect(x0, y0, x1, y1, LIGHT)
    base = y1 - 4
    # pediment
    c.fill_triangle((x0 + 20, y0 + 14), ((x0 + x1) // 2, y0 + 2),
                    (x1 - 20, y0 + 14), NAVY)
    c.fill_rect(x0 + 20, y0 + 14, x1 - 20, y0 + 18, INK)
    # columns
    for cx in range(x0 + 34, x1 - 30, 44):
        c.fill_rect(cx, y0 + 20, cx + 12, base, WHITE)
        c.rect(cx, y0 + 20, cx + 12, base, INK, 1)
    c.fill_rect(x0 + 20, base - 4, x1 - 20, base, INK)
    # gavel: head + handle, lower right
    gx, gy = x1 - 62, y1 - 22
    c.fill_rect(gx, gy - 6, gx + 26, gy + 2, BROWN)
    c.line(gx + 26, gy - 2, gx + 44, gy + 8, BROWN)
    c.line(gx + 26, gy - 2, gx + 44, gy + 8, BROWN)

def scene_cyber(c, x0, y0, x1, y1):
    """Laptop with warning and padlock."""
    c.fill_rect(x0, y0, x1, y1, LIGHT)
    # laptop
    lx0, lx1 = x0 + 30, x0 + 190
    ly0, ly1 = y0 + 8, y1 - 14
    c.fill_rect(lx0, ly0, lx1, ly1, INK)
    c.fill_rect(lx0 + 4, ly0 + 4, lx1 - 4, ly1 - 4, (40, 120, 90))
    # code lines on screen
    for i, wy in enumerate(range(ly0 + 9, ly1 - 8, 7)):
        c.hline(lx0 + 10, wy, lx0 + 10 + (60 - i * 9), (150, 220, 190))
    c.fill_rect(lx0 - 8, ly1, lx1 + 8, ly1 + 6, DARKGREY)
    # warning triangle
    tx, ty = x1 - 52, y0 + 16
    c.fill_triangle((tx, ty + 22), (tx + 14, ty), (tx + 28, ty + 22), YELLOW)
    draw_text(c, tx + 11, ty + 8, "!", 1, INK)
    # padlock
    px, py = x1 - 62, y1 - 26
    c.circle(px + 10, py - 2, 8, INK)
    c.fill_rect(px, py, px + 20, py + 14, RED)
    c.fill_rect(px + 8, py + 5, px + 12, py + 11, WHITE)

def scene_nato(c, x0, y0, x1, y1):
    """Early-warning aircraft over Poland, satellite above."""
    c.fill_rect(x0, y0, x1, y1, SKY)
    # stars
    for sx, sy in ((x0 + 40, y0 + 10), (x0 + 250, y0 + 8), (x0 + 200, y0 + 16)):
        c.filled_circle(sx, sy, 2, WHITE)
    # satellite top right
    sx, sy = x1 - 70, y0 + 16
    c.fill_rect(sx - 26, sy - 3, sx - 8, sy + 3, NAVY)
    c.fill_rect(sx + 8, sy - 3, sx + 26, sy + 3, NAVY)
    c.fill_rect(sx - 8, sy - 6, sx + 8, sy + 6, CONTAINER_BLUE)
    c.line(sx - 8, sy, sx - 26, sy, WHITE)
    # aircraft: fuselage + swept wings + radar dome
    ax, ay = x0 + 60, y0 + 34
    c.fill_poly([(ax, ay), (ax + 150, ay - 4), (ax + 170, ay + 2),
                 (ax + 150, ay + 8), (ax, ay + 6)], WHITE)
    c.fill_poly([(ax + 60, ay), (ax + 100, ay - 18), (ax + 116, ay - 18),
                 (ax + 96, ay)], (200, 210, 220))
    c.fill_poly([(ax + 60, ay + 6), (ax + 96, ay + 20), (ax + 112, ay + 20),
                 (ax + 92, ay + 6)], (200, 210, 220))
    c.filled_circle(ax + 88, ay - 10, 9, NAVY)
    c.fill_rect(ax + 150, ay - 2, ax + 162, ay + 4, RED)
    # ground line
    c.hline(x0 + 8, y1 - 6, x1 - 8, GREEN)
    c.fill_rect(x0 + 8, y1 - 6, x1 - 8, y1 - 2, GREEN)

def scene_cricket(c, x0, y0, x1, y1):
    """Cricket stumps, bat and ball."""
    c.fill_rect(x0, y0, x1, y1, (190, 220, 170))
    base = y1 - 6
    # pitch strip
    c.fill_rect(x0 + 20, base - 6, x1 - 20, base, (210, 190, 140))
    # stumps
    for sx in (x0 + 40, x0 + 48, x0 + 56):
        c.vline(sx, base - 26, base, (220, 190, 120))
    c.hline(x0 + 40, base - 28, x0 + 58, (220, 190, 120))
    # bat leaning
    c.fill_poly([(x0 + 120, base - 34), (x0 + 132, base - 34),
                 (x0 + 150, base), (x0 + 138, base)], (200, 170, 110))
    c.line(x0 + 126, base - 34, x0 + 112, base - 52, BROWN)
    # ball
    c.filled_circle(x0 + 210, base - 12, 8, RED)
    c.circle(x0 + 210, base - 12, 8, WHITE)
    # score board block
    c.fill_rect(x1 - 90, y0 + 8, x1 - 12, y0 + 24, INK)
    draw_text(c, x1 - 84, y0 + 12, "185", 1, WHITE)

SCENES = {
    'benghazi': scene_benghazi,
    'riyadh': scene_riyadh,
    'huawei': scene_huawei,
    'cyber': scene_cyber,
    'nato': scene_nato,
    'cricket': scene_cricket,
}

# -------------------------------------------------------------------- page
GRID_STORIES = [
    {
        'label': '23 NOV',
        'headline': "UKRAINE SINKS RUSSIAN WARSHIP OFF BENGHAZI",
        'body': "ZELENSKY CONFIRMED SEA DRONES SANK THE CORVETTE MERKURY "
                "OFF LIBYA AND HIT THE CARGO SHIP ANGARA.",
        'scene': 'benghazi',
    },
    {
        'label': '24 NOV',
        'headline': "HOUTHIS HIT RIYADH'S PIF TOWER, 11 WOUNDED",
        'body': "SECOND HIT IN UNDER A WEEK ON THE CAPITAL'S TALLEST "
                "TOWER. 2 SAUDIS, 2 INDIANS, 3 NEPALIS, 4 EGYPTIANS HURT.",
        'scene': 'riyadh',
    },
    {
        'label': '24 NOV',
        'headline': "HUAWEI CONVICTED IN US TRIAL OVER IRAN BUSINESS",
        'body': "GUILTY OF TRADE-SECRET THEFT IN A US CRIMINAL TRIAL. "
                "ACQUITTED OF RACKETEERING.",
        'scene': 'huawei',
    },
    {
        'label': '24 NOV',
        'headline': "CIA AND ODNI HIT BY CYBERSECURITY BREACH",
        'body': "SOME UNCLASSIFIED INFORMATION WAS INVOLVED, "
                "SOURCES TOLD REUTERS.",
        'scene': 'cyber',
    },
    {
        'label': '23-24 NOV',
        'headline': "NATO SENDS EARLY-WARNING AIRCRAFT TO POLAND",
        'body': "EARLY-WARNING AIRCRAFT FOR POLAND AFTER MISSILES LANDED "
                "DURING AN ATTACK ON UKRAINE. NATO ALSO VOWS TO DEFEND SPACE.",
        'scene': 'nato',
    },
    {
        'label': '24 NOV',
        'headline': "ENGLAND BEAT AUSTRALIA BY 8 WICKETS",
        'body': "ENGLAND CHASED 185 TO WIN THE 2ND T20I IN AUSTRALIA.",
        'scene': 'cricket',
    },
]

LEAD_HEADLINE = ("ZELENSKY CONFIRMS UKRAINE DRONE STRIKE ON "
                 "RUSSIAN CARGO SHIP SPARTA II")
LEAD_BODY = ("UKRAINE DRONES HIT THE RUSSIAN-FLAGGED CARGO SHIP SPARTA II "
             "IN THE GULF OF FINLAND. THE SHIP, LINKED TO RUSSIA'S "
             "DEFENCE MINISTRY AND SAID TO BE CARRYING WEAPONS, WAS SET "
             "AFLAME AND DRIFTED INTO FINNISH WATERS BEFORE BEING TOWED "
             "BACK TO ST PETERSBURG. NORWAY, A STRONG KYIV SUPPORTER, "
             "URGED CAUTION.")
LEAD_FACTS = [
    "SHIP: SPARTA II, RUSSIAN-FLAGGED",
    "OWNER: OBORONLOGISTIKA",
    "CARGO: SAID TO BE WEAPONS",
    "AFTERMATH: TOWED TO ST PETERSBURG",
]

def build_page():
    c = Canvas()
    # outer double border
    c.rect(8, 8, 1016, 1016, INK, 3)
    c.rect(14, 14, 1010, 1010, INK, 1)

    # ---- masthead ----
    draw_text_centered(c, 512, 28, "THE WORLD TODAY", 4, INK, tracking=10)
    c.fill_rect(24, 66, 1000, 69, RED)
    c.hline(24, 72, 1000, INK)
    draw_text_centered(c, 512, 82, "WEDNESDAY 25 NOVEMBER 2026", 2, INK)
    draw_text_centered(c, 512, 104, "ONE PAGE - EVERY STORY THAT MATTERED",
                       1, DARKGREY)
    c.hline(24, 118, 1000, INK)

    # ---- lead story panel ----
    c.rect(24, 126, 1000, 484, INK, 2)
    c.fill_rect(26, 128, 998, 482, PAPER)
    # left text column
    draw_text(c, 40, 140, "LEAD STORY - GULF OF FINLAND", 1, RED)
    n = draw_wrapped(c, 40, 158, LEAD_HEADLINE, 3, INK, 460, line_h=24)
    date_y = 158 + n * 24 + 8
    draw_text(c, 40, date_y, "STRIKE 21 NOV - CONFIRMED 24 NOV", 1, RED)
    body_y = date_y + 18
    nb = draw_wrapped(c, 40, body_y, LEAD_BODY, 1, INK, 460, line_h=10)
    # key facts box
    box_y = body_y + nb * 10 + 12
    c.fill_rect(40, box_y, 500, box_y + 76, LIGHT)
    c.rect(40, box_y, 500, box_y + 76, INK, 1)
    draw_text(c, 52, box_y + 8, "KEY FACTS", 1, RED)
    for i, fact in enumerate(LEAD_FACTS):
        draw_text(c, 52, box_y + 22 + i * 12, fact, 1, INK)
    # right illustration
    draw_lead_scene(c, 520, 140, 984, 428)

    # ---- grid of six stories: 3 cols x 2 rows ----
    col_x = [24, 352, 680]
    row_y = [496, 690]
    cell_w, cell_h = 320, 182
    for idx, story in enumerate(GRID_STORIES):
        cx0 = col_x[idx % 3]
        cy0 = row_y[idx // 3]
        cx1 = cx0 + cell_w
        cy1 = cy0 + cell_h
        c.rect(cx0, cy0, cx1, cy1, INK, 1)
        c.fill_rect(cx0 + 1, cy0 + 1, cx1 - 1, cy1 - 1, PAPER)
        # red date label
        draw_text(c, cx0 + 10, cy0 + 10, story['label'], 1, RED)
        c.hline(cx0 + 10, cy0 + 22, cx1 - 10, GREY)
        # headline, scale 2
        nh = draw_wrapped(c, cx0 + 10, cy0 + 30, story['headline'],
                          2, INK, 300, line_h=16)
        # body, scale 1
        body_y = cy0 + 30 + nh * 16 + 4
        draw_wrapped(c, cx0 + 10, body_y, story['body'],
                     1, INK, 300, line_h=10)
        # small scene strip at the bottom of the cell
        sy0 = cy1 - 52
        sy1 = cy1 - 10
        c.rect(cx0 + 10, sy0, cx1 - 10, sy1, INK, 1)
        SCENES[story['scene']](c, cx0 + 11, sy0 + 1, cx1 - 11, sy1 - 1)

    # ---- "also today" footer strip ----
    draw_text(c, 24, 890, "ALSO TODAY -", 1, RED)
    draw_text_centered(
        c, 512, 890,
        "GIULIANI GIVEN THE MEDAL OF FREEDOM - TRUMP PARDONS TURKEYS "
        "FREEDOM AND FEATHERS", 1, INK)
    draw_text_centered(
        c, 512, 906,
        "ANALYSIS: 700,000+ RUSSIAN SOLDIERS KILLED - SOUTH KOREA "
        "EDUCATION MINISTER RESIGNS", 1, INK)
    c.hline(24, 926, 1000, INK)

    # ---- markets ticker strip (no invented figures) ----
    c.fill_rect(24, 938, 1000, 976, INK)
    draw_text_centered(
        c, 512, 952,
        "LONDON - NEW YORK - TOKYO - FRANKFURT - PARIS - SYDNEY - "
        "MARKETS WATCH THE BALTIC", 1, WHITE)

    # ---- credit line ----
    draw_text_centered(
        c, 512, 988,
        "SOURCES: REUTERS - BLOOMBERG - RFE/RL - ALL DATES AS FIRST REPORTED",
        1, DARKGREY)
    return c

# --------------------------------------------------------------------- png
def chunk(ctype, data):
    out = struct.pack('>I', len(data)) + ctype + data
    out += struct.pack('>I', zlib.crc32(ctype + data) & 0xFFFFFFFF)
    return out

def encode_png(c):
    raw = bytearray()
    stride = W * 3
    for y in range(H):
        raw.append(0)  # filter: none
        start = y * stride
        raw += c.px[start:start + stride]
    ihdr = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', ihdr)
    png += chunk(b'IDAT', zlib.compress(bytes(raw), 6))
    png += chunk(b'IEND', b'')
    return png

def main():
    out_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output/entry.png')
    out_path = out_dir if out_dir.endswith('.png') else os.path.join(out_dir, 'entry.png')
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    canvas = build_page()
    data = encode_png(canvas)
    with open(out_path, 'wb') as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (out_path, len(data)), file=sys.stderr)
    return 0

if __name__ == '__main__':
    sys.exit(main())
