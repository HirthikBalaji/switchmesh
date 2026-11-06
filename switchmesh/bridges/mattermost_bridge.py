"""
Real Mattermost Platform Bridge for SwitchMesh.
Connects directly to local or cloud Mattermost installations (including the default
Mattermost spun up by Switch Console in Docker at http://localhost:8065).
"""

from __future__ import annotations
import asyncio
import json
import os
from typing import Dict, Optional
import httpx
from switchmesh.protocol.types import MessageRole
from switchmesh.workflows.business_sre.incident_sim import SREWarRoomWorkflow
from switchmesh.workflows.creative_studio.studio_sim import CreativeStudioWorkflow


class MattermostSwitchBridge:
    def __init__(
        self,
        base_url: str = "http://localhost:8065",
        bot_token: str = "",
        channel_id: str = "",
        workflow_type: str = "sre"
    ):
        self.base_url = base_url.rstrip("/")
        self.bot_token = bot_token
        self.channel_id = channel_id
        self.workflow_type = workflow_type

        self.headers = {
            "Authorization": f"Bearer {bot_token}",
            "Content-Type": "application/json"
        }

        if workflow_type == "sre":
            self.sre_flow = SREWarRoomWorkflow("mattermost-sre-room", bridge="mattermost")
            self.harness = self.sre_flow.harness
        else:
            self.creative_flow = CreativeStudioWorkflow("mattermost-creative-room", bridge="mattermost")
            self.harness = self.creative_flow.harness

    async def post_to_channel(self, message: str, root_id: Optional[str] = None):
        """Posts a message to the Mattermost channel."""
        async with httpx.AsyncClient() as client:
            payload = {
                "channel_id": self.channel_id,
                "message": message
            }
            if root_id:
                payload["root_id"] = root_id

            resp = await client.post(
                f"{self.base_url}/api/v4/posts",
                headers=self.headers,
                json=payload,
                timeout=10.0
            )
            return resp.json()

    async def poll_channel_posts(self):
        """Polls Mattermost channel for latest posts."""
        print(f"⚡ Connected to Mattermost at {self.base_url} (Channel: {self.channel_id})")
        last_post_id = None

        async with httpx.AsyncClient() as client:
            while True:
                try:
                    resp = await client.get(
                        f"{self.base_url}/api/v4/channels/{self.channel_id}/posts?per_page=5",
                        headers=self.headers,
                        timeout=10.0
                    )
                    data = resp.json()
                    order = data.get("order", [])
                    posts = data.get("posts", {})

                    if order:
                        latest_id = order[0]
                        if last_post_id and latest_id != last_post_id:
                            post = posts.get(latest_id, {})
                            # Check if human post (not bot)
                            props = post.get("props", {})
                            if not props.get("from_bot"):
                                text = post.get("message", "")
                                user_id = post.get("user_id", "human_lead")
                                print(f"📥 [Mattermost] {user_id}: {text}")

                                self.harness.post_message(
                                    author_id=user_id,
                                    author_name="MattermostLead",
                                    role=MessageRole.HUMAN,
                                    content=text
                                )

                                # Handle SRE
                                if self.workflow_type == "sre":
                                    if "approve" in text.lower():
                                        res = self.harness.resolve_gate_from_message("MattermostLead", text)
                                        if res and res.outcome.value == "APPROVED":
                                            report = self.sre_flow.sentinel.execute_post_approval_remediation(self.harness, res)
                                            await self.post_to_channel(f"🚀 **Security Sentinel**\n\n{report}", root_id=latest_id)
                                    elif any(k in text.lower() for k in ["checkout", "failing", "500"]):
                                        triage = self.sre_flow.triager.handle_message(self.harness.messages[-1])
                                        await self.post_to_channel(f"🚨 **SRE Triager**\n\n{triage}", root_id=latest_id)

                                        _, repro = self.sre_flow.reproducer.reproduce_bug()
                                        await self.post_to_channel(f"🔍 **Chaos Reproducer**\n\n{repro}", root_id=latest_id)

                                        _, patch = self.sre_flow.patcher.generate_and_verify_patch()
                                        await self.post_to_channel(f"🛠️ **Patch Architect**\n\n{patch}", root_id=latest_id)

                                        gate = self.sre_flow.sentinel.request_production_gate(self.harness)
                                        await self.post_to_channel(f"🔒 **Dual-Custody Gate**\n\n{self.harness.messages[-1].content}", root_id=latest_id)

                        last_post_id = latest_id

                    await asyncio.sleep(2.5)
                except Exception as e:
                    print(f"⚠️ Mattermost poll error: {e}")
                    await asyncio.sleep(5)
