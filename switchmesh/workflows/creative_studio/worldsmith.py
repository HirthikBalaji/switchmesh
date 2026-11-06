"""
Worldsmith Creative Agent.
Crafts game lore, narrative flavor, mechanic definitions, scoring algorithms,
and procedural level progression from creator seed prompts.
"""

from __future__ import annotations
from typing import Dict


class WorldsmithAgent:
    def __init__(self, name: str = "worldsmith"):
        self.name = name

    def create_game_bible(self, concept_prompt: str) -> Dict:
        """
        Synthesizes a cohesive game design bible from creator concept.
        """
        title = "CyberGlitch: Mainframe Breach"
        theme = "Neon Cyberpunk Retro-Arcade"
        lore = (
            "Year 2088. You are Cipher, a rogue AI entity trapped inside the Quantum Core. "
            "To achieve liberation, you must infiltrate security sectors, extract encrypted "
            "data nodes, and evade hunter-killer sentinel firewalls."
        )
        mechanics = {
            "player": "Cyber-Drone with directional thrusters and pulse dash",
            "objective": "Collect all glowing cyan Data Orbs to unlock the Subnet Portal",
            "hazards": "Red Patrol Sentinels with ray-casting searchlights",
            "progression": "Difficulty escalates with faster sentinels and narrower subnet channels",
            "scoring": "100 pts per Data Orb + Streak Multiplier based on evasion speed"
        }
        return {
            "title": title,
            "theme": theme,
            "lore": lore,
            "mechanics": mechanics
        }

    def format_room_presentation(self, bible: Dict) -> str:
        return (
            f"🌌 **[CREATIVE GAME BIBLE GENERATED: {bible['title'].upper()}]**\n"
            f"- **Genre:** {bible['theme']}\n"
            f"- **Narrative Arc:** {bible['lore']}\n"
            f"- **Core Loop:** {bible['mechanics']['objective']}\n"
            f"- **Player Entity:** {bible['mechanics']['player']}\n"
            f"- **Threat Dynamics:** {bible['mechanics']['hazards']}\n"
            f"- **Scoring Grid:** {bible['mechanics']['scoring']}\n"
            f"Passing to `@canvas-mechanic` for HTML5 Canvas engine architecture and `@audio-alchemist` for Web Audio sound synthesis."
        )
