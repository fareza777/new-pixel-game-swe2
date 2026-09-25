using UnityEngine;

namespace FarmSlice
{
    // One tillable soil cell: E plants a seed (spends 1 seed, auto-watered),
    // E again waters it daily; on NewDay watered crops advance one stage,
    // and a fully grown crop is harvested for gold.
    public class CropPlot : MonoBehaviour, IInteractable
    {
        static readonly int[] CropIds = { 1, 3, 8, 13, 18, 21 };
        const string SpriteDir = "Prefabs/Crops/Sprites";

        public bool watered;
        public int cropId;      // 0 = empty
        public int stage;

        SpriteRenderer _cropSr;
        Sprite[] _cropFrames;

        public string Prompt
        {
            get
            {
                if (cropId == 0)
                    return FarmSliceManager.I.seeds > 0 ? "tanam bibit" : "bibit habis";
                if (stage >= _cropFrames.Length - 1) return $"panen (+{FarmSliceManager.I.cropSellPrice}g)";
                return watered ? "tumbuh…" : "siram tanaman";
            }
        }

        public void Interact(GameObject actor)
        {
            var gm = FarmSliceManager.I;
            if (cropId == 0)
            {
                if (!gm.TrySpendSeed()) { gm.Say("", "Bibit habis!"); return; }
                cropId = CropIds[Random.Range(0, CropIds.Length)];
                stage = 1;
                watered = true;
                Show();
            }
            else if (stage >= _cropFrames.Length - 1)
            {
                gm.SellHarvest();
                Destroy(_cropSr.gameObject);
                _cropSr = null; _cropFrames = null;
                cropId = 0; stage = 0; watered = false;
            }
            else if (!watered)
            {
                watered = true;
            }
        }

        void Start()
        {
            // subscribe after the manager's Awake has run
            if (FarmSliceManager.I) FarmSliceManager.I.NewDay += OnNewDay;
        }
        void OnDestroy()
        {
            if (FarmSliceManager.I) FarmSliceManager.I.NewDay -= OnNewDay;
        }

        void OnNewDay()
        {
            if (cropId > 0 && watered)
            {
                stage = Mathf.Min(stage + 1, _cropFrames.Length - 1);
                Apply();
            }
            watered = false;
        }

        void Show()
        {
            var go = new GameObject($"crop_{cropId:00}");
            go.transform.SetParent(transform, false);
            go.transform.localPosition = new Vector3(0f, 0.1f, 0f);
            _cropSr = go.AddComponent<SpriteRenderer>();
            _cropSr.sortingOrder = 10;
            _cropFrames = Resources.LoadAll<Sprite>($"{SpriteDir}/crop_{cropId:00}");
            Apply();
        }

        void Apply()
        {
            if (_cropSr && _cropFrames != null && _cropFrames.Length > 0)
                _cropSr.sprite = _cropFrames[Mathf.Clamp(stage, 0, _cropFrames.Length - 1)];
        }
    }
}
