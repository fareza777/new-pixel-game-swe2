using UnityEngine;

namespace FarmSlice
{
    // Global slice state: clock, day count, gold, seeds + minimal HUD/dialog UI.
    public class FarmSliceManager : MonoBehaviour
    {
        public static FarmSliceManager I { get; private set; }

        [Header("Time")]
        public float secondsPerGameMinute = 1f;   // 1 real second = 1 game minute -> ~24min day
        [Range(0f, 24f * 60f)] public float clockMinutes = 8f * 60f; // day starts 08:00
        public int day = 1;

        [Header("Economy")]
        public int gold = 0;
        public int seeds = 6;
        public int cropSellPrice = 12;

        public string Dialog { get; private set; }
        float _dialogTimer;

        // Fired when the clock rolls over into a new day.
        public event System.Action NewDay;

        void Awake()
        {
            if (I && I != this) { Destroy(gameObject); return; }
            I = this;
        }

        void Update()
        {
            clockMinutes += Time.deltaTime / secondsPerGameMinute;
            if (Input.GetKeyDown(KeyCode.T)) clockMinutes += 60f; // debug: skip 1h

            if (clockMinutes >= 24f * 60f)
            {
                clockMinutes -= 24f * 60f;
                day++;
                NewDay?.Invoke();
            }

            if (_dialogTimer > 0f)
            {
                _dialogTimer -= Time.deltaTime;
                if (_dialogTimer <= 0f) Dialog = null;
            }
        }

        public void Say(string who, string line)
        {
            Dialog = string.IsNullOrEmpty(who) ? line : $"{who}: {line}";
            _dialogTimer = 4f;
        }

        public bool TrySpendSeed()
        {
            if (seeds <= 0) return false;
            seeds--;
            return true;
        }

        public void SellHarvest() => gold += cropSellPrice;

        void OnGUI()
        {
            var hud = new Rect(10, 10, 240, 74);
            GUI.Box(hud, GUIContent.none);
            GUILayout.BeginArea(new Rect(18, 14, 232, 70));
            int hh = Mathf.FloorToInt(clockMinutes / 60f) % 24;
            int mm = Mathf.FloorToInt(clockMinutes) % 60;
            GUILayout.Label($"<b>HARI {day} — {hh:00}:{mm:00}</b>");
            GUILayout.Label($"{gold}g   ·   bibit x{seeds}");
            GUILayout.Label("<i>tanam · panen · jual</i>");
            GUILayout.EndArea();

            if (Dialog != null)
            {
                var d = new Rect(Screen.width / 2f - 320, Screen.height - 90, 640, 52);
                GUI.Box(d, GUIContent.none);
                GUI.Label(new Rect(d.x + 14, d.y + 8, d.width - 28, 40), Dialog);
            }
        }
    }
}
