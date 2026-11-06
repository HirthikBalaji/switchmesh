"""
SwitchMesh Track 1: SRE Incident War Room End-to-End Orchestrator.
Demonstrates the full multi-agent human-in-the-loop incident resolution lifecycle.
"""

from __future__ import annotations
from typing import Dict, List, Optional
from switchmesh.protocol.client import SwitchRoomHarness
from switchmesh.protocol.types import MessageRole, RoomMessage
from switchmesh.workflows.business_sre.patcher import PatchArchitectAgent
from switchmesh.workflows.business_sre.reproducer import ChaosReproducerAgent
from switchmesh.workflows.business_sre.sentinel import SecuritySentinelAgent
from switchmesh.workflows.business_sre.triager import SRETriagerAgent


class SREWarRoomWorkflow:
    def __init__(self, room_name: str = "prod-incidents-warroom", bridge: str = "slack"):
        self.harness = SwitchRoomHarness("room-sre-01", room_name, bridge=bridge)
        self.triager = SRETriagerAgent("sre-triager")
        self.reproducer = ChaosReproducerAgent("chaos-reproducer")
        self.patcher = PatchArchitectAgent("patch-architect")
        self.sentinel = SecuritySentinelAgent("security-sentinel")

        self.harness.register_agent(self.triager.name, self.triager)
        self.harness.register_agent(self.reproducer.name, self.reproducer)
        self.harness.register_agent(self.patcher.name, self.patcher)
        self.harness.register_agent(self.sentinel.name, self.sentinel)

    def run_stage_1_alert(self) -> RoomMessage:
        """Sam alerts the room that checkout is failing."""
        msg = self.harness.post_message(
            author_id="sam",
            author_name="Sam (On-Call Engineer)",
            role=MessageRole.HUMAN,
            content="@sre-triager checkout is failing since this morning. 500s spiking on cart. Can you look?",
            mentions=["sre-triager"]
        )
        return msg

    def run_stage_2_triage(self) -> RoomMessage:
        """Triager reviews telemetry and alerts room."""
        triage_text = self.triager.handle_message(self.harness.messages[-1])
        msg = self.harness.post_message(
            author_id=self.triager.name,
            author_name="SRE Triager (Agent)",
            role=MessageRole.AGENT,
            content=triage_text,
            mentions=["chaos-reproducer"]
        )
        return msg

    def run_stage_3_repro(self) -> Tuple[RoomMessage, Dict]:
        """Chaos reproducer executes deterministic sandbox reproduction."""
        res, repro_text = self.reproducer.reproduce_bug()
        msg = self.harness.post_message(
            author_id=self.reproducer.name,
            author_name="Chaos Reproducer (Agent)",
            role=MessageRole.AGENT,
            content=repro_text,
            mentions=["patch-architect"]
        )
        return msg, res.model_dump()

    def run_stage_4_patch(self) -> Tuple[RoomMessage, Dict]:
        """Patch architect creates and verifies fix in sandbox."""
        res, patch_text = self.patcher.generate_and_verify_patch()
        msg = self.harness.post_message(
            author_id=self.patcher.name,
            author_name="Patch Architect (Agent)",
            role=MessageRole.AGENT,
            content=patch_text,
            mentions=["security-sentinel"]
        )
        return msg, res.model_dump()

    def run_stage_5_gate(self, approver: str = "priya") -> RoomMessage:
        """Security sentinel initiates the dual-custody approval gate."""
        self.sentinel.request_production_gate(self.harness, approver=approver)
        return self.harness.messages[-1]

    def run_stage_6_human_approval(self, approver: str = "priya", approval_text: str = "Approved. Roll it back.") -> RoomMessage:
        """Priya (Team Lead) reviews telemetry and approves rollback."""
        msg = self.harness.post_message(
            author_id=approver,
            author_name="Priya (Engineering Lead)",
            role=MessageRole.HUMAN,
            content=approval_text
        )
        # Check gate resolution
        gate = self.harness.resolve_gate_from_message(approver, approval_text)
        if gate and gate.outcome.value == "APPROVED":
            self.sentinel.execute_post_approval_remediation(self.harness, gate)
        return msg
