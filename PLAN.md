# newsimage25 — PLAN

## Competition

- **Slug:** `news-image-20261125`
- **Title:** Sum up 25 November's world news in one image
- **Prize:** $100
- **Deadline:** 2026-11-27T00:00:00Z = 2026-11-27 07:00 WIB
- **Account:** @katzuomaru (make.fun) · GitHub: yzrzlwirmansyah
- **Repo:** https://github.com/yzrzlwirmansyah/newsimage25
- **Local path:** `/home/hatch/workspace/makefun/newsimage25`
- **Kit path:** `/home/hatch/workspace/makefun/news-image-20261125-kit/news-image-20261125-kit`
- **Referral code:** `er9011hp` (verified 24 Nov; to be re-verified live before submit)

## Anchor (turn t1)

```
makefun anchor 4e1adde340bdf2775d5eab5fbc25022a226d2831 round 34255617
```

Init run first, before any file write, per the make.fun freshness rule.
Local git identity is the wallet `3PzMbJEm38BnNzmedWJY5GuJQRGytFGWBQcHEzdn4QtE`
(name and email). Remote `origin` set to the GitHub URL above. Nothing pushed
in t1 — push happens in a later turn.

## Entry design

- `main.py` at repo root, **Python 3.13 stdlib only** (no pip installs, no
  network at runtime — deterministic, reproducible).
- Draws a **1024×1024 newspaper front page** ("THE WORLD — 25 NOVEMBER 2026")
  with a masthead, one lead story with a large illustration panel, and 5–6
  shorter stories in columns, each with a date label.
- Writes `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`),
  **max 1 MiB**.
- All artwork drawn in code (no external images, no fonts beyond what the
  stdlib/PIL-free drawing can do — pure-Python PNG via `zlib`/`struct`, or
  stdlib only; keep it self-contained).
- **Date honesty rule:** the judge only credits events that happened or were
  first reported on 25 Nov 2026 in any timezone. Every story on the page
  carries its true report date; items first reported 24 Nov are labelled
  "24 Nov" and are supporting items, while items first reported 25 Nov get
  the 25 Nov label. No invented figures — every number comes from a checked
  source (see recon below).

## Recon summary (verified 25 Nov ~01:20 UTC, re-checked 08:30 WIB)

1. **Zelensky confirms Ukraine hit a Russian cargo ship in the Gulf of
   Finland.** Strike was Saturday 21 Nov; confirmation in a Bloomberg
   interview late Mon 23 Nov, reported Tue 24 Nov (Reuters/Bloomberg).
   Ship: Russian-flagged **Sparta II**, owned by Oboronlogistika (Russian
   Defence Ministry logistics), bound for Kaliningrad, said by Zelensky to
   be carrying weapons (Bloomberg could not independently verify). It
   drifted into Finnish waters after being struck and set aflame; Finnish,
   Estonian and Russian vessels fought the fire; towed back to St Petersburg
   on Sunday. Norway, a strong Kyiv supporter, urged caution.
2. **Houthis strike Riyadh's PIF Tower (tallest tower), 11 wounded** —
   Tue 24 Nov, second hit in under a week (first was 19 Nov, no injuries).
   Saudi Civil Defence: 2 Saudis, 2 Indians, 3 Nepalis, 4 Egyptians hurt.
   Saudi-led coalition says it was a drone; Houthis had not claimed it by
   16:00 GMT 24 Nov.
3. **China's Huawei convicted in a US criminal trial over Iran business**
   — guilty of trade-secret theft, acquitted of racketeering (reported
   24 Nov).
4. **Trump awards Rudy Giuliani the Presidential Medal of Freedom**
   (reported 24 Nov).
5. **US CIA and ODNI suffered a cybersecurity breach** involving some
   unclassified information (Reuters, source says; reported 24 Nov).
6. **NATO plans early-warning aircraft deployment in Poland** after
   missiles landed during an attack on Ukraine (reported 24–25 Nov).
7. **South Korea's education minister resigns** over an exam-cheating
   scandal.
8. **New analysis: more than 700,000 Russian soldiers killed** in the
   Ukraine war (RFE/RL, 25 Nov).
9. **England beat Australia by 8 wickets in the 2nd T20I**, chasing 185
   (24 Nov).
10. **NATO vows space defence** amid reports Russia is preparing a
    nuclear-armed satellite launch.
11. **Trump pardons Thanksgiving turkeys "Freedom" and "Feathers"**
    (24 Nov).

## Fresh check (25 Nov ~08:30 WIB) — new items

- **Ukraine sank a Russian warship off Benghazi, Libya** (Zelensky
  confirmed; RFE/RL published 2026-11-25 01:00 UTC). Same widening
  retaliation campaign as the Gulf of Finland strike — strong companion to
  the lead, and genuinely first reported 25 Nov.
- **Russian drone attack on an apartment block near Kyiv: 11 killed**
  (RFE/RL, 25 Nov).
- **Houthis pushed to within 60 km of Aden**; Yemeni military says they
  will not capture the city (Reuters, Tue 24 Nov).
- **Fort Hood shooter Nidal Hasan seeks a stay of execution** set for
  next week (US court records, Tue 24 Nov).
- **French officials order ex-President Sarkozy's corruption case to
  trial**; pre-trial hearing 1 Apr 2027 (Tue 24 Nov).
- **Iran's Revolutionary Guard Navy claims three oil tankers hit by naval
  mines in the Strait of Hormuz** — single aggregator source so far;
  treat as unconfirmed, do not headline it.
- No bigger 25-November story broke overnight that displaces the lead.

## Lead-story pick

**Lead: Zelensky confirms the Gulf of Finland strike on the Sparta II.**
Most consequential: a Ukrainian drone strike on a Russian military-linked
cargo ship in NATO-adjacent Baltic waters, openly claimed by a head of
state, with an ally (Norway) publicly urging restraint — escalation signal
plus alliance friction in one story. The Benghazi sinking runs as the
second story (same campaign, first reported 25 Nov).

## Stories for the page (7)

1. LEAD — Ukraine confirms Gulf of Finland strike on Sparta II (label: strike 21 Nov, confirmed 24 Nov).
2. Ukraine sinks Russian warship off Benghazi, Libya (25 Nov).
3. Houthis hit Riyadh's PIF Tower again, 11 wounded (24 Nov).
4. Huawei convicted in US criminal trial over Iran business (24 Nov).
5. CIA/ODNI cybersecurity breach, some unclassified data (24 Nov).
6. NATO early-warning aircraft for Poland; NATO vows space defence (24–25 Nov).
7. Sport — England beat Australia by 8 wickets, 2nd T20I, chasing 185 (24 Nov).

Small footer items (if space): Giuliani Medal of Freedom; turkey pardon
("Freedom" and "Feathers"); 700,000+ Russian soldiers killed (analysis);
South Korea education minister resigns.

## Build order (later turns)

- t2: `main.py` (stdlib-only, 1024×1024, writes entry.png ≤ 1 MiB).
- t3: run, verify output + size, commit, push, submit.
- Before submit: re-verify referral code `er9011hp` live.
