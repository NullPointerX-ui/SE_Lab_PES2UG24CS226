# SE Lab 4 — Dino Run Repair Lab (LLM-Assisted Debugging)

**Name:** Khush Bhardwaj
**SRN:** PES2UG24CS226
**Project:** Single-file Pygame endless runner

## Files

| File | Description |
|------|-------------|
| `game.py` | The repaired game — bug fixed and all three features implemented |
| `game_original.py` | The starter file as provided, kept so the "before" behaviour can be recorded |

## Run it

```bash
pip install pygame
python game.py
```

**Controls:** `Space` / `Up` / `W` to start and jump, and the same keys to restart after Game Over.

---

## Task 1 — The high-score bug (fixed)

In `Game.update`, the moment a collision is detected:

```python
current = self.score // 10
if self.high_score > current:        # BUG
    self.high_score = current
    save_high_score(self.high_score)
```

The comparison was backwards. It only replaced the best score when the run that just
ended was **worse** than the record, so on a fresh install — where the record starts at
0 — the condition was never true and `dino_highscore.txt` was never written. Worse, if a
high score did somehow exist, a bad run would have *overwritten* it with a lower number.

The fix is one operand swap:

```python
if current > self.high_score:        # the run that just ended beat the record
    self.high_score = current
    save_high_score(self.high_score)
```

Verified both ways: a score of 123 is now written to `dino_highscore.txt` and reloaded on
the next launch, and a following run of 5 leaves the stored 123 untouched.

## Task 2 — `dino_tint(on_ground)`

Returns `None` while the dino is on the ground, so `Dino.draw` falls back to its default
green through `dino_tint(self.on_ground) or self.color`, and returns a blue
`(62, 124, 196)` while it is airborne. The dino visibly changes colour for the duration of
a jump, which also makes the new double jump easy to see.

## Task 3 — `on_obstacle_passed(obstacle, score)`

Implemented as a combo counter. Module-level `combo` state holds the current run of
obstacles cleared, the best run of the session, and a countdown of frames for a floating
"+1". Each call increments the count, updates the best, and restarts the popup timer;
`Game.draw` shows `Combo xN` in the top-left once the count reaches 2 and floats the "+1"
upward above the dino, and `Game.reset` calls `reset_combo()` so a new run starts from
zero while the session best is kept.

## Task 4 — `max_jumps()`

Returns `2`, giving the dino a double jump. The existing bookkeeping in `Dino.jump`
(`if self.jump_count < (max_jumps() or 1)`) and the reset to 0 on landing already handled
the rest, so no other change was needed. Verified that a third jump in mid-air is still
refused.

---

## Verification

Each change was checked by driving the game headless (`SDL_VIDEODRIVER=dummy`) and
asserting the state directly, rather than only by eye:

| Check | Result |
|-------|--------|
| Two jumps allowed in the air, third refused | `jump_count` 2, then still 2 |
| `dino_tint(True)` / `dino_tint(False)` | `None` / `(62, 124, 196)` |
| One obstacle passed | combo 1, popup armed |
| Run of 123 after a collision | high score 123, written to disk, reloaded as 123 |
| Weaker run of 5 afterwards | high score still 123 |
| Combo on restart | reset to 0, session best retained |
| Full frame drawn with the combo HUD visible | no errors |

## Submission checklist

- [ ] 10-second gameplay video **before** the changes (run `game_original.py`)
- [ ] 10-second gameplay video **after** the changes (run `game.py`)
- [ ] Link to the LLM chat used for the lab
