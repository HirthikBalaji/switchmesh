"""
SwitchMesh Room Protocol Client & Harness.
Provides a client that connects to Switch's Room Broker (or local in-memory event bus)
handling addressing policies, mentions, streaming turns, and dual-custody gates.
"""

from __future__ import annotations
import asyncio
from typing import Callable, Dict, List, Optional
import uuid
from switchmesh.protocol.guardrails import TrustGuardrail
from switchmesh.protocol.types import (
    GateOutcome,
    HumanGateRequest,
    MessageRole,
    RoomMessage,
    SwitchEvent,
)


class SwitchRoomHarness:
    """
    Simulates or connects to a Switch Room (Slack/Discord/Mattermost bridge).
    Coordinates human users and AI agents reading from the same shared log.
    """

    def __init__(self, room_id: str, room_name: str, bridge: str = "slack"):
        self.room_id = room_id
        self.room_name = room_name
        self.bridge = bridge
        self.messages: List[RoomMessage] = []
        self.subscribers: List[Callable[[SwitchEvent], None]] = []
        self.guardrail = TrustGuardrail()
        self.agent_registry: Dict[str, Any] = {}

    def register_agent(self, agent_name: str, agent_instance: Any):
        """Register an AI agent listening to this room."""
        self.agent_registry[agent_name] = agent_instance

    def post_message(
        self,
        author_id: str,
        author_name: str,
        role: MessageRole,
        content: str,
        mentions: Optional[List[str]] = None,
        metadata: Optional[Dict] = None
    ) -> RoomMessage:
        """
        Posts a message to the room. Runs Trust guardrail inspection first.
        """
        msg = RoomMessage(
            id=f"msg-{uuid.uuid4().hex[:8]}",
            room_id=self.room_id,
            author_id=author_id,
            author_name=author_name,
            role=role,
            content=content,
            mentions=mentions or [],
            metadata=metadata or {}
        )

        outcome, processed_content, finding = self.guardrail.inspect_message(msg)
        msg.content = processed_content
        if finding:
            msg.metadata["guardrail_finding"] = finding
            msg.metadata["guardrail_outcome"] = outcome.value

        self.messages.append(msg)

        # Broadcast event
        event = SwitchEvent(
            event_type="message.created",
            room_id=self.room_id,
            payload=msg.model_dump()
        )
        self._dispatch_event(event)
        return msg

    def post_gate_request(
        self,
        proposed_by: str,
        action_type: str,
        summary: str,
        risk_level: str,
        required_approver: str,
        details: Dict
    ) -> HumanGateRequest:
        """
        Posts an interactive dual-custody gate request to the room.
        """
        gate = self.guardrail.create_gate_request(
            room_id=self.room_id,
            action_type=action_type,
            summary=summary,
            risk_level=risk_level,
            proposed_by=proposed_by,
            required_approver=required_approver,
            details=details
        )

        # Notify room of gate
        gate_text = (
            f"🔒 **[DUAL-CUSTODY GATE REQUIRED]**\n"
            f"**Action:** `{action_type}`\n"
            f"**Summary:** {summary}\n"
            f"**Risk Level:** `{risk_level.upper()}`\n"
            f"**Proposed by:** `@{proposed_by}`\n"
            f"**Requires sign-off from:** `@{required_approver}`\n"
            f"Please reply with `Approved. <instruction>` or `Reject`."
        )
        self.post_message(
            author_id="switch-sentinel",
            author_name="Switch Sentinel (Trust Gate)",
            role=MessageRole.SYSTEM,
            content=gate_text,
            mentions=[required_approver],
            metadata={"gate_id": gate.gate_id, "is_gate": True}
        )
        return gate

    def resolve_gate_from_message(self, approver: str, text: str) -> Optional[HumanGateRequest]:
        """
        Checks if a human message resolves any pending gate.
        """
        clean_text = text.strip().lower()
        if not ("approve" in clean_text or "reject" in clean_text):
            return None

        # Find latest pending gate
        pending_gates = [g for g in self.guardrail.active_gates.values() if g.outcome == GateOutcome.PENDING]
        if not pending_gates:
            return None

        gate = pending_gates[-1]
        decision = GateOutcome.APPROVED if "approve" in clean_text else GateOutcome.REJECTED
        try:
            resolved = self.guardrail.resolve_gate(gate.gate_id, approver, decision, reason=text)
            status_text = f"✅ **[GATE RESOLVED]** Action `{gate.action_type}` marked **{decision.value}** by `@{approver}`."
            self.post_message(
                author_id="switch-sentinel",
                author_name="Switch Sentinel",
                role=MessageRole.SYSTEM,
                content=status_text,
                metadata={"gate_id": gate.gate_id, "outcome": decision.value}
            )
            return resolved
        except Exception as e:
            self.post_message(
                author_id="switch-sentinel",
                author_name="Switch Sentinel",
                role=MessageRole.SYSTEM,
                content=f"⚠️ Gate resolution failed: {str(e)}"
            )
            return None

    def subscribe(self, callback: Callable[[SwitchEvent], None]):
        self.subscribers.append(callback)

    def _dispatch_event(self, event: SwitchEvent):
        for sub in self.subscribers:
            sub(event)
