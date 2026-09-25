---
name: testing-farm-preview
description: How to serve, drive, and verify the Sunpetal Valley browser preview (WebPreview / farm_preview_build) end-to-end
---

# Testing the Sunpetal Valley preview

## Serve
- `python3 -m http.server 8123 -d /home/ubuntu/farm_preview_build` (or repo `WebPreview/` — identical bundle). Open `http://localhost:8123/index.html`.
- Everything is inlined in index.html (MDATA/ADATA/ATLAS_SRC/AUDIO consts) — no fetch, so it also works in a WebView `file://` context.
- To drive it headless: Playwright `connect_over_cdp('http://localhost:29229')` on the box's Chrome; `pg.mouse.click`/`pg.keyboard` work, and `pg.evaluate` reaches game globals.

## Flow / states
`G.state`: `title` → `intro` (4 VO slides, tap/E advances) → `play` (or `dlg`/`shop`/`bag`/`festival`).
Title tap starts the intro; 4 taps advance all slides.

## Globals (all under `G`)
`G.hero.x/y/dir`, `G.map` ('farm'|'village'), `G.L` (current map layers), `G.objs`, `G.crops[mapId]['x,y']`,
`G.gold`, `G.day`, `G.clock` (minutes), `G.inv.seed/crop`, `G.selSeed`, `G.flags` (metBram, planted, watered,
harvested, sold2, mq2done, haveSunseed, sunpetalPlanted, sunpetalBloom, festival, metAll, fedFen).
Helpers: `loadMap(id,x,y)`, `interact()`, `talkTo(obj)`, `skipHour()` (+60min), `openShop()`, `toggleBag()`.

## Maps
- farm 64×40: exit x30-33 y0 → village (spawn 31.5,36.5). Beds pre-tilled (G.crops.farm).
- village 64×40: exit x30-33 y39 → farm. Plaza ~y14-20, torii shrine y6-8, festival beds x28-30+33-35 y9-10
  (Sunpetal-only, gated by `flags.haveSunseed`). NPCs: bram (32,17), sari shop stall (39,16.8), vilo (26,18), nana (37,18.5).
- NPC `meta.id` gates dialogs in `DIALOGS{}`; `meta.portrait` key drives the animated portrait box.

## Controls
WASD/arrows move, Shift/RUN run, E/A interact (+advance dialog), T/T+ skip hour, B/I bag, Q cycles selected seed, Esc closes panels. Touch UI auto-shows (joystick + A/BAG/RUN/T+).

## Main quest chain (for E2E)
1. Met Bram (vo_bram1) → 2. plant 3 seeds → 3. harvest 4 → 4. sell 2 to Sari → 5. report to Bram (vo_bram2)
→ 6. buy Sunpetal Seed 100g → 7. plant in shrine beds → water → next day `sunpetalBloom`
→ 8. talk to Bram → vo_finale + festival state.

## Fast-travel / cheat evals
`loadMap('village',31.5,18.5)` to stand next to Bram; `G.gold=200`; `G.inv.crop[8]=5` to add crops;
`G.flags.mq2done=true` to unlock the Sunpetal Seed in the shop.

## Rebuild pipeline
`gen_farm_slice.py` → map.json + sprites; `gen_village.py` → village.json; `bake_game.py` merges both into
one atlas + inlines audio/icon → `farm_preview_build/index.html` (also copied to `apkproj/.../assets/www/`).
APK: aapt2 compile/link + javac + d8 + `zip -0` classes.dex + zipalign + apksigner (keystore /tmp/cozy.keystore —
recreate if /tmp was wiped: `keytool -genkeypair -alias cozy -storepass cozyfarm -keypass cozyfarm`).
