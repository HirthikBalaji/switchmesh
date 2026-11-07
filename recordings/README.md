# SwitchMesh asciinema Recordings

This directory contains standalone automated demo drivers and pre-recorded `.cast` files generated with [asciinema](https://asciinema.org/) for all 3 hackathon tracks.

## Recorded Demo Casts

| Track | File | Description | Duration |
|---|---|---|---|
| **Track 1** | [`track1_sre_warroom.cast`](./track1_sre_warroom.cast) | Autonomous SRE Incident War Room: triage, ephemeral sandbox repro, hotfix diff, dual-custody gate, and rollback. | ~12s |
| **Track 2** | [`track2_creative_studio.cast`](./track2_creative_studio.cast) | Creative Studio: Wispr voice brief, narrative lore bible, Web Audio sound synthesis, 60 FPS HTML5 canvas engine compilation, automated playtest, and zero-latency hot-reload. | ~10s |
| **Track 3** | [`track3_test_suite.cast`](./track3_test_suite.cast) | Core Contribution & Verification Suite: Supabase connector catalog inspection, MCP skill spec, and 12/12 passing pytest suite. | ~7s |

---

## How to Play Back the Recordings Locally

To play back any of the recordings inside your terminal with full rich formatting and simulated typing:

```bash
# Track 1: SRE Incident War Room
asciinema play recordings/track1_sre_warroom.cast

# Track 2: Creative Studio Voice-to-Game Engine
asciinema play recordings/track2_creative_studio.cast

# Track 3: Supabase Core Contribution & Pytest Suite
asciinema play recordings/track3_test_suite.cast
```

### Controls during playback:
- **`Space`**: Pause / Resume playback
- **`.`**: Step forward a frame while paused
- **`Ctrl+C`**: Exit playback

---

## How to Re-Record

If you modify any code and want to regenerate the `.cast` files:

```bash
# Record Track 1
asciinema rec --overwrite --headless --window-size 110x35 --idle-time-limit 2 \
  -t "SwitchMesh Track 1 - Autonomous SRE Incident War Room" \
  -c "python3 recordings/demo_sre.py" recordings/track1_sre_warroom.cast

# Record Track 2
asciinema rec --overwrite --headless --window-size 110x35 --idle-time-limit 2 \
  -t "SwitchMesh Track 2 - Creative Studio Voice-to-Playable Game Engine" \
  -c "python3 recordings/demo_creative.py" recordings/track2_creative_studio.cast

# Record Track 3
asciinema rec --overwrite --headless --window-size 110x35 --idle-time-limit 2 \
  -t "SwitchMesh Track 3 - Supabase Core Contribution & Verification Suite" \
  -c "python3 recordings/demo_tests.py" recordings/track3_test_suite.cast
```

---

## How to Upload to asciinema.org (Optional)

To publish any recording to the public asciinema web player for sharing in your hackathon submission or README:

```bash
# First authenticate CLI once (if not already authenticated)
asciinema auth

# Upload the recording
asciinema upload recordings/track1_sre_warroom.cast
asciinema upload recordings/track2_creative_studio.cast
asciinema upload recordings/track3_test_suite.cast
```
