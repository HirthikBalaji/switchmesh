"""
Real Telegram Platform Bridge for SwitchMesh.
Uses Telegram Bot API long-polling to connect Telegram group chats or direct messages
directly into SwitchMesh multi-agent rooms.
"""

from __future__ import annotations
import asyncio
import os
from typing import Dict, Optional
import httpx
from switchmesh.protocol.types import MessageRole
from switchmesh.workflows.business_sre.incident_sim import SREWarRoomWorkflow
from switchmesh.workflows.creative_studio.studio_sim import CreativeStudioWorkflow


class TelegramSwitchBridge:
    def __init__(self, bot_token: str, chat_id: Optional[str] = None, workflow_type: str = "sre"):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.workflow_type = workflow_type
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.offset = 0

        if workflow_type == "sre":
            self.sre_flow = SREWarRoomWorkflow("telegram-sre-room", bridge="telegram")
            self.harness = self.sre_flow.harness
        else:
            self.creative_flow = CreativeStudioWorkflow("telegram-creative-room", bridge="telegram")
            self.harness = self.creative_flow.harness

    async def send_message(self, chat_id: str | int, text: str):
        """Sends a message to Telegram with Markdown formatting."""
        async with httpx.AsyncClient() as client:
            try:
                await client.post(
                    f"{self.base_url}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": text,
                        "parse_mode": "Markdown"
                    },
                    timeout=10.0
                )
            except Exception as e:
                # If markdown parsing fails due to special chars, send plain text
                await client.post(
                    f"{self.base_url}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": text
                    },
                    timeout=10.0
                )

    async def poll_updates(self):
        print(f"⚡ Telegram Bridge Polling Active for Bot `{self.bot_token[:10]}...`")
        async with httpx.AsyncClient(timeout=35.0) as client:
            while True:
                try:
                    resp = await client.get(
                        f"{self.base_url}/getUpdates",
                        params={"offset": self.offset, "timeout": 25}
                    )
                    data = resp.json()
                    if not data.get("ok"):
                        await asyncio.sleep(3)
                        continue

                    updates = data.get("result", [])
                    for update in updates:
                        self.offset = update["update_id"] + 1
                        message = update.get("message")
                        if not message or "text" not in message:
                            continue

                        chat_id = message["chat"]["id"]
                        text = message["text"]
                        user = message.get("from", {}).get("username") or message.get("from", {}).get("first_name", "TelegramUser")

                        print(f"📥 [Telegram] {user}: {text}")

                        # Forward to Switch harness
                        self.harness.post_message(
                            author_id=str(user),
                            author_name=user,
                            role=MessageRole.HUMAN,
                            content=text
                        )

                        # Check Dual Custody resolution
                        if "approve" in text.lower() or "reject" in text.lower():
                            resolved = self.harness.resolve_gate_from_message(user, text)
                            if resolved and resolved.outcome.value == "APPROVED" and self.workflow_type == "sre":
                                await asyncio.sleep(1)
                                report = self.sre_flow.sentinel.execute_post_approval_remediation(self.harness, resolved)
                                await self.send_message(chat_id, f"🛡️ *Security Sentinel*\n\n{report}")
                            continue

                        # SRE Workflow
                        if self.workflow_type == "sre":
                            if any(k in text.lower() for k in ["checkout", "failing", "500", "alert"]):
                                # 1. Triage
                                triage_text = self.sre_flow.triager.handle_message(self.harness.messages[-1])
                                await self.send_message(chat_id, f"🚨 *SRE Triager*\n\n{triage_text}")

                                # 2. Repro
                                res, repro_text = self.sre_flow.reproducer.reproduce_bug()
                                await self.send_message(chat_id, f"🔍 *Chaos Reproducer*\n\n{repro_text}")

                                # 3. Patch
                                res_patch, patch_text = self.sre_flow.patcher.generate_and_verify_patch()
                                await self.send_message(chat_id, f"🛠️ *Patch Architect*\n\n{patch_text}")

                                # 4. Gate
                                gate = self.sre_flow.sentinel.request_production_gate(self.harness, approver=user)
                                await self.send_message(chat_id, f"🔒 *Switch Trust Dual-Custody Gate*\n\n{self.harness.messages[-1].content}")

                        # Creative Workflow
                        else:
                            if any(k in text.lower() for k in ["build", "game", "create"]):
                                bible = self.creative_flow.worldsmith.create_game_bible(text)
                                await self.send_message(chat_id, f"🌌 *Worldsmith*\n\n{self.creative_flow.worldsmith.format_room_presentation(bible)}")

                                await self.send_message(chat_id, f"🎵 *Audio Alchemist*\n\n{self.creative_flow.alchemist.format_room_presentation()}")

                                url = self.creative_flow.game_server.start()
                                await self.send_message(chat_id, f"🎮 *Canvas Mechanic*\n\n{self.creative_flow.mechanic.format_room_presentation(url)}")

                                game_html = self.creative_flow.mechanic.generate_html5_game()
                                eval_data = self.creative_flow.critic.evaluate_game_balance(game_html)
                                await self.send_message(chat_id, f"🎯 *Game Critic*\n\n{self.creative_flow.critic.format_room_presentation(eval_data)}")

                except Exception as e:
                    print(f"⚠️ Telegram poll error: {e}")
                    await asyncio.sleep(5)
