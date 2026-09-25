using UnityEngine;

namespace FarmSlice
{
    // Sits next to the pack's chest_open_on_contact prefab: grants gold once
    // when the player interacts. The prefab itself plays its own open anim on contact.
    public class ChestGold : MonoBehaviour, IInteractable
    {
        public int gold = 25;
        bool _opened;

        public string Prompt => _opened ? "" : "buka peti";

        public void Interact(GameObject actor)
        {
            if (_opened) return;
            _opened = true;
            FarmSliceManager.I.gold += gold;
            FarmSliceManager.I.Say("", $"Kamu menemukan {gold}g!");
        }
    }
}
