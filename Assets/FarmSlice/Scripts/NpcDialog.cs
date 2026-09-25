using UnityEngine;

namespace FarmSlice
{
    // NPC that plays an idle loop and speaks one line when interacted with.
    [RequireComponent(typeof(SheetAnimator))]
    public class NpcDialog : MonoBehaviour, IInteractable
    {
        public string npcName = "???";
        [TextArea] public string line = "...";

        public string Prompt => $"bicara dengan {npcName}";
        public void Interact(GameObject actor) => FarmSliceManager.I.Say(npcName, line);
    }
}
