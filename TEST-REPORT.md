# TEST REPORT — news-image-20261125 (turn t3)

Date: 2026-11-25 (WIB). Repo: `/home/hatch/workspace/makefun/newsimage25`.
Tester: turn t3 (test). No commit or push made.

## Anchor (first action)

```
cd /home/hatch/workspace/makefun/newsimage25 && node /home/hatch/workspace/makefun/news-image-20261125-kit/news-image-20261125-kit/cli/makefun.mjs init --license MIT --keypair /home/hatch/workspace/makefun/makefun-keypair.json
```

Output: `makefun anchor 4e1adde340bdf2775d5eab5fbc25022a226d2831 round 34255617`

## Commands run

```
MAKEFUN_OUTPUT_DIR=/tmp/news25-run1 python3 main.py
MAKEFUN_OUTPUT_DIR=/tmp/news25-run2 python3 main.py
```

Both runs executed from the repo directory.

## Results

| Check | Result |
|---|---|
| Run 1 succeeds | PASS — `wrote /tmp/news25-run1/entry.png (39047 bytes)`, 0.61 s |
| Run 2 succeeds | PASS — `wrote /tmp/news25-run2/entry.png (39047 bytes)`, 0.57 s |
| Both within 60 s | PASS (~0.6 s each) |
| PNG signature | PASS — `89 50 4E 47 0D 0A 1A 0A` on both |
| IHDR | PASS — width 1024, height 1024, bit depth 8, colour type 2, compression 0, filter 0, interlace 0 (both) |
| File size < 1 MiB | PASS — 39,047 bytes each (limit 1,048,576) |
| IDAT decodes fully | PASS — zlib-decompressed pixel data 3,146,752 bytes = exactly 1024 × (1 + 1024 × 3) on both |
| Determinism (byte-identical) | PASS — sha256 identical across both runs |

## sha256 hashes

```
9b398407744e329d3f42e730b901f12e820562287661b7c9b9fd674465aa6fc9  /tmp/news25-run1/entry.png
9b398407744e329d3f42e730b901f12e820562287661b7c9b9fd674465aa6fc9  /tmp/news25-run2/entry.png
```

File size: **39,047 bytes** (both runs).

## Visual check

Read `/tmp/news25-run1/entry.png` directly and inspected it.

- Masthead "THE WORLD TODAY" large and legible; "WEDNESDAY 25 NOVEMBER 2026" and tagline "ONE PAGE - EVERY STORY THAT MATTERED" clearly readable.
- Lead headline "ZELENSKY CONFIRMS UKRAINE DRONE STRIKE ON RUSSIAN CARGO SHIP SPARTA II" — three lines, no overlap, no clipping. Body text and KEY FACTS box fully legible.
- Lead scene (cargo ship Sparta II aflame in the Gulf of Finland, drone, smoke, shoreline) recognisable; caption legible.
- Six lower stories all legible, headlines wrapped cleanly with no overlap or clipping:
  - "UKRAINE SINKS RUSSIAN WARSHIP OFF BENGHAZI" (sinking-ship scene)
  - "HOUTHIS HIT RIYADH'S PIF TOWER, 11 WOUNDED" (skyline + blast scene)
  - "HUAWEI CONVICTED IN US TRIAL OVER IRAN BUSINESS" (courthouse scene)
  - "CIA AND ODNI HIT BY CYBERSECURITY BREACH" (server + padlock scene)
  - "NATO SENDS EARLY-WARNING AIRCRAFT TO POLAND" (aircraft scene)
  - "ENGLAND BEAT AUSTRALIA BY 8 WICKETS" (cricket pitch, "185" label matches body text)
- Footer "ALSO TODAY" items, black city/market bar, and sources line all readable.
- No garbled text, no overlapping or clipped text, no self-contradiction spotted (dates consistent: strike 21 Nov, confirmed 24 Nov, paper dated 25 Nov).

**Visual check: PASS.** No layout/text problem found.

## Fixes made

None. No run failed, no check failed, no legibility problem found, so `main.py` was not edited. Before/after hashes are therefore not applicable (single hash above covers both runs).

## Overall verdict

**PASS — all checks passed.** Entry is deterministic, valid 1024×1024 PNG, 39,047 bytes, and visually clean. Ready for submission.

---

# TEST REPORT — addendum, turn t4 (revise), 2026-11-25

Re-tested after t4 edits (see REVISE.md). Edits: Benghazi label
`REPORTED 25 NOV` → `23 NOV` + body now names corvette Merkury / cargo ship
Angara; NATO label `24-25 NOV` → `23-24 NOV`; `scene_benghazi` redrawn
compactly so its smoke/hull no longer paint over the body text (pre-existing
overlap caught on a cropped zoom).

Commands run (from repo directory):

```
MAKEFUN_OUTPUT_DIR=/tmp/news25-rev1 python3 main.py
MAKEFUN_OUTPUT_DIR=/tmp/news25-rev2 python3 main.py
```

| Check | Result |
|---|---|
| Run 1 succeeds | PASS — `wrote /tmp/news25-rev1/entry.png (38568 bytes)` |
| Run 2 succeeds | PASS — `wrote /tmp/news25-rev2/entry.png (38568 bytes)` |
| PNG signature | PASS — `89 50 4E 47 0D 0A 1A 0A` on both |
| IHDR | PASS — 1024×1024, bit depth 8, colour type 2 |
| File size < 1 MiB | PASS — 38,568 bytes each |
| IDAT decodes fully | PASS — 3,146,752 bytes = 1024 × (1 + 1024 × 3) |
| Determinism (byte-identical) | PASS — sha256 identical across both runs |

## sha256 hashes (t4, supersedes t3)

```
79c0d4f986f437f79d32d0bfd64ffcf218fb517881a0af6e3a831fd2a4488bba  /tmp/news25-rev1/entry.png
79c0d4f986f437f79d32d0bfd64ffcf218fb517881a0af6e3a831fd2a4488bba  /tmp/news25-rev2/entry.png
```

Old t3 hash (pre-edit): `9b398407744e329d3f42e730b901f12e820562287661b7c9b9fd674465aa6fc9`.

## Visual check (t4)

Full page re-read plus a 2× crop of the Benghazi cell: corrected labels render
as "23 NOV" (Benghazi) and "23-24 NOV" (NATO); Benghazi body text fully legible
with ship/flame/smoke contained inside the scene strip; no overlap or clipping
anywhere else. **Visual check: PASS.**

Xingchi review: attempted twice, failed both times (local code-mode host binary
`/opt/hatch-image/bin/codex-code-mode-host` missing — relay connected but Codex
could not read main.py). See REVISE.md.

## Overall verdict (t4)

**PASS — all checks passed after corrections.** Deterministic, valid 1024×1024
PNG, 38,568 bytes, visually clean. Ready for submission.
