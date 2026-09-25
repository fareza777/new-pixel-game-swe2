using UnityEngine;

namespace FarmSlice
{
    public interface IInteractable
    {
        string Prompt { get; }
        void Interact(GameObject actor);
    }
}
