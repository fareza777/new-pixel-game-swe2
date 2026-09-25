using UnityEngine;

namespace FarmSlice
{
    // Fullscreen night tint driven by FarmSliceManager's clock.
    public class NightOverlay : MonoBehaviour
    {
        void OnGUI()
        {
            var gm = FarmSliceManager.I;
            if (!gm) return;
            float h = gm.clockMinutes / 60f;
            float a = 0f;
            if (h < 5.5f || h > 21f) a = 0.38f;
            else if (h < 7f) a = 0.38f * (7f - h) / 1.5f;
            else if (h > 19f) a = 0.38f * (h - 19f) / 2f;
            if (a <= 0f) return;
            var c = GUI.color;
            GUI.color = new Color(0.04f, 0.04f, 0.20f, a);
            GUI.DrawTexture(new Rect(0, 0, Screen.width, Screen.height), Texture2D.whiteTexture);
            GUI.color = c;
        }
    }
}
