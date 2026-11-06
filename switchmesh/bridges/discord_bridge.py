"""
Real Discord Platform Bridge for SwitchMesh.
Connects a real Discord bot to Switch rooms, enabling multi-agent collaboration
where each agent speaks with its own persona and avatar via Webhooks or Rich Embeds.
"""

from __future__ import annotations
import asyncio
import os
import sys
from typing import Dict, Optional
import discord
from switchmesh.protocol.client import SwitchRoomHarness
from switchmesh.protocol.types import MessageRole, RoomMessage, SwitchEvent
from switchmesh.workflows.business_sre.incident_sim import SREWarRoomWorkflow
from switchmesh.workflows.creative_studio.studio_sim import CreativeStudioWorkflow

AGENT_AVATARS = {
    "sre-triager": "https://cdn-icons-png.flaticon.com/512/3208/3208676.png",
    "chaos-reproducer": "https://cdn-icons-png.flaticon.com/512/2621/2621183.png",
    "patch-architect": "https://cdn-icons-png.flaticon.com/512/1005/1005141.png",
    "security-sentinel": "https://cdn-icons-png.flaticon.com/512/1161/1161388.png",
    "worldsmith": "https://cdn-icons-png.flaticon.com/512/3593/3593452.png",
    "canvas-mechanic": "https://cdn-icons-png.flaticon.com/512/808/808439.png",
    "audio-alchemist": "https://cdn-icons-png.flaticon.com/512/2907/2907253.png",
    "game-critic": "https://cdn-icons-png.flaticon.com/512/3062/3062634.png",
}


class DiscordSwitchBridge:
    def __init__(
        self,
        bot_token: str,
        channel_id: int,
        workflow_type: str = "sre"
    ):
        self.bot_token = bot_token
        self.channel_id = channel_id
        self.workflow_type = workflow_type

        # Initialize Switch Workflow
        if workflow_type == "sre":
            self.sre_flow = SREWarRoomWorkflow("discord-sre-room", bridge="discord")
            self.harness = self.sre_flow.harness
        else:
            self.creative_flow = CreativeStudioWorkflow("discord-creative-room", bridge="discord")
            self.harness = self.creative_flow.harness

        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.target_channel: Optional[discord.TextChannel] = None
        self.webhook: Optional[discord.Webhook] = None

        self._setup_events()

    def _setup_events(self):
        @self.client.event
        async def on_ready():
            print(f"✅ Discord Bridge Connected as {self.client.user} (ID: {self.client.user.id})")
            self.target_channel = self.client.get_channel(self.channel_id)
            if not self.target_channel:
                try:
                    self.target_channel = await self.client.fetch_channel(self.channel_id)
                except Exception as e:
                    print(f"❌ Could not fetch Discord channel {self.channel_id}: {e}")
                    return

            print(f"📡 Joined Discord Channel: #{self.target_channel.name}")

            # Try finding or creating a Webhook for multi-avatar agent posting
            try:
                webhooks = await self.target_channel.webhooks()
                self.webhook = webhooks[0] if webhooks else await self.target_channel.create_webhook(name="SwitchMesh Bridge")
                print(f"🔗 Multi-Agent Webhook Active: {self.webhook.name}")
            except Exception as e:
                print(f"⚠️ Webhook creation restricted; falling back to Embed replies: {e}")

            # Post room activation notice
            welcome = (
                f"⚡ **SwitchMesh Multi-Agent Room Active**\n"
                f"Mode: `{self.workflow_type.upper()}`\n"
                f"Agents in room: " + ", ".join([f"`@{a}`" for a in self.harness.agent_registry.keys()]) + "\n"
                f"Type a task or report to begin collaboration!"
            )
            await self.target_channel.send(welcome)

        @self.client.event
        async def on_message(message: discord.Message):
            # Ignore own messages
            if message.author == self.client.user:
                return
            if message.channel.id != self.channel_id:
                return

            author_name = message.author.display_name
            content = message.content

            print(f"📥 [Discord] {author_name}: {content}")

            # 1. Forward human message to Switch harness
            self.harness.post_message(
                author_id=str(message.author.id),
                author_name=author_name,
                role=MessageRole.HUMAN,
                content=content
            )

            # 2. Check if this resolves a pending Dual-Custody Gate
            if "approve" in content.lower() or "reject" in content.lower():
                resolved_gate = self.harness.resolve_gate_from_message(author_name, content)
                if resolved_gate:
                    if resolved_gate.outcome.value == "APPROVED" and self.workflow_type == "sre":
                        await asyncio.sleep(1)
                        report = self.sre_flow.sentinel.execute_post_approval_remediation(self.harness, resolved_gate)
                        await self.post_agent_message("security-sentinel", "Security Sentinel", report)
                    return

            # 3. Process workflow triggers
            if self.workflow_type == "sre":
                await self._handle_sre_triggers(content, author_name)
            else:
                await self._handle_creative_triggers(content, author_name)

    async def _handle_sre_triggers(self, content: str, author_name: str):
        lower = content.lower()
        if "checkout" in lower or "failing" in lower or "500" in lower or "alert" in lower:
            # Stage 2: Triage
            await self.target_channel.typing()
            await asyncio.sleep(1.5)
            triage_text = self.sre_flow.triager.handle_message(self.harness.messages[-1])
            await self.post_agent_message("sre-triager", "SRE Triager (Agent)", triage_text)

            # Stage 3: Chaos Repro
            await self.target_channel.typing()
            await asyncio.sleep(2.0)
            res, repro_text = self.sre_flow.reproducer.reproduce_bug()
            await self.post_agent_message("chaos-reproducer", "Chaos Reproducer (Agent)", repro_text)

            # Stage 4: Patch Architect
            await self.target_channel.typing()
            await asyncio.sleep(2.0)
            res_patch, patch_text = self.sre_flow.patcher.generate_and_verify_patch()
            await self.post_agent_message("patch-architect", "Patch Architect (Agent)", patch_text)

            # Stage 5: Dual Custody Gate
            await asyncio.sleep(1.0)
            gate = self.sre_flow.sentinel.request_production_gate(self.harness, approver=author_name)
            gate_msg = self.harness.messages[-1]
            await self.post_agent_message("security-sentinel", "Security Sentinel (Trust Gate)", gate_msg.content)

    async def _handle_creative_triggers(self, content: str, author_name: str):
        lower = content.lower()
        if "build" in lower or "game" in lower or "create" in lower:
            # Stage 2: Worldsmith
            await self.target_channel.typing()
            await asyncio.sleep(1.5)
            bible = self.creative_flow.worldsmith.create_game_bible(content)
            text_bible = self.creative_flow.worldsmith.format_room_presentation(bible)
            await self.post_agent_message("worldsmith", "Worldsmith (Narrative Agent)", text_bible)

            # Stage 3: Audio Alchemist
            await self.target_channel.typing()
            await asyncio.sleep(1.5)
            text_audio = self.creative_flow.alchemist.format_room_presentation()
            await self.post_agent_message("audio-alchemist", "Audio Alchemist (Synthesizer Agent)", text_audio)

            # Stage 4: Canvas Mechanic
            await self.target_channel.typing()
            await asyncio.sleep(2.0)
            url = self.creative_flow.game_server.start()
            text_canvas = self.creative_flow.mechanic.format_room_presentation(url)
            await self.post_agent_message("canvas-mechanic", "Canvas Mechanic (Engine Agent)", text_canvas)

            # Stage 5: Game Critic
            await asyncio.sleep(1.0)
            game_html = self.creative_flow.mechanic.generate_html5_game()
            eval_data = self.creative_flow.critic.evaluate_game_balance(game_html)
            text_critic = self.creative_flow.critic.format_room_presentation(eval_data)
            await self.post_agent_message("game-critic", "Game Critic (Playtester Agent)", text_critic)

        elif "speed" in lower or "particle" in lower or "color" in lower or "tweak" in lower:
            # Hot reload
            await self.target_channel.typing()
            await asyncio.sleep(1.0)
            self.creative_flow.run_stage_6_creator_tweak(content)
            await self.post_agent_message(
                "canvas-mechanic",
                "Canvas Mechanic",
                f"⚡ **[HOT-RELOAD LIVE]** Applied voice tweak: '{content}'. Re-rendered 60 FPS Canvas engine at http://localhost:8800!"
            )

    async def post_agent_message(self, agent_id: str, display_name: str, content: str):
        """Posts a message using Webhook (with avatar/name) or Rich Embed fallback."""
        avatar_url = AGENT_AVATARS.get(agent_id)
        if self.webhook:
            try:
                await self.webhook.send(
                    content=content,
                    username=display_name,
                    avatar_url=avatar_url
                )
                return
            except Exception:
                pass

        # Fallback to bot embed
        embed = discord.Embed(
            description=content,
            color=0x00f3ff if "patch" in agent_id or "mechanic" in agent_id else 0xff0055
        )
        embed.set_author(name=display_name, icon_url=avatar_url)
        await self.target_channel.send(embed=embed)

    def run(self):
        self.client.run(self.bot_token)
