#!/usr/bin/env python3
"""v1.9 extras: hero house interior map, Sunpetal Forest map, farm/village patches,
   PIL-generated furniture/deco sprites matching the Super Retro palette."""
import json, os, math, random
from PIL import Image, ImageDraw

OUT = "/home/ubuntu/farm_preview_build"
SPR = os.path.join(OUT, "sprites")
random.seed(42)

# ---------------------------------------------------------------- PIL sprites
def spr(key, w, h, fn):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fn(ImageDraw.Draw(im))
    im.save(os.path.join(SPR, key + ".png"))
    return {"key": key, "w": w, "h": h}

def px(d, x, y, w, h, c): d.rectangle([x, y, x + w - 1, y + h - 1], fill=c)

WOOD = (146, 102, 62); WOOD_D = (110, 74, 44); WOOD_L = (178, 132, 84)
CREAM = (244, 232, 205); RED = (196, 82, 60); RED_D = (150, 58, 42)
TEAL = (76, 158, 148); GOLD = (238, 196, 90); STONE = (120, 118, 128)
STONE_D = (84, 82, 96); LEAF = (86, 156, 92); LEAF_D = (58, 116, 66)

sprites = {}

# wood floor tile 16x16 — horizontal planks
def _floor(d):
    px(d, 0, 0, 16, 16, WOOD)
    for yy in (0, 5, 10):
        px(d, 0, yy + 4, 16, 1, WOOD_D)
    px(d, 5, 0, 1, 4, WOOD_D); px(d, 12, 5, 1, 5, WOOD_D); px(d, 3, 10, 1, 5, WOOD_D)
    px(d, 0, 0, 16, 1, WOOD_L)
sprites["floor_wood"] = spr("floor_wood", 16, 16, _floor)

# wall tile 16x16 — warm plaster with wood trim bottom
def _wall(d):
    px(d, 0, 0, 16, 16, (214, 190, 156))
    px(d, 0, 12, 16, 4, WOOD_D)
    px(d, 0, 12, 16, 1, WOOD_L)
    px(d, 3, 3, 2, 2, (196, 170, 136)); px(d, 10, 7, 2, 2, (196, 170, 136))
sprites["wall_wood"] = spr("wall_wood", 16, 16, _wall)

# wall top band 16x32 (drawn on row0 cells, covers rows 0-1 visually)
def _walltop(d):
    px(d, 0, 0, 16, 32, (60, 44, 38))
    px(d, 0, 20, 16, 12, (214, 190, 156))
    px(d, 0, 20, 16, 2, WOOD_L)
    for x in (3, 9):
        px(d, x, 24, 3, 3, (180, 154, 120))
sprites["wall_top"] = spr("wall_top", 16, 32, _walltop)

# bed 48x30 — wood frame, pillow, blanket
def _bed(d):
    px(d, 0, 0, 48, 30, WOOD_D)                       # frame
    px(d, 2, 2, 44, 26, CREAM)                        # mattress
    px(d, 0, 0, 48, 3, WOOD_L); px(d, 0, 27, 48, 3, WOOD_L)
    px(d, 4, 6, 14, 18, (250, 248, 240))              # pillow
    px(d, 4, 6, 14, 3, (226, 220, 204))
    px(d, 20, 4, 24, 22, RED)                         # blanket
    px(d, 20, 4, 24, 3, RED_D); px(d, 20, 14, 24, 2, RED_D)
    for x in range(22, 44, 6): px(d, x, 7, 2, 18, GOLD)
    px(d, 0, 0, 2, 30, WOOD_L); px(d, 46, 0, 2, 30, WOOD_L)
sprites["bed_01"] = spr("bed_01", 48, 30, _bed)

# table 32x22
def _table(d):
    px(d, 0, 0, 32, 14, WOOD_L)
    px(d, 0, 12, 32, 3, WOOD_D)
    px(d, 2, 15, 4, 7, WOOD_D); px(d, 26, 15, 4, 7, WOOD_D)
    px(d, 12, 3, 8, 6, (233, 120, 90))                # fruit bowl
    px(d, 14, 1, 4, 3, LEAF)
sprites["table_01"] = spr("table_01", 32, 22, _table)

# chair 16x20
def _chair(d):
    px(d, 3, 0, 10, 9, WOOD_L)
    px(d, 3, 9, 10, 4, WOOD)
    px(d, 3, 13, 3, 7, WOOD_D); px(d, 10, 13, 3, 7, WOOD_D)
sprites["chair_01"] = spr("chair_01", 16, 20, _chair)

# bookshelf 32x40
def _shelf(d):
    px(d, 0, 0, 32, 40, WOOD_D)
    px(d, 2, 2, 28, 36, (58, 40, 26))
    cols = [(196, 82, 60), (76, 158, 148), (238, 196, 90), (120, 118, 170), (86, 156, 92), (210, 140, 100)]
    i = 0
    for sy in (4, 15, 26):
        px(d, 3, sy + 8, 26, 2, WOOD_L)
        x = 4
        while x < 26:
            w = random.choice((2, 3))
            h = random.choice((6, 8))
            px(d, x, sy + 8 - h, w, h, cols[i % len(cols)])
            i += 1; x += w + 1
sprites["shelf_01"] = spr("shelf_01", 32, 40, _shelf)

# fireplace 32x32 — stone hearth + fire
def _firep(d):
    px(d, 0, 8, 32, 24, STONE)
    px(d, 0, 8, 32, 3, STONE_D); px(d, 0, 0, 10, 10, STONE)
    px(d, 4, 14, 24, 16, (40, 30, 30))
    px(d, 9, 22, 14, 6, (140, 70, 30))
    px(d, 11, 16, 10, 10, (240, 150, 60)); px(d, 13, 13, 6, 8, (255, 210, 90))
    px(d, 14, 11, 4, 5, (255, 244, 180))
sprites["fireplace_01"] = spr("fireplace_01", 32, 32, _firep)

# rug tiles 16x16 — red border / woven center
def _rugc(d):
    px(d, 0, 0, 16, 16, RED)
    for x in (4, 10): px(d, x, 0, 2, 16, GOLD)
    px(d, 0, 6, 16, 1, RED_D)
sprites["rug_c"] = spr("rug_c", 16, 16, _rugc)
def _rugb(d):
    px(d, 0, 0, 16, 16, RED_D)
    px(d, 2, 2, 12, 12, RED)
    px(d, 6, 6, 4, 4, GOLD)
sprites["rug_b"] = spr("rug_b", 16, 16, _rugb)

# doormat 16x16
def _mat(d):
    px(d, 0, 2, 16, 12, (160, 110, 70))
    px(d, 0, 2, 16, 2, (120, 80, 50)); px(d, 0, 12, 16, 2, (120, 80, 50))
    for x in range(2, 16, 4): px(d, x, 5, 2, 6, (140, 95, 60))
sprites["doormat"] = spr("doormat", 16, 16, _mat)

# window 20x24 — hangs on top wall
def _win(d):
    px(d, 0, 0, 20, 24, WOOD_D)
    px(d, 2, 2, 16, 20, (140, 190, 220))
    px(d, 9, 2, 2, 20, WOOD_D); px(d, 2, 10, 16, 2, WOOD_D)
    px(d, 4, 4, 4, 5, (190, 225, 245))
sprites["window_01"] = spr("window_01", 20, 24, _win)

# bench 32x16 — for the village plaza
def _bench(d):
    px(d, 0, 0, 32, 6, WOOD_L)
    px(d, 0, 8, 32, 5, WOOD)
    px(d, 3, 13, 4, 3, WOOD_D); px(d, 25, 13, 4, 3, WOOD_D)
sprites["bench_01"] = spr("bench_01", 32, 16, _bench)

# flowers 16x16 x3 colors
def _flower(c):
    def f(d):
        px(d, 7, 8, 2, 8, LEAF_D)
        px(d, 5, 4, 6, 6, c); px(d, 7, 2, 2, 2, c)
        px(d, 7, 6, 2, 2, GOLD)
        px(d, 4, 10, 3, 2, LEAF); px(d, 9, 12, 3, 2, LEAF)
    return f
sprites["flower_r"] = spr("flower_r", 16, 16, _flower((226, 90, 90)))
sprites["flower_y"] = spr("flower_y", 16, 16, _flower((240, 200, 80)))
sprites["flower_b"] = spr("flower_b", 16, 16, _flower((120, 150, 235)))

# mushroom 16x16 — forageable
def _mush(d):
    px(d, 6, 8, 5, 7, (235, 225, 200))
    px(d, 3, 3, 11, 7, (210, 80, 70))
    px(d, 5, 4, 2, 2, (255, 240, 230)); px(d, 10, 5, 2, 2, (255, 240, 230))
sprites["mushroom_01"] = spr("mushroom_01", 16, 16, _mush)

# herb bush 16x16 — forageable
def _herb(d):
    for x, y, c in ((7, 2, LEAF), (4, 6, LEAF), (10, 6, LEAF_D), (7, 9, LEAF), (3, 10, LEAF_D), (11, 10, LEAF)):
        px(d, x, y, 4, 4, c)
    px(d, 7, 12, 3, 3, (70, 50, 30))
sprites["herb_01"] = spr("herb_01", 16, 16, _herb)

# ---- tool icons (20x20) for the new equipment UI ----
def _hoe(d):
    px(d, 9, 4, 3, 13, WOOD_D)
    px(d, 9, 4, 3, 2, WOOD_L)
    px(d, 4, 2, 12, 3, (170, 175, 190))
    px(d, 3, 3, 3, 6, (120, 125, 140))
sprites["tool_hoe"] = spr("tool_hoe", 20, 20, _hoe)
def _can(d):
    px(d, 5, 7, 10, 10, (90, 140, 190))
    px(d, 5, 7, 10, 3, (120, 175, 225))
    px(d, 15, 9, 4, 2, (90, 140, 190)); px(d, 18, 8, 2, 4, (90, 140, 190))
    px(d, 2, 5, 4, 2, (90, 140, 190)); px(d, 2, 3, 2, 4, (90, 140, 190))
sprites["tool_can"] = spr("tool_can", 20, 20, _can)
def _basket(d):
    px(d, 3, 8, 14, 9, (170, 120, 60))
    px(d, 3, 8, 14, 2, (200, 150, 85))
    for x in (5, 9, 13): px(d, x, 10, 1, 7, (140, 95, 45))
    px(d, 7, 4, 6, 4, (0, 0, 0, 0)); px(d, 6, 4, 8, 2, (200, 150, 85))
sprites["tool_basket"] = spr("tool_basket", 20, 20, _basket)
def _letter(d):
    px(d, 2, 4, 16, 12, CREAM)
    px(d, 2, 4, 16, 2, (226, 214, 185))
    px(d, 2, 4, 8, 1, (190, 170, 140)); px(d, 8, 4, 2, 6, (190, 170, 140))
    px(d, 9, 9, 4, 4, RED)
sprites["item_letter"] = spr("item_letter", 20, 20, _letter)

# ---------------------------------------------------------------- HOUSE map
HW, HH = 16, 11
hground = {f"{x},{y}": "floor_wood" for x in range(HW) for y in range(HH)}
hdecor = {}
hsolid = []
# walls: top band rows 0-1, sides, bottom except door gap x7-8
for x in range(HW):
    hdecor[f"{x},0"] = "wall_top"
    hdecor[f"{x},1"] = "wall_wood"
    hsolid += [[x, 0], [x, 1]]
for y in range(2, 10):
    hdecor[f"0,{y}"] = "wall_wood"; hdecor[f"15,{y}"] = "wall_wood"
    hsolid += [[0, y], [15, y]]
for x in range(HW):
    if x in (7, 8): continue
    hdecor[f"{x},10"] = "wall_wood"; hsolid.append([x, 10])
# rug in the middle
for x in range(5, 9):
    for y in range(5, 8):
        hdecor[f"{x},{y}"] = "rug_b" if (x in (5, 8) or y in (5, 7)) else "rug_c"
hdecor["7,9"] = "doormat"; hdecor["8,9"] = "doormat"
# windows on top wall
hdecor["5,1"] = "window_01"; hdecor["10,1"] = "window_01"

hobjects = [
    {"key": "bed_01", "x": 3.5, "y": 3.0, "meta": {"kind": "bed", "name": "Your bed"}},
    {"key": "fireplace_01", "x": 8.5, "y": 2.6, "meta": {"kind": "deco", "name": "Fireplace", "light": True}},
    {"key": "shelf_01", "x": 13.5, "y": 2.4, "meta": {"kind": "deco", "name": "Bookshelf"}},
    {"key": "table_01", "x": 12.0, "y": 6.0, "meta": {"kind": "deco", "name": "Table"}},
    {"key": "chair_01", "x": 10.5, "y": 6.6, "meta": {"kind": "deco"}},
    {"key": "chair_01", "x": 13.5, "y": 6.6, "meta": {"kind": "deco"}},
    {"key": "pot10", "x": 1.5, "y": 2.6, "meta": {"kind": "deco"}},
    {"key": "crate_03", "x": 14.5, "y": 8.6, "meta": {"kind": "deco", "name": "Storage crate"}},
    {"key": "torch_05", "x": 1.5, "y": 5.5, "anim": {"frames": ["torch_f0", "torch_f1", "torch_f2"], "fps": 6},
     "meta": {"kind": "deco", "name": "Lamp", "light": True}},
]
hsolid += [[2, 2], [3, 2], [4, 2], [7, 2], [8, 2], [9, 2], [13, 2], [14, 2],
           [11, 5], [12, 5], [10, 6], [13, 6], [1, 2], [14, 8], [1, 5]]

house = {"W": HW, "H": HH, "id": "house",
         "layers": {"W": HW, "H": HH, "ground": hground, "decor": hdecor,
                    "objects": hobjects, "solid": sorted(hsolid),
                    "water_cells": [], "spawn": {"x": 7.5, "y": 8.6},
                    "exits": [{"x0": 7, "y0": 10, "x1": 8, "y1": 10,
                               "to": "farm", "sx": 15.5, "sy": 24.6}],
                    "tilled_cells": []},
         "sprites": {k: k + ".png" for k in sprites}}
json.dump(house, open(os.path.join(OUT, "house.json"), "w"))
print("house.json written")

# ---------------------------------------------------------------- FOREST map
FW, FH = 40, 28
fgrass, fdirt, fdecor, fobjects, fsolid = {}, {}, {}, [], set()

def cell_solid(x, y): fsolid.add((x, y))
def obj(key, x, y, **kw):
    o = {"key": key, "x": x, "y": y}; o.update(kw); fobjects.append(o)
# base grass
gtiles = {}
AM = json.load(open("/home/ubuntu/autotile_map_full.json"))
def asset_guid(suffix):
    for g, d in AM.items():
        if d["path"].endswith(suffix): return g
    raise KeyError(suffix)
G_GRASS = asset_guid("single/New FangAuto Tile.asset")
G_DIRT = asset_guid("single/New FangAuto Tile 25.asset")
DIRS8 = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
CARD = [0, 2, 4, 6]
def resolve_tile(guid, grid, x, y):
    mask = 0
    for i, (dx, dy) in enumerate(DIRS8):
        if (x + dx, y + dy) in grid: mask |= 1 << i
    tab = AM[guid]["masks"]; cands = None
    for m in (mask, mask & 0b01010101):
        if str(m) in tab: cands = tab[str(m)]; break
    if cands is None:
        for i in CARD:
            pass
        for i, (dx, dy) in enumerate(DIRS8):
            if i in CARD: continue
            if mask >> i & 1:
                m3 = mask & ~(1 << i)
                if str(m3) in tab: cands = tab[str(m3)]; break
    if cands is None:
        cands = tab.get("255") or next(iter(tab.values()))
    dom = {}
    for cc in tab.values():
        for k, v in cc.items():
            g = k.split(",")[0]; dom[g] = dom.get(g, 0) + v
    dg = max(dom, key=dom.get)
    own = {k: v for k, v in cands.items() if k.split(",")[0] == dg} or cands
    sg, fid = sorted(own.items(), key=lambda kv: -kv[1])[0][0].split(",")
    return sg, fid

import sys
sys.path.insert(0, "/home/ubuntu")
from render_scene import get_sprite, load_img
def export_asset(key, sg, fid):
    s = get_sprite(sg, int(fid))
    img, (x, y, w, h) = s
    iy = img.height - (y + h)
    sp = img.crop((int(x), int(iy), int(x + w), int(iy + h)))
    sp.save(os.path.join(SPR, key + ".png"))
    sprites[key] = {"key": key, "w": w, "h": h}
    return key

def resolve_layer(gridset, guid, prefix):
    tiles = {}
    for x in range(FW):
        for y in range(FH):
            if (x, y) not in gridset: continue
            sg, fid = resolve_tile(guid, gridset, x, y)
            key = f"{prefix}_{sg[:4]}_{fid}"
            if key not in sprites: export_asset(key, sg, fid)
            tiles[(x, y)] = key
    return tiles

allcells = {(x, y) for x in range(FW) for y in range(FH)}
fgrass = resolve_layer(allcells, G_GRASS, "g")

# winding dirt path: west entrance (y19-21) → south curve → clearing at east
path = set()
for x in range(0, 10):
    path |= {(x, 20), (x, 21)}
for x in range(9, 15):
    for y in range(20 - (x - 9), 22 - (x - 9) + 1):
        path.add((x, y))
for x in range(14, 22):
    path |= {(x, 15), (x, 16)}
for x in range(21, 27):
    for y in range(15 - (x - 21), 17 - (x - 21) + 1):
        path.add((x, y))
for x in range(26, 40):
    path |= {(x, 10), (x, 11)}
# clearing bowl (dirt circle) at east
for x in range(28, 38):
    for y in range(6, 16):
        if math.hypot(x - 32.5, y - 10.5) < 5.2: path.add((x, y))
fdirt = resolve_layer(path, G_DIRT, "d")

# tree walls: border 2-thick, plus inner groves — leave west gap at y19-21
tree_keys = ["v_tree0", "v_tree1", "v_tree2", "v_tree3", "v_tree4"]
def tree(x, y):
    obj(random.choice(tree_keys), x + .5, y + .6, meta={"kind": "deco"})
    cell_solid(x, y)
for x in range(FW):
    tree(x, 0); tree(x, FH - 1)
    if x % 2 == 0: tree(x, 1); tree(x, FH - 2)
for y in range(FH):
    if 19 <= y <= 21:  # west entrance gap
        continue
    tree(0, y)
    if y % 2 == 0: tree(1, y)
    tree(FW - 1, y)
    if y % 2 == 1: tree(FW - 2, y)
# inner groves — clusters framing the path, not on it
groves = [(8, 10), (11, 9), (9, 26), (13, 25), (18, 24), (20, 22), (6, 13),
          (17, 9), (20, 8), (24, 6), (36, 20), (33, 21), (30, 19), (25, 23), (37, 14)]
for gx, gy in groves:
    if (gx, gy) in path: continue
    tree(gx, gy)
    if (gx + 1, gy) not in path and random.random() < .7: tree(gx + 1, gy)
    if (gx, gy + 1) not in path and random.random() < .7: tree(gx, gy + 1)

# clearing center: ancient statue + stone circle + torches
obj("statue_01", 32.5, 9.5, meta={"kind": "deco", "name": "Ancient Statue"})
for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
    obj("torch_05", 32.5 + dx, 10.5 + dy,
        anim={"frames": ["torch_f0", "torch_f1", "torch_f2"], "fps": 6},
        meta={"kind": "deco", "light": True})
    cell_solid(32 + dx, 10 + dy)
cell_solid(31, 9); cell_solid(32, 9); cell_solid(33, 9)
# hidden chest behind statue
obj("chest_c", 32.5, 8.0, meta={"kind": "chest", "gold": 75, "name": "Mossy Chest"})
cell_solid(32, 7)
# rocks ring in clearing
for a in range(0, 360, 45):
    rx = 32.5 + math.cos(math.radians(a)) * 4.2
    ry = 10.5 + math.sin(math.radians(a)) * 4.2
    obj(random.choice(["rock04", "rock10", "rock11", "rock28"]), rx, ry, meta={"kind": "deco"})

# forageables: mushrooms + herbs scattered, respawn next day
forage_spots = [(6, 17), (12, 22), (16, 19), (19, 12), (23, 18), (27, 14), (30, 21),
                (35, 17), (10, 15), (25, 9), (37, 8), (5, 24), (21, 20), (14, 12)]
for i, (fx, fy) in enumerate(forage_spots):
    if (fx, fy) in fsolid or (fx, fy) in path: continue
    k = "mushroom_01" if i % 2 == 0 else "herb_01"
    obj(k, fx + .5, fy + .9, meta={"kind": "forage", "name": "Wild Mushroom" if k == "mushroom_01" else "Wild Herb", "gold": 6 + (i % 3) * 3})
# flowers as decor tiles sprinkled
flowers = ["flower_r", "flower_y", "flower_b"]
for _ in range(60):
    x, y = random.randrange(FW), random.randrange(FH)
    if (x, y) in fsolid or (x, y) in path or (x, y) in [tuple(map(int, k.split(','))) for k in fdecor]:
        continue
    fdecor[f"{x},{y}"] = random.choice(flowers)
# tall grass tufts near trees
for _ in range(18):
    x, y = random.randrange(2, FW - 2), random.randrange(2, FH - 2)
    if (x, y) in fsolid or (x, y) in path: continue
    obj("tgrass_f0", x + .5, y + .9,
        anim={"frames": ["tgrass_f0", "tgrass_f1", "tgrass_f2", "tgrass_f3"], "fps": 3},
        meta={"kind": "deco"})
# two birds wandering the clearing
obj("bird_down1", 30.5, 12.5, meta={"kind": "animal", "name": "Sparrow"})
obj("bird2_down1", 35.5, 13.5, meta={"kind": "animal", "name": "Robin"})
# lamps marking the entrance + path
for lx, ly in ((2.5, 19.5), (8.5, 22.5), (14.5, 14.5), (21.5, 13.5), (26.5, 9.5)):
    obj("lamp01", lx, ly, meta={"kind": "deco", "light": True}); cell_solid(int(lx), int(ly))

forest = {"W": FW, "H": FH, "id": "forest",
          "layers": {"W": FW, "H": FH,
                     "ground": {f"{x},{y}": k for (x, y), k in fgrass.items()},
                     "dirt": {f"{x},{y}": k for (x, y), k in fdirt.items()},
                     "decor": fdecor, "objects": fobjects,
                     "solid": sorted([list(c) for c in fsolid]),
                     "water_cells": [],
                     "spawn": {"x": 1.5, "y": 20.5},
                     "exits": [{"x0": 0, "y0": 19, "x1": 0, "y1": 21,
                                "to": "village", "sx": 61.5, "sy": 20.5}],
                     "tilled_cells": []},
          "sprites": {k: v["key"] + ".png" if isinstance(v, dict) else v
                       for k, v in sprites.items()}}
json.dump(forest, open(os.path.join(OUT, "forest.json"), "w"))
print("forest.json written:", len(fobjects), "objects,", len(fsolid), "solid")

# ---------------------------------------------------------------- patches
# farm: door of the hero's house -> interior
fm = json.load(open(os.path.join(OUT, "map.json")))
fl = fm["layers"]
fl["exits"] = [e for e in fl.get("exits", []) if e.get("to") != "house"]
fl["exits"] += [{"x0": 15, "y0": 23, "x1": 16, "y1": 23,
                 "to": "house", "sx": 7.5, "sy": 9.4}]
fl.setdefault("decor", {})["15,23"] = "doormat"
fl["decor"]["16,23"] = "doormat"
json.dump(fm, open(os.path.join(OUT, "map.json"), "w"))
print("farm patched: house exit")

# village: east exit -> forest + beautify (flower ring at fountain, benches, lamps)
vl = json.load(open(os.path.join(OUT, "village.json")))
L = vl["layers"]
L["exits"] = [e for e in L.get("exits", []) if e.get("to") != "forest"]
L["exits"] += [{"x0": 63, "y0": 19, "x1": 63, "y1": 21,
                "to": "forest", "sx": 1.5, "sy": 20.5}]
# bench/lamp objects are idempotent additions only once
L["objects"] = [o for o in L["objects"] if o.get("key") != "bench_01"]
# carve east path through the tree column x62 at y20 + mark dirt (reuse an existing dirt tile)
if "dirt" not in L: L["dirt"] = {}
dirt_key = next((k for k in set(L["dirt"].values()) if k and k.startswith("d_")), None)
if dirt_key:
    for x in range(50, 64):
        for y in (19, 20, 21):
            L["dirt"][f"{x},{y}"] = dirt_key
# remove the tree object blocking x62,y20 & its solid cell
L["objects"] = [o for o in L["objects"]
                if not (int(o.get("x", -1)) == 62 and int(o.get("y", -1)) in (19, 20))]
L["solid"] = [c for c in L["solid"] if not (c[0] == 62 and c[1] == 20)]
# flowers ringing the fountain plaza (statue at 32,15)
for x in range(28, 37):
    for y in (13, 17):
        if (x, y) not in [tuple(c) for c in L["solid"]]:
            L.setdefault("decor", {})[f"{x},{y}"] = flowers[(x + y) % 3]
for y in range(13, 18):
    for x in (28, 36):
        if f"{x},{y}" not in L["decor"]:
            L["decor"][f"{x},{y}"] = flowers[(x + y) % 3]
# benches facing the fountain
L["objects"].append({"key": "bench_01", "x": 29.5, "y": 16.8, "meta": {"kind": "deco", "name": "Bench"}})
L["objects"].append({"key": "bench_01", "x": 34.5, "y": 16.8, "meta": {"kind": "deco", "name": "Bench"}})
L["solid"] += [[29, 16], [30, 16], [34, 16], [35, 16]]
# lamps marking the east road
L["objects"] = [o for o in L["objects"]
                if not (o.get("key") == "lamp01" and int(o.get("x", 0)) in (55, 60))]
for lx, ly in ((55.5, 19.5), (60.5, 20.5)):
    L["objects"].append({"key": "lamp01", "x": lx, "y": ly, "meta": {"kind": "deco", "light": True}})
    if [int(lx), int(ly)] not in L["solid"]:
        L["solid"].append([int(lx), int(ly)])
json.dump(vl, open(os.path.join(OUT, "village.json"), "w"))
print("village patched: forest exit + plaza flowers + benches + lamps")
