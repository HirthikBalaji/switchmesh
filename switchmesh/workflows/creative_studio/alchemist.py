"""
Audio Alchemist Agent.
Synthesizes procedural chiptune sound effects, Web Audio API oscillators,
and SVG vector assets without requiring external binary asset dependencies.
"""

from __future__ import annotations


class AudioAlchemistAgent:
    def __init__(self, name: str = "audio-alchemist"):
        self.name = name

    def generate_web_audio_synth_script(self) -> str:
        """
        Generates pure JavaScript Web Audio API synthesizers for retro arcade sound effects.
        """
        js_code = """
// Web Audio API Procedural Chiptune Sound Synthesizer
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playTone(freq, type, duration, rampFreq = null) {
    if (audioCtx.state === 'suspended') {
        audioCtx.resume();
    }
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
    if (rampFreq) {
        osc.frequency.exponentialRampToValueAtTime(rampFreq, audioCtx.currentTime + duration);
    }
    gain.gain.setValueAtTime(0.25, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + duration);
}

function sfxCollect() {
    playTone(523.25, 'triangle', 0.08, 659.25); // C5 -> E5
    setTimeout(() => playTone(783.99, 'sine', 0.12, 1046.50), 60); // G5 -> C6
}

function sfxDash() {
    playTone(300, 'sawtooth', 0.15, 80);
}

function sfxExplosion() {
    playTone(140, 'square', 0.35, 30);
}

function sfxWinLevel() {
    [523.25, 659.25, 783.99, 1046.50].forEach((f, i) => {
        setTimeout(() => playTone(f, 'sine', 0.18), i * 80);
    });
}
"""
        return js_code

    def format_room_presentation(self) -> str:
        return (
            "🎵 **[AUDIO & ASSET SYNTHESIS COMPLETE]**\n"
            "- **Synthesis Engine:** Pure Web Audio API (Zero external MP3 dependencies)\n"
            "- **Audio Cues:** `sfxCollect()` (C5->C6 chime), `sfxDash()` (pitch sweep), `sfxExplosion()` (square wave drop), `sfxWinLevel()` (4-note arpeggio)\n"
            "- **Visual Palette:** Tron Cyan (`#00f3ff`), Neon Crimson (`#ff0055`), Quantum Purple (`#b026ff`)\n"
            "Handing assets over to `@canvas-mechanic` for compilation."
        )
