using UnityEngine;

namespace FarmSlice
{
    // Attach to the player. E key -> interact with the nearest IInteractable in range.
    public class Interactor : MonoBehaviour
    {
        public float radius = 0.9f;
        IInteractable _current;

        void Update()
        {
            _current = FindNearest();
            if (_current != null && Input.GetKeyDown(KeyCode.E))
                _current.Interact(gameObject);
        }

        IInteractable FindNearest()
        {
            IInteractable best = null;
            float bestD = float.MaxValue;
            foreach (var col in Physics2D.OverlapCircleAll(transform.position, radius))
            {
                var it = col.GetComponentInParent<IInteractable>();
                if (it == null) continue;
                float d = (((Component)it).transform.position - transform.position).sqrMagnitude;
                if (d < bestD) { bestD = d; best = it; }
            }
            return best;
        }

        void OnGUI()
        {
            if (_current == null) return;
            var p = _current.Prompt;
            if (string.IsNullOrEmpty(p)) return;
            var r = new Rect(Screen.width / 2f - 160, Screen.height - 130, 320, 26);
            GUI.Box(r, GUIContent.none);
            var c = GUI.color; GUI.color = Color.white;
            GUI.Label(new Rect(r.x + 10, r.y + 4, r.width - 20, 20), $"E — {p}");
            GUI.color = c;
        }
    }
}
