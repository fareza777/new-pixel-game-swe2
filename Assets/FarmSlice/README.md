# Farm Slice — Farming Life-Sim RPG Vertical Slice

Vertical slice yang memakai aset `Assets/Gif/Super_Retro_Collection` (paket "2D Cozy RPG").

## Cara pakai di Unity

1. Buka project ini di Unity 6 (6000.0.x).
2. Menu **Farm Slice → Build Farm Slice Scene** — scene `Assets/FarmSlice/Scenes/FarmSlice.unity`
   dibuat dari `farm_slice_map.json` (tilemap + prefab + collider + actor).
3. Buka scene itu, tekan **Play**.

Kontrol: WASD/Arrow jalan, **E** interaksi (tanam/siram/panen/bicara/elus hewan/buka peti), **T** skip 1 jam.

## Isi slice

- Map 64x40 tile: rumah + gudang, 4 petak ladang berpagar, kandang babi, kolam + dermaga + api unggun, kebun buah, jalan tanah + lampu/obor.
- Loop farming: bibit → tanam di tanah gembur → siram tiap hari → panen → +gold.
- Day/night cycle (24 menit real-time per hari) + overlay malam; obor menyala lewat animasi prefab.
- 2 NPC (dialog), kucing + 3 babi yang wander, peti harta, tall grass.

## File

- `farm_slice_map.json` — layout map (sel per layer, objek, solid, tilled cells).
- `Scripts/` — gameplay: FarmSliceManager (jam/gold/HUD), CropPlot, Interactor,
  SheetAnimator (animasi runtime dari sheet Resources), WanderAnimal, NpcDialog,
  ChestGold, NightOverlay.
- `Editor/FarmSliceSceneBuilder.cs` — generator scene satu-klik.

## Preview browser (tanpa Unity)

Folder `WebPreview/` di root repo berisi versi playable berbasis canvas + sprite
asli — jalankan `python3 -m http.server` di folder itu lalu buka `index.html`.
