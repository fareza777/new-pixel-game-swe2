using UnityEngine;

namespace FarmSlice
{
    // Animals that wander inside a small radius around their home position.
    [RequireComponent(typeof(SheetAnimator))]
    public class WanderAnimal : MonoBehaviour, IInteractable
    {
        public float radius = 2.2f;
        public float speed = 0.7f;
        public float pauseChance = 0.65f;
        public string petName = "hewan";

        SheetAnimator _anim;
        Vector3 _home, _target;
        float _wait;

        void Awake()
        {
            _anim = GetComponent<SheetAnimator>();
            _home = transform.position;
            _target = _home;
        }

        void Update()
        {
            if (_wait > 0f)
            {
                _wait -= Time.deltaTime;
                _anim.playing = false;
                return;
            }

            var d = _target - transform.position;
            if (d.sqrMagnitude < 0.02f)
            {
                if (Random.value < pauseChance) { _wait = Random.Range(0.8f, 2.4f); _anim.playing = false; return; }
                _target = _home + (Vector3)(Random.insideUnitCircle * radius);
                return;
            }

            _anim.playing = true;
            if (Mathf.Abs(d.x) > Mathf.Abs(d.y))
                _anim.Facing = d.x > 0 ? SheetAnimator.Dir.Right : SheetAnimator.Dir.Left;
            else
                _anim.Facing = d.y > 0 ? SheetAnimator.Dir.Up : SheetAnimator.Dir.Down;
            transform.position += d.normalized * speed * Time.deltaTime;
        }

        public string Prompt => $"elus {petName}";
        public void Interact(GameObject actor)
        {
            FarmSliceManager.I.Say("", $"{petName} senang!");
            _wait = 1.2f;
        }
    }
}
