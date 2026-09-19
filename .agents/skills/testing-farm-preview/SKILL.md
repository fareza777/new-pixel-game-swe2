---
name: testing-farm-preview
description: How to serve, drive, and verify the Cozy Farm browser preview (WebPreview / farm_preview_build) end-to-end
---

# Testing the Cozy Farm browser preview

## Serve
- Serve the static folder: `python3 -m http.server 8123` from `/home/ubuntu/farm_preview_build` (or repo `WebPreview/` — identical). Then open `http://localhost:8123/index.html` in Chrome and click the title overlay to start.
- No build step, no secrets needed. `map.json` + `sprites/` are loaded by `index.html` at boot.

## Driving the game
- Keys: WASD/arrows move, Shift run, E interact, T = +60 in-game min. Real key taps via the computer tool reach the page; for sustained movement use `hold_key` (durations ≥1s work, sub-0.5s can act like taps). Shell `xdotool keydown/keyup` did NOT reach the page in this env — don't rely on it.
- Time flows 8 game-min per real second; a full day ≈ 3 min real. Don't fight the clock — press T to jump.
- The heart/`-<3` marker on petting lasts only ~1s (60 frames) — too fast for the computer screenshot. Verify via console `objs.find(o=>(o.meta||{}).name=='kucing').heart` (==60 right after E) or capture during `hold_key e` auto-repeat with a background `scrot`.

## Verifying state (console globals — all top-level bindings)
`hero.x/hero.y`, `crops` (map "x,y" → {crop,stage,watered,soil}), `seeds`, `gold`, `day`, `clock` (minutes), `objs`, `blocked(x,y)`, `L` (layers), `M.sprites`. Use `browser_console` evals to read positions/states; screenshots alone can't prove movement because the camera re-centers the hero.

## Key map facts (map.json, 64x40)
- Spawn (16.5,22.5); house solid x13-18 y18-21 with a walkable gap at x19; chest (20.8,20.9) +25g opened via E from cell (20,20)/(21,20) — NOT open-on-contact.
- Tilled cells: rows y6-7 (x9-16 west, x21-28 + 22,23 y7 east). Staged decor crops sit on odd-x y7 cells — plant on even-x or row y6 to avoid sprite overlap.
- NPCs: Mira (24.5,16.4), Old Fen (47.5,24.3) — Old Fen only reachable from cell (46,24) (west-south-east around pond edge; 46,23 is water).
- Cat "kucing" (14.3,21.5); 3 pigs wander bounded x34-43 y10-17.
- Pond water x46-60 y21-32 blocks movement. Some rail fences solid (e.g. x24-25 y16); pen/bed border fences are NOT solid (hero can walk into the pen).

## Known gaps to look for (as of PR #1)
- No watering action in the preview: E on a dry crop plants a new seed on the next empty soil cell instead; crops freeze at stage 2 and never reach harvest stage via gameplay. Harvest code works if stage is forced (`crops['x,y'].stage=5` → E → +12g).
- Chest needs an E press, not contact-open (differs from Unity prefab behavior).
