"""
SwitchMesh Track 2: Creative Studio End-to-End Orchestrator.
Demonstrates solo creator voice/chat collaboration with Worldsmith, Canvas Mechanic, Audio Alchemist, and Critic.
"""

from __future__ import annotations
from typing import Dict, Tuple
from switchmesh.protocol.client import SwitchRoomHarness
from switchmesh.protocol.types import MessageRole, RoomMessage
from switchmesh.workflows.creative_studio.alchemist import AudioAlchemistAgent
from switchmesh.workflows.creative_studio.canvas_engine import CanvasMechanicAgent
from switchmesh.workflows.creative_studio.critic import GameCriticAgent
from switchmesh.workflows.creative_studio.game_server import GameServer
from switchmesh.workflows.creative_studio.worldsmith import WorldsmithAgent


class CreativeStudioWorkflow:
    def __init__(self, room_name: str = "indie-arcade-studio", bridge: str = "discord"):
        self.harness = SwitchRoomHarness("room-creative-01", room_name, bridge=bridge)
        self.worldsmith = WorldsmithAgent("worldsmith")
        self.alchemist = AudioAlchemistAgent("audio-alchemist")
        self.mechanic = CanvasMechanicAgent("canvas-mechanic")
        self.critic = GameCriticAgent("game-critic")
        self.game_server = GameServer(port=8800)

        self.harness.register_agent(self.worldsmith.name, self.worldsmith)
        self.harness.register_agent(self.alchemist.name, self.alchemist)
        self.harness.register_agent(self.mechanic.name, self.mechanic)
        self.harness.register_agent(self.critic.name, self.critic)

    def run_stage_1_creator_prompt(self, voice_dictation: str = None) -> RoomMessage:
        """Creator speaks or types idea via Wispr Flow voice."""
        prompt = voice_dictation or (
            "@worldsmith @canvas-mechanic: Let's build 'CyberGlitch: Mainframe Breach'! "
            "A fast retro arcade hack-and-evade game where you pilot a cyber-drone collecting "
            "encrypted data nodes while avoiding hunter-killer firewalls. Add screen pulse, "
            "chiptune audio, and dash mechanics."
        )
        msg = self.harness.post_message(
            author_id="creator",
            author_name="Alex (Indie Creator)",
            role=MessageRole.HUMAN,
            content=prompt,
            mentions=["worldsmith", "canvas-mechanic"]
        )
        return msg

    def run_stage_2_worldsmith(self) -> Tuple[RoomMessage, Dict]:
        """Worldsmith generates the lore and game rules."""
        bible = self.worldsmith.create_game_bible("CyberGlitch")
        text = self.worldsmith.format_room_presentation(bible)
        msg = self.harness.post_message(
            author_id=self.worldsmith.name,
            author_name="Worldsmith (Narrative Agent)",
            role=MessageRole.AGENT,
            content=text,
            mentions=["audio-alchemist", "canvas-mechanic"]
        )
        return msg, bible

    def run_stage_3_alchemist(self) -> RoomMessage:
        """Audio Alchemist synthesizes Web Audio procedural SFX."""
        text = self.alchemist.format_room_presentation()
        msg = self.harness.post_message(
            author_id=self.alchemist.name,
            author_name="Audio Alchemist (Synthesizer Agent)",
            role=MessageRole.AGENT,
            content=text,
            mentions=["canvas-mechanic"]
        )
        return msg

    def run_stage_4_mechanic(self) -> Tuple[RoomMessage, str]:
        """Canvas Mechanic compiles HTML5 game and boots live server."""
        url = self.game_server.start()
        text = self.mechanic.format_room_presentation(url)
        msg = self.harness.post_message(
            author_id=self.mechanic.name,
            author_name="Canvas Mechanic (Engine Agent)",
            role=MessageRole.AGENT,
            content=text,
            mentions=["game-critic"]
        )
        return msg, url

    def run_stage_5_critic(self) -> Tuple[RoomMessage, Dict]:
        """Critic evaluates balance and frame budget."""
        game_html = self.mechanic.generate_html5_game()
        eval_data = self.critic.evaluate_game_balance(game_html)
        text = self.critic.format_room_presentation(eval_data)
        msg = self.harness.post_message(
            author_id=self.critic.name,
            author_name="Game Critic (Playtester Agent)",
            role=MessageRole.AGENT,
            content=text
        )
        return msg, eval_data

    def run_stage_6_creator_tweak(self, tweak_voice_prompt: str = "Make the drone speed faster and add more data nodes") -> RoomMessage:
        """Creator dictates live hot-reload tweak."""
        msg = self.harness.post_message(
            author_id="creator",
            author_name="Alex (Indie Creator)",
            role=MessageRole.HUMAN,
            content=f"Voice update via Wispr Flow: '{tweak_voice_prompt}'. Hot-reload that now!"
        )
        self.game_server.write_game_file("CyberGlitch: Mainframe Breach (v1.1 Hot-Reload)")
        self.harness.post_message(
            author_id=self.mechanic.name,
            author_name="Canvas Mechanic (Engine Agent)",
            role=MessageRole.AGENT,
            content="⚡ **[HOT-RELOAD APPLIED]** Drone speed updated (+25%) and node density increased. Live preview re-rendered."
        )
        return msg
