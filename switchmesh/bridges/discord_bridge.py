"""
Real Discord Platform Bridge for SwitchMesh.
Connects a real Discord bot to Switch rooms, enabling multi-agent collaboration
where each agent speaks with its own persona and avatar via Webhooks or Rich Embeds.
Supports real GitHub Pull Request creation, human approval gating, and auto-merging!
"""

from __future__ import annotations
import asyncio
import os
import sys
import traceback
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

# Configurable agent delay for realistic deterministic cadence (1 to 2 minutes)
DEFAULT_DELAY = int(os.getenv("AGENT_DELAY_SECONDS", "60"))


class DiscordSwitchBridge:
    def __init__(
        self,
        bot_token: str,
        channel_id: Optional[int] = None,
        workflow_type: str = "sre",
        delay_seconds: int = DEFAULT_DELAY
    ):
        self.bot_token = bot_token
        self.target_channel_id = channel_id if channel_id and channel_id > 0 else None
        self.workflow_type = workflow_type
        self.delay_seconds = delay_seconds

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
        self.channel_webhooks: Dict[int, discord.Webhook] = {}

        self._setup_events()

    def _setup_events(self):
        @self.client.event
        async def on_ready():
            print(f"✅ Discord Bridge Connected as {self.client.user} (ID: {self.client.user.id})")
            print(f"⏱️ Agent Response Delay set to: {self.delay_seconds}s (Deterministic pacing)")
            print(f"📡 Bot is member of {len(self.client.guilds)} server(s):")
            for g in self.client.guilds:
                print(f"  • Guild: '{g.name}' (ID: {g.id})")
                for ch in g.text_channels:
                    print(f"    - #{ch.name} (ID: {ch.id})")

        @self.client.event
        async def on_message(message: discord.Message):
            # Ignore own messages
            if message.author == self.client.user:
                return

            # Check channel filter if specified
            if self.target_channel_id and message.channel.id != self.target_channel_id:
                return

            author_name = message.author.display_name
            content = message.content.strip()
            if not content:
                return

            print(f"📥 [Discord] #{message.channel.name} | {author_name}: {content}")

            try:
                # 1. Forward human message to Switch harness
                self.harness.post_message(
                    author_id=str(message.author.id),
                    author_name=author_name,
                    role=MessageRole.HUMAN,
                    content=content
                )

                # 2. Check if this resolves a pending Dual-Custody Gate
                if any(w in content.lower() for w in ["approve", "reject", "merge", "roll back", "rollback"]):
                    resolved_gate = self.harness.resolve_gate_from_message(author_name, content)
                    if resolved_gate:
                        if resolved_gate.outcome.value == "APPROVED" and self.workflow_type == "sre":
                            await channel_typing_wait(message.channel, min(10, self.delay_seconds))
                            report = self.sre_flow.sentinel.execute_post_approval_remediation(self.harness, resolved_gate)
                            await self.post_agent_message(message.channel, "security-sentinel", "Security Sentinel (Trust Gate)", report)
                        return

                # 3. Process workflow triggers
                if self.workflow_type == "sre":
                    await self._handle_sre_triggers(message.channel, content, author_name)
                else:
                    await self._handle_creative_triggers(message.channel, content, author_name)

            except Exception as e:
                print(f"❌ Error in on_message: {e}")
                traceback.print_exc()

    async def _handle_sre_triggers(self, channel: discord.TextChannel, content: str, author_name: str):
        lower = content.lower()
        if any(k in lower for k in ["checkout", "failing", "500", "alert", "error", "cart", "bug", "crash"]):
            print(f"🚀 Triggering SRE Multi-Agent Swarm with {self.delay_seconds}s realistic cadence...")

            # Stage 2: Triage
            await channel_typing_wait(channel, self.delay_seconds, "SRE Triager is analyzing telemetry & git log...")
            triage_text = await self.sre_flow.triager.handle_message_async(content)
            await self.post_agent_message(channel, "sre-triager", "SRE Triager (Agent)", triage_text)

            # Stage 3: Chaos Repro
            await channel_typing_wait(channel, self.delay_seconds, "Chaos Reproducer is executing isolated ephemeral sandbox...")
            res, repro_text = self.sre_flow.reproducer.reproduce_bug()
            await self.post_agent_message(channel, "chaos-reproducer", "Chaos Reproducer (Agent)", repro_text)

            # Stage 4: Patch Architect
            await channel_typing_wait(channel, self.delay_seconds, "Patch Architect is writing regression tests & opening Pull Request on GitHub...")
            res_patch, patch_text = self.sre_flow.patcher.generate_and_verify_patch(create_pr=True)
            await self.post_agent_message(channel, "patch-architect", "Patch Architect (Agent)", patch_text)

            # Stage 5: Dual Custody Gate
            await asyncio.sleep(2.0)
            gate = self.sre_flow.sentinel.request_production_gate(
                self.harness,
                approver=author_name,
                pr_number=self.sre_flow.patcher.last_pr_number,
                pr_url=self.sre_flow.patcher.last_pr_url
            )
            gate_msg = self.harness.messages[-1]
            await self.post_agent_message(channel, "security-sentinel", "Security Sentinel (Trust Gate)", gate_msg.content)

        elif any(k in lower for k in ["hi", "hello", "hey", "help", "who"]):
            greeting = (
                f"👋 **Hello {author_name}!** I am the **SwitchMesh Autonomous SRE Incident Coordinator**.\n"
                f"- **Active Teammates:** `@sre-triager`, `@chaos-reproducer`, `@patch-architect`, `@security-sentinel`\n"
                f"- **Live Demo Repository:** https://github.com/HirthikBalaji/cart-service-demo (Check main branch: code is broken and 0 PRs exist!)\n"
                f"- **Trigger the incident response:** Type `checkout is failing with 500 errors on cart service`\n"
                f"- **Realistic Agent Delay:** `{self.delay_seconds}s` per stage to showcase live to judges!"
            )
            await channel.send(greeting)

    async def _handle_creative_triggers(self, channel: discord.TextChannel, content: str, author_name: str):
        lower = content.lower()
        if any(k in lower for k in ["build", "game", "create", "arcade", "cyberglitch"]):
            # Stage 2: Worldsmith
            await channel_typing_wait(channel, min(15, self.delay_seconds), "Worldsmith is writing Game Bible & mechanics...")
            bible = self.creative_flow.worldsmith.create_game_bible(content)
            text_bible = self.creative_flow.worldsmith.format_room_presentation(bible)
            await self.post_agent_message(channel, "worldsmith", "Worldsmith (Narrative Agent)", text_bible)

            # Stage 3: Audio Alchemist
            await channel_typing_wait(channel, min(15, self.delay_seconds), "Audio Alchemist is synthesizing Web Audio oscillators...")
            text_audio = self.creative_flow.alchemist.format_room_presentation()
            await self.post_agent_message(channel, "audio-alchemist", "Audio Alchemist (Synthesizer Agent)", text_audio)

            # Stage 4: Canvas Mechanic
            await channel_typing_wait(channel, min(20, self.delay_seconds), "Canvas Mechanic is compiling HTML5 engine...")
            url = self.creative_flow.game_server.start()
            text_canvas = self.creative_flow.mechanic.format_room_presentation(url)
            await self.post_agent_message(channel, "canvas-mechanic", "Canvas Mechanic (Engine Agent)", text_canvas)

            # Stage 5: Game Critic
            await asyncio.sleep(2.0)
            game_html = self.creative_flow.mechanic.generate_html5_game()
            eval_data = self.creative_flow.critic.evaluate_game_balance(game_html)
            text_critic = self.creative_flow.critic.format_room_presentation(eval_data)
            await self.post_agent_message(channel, "game-critic", "Game Critic (Playtester Agent)", text_critic)

        elif any(k in lower for k in ["speed", "particle", "color", "tweak", "hot-reload"]):
            async with channel.typing():
                await asyncio.sleep(2.0)
                self.creative_flow.run_stage_6_creator_tweak(content)
            await self.post_agent_message(
                channel,
                "canvas-mechanic",
                "Canvas Mechanic (Engine Agent)",
                f"⚡ **[HOT-RELOAD LIVE]** Applied voice tweak: '{content}'. Live 60 FPS Canvas engine re-rendered at http://localhost:8800!"
            )

    async def post_agent_message(self, channel: discord.TextChannel, agent_id: str, display_name: str, content: str):
        """Posts a message using Webhook or Rich Embed fallback."""
        if not content:
            return

        avatar_url = AGENT_AVATARS.get(agent_id)

        # 1. Try Webhook first (if permitted)
        webhook = self.channel_webhooks.get(channel.id)
        if not webhook:
            try:
                hooks = await channel.webhooks()
                webhook = hooks[0] if hooks else await channel.create_webhook(name="SwitchMesh Bridge")
                self.channel_webhooks[channel.id] = webhook
            except Exception:
                webhook = None

        if webhook:
            try:
                await webhook.send(
                    content=content[:2000],
                    username=display_name,
                    avatar_url=avatar_url
                )
                print(f"📤 Sent via Webhook: {display_name}")
                return
            except Exception as e:
                print(f"⚠️ Webhook send failed: {e}")

        # 2. Try Embed fallback
        try:
            embed = discord.Embed(
                description=content[:4000],
                color=0x00f3ff if "patch" in agent_id or "mechanic" in agent_id else 0xff0055
            )
            embed.set_author(name=display_name, icon_url=avatar_url)
            await channel.send(embed=embed)
            print(f"📤 Sent via Embed: {display_name}")
            return
        except Exception as e:
            print(f"⚠️ Embed send failed: {e}; attempting plain text fallback")

        # 3. Plain text fallback
        for i in range(0, len(content), 1900):
            await channel.send(f"**[{display_name}]**\n{content[i:i+1900]}")
        print(f"📤 Sent via Plain Text: {display_name}")

    def run(self):
        self.client.run(self.bot_token)


async def channel_typing_wait(channel: discord.TextChannel, duration_seconds: int, status_notice: str = ""):
    """Shows typing indicator and waits for the configured duration."""
    if status_notice and duration_seconds >= 10:
        await channel.send(f"⏳ *{status_notice} (Realistic cadence: ~{duration_seconds}s)*")
    chunks = max(1, duration_seconds // 8)
    for _ in range(chunks):
        async with channel.typing():
            await asyncio.sleep(min(8, duration_seconds / chunks))
