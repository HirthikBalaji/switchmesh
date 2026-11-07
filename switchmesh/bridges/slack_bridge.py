"""
Real Slack Platform Bridge for SwitchMesh.
Uses Slack Socket Mode to establish an outbound WebSocket connection,
delivering multi-agent turns, real GitHub PR creation, Block Kit cards, and auto-merging into Slack.
"""

from __future__ import annotations
import asyncio
import os
import sys
from typing import Dict, Optional
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse
from switchmesh.protocol.types import MessageRole, RoomMessage
from switchmesh.workflows.business_sre.incident_sim import SREWarRoomWorkflow
from switchmesh.workflows.creative_studio.studio_sim import CreativeStudioWorkflow

DEFAULT_DELAY = int(os.getenv("AGENT_DELAY_SECONDS", "60"))


class SlackSwitchBridge:
    def __init__(
        self,
        bot_token: str,
        app_token: str,
        channel_id: Optional[str] = None,
        workflow_type: str = "sre",
        delay_seconds: int = DEFAULT_DELAY
    ):
        self.bot_token = bot_token
        self.app_token = app_token
        self.default_channel_id = channel_id
        self.workflow_type = workflow_type
        self.delay_seconds = delay_seconds

        self.web_client = AsyncWebClient(token=bot_token)
        self.socket_client: Optional[SocketModeClient] = None

        if workflow_type == "sre":
            self.sre_flow = SREWarRoomWorkflow("slack-sre-room", bridge="slack")
            self.harness = self.sre_flow.harness
        else:
            self.creative_flow = CreativeStudioWorkflow("slack-creative-room", bridge="slack")
            self.harness = self.creative_flow.harness

    async def _process_socket_request(self, client: SocketModeClient, req: SocketModeRequest):
        # Acknowledge receipt immediately to Slack
        response = SocketModeResponse(envelope_id=req.envelope_id)
        await client.send_socket_mode_response(response)

        if req.type == "events_api":
            event = req.payload.get("event", {})
            event_type = event.get("type")

            # Ignore own bot messages or subtype updates
            if event.get("bot_id") or event.get("subtype") == "bot_message":
                return

            # Handle user messages and mentions
            if event_type in ("message", "app_mention"):
                channel = event.get("channel") or self.default_channel_id
                text = event.get("text", "").strip()
                user = event.get("user", "human_lead")
                thread_ts = event.get("thread_ts") or event.get("ts")

                if not text:
                    return

                print(f"📥 [Slack] User {user} in #{channel}: {text}")

                # Forward to Switch harness
                self.harness.post_message(
                    author_id=user,
                    author_name=f"SlackUser-{user[-4:]}",
                    role=MessageRole.HUMAN,
                    content=text
                )

                # Check for Dual Custody resolution
                if any(w in text.lower() for w in ["approve", "reject", "merge", "roll back", "rollback"]):
                    resolved = self.harness.resolve_gate_from_message(user, text)
                    if resolved and resolved.outcome.value == "APPROVED" and self.workflow_type == "sre":
                        await asyncio.sleep(min(10, self.delay_seconds))
                        report = self.sre_flow.sentinel.execute_post_approval_remediation(self.harness, resolved)
                        await self.post_agent_message(
                            "Security Sentinel (Trust Gate)",
                            report,
                            channel=channel,
                            thread_ts=thread_ts
                        )
                    return

                # Trigger workflow turns
                if self.workflow_type == "sre":
                    await self._handle_sre_triggers(text, user, channel, thread_ts)
                else:
                    await self._handle_creative_triggers(text, user, channel, thread_ts)

    async def _handle_sre_triggers(self, text: str, user: str, channel: str, thread_ts: str):
        lower = text.lower()
        if any(k in lower for k in ["checkout", "failing", "500", "alert", "error", "cart", "bug"]):
            # 1. Triage
            if self.delay_seconds >= 10:
                await self.post_agent_message("Switch Coordinator", f"⏳ *Incident received. SRE Triager analyzing... (~{self.delay_seconds}s cadence)*", channel=channel, thread_ts=thread_ts)
                await asyncio.sleep(self.delay_seconds)
            triage_text = await self.sre_flow.triager.handle_message_async(text)
            await self.post_agent_message("SRE Triager (Agent)", triage_text, channel=channel, thread_ts=thread_ts)

            # 2. Chaos Repro
            if self.delay_seconds >= 10:
                await self.post_agent_message("Switch Coordinator", f"⏳ *Chaos Reproducer spinning up isolated ephemeral sandbox... (~{self.delay_seconds}s)*", channel=channel, thread_ts=thread_ts)
                await asyncio.sleep(self.delay_seconds)
            res, repro_text = self.sre_flow.reproducer.reproduce_bug()
            await self.post_agent_message("Chaos Reproducer (Agent)", repro_text, channel=channel, thread_ts=thread_ts)

            # 3. Patch Architect (Creates real GitHub PR)
            if self.delay_seconds >= 10:
                await self.post_agent_message("Switch Coordinator", f"⏳ *Patch Architect synthesizing hotfix & opening Pull Request on GitHub... (~{self.delay_seconds}s)*", channel=channel, thread_ts=thread_ts)
                await asyncio.sleep(self.delay_seconds)
            res_patch, patch_text = self.sre_flow.patcher.generate_and_verify_patch(create_pr=True)
            await self.post_agent_message("Patch Architect (Agent)", patch_text, channel=channel, thread_ts=thread_ts)

            # 4. Dual Custody Gate
            await asyncio.sleep(2.0)
            gate = self.sre_flow.sentinel.request_production_gate(
                self.harness,
                approver=user,
                pr_number=self.sre_flow.patcher.last_pr_number,
                pr_url=self.sre_flow.patcher.last_pr_url
            )
            gate_msg = self.harness.messages[-1]
            await self.post_agent_message("Security Sentinel (Trust Gate)", gate_msg.content, channel=channel, thread_ts=thread_ts)

        elif any(k in lower for k in ["hi", "hello", "help", "who"]):
            greeting = (
                f"👋 *SwitchMesh Autonomous SRE Incident Coordinator*\n"
                f"• Active Swarm: `@sre-triager`, `@chaos-reproducer`, `@patch-architect`, `@security-sentinel`\n"
                f"• Live Demo Repo: https://github.com/HirthikBalaji/cart-service-demo (Check main: broken code & 0 PRs!)\n"
                f"• To begin: Type `checkout is failing with 500 errors on cart service`"
            )
            await self.post_agent_message("Switch Coordinator", greeting, channel=channel, thread_ts=thread_ts)

    async def _handle_creative_triggers(self, text: str, user: str, channel: str, thread_ts: str):
        lower = text.lower()
        if any(k in lower for k in ["build", "game", "create", "arcade", "cyberglitch"]):
            # Worldsmith
            await asyncio.sleep(min(15, self.delay_seconds))
            bible = self.creative_flow.worldsmith.create_game_bible(text)
            await self.post_agent_message(
                "Worldsmith (Narrative Agent)",
                self.creative_flow.worldsmith.format_room_presentation(bible),
                channel=channel,
                thread_ts=thread_ts
            )

            # Audio Alchemist
            await asyncio.sleep(min(15, self.delay_seconds))
            await self.post_agent_message(
                "Audio Alchemist (Synthesizer Agent)",
                self.creative_flow.alchemist.format_room_presentation(),
                channel=channel,
                thread_ts=thread_ts
            )

            # Canvas Mechanic
            await asyncio.sleep(min(20, self.delay_seconds))
            url = self.creative_flow.game_server.start()
            await self.post_agent_message(
                "Canvas Mechanic (Engine Agent)",
                self.creative_flow.mechanic.format_room_presentation(url),
                channel=channel,
                thread_ts=thread_ts
            )

            # Critic
            await asyncio.sleep(2.0)
            game_html = self.creative_flow.mechanic.generate_html5_game()
            eval_data = self.creative_flow.critic.evaluate_game_balance(game_html)
            await self.post_agent_message(
                "Game Critic (Playtester Agent)",
                self.creative_flow.critic.format_room_presentation(eval_data),
                channel=channel,
                thread_ts=thread_ts
            )

        elif any(k in lower for k in ["speed", "particle", "color", "tweak", "hot-reload"]):
            self.creative_flow.run_stage_6_creator_tweak(text)
            await self.post_agent_message(
                "Canvas Mechanic (Engine Agent)",
                f"⚡ **[HOT-RELOAD APPLIED]** Voice tweak '{text}' applied to live canvas game at http://localhost:8800!",
                channel=channel,
                thread_ts=thread_ts
            )

    async def post_agent_message(self, agent_name: str, content: str, channel: Optional[str] = None, thread_ts: Optional[str] = None):
        """Posts a formatted message to Slack."""
        target_channel = channel or self.default_channel_id
        if not target_channel:
            print(f"⚠️ No target channel for agent {agent_name}")
            return

        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{agent_name}*\n{content}"
                }
            }
        ]
        try:
            await self.web_client.chat_postMessage(
                channel=target_channel,
                text=f"{agent_name}: {content[:100]}...",
                blocks=blocks,
                thread_ts=thread_ts
            )
        except Exception as e:
            print(f"❌ Slack post error in #{target_channel}: {e}")

    async def start(self):
        print("⚡ Initializing Slack Socket Mode client...")
        self.socket_client = SocketModeClient(
            app_token=self.app_token,
            web_client=self.web_client
        )
        self.socket_client.socket_mode_request_listeners.append(self._process_socket_request)

        print("⚡ Connecting outbound WebSocket to Slack...")
        await self.socket_client.connect()
        print(f"✅ Slack Bridge Connected! Listening on workspace (Default Channel: {self.default_channel_id})")
        # Keep alive
        await asyncio.Event().wait()
