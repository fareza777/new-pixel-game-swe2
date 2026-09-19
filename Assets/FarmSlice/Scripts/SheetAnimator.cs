using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace FarmSlice
{
    // Runtime sprite animation driven by the asset's own sheets — no Animator assets needed.
    //
    // Two sheet layouts are supported:
    //  - "grid" : one texture sliced 3x4 (cols x dirs) like Characters/chara_N or cats/birds
    //             (dir rows in sheet order: down, left, right, up — Unity y-up sorted)
    //  - "dirs" : one file per direction "<sheet>_<dir>_32x32_4frames" (pigs)
    public class SheetAnimator : MonoBehaviour
    {
        public enum Layout { Grid, Dirs }
        public enum Dir { Down = 0, Left = 1, Right = 2, Up = 3 }

        public string sheet;          // Resources-relative path (grid) or prefix (dirs)
        public Layout layout = Layout.Grid;
        public float fps = 4f;
        public bool playing = true;

        [SerializeField] Dir _dir = Dir.Down;
        public Dir Facing
        {
            get => _dir;
            set { if (_dir != value) { _dir = value; _frame = 0; _t = 0f; } }
        }

        SpriteRenderer _sr;
        Sprite[][] _frames;           // [dir][frame]
        int _frame;
        float _t;

        void Awake()
        {
            _sr = GetComponent<SpriteRenderer>();
            Load();
        }

        void Load()
        {
            _frames = new Sprite[4][];
            if (layout == Layout.Grid)
            {
                var all = Resources.LoadAll<Sprite>(sheet)
                    .OrderByDescending(s => s.rect.y)
                    .ThenBy(s => s.rect.x)
                    .ToArray();
                if (all.Length < 12) { Debug.LogWarning($"SheetAnimator: {sheet} -> {all.Length} sprites"); return; }
                for (int d = 0; d < 4; d++)
                    _frames[d] = all.Skip(d * 3).Take(3).ToArray(); // 3 frames per dir row
            }
            else
            {
                string[] names = { "down", "left", "right", "up" };
                for (int d = 0; d < 4; d++)
                {
                    var all = Resources.LoadAll<Sprite>($"{sheet}_{names[d]}_32x32_4frames")
                        .OrderBy(s => s.rect.x)
                        .ToArray();
                    if (all.Length == 0)
                        Debug.LogWarning($"SheetAnimator: {sheet}_{names[d]}... empty");
                    _frames[d] = all;
                }
            }
            Apply();
        }

        void Update()
        {
            if (!playing || _frames == null) return;
            var row = _frames[(int)_dir];
            if (row == null || row.Length == 0) return;
            _t += Time.deltaTime;
            if (_t >= 1f / fps)
            {
                _t = 0f;
                _frame = (_frame + 1) % row.Length;
                Apply();
            }
        }

        void Apply()
        {
            var row = _frames[(int)_dir];
            if (row != null && row.Length > 0 && _sr)
                _sr.sprite = row[Mathf.Clamp(_frame, 0, row.Length - 1)];
        }
    }
}
