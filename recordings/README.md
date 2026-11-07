# SwitchMesh Terminal Recordings & MP4 Videos

This directory contains standalone automated demo drivers, `.cast` recordings generated with [asciinema](https://asciinema.org/), and high-definition `.mp4` video exports for all 3 hackathon tracks.

---

## 🎬 MP4 Video Files (Ready to Watch & Embed)

| Video File | Track / Description | Duration | Size |
|---|---|---|---|
| [**`switchmesh_full_demo.mp4`**](./switchmesh_full_demo.mp4) | **All 3 Tracks Combined**: Incident War Room + Creative Studio + Supabase Core Contribution | **47s** | 1.9 MB |
| [**`track1_sre_warroom.mp4`**](./track1_sre_warroom.mp4) | **Track 1**: Autonomous SRE War Room: triage, ephemeral sandbox repro, hotfix diff, dual-custody gate, and rollback | **19s** | 586 KB |
| [**`track2_creative_studio.mp4`**](./track2_creative_studio.mp4) | **Track 2**: Creative Studio: Wispr voice brief, narrative lore bible, Web Audio synth, 60 FPS Canvas compilation & hot-reload | **18s** | 829 KB |
| [**`track3_test_suite.mp4`**](./track3_test_suite.mp4) | **Track 3**: Switch Core Supabase connector spec, MCP skill markdown, and 12/12 passing pytest suite | **10s** | 472 KB |

All MP4 files are rendered using H.264 video codec at 30 FPS (`yuv420p` profile) with progressive `faststart` metadata for instant browser and mobile playback.

---

## 📼 Asciinema Terminal Casts

| Cast File | Command |
|---|---|
| [`track1_sre_warroom.cast`](./track1_sre_warroom.cast) | `asciinema play recordings/track1_sre_warroom.cast` |
| [`track2_creative_studio.cast`](./track2_creative_studio.cast) | `asciinema play recordings/track2_creative_studio.cast` |
| [`track3_test_suite.cast`](./track3_test_suite.cast) | `asciinema play recordings/track3_test_suite.cast` |

### Playback Controls:
- **`Space`**: Pause / Resume playback
- **`.`**: Step forward a frame while paused
- **`Ctrl+C`**: Exit playback

---

## 🔄 How to Re-generate MP4 Videos

To re-record and compile new MP4 videos from the demo scripts:

```bash
# 1. Record terminal session with asciinema
asciinema rec --overwrite --headless --window-size 110x35 --idle-time-limit 2 \
  -t "SwitchMesh Track 1 - Autonomous SRE Incident War Room" \
  -c "python3 recordings/demo_sre.py" recordings/track1_sre_warroom.cast

# 2. Render to crisp GIF using agg
agg --theme monokai --font-size 16 --fps-cap 30 \
  recordings/track1_sre_warroom.cast /tmp/track1.gif

# 3. Transcode to faststart MP4 using ffmpeg
ffmpeg -y -i /tmp/track1.gif -movflags faststart -pix_fmt yuv420p \
  -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -r 30 recordings/track1_sre_warroom.mp4
```

---

## ☁️ How to Upload to asciinema.org (Optional)

```bash
# Link CLI to your asciinema.org account
asciinema auth

# Upload the recordings
asciinema upload recordings/track1_sre_warroom.cast
asciinema upload recordings/track2_creative_studio.cast
asciinema upload recordings/track3_test_suite.cast
```
