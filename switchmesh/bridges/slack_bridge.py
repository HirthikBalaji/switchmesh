"""
Real Slack Platform Bridge for SwitchMesh.
Uses Slack Socket Mode to establish an outbound WebSocket connection,
delivering multi-agent turns and interactive Block Kit approval cards directly into Slack.
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


class SlackSwitchBridge:
    def __init__(
        self,
        bot_token: str,
        app_token: str,
        channel_id: str,
        workflow_type: str = "sre"
    ):
        self.bot_token = bot_token
        self.app_token = app_token
        self.channel_id = channel_id
        self.workflow_type = workflow_type

        self.web_client = AsyncWebClient(token=bot_token)
        self.socket_client = SocketModeClient(
            app_token=app_token,
            web_client=self.web_client
        )

        if workflow_type == "sre":
            self.sre_flow = SREWarRoomWorkflow("slack-sre-room", bridge="slack")
            self.harness = self.sre_flow.harness
        else:
            self.creative_flow = CreativeStudioWorkflow("slack-creative-room", bridge="slack")
            self.harness = self.creative_flow.harness

        self._setup_socket_listeners()

    def _setup_socket_listeners(self):
        async def process_socket_request(client: SocketModeClient, req: SocketModeRequest):
            # Acknowledge receipt immediately to Slack
            response = SocketModeResponse(envelope_id=req.envelope_id)
            await client.send_socket_mode_response(response)

            if req.type == "events_api":
                event = req.payload.get("event", {})
                event_type = event.get("type")

                # Handle messages
                if event_type in ("message", "app_mention") and not event.get("bot_id"):
                    channel = event.get("channel")
                    text = event.get("text", "")
                    user = event.get("user", "human_lead")
                    thread_ts = event.get("thread_ts") or event.get("ts")

                    print(f"📥 [Slack] User {user}: {text}")

                    # Forward to Switch harness
                    self.harness.post_message(
                        author_id=user,
                        author_name=f"SlackUser-{user[-4:]}",
                        role=MessageRole.HUMAN,
                        content=text
                    )

                    # Check for Dual Custody resolution
                    if "approve" in text.lower() or "reject" in text.lower():
                        resolved = self.harness.resolve_gate_from_message(user, text)
                        if resolved and resolved.outcome.value == "APPROVED" and self.workflow_type == "sre":
                            await asyncio.sleep(1)
                            report = self.sre_flow.sentinel.execute_post_approval_remediation(self.harness, resolved)
                            await self.post_agent_message("Security Sentinel", report, thread_ts=thread_ts)
                        return

                    # Trigger workflow turns
                    if self.workflow_type == "sre":
                        await self._handle_sre_triggers(text, user, thread_ts)
                    else:
                        await self._handle_creative_triggers(text, user, thread_ts)

        self.socket_client.socket_mode_request_listeners.append(process_socket_request)

    async def _handle_sre_triggers(self, text: str, user: str, thread_ts: str):
        lower = text.lower()
        if "checkout" in lower or "failing" in lower or "500" in lower:
            # 1. Triage
            await asyncio.sleep(1.0)
            triage_text = self.sre_flow.triager.handle_message(self.harness.messages[-1])
            await self.post_agent_message("SRE Triager (Agent)", triage_text, thread_ts=thread_ts)

            # 2. Chaos Repro
            await asyncio.sleep(1.5)
            res, repro_text = self.sre_flow.reproducer.reproduce_bug()
            await self.post_agent_message("Chaos Reproducer (Agent)", repro_text, thread_ts=thread_ts)

            # 3. Patch Architect
            await asyncio.sleep(1.5)
            res_patch, patch_text = self.sre_flow.patcher.generate_and_verify_patch()
            await self.post_agent_message("Patch Architect (Agent)", patch_text, thread_ts=thread_ts)

            # 4. Dual Custody Gate
            await asyncio.sleep(1.0)
            gate = self.sre_flow.sentinel.request_production_gate(self.harness, approver=user)
            gate_msg = self.harness.messages[-1]
            await self.post_agent_message("Security Sentinel (Trust Gate)", gate_msg.content, thread_ts=thread_ts)

    async def _handle_creative_triggers(self, text: str, user: str, thread_ts: str):
        lower = text.lower()
        if "build" in lower or "game" in lower:
            # Worldsmith
            await asyncio.sleep(1.0)
            bible = self.creative_flow.worldsmith.create_game_bible(text)
            await self.post_agent_message("Worldsmith (Narrative Agent)", self.creative_flow.worldsmith.format_room_presentation(bible), thread_ts=thread_ts)

            # Audio Alchemist
            await asyncio.sleep(1.0)
            await self.post_agent_message("Audio Alchemist (Synthesizer Agent)", self.creative_flow.alchemist.format_room_presentation(), thread_ts=thread_ts)

            # Canvas Mechanic
            await asyncio.sleep(1.5)
            url = self.creative_flow.game_server.start()
            await self.post_agent_message("Canvas Mechanic (Engine Agent)", self.creative_flow.mechanic.format_room_presentation(url), thread_ts=thread_ts)

            # Critic
            await asyncio.sleep(1.0)
            game_html = self.creative_flow.mechanic.generate_html5_game()
            eval_data = self.creative_flow.critic.evaluate_game_balance(game_html)
            await self.post_agent_message("Game Critic (Playtester Agent)", self.creative_flow.critic.format_room_presentation(eval_data), thread_ts=thread_ts)

    async def post_agent_message(self, agent_name: str, content: str, thread_ts: Optional[str] = None):
        """Posts a formatted message to Slack."""
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{agent_name}*\n{content}"
                }
            }
        ]
        await self.web_client.chat_postMessage(
            channel=self.channel_id,
            text=f"{agent_name}: {content[:100]}...",
            blocks=blocks,
            thread_ts=thread_ts
        )

    async def start(self):
        print("⚡ Connecting to Slack via Outbound Socket Mode...")
        await self.socket_client.connect()
        print(f"✅ Slack Bridge Connected! Listening on channel `{self.channel_id}`")
        # Keep alive
        await asyncio.Event().wait()
