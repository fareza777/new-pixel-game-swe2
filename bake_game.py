#!/usr/bin/env python3
"""Bake Sunpetal Valley web bundle: combined atlas + inlined maps + audio -> index.html"""
import json, base64, os, shutil
from PIL import Image

OUT = "/home/ubuntu/farm_preview_build"
SPRDIR = os.path.join(OUT, "sprites")

farm = json.load(open(os.path.join(OUT, "map.json")))
vill = json.load(open(os.path.join(OUT, "village.json")))
house = json.load(open(os.path.join(OUT, "house.json")))
forest = json.load(open(os.path.join(OUT, "forest.json")))
bramh = json.load(open(os.path.join(OUT, "bramhouse.json")))
nanah = json.load(open(os.path.join(OUT, "nanahouse.json")))
cave = json.load(open(os.path.join(OUT, "cave.json")))
cave2 = json.load(open(os.path.join(OUT, "cave2.json")))
river = json.load(open(os.path.join(OUT, "river.json")))
hill = json.load(open(os.path.join(OUT, "hill.json")))
wrenh = json.load(open(os.path.join(OUT, "wrenhut.json")))
islet = json.load(open(os.path.join(OUT, "islet.json")))
orch  = json.load(open(os.path.join(OUT, "orchard.json")))
viloh = json.load(open(os.path.join(OUT, "vilohouse.json")))
mirah = json.load(open(os.path.join(OUT, "mirahouse.json")))
grows = json.load(open(os.path.join(OUT, "grows.json")))
inn   = json.load(open(os.path.join(OUT, "inn.json")))
carp  = json.load(open(os.path.join(OUT, "carpentry.json")))
tail  = json.load(open(os.path.join(OUT, "tailor.json")))
barnm = json.load(open(os.path.join(OUT, "barn.json")))
cave3 = json.load(open(os.path.join(OUT, "cave3.json")))
cave4 = json.load(open(os.path.join(OUT, "cave4.json")))
loft  = json.load(open(os.path.join(OUT, "loft.json")))
cellar = json.load(open(os.path.join(OUT, "cellar.json")))

# ---- unify map format -------------------------------------------------------
def unify(m, name):
    L = m["layers"]
    # tile-layer order (decor & objects handled separately)
    order = [n for n in ("ground", "soil", "path", "dirt", "sand", "water") if n in L and L[n]]
    tiles = {n: L[n] for n in order}
    tiles["decor"] = L.get("decor", {})
    out = {
        "W": L.get("W", m.get("W")), "H": L.get("H", m.get("H")), "id": name,
        "order": order, "tiles": tiles,
        "objects": L["objects"], "solid": L["solid"],
        "water": L.get("water_cells", []),
        "spawn": L["spawn"], "exits": L.get("exits", []),
        "tilled": L.get("tilled_cells", []) + L.get("festival_beds", []),
        "tillable": L.get("tillable", []),
        "sprites": m["sprites"],
    }
    return out

MF = unify(farm, "farm")
MV = unify(vill, "village")
MH = unify(house, "house")
MO = unify(forest, "forest")
MB = unify(bramh, "bramhouse")
MN = unify(nanah, "nanahouse")
MB["indoor"]=True; MN["indoor"]=True
MC = unify(cave, "cave")
MC["indoor"]=True; MC["dark"]=True
MC2 = unify(cave2, "cave2"); MC3 = unify(cave3, "cave3"); MC4 = unify(cave4, "cave4")
MC2["indoor"]=True; MC2["dark"]=True
MR = unify(river, "river"); MR["crop_frames"]=farm["layers"]["crop_frames"]
MHill = unify(hill, "hill"); MHill["crop_frames"]=farm["layers"]["crop_frames"]
MWr = unify(wrenh, "wrenhut"); MWr["indoor"]=True; MWr["crop_frames"]=farm["layers"]["crop_frames"]
MIs = unify(islet, "islet"); MIs["crop_frames"]=farm["layers"]["crop_frames"]
MOd = unify(orch, "orchard"); MOd["crop_frames"]=farm["layers"]["crop_frames"]
MIn = unify(inn, "inn"); MIn["indoor"]=True; MIn["crop_frames"]=farm["layers"]["crop_frames"]
MCp = unify(carp, "carpentry"); MCp["indoor"]=True; MCp["crop_frames"]=farm["layers"]["crop_frames"]
MTa = unify(tail, "tailor"); MTa["indoor"]=True; MTa["crop_frames"]=farm["layers"]["crop_frames"]
MBa = unify(barnm, "barn"); MBa["indoor"]=True; MBa["crop_frames"]=farm["layers"]["crop_frames"]
MH["indoor"] = True
MLf = unify(loft, "loft"); MLf["indoor"]=True
MCe = unify(cellar, "cellar"); MCe["indoor"]=True; MCe["dark"]=True
# village tilled = ONLY festival beds (not whole map) -> fix: festival beds only
MV["tilled"] = vill["layers"].get("festival_beds", [])
# crop_frames shared to all maps (+ sunpetal id 22 reuses melon frames for now)
MF["crop_frames"] = farm["layers"]["crop_frames"]
MV["crop_frames"] = dict(farm["layers"]["crop_frames"])
MV["crop_frames"]["22"] = farm["layers"]["crop_frames"]["21"]
MH["crop_frames"] = MF["crop_frames"]
MO["crop_frames"] = MF["crop_frames"]
MB["crop_frames"]=MF["crop_frames"]; MN["crop_frames"]=MF["crop_frames"]; MC["crop_frames"]=MF["crop_frames"]
MVi = unify(viloh, "vilohouse"); MMh = unify(mirah, "mirahouse")
MVi["indoor"]=True; MMh["indoor"]=True
MG = unify(grows, "grows"); MG["indoor"]=True; MG["crop_frames"]=farm["layers"]["crop_frames"]
MVi["crop_frames"]=MF["crop_frames"]; MMh["crop_frames"]=MF["crop_frames"]

# ---- merge sprite dictionaries (prefix village keys on collision) -----------
merged = dict(farm["sprites"])
for srcmap, mname in ((house, MH), (forest, MO), (bramh, MB), (nanah, MN), (cave, MC), (cave2, MC2), (viloh, MVi), (mirah, MMh), (river, MR), (grows, MG), (hill, MHill), (wrenh, MWr), (islet, MIs), (orch, MOd), (inn, MIn), (carp, MCp), (tail, MTa), (barnm, MBa), (cave3, MC3), (cave4, MC4), (cellar, MCe)):
    for k, v in srcmap["sprites"].items():
        merged[k] = v; mname["sprites"][k] = v
collisions = 0
for k, v in list(vill["sprites"].items()):
    if k in merged and merged[k] != v:
        collisions += 1
        nk = "v_" + k
        MV["sprites"][nk] = v
        # rewrite references in village map
        for layer in MV["tiles"].values():
            for ck in list(layer):
                if layer[ck] == k:
                    layer[ck] = nk
        for o in MV["objects"]:
            if o.get("key") == k:
                o["key"] = nk
            if o.get("anim"):
                o["anim"]["frames"] = [nk if f == k else f for f in o["anim"]["frames"]]
            if o.get("meta", {}).get("portrait") == k:
                o["meta"]["portrait"] = nk
        merged[nk] = v
    else:
        merged[k] = v
        MV["sprites"][k] = v
print("sprite key collisions renamed:", collisions)

MAPS = {"farm": MF, "village": MV, "house": MH, "forest": MO, "bramhouse": MB, "nanahouse": MN, "cave": MC, "cave2": MC2, "vilohouse": MVi, "mirahouse": MMh, "river": MR, "grows": MG, "hill": MHill, "wrenhut": MWr, "islet": MIs, "orchard": MOd, "inn": MIn, "carpentry": MCp, "tailor": MTa, "barn": MBa, "cave3": MC3, "cave4": MC4, "loft": MLf, "cellar": MCe}

# ---- build combined atlas ----------------------------------------------------
files = sorted(set(merged.values()))
imgs = {}
for fn in files:
    p = os.path.join(SPRDIR, fn)
    if not os.path.exists(p):
        print("MISSING SPRITE FILE:", fn)
        continue
    imgs[fn] = Image.open(p).convert("RGBA")

# shelf packer
AW = 1024
x = y = rowh = 0
adata = {}
margin = 2
for fn in files:
    if fn not in imgs:
        continue
    im = imgs[fn]
    w, h = im.size
    if x + w + margin > AW:
        x = 0
        y += rowh + margin
        rowh = 0
    adata[fn] = [x, y, w, h]
    x += w + margin
    rowh = max(rowh, h)
AH = y + rowh + margin
atlas = Image.new("RGBA", (AW, AH), (0, 0, 0, 0))
for fn, (ax, ay, w, h) in adata.items():
    atlas.paste(imgs[fn], (ax, ay))
atlas.save("/tmp/atlas_full.png")
print("atlas:", AW, "x", AH, len(adata), "sprites")

# sanity: key sprites exist
for need in ("hero_idle_DOWN0", "hero_walk_DOWN0"):
    assert need in merged, need + " missing"
for nid in ("bram", "sari", "vilo", "nana"):
    assert any(o.get("meta", {}).get("id") == nid for o in MV["objects"]), nid
print("npc portraits ok:", [o["meta"].get("portrait") for o in MV["objects"] if o.get("meta", {}).get("kind") == "npc"])

# ---- audio -------------------------------------------------------------------
audio = {}
audir = os.path.join(OUT, "audio")
for fn in sorted(os.listdir(audir)):
    if fn.endswith(".mp3"):
        audio[fn[:-4]] = "data:audio/mpeg;base64," + base64.b64encode(open(os.path.join(audir, fn), "rb").read()).decode()
print("audio:", list(audio), sum(len(v) for v in audio) // 1024, "KB inlined")

# ---- icon --------------------------------------------------------------------
icon_b64 = base64.b64encode(open("/home/ubuntu/sunpetal_icon.png", "rb").read()).decode()

# ---- cinematic art (downscaled for size) --------------------------------------
art = {}
artdir = os.path.join(OUT, "art")
for fn in sorted(os.listdir(artdir)):
    if fn.endswith(".png"):
        im = Image.open(os.path.join(artdir, fn)).convert("RGB")
        im.thumbnail((640, 640), Image.LANCZOS)
        im.save("/tmp/_art.jpg", "JPEG", quality=72)
        art[fn[:-4]] = "data:image/jpeg;base64," + base64.b64encode(open("/tmp/_art.jpg", "rb").read()).decode()
print("art:", list(art), sum(len(v) for v in art.values()) // 1024, "KB")

# ---- emit index.html ---------------------------------------------------------
atlas_b64 = base64.b64encode(open("/tmp/atlas_full.png", "rb").read()).decode()
tpl = open("/home/ubuntu/game_template.html").read()
tpl = tpl.replace("__MDATA__", json.dumps(MAPS, separators=(",", ":")))
tpl = tpl.replace("__ADATA__", json.dumps(adata, separators=(",", ":")))
tpl = tpl.replace("__ATLAS_SRC__", "data:image/png;base64," + atlas_b64)
tpl = tpl.replace("__AUDIO__", json.dumps(audio, separators=(",", ":")))
tpl = tpl.replace("__ART__", json.dumps(art, separators=(",", ":")))
tpl = tpl.replace("__ICON__", "data:image/png;base64," + icon_b64)
tpl = tpl.replace("__VER__", "2.08")
open(os.path.join(OUT, "index.html"), "w").write(tpl)
print("index.html:", len(tpl) // 1024, "KB")

# copy to APK www
apkdir = "/home/ubuntu/apkproj/app/src/main/assets/www"
if os.path.isdir(apkdir):
    shutil.copy2(os.path.join(OUT, "index.html"), os.path.join(apkdir, "index.html"))
    print("copied to", apkdir)
