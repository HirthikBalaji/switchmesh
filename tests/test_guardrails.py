"""
Unit tests for TrustGuardrail and Dual-Custody Gating.
"""

import pytest
from switchmesh.protocol.guardrails import TrustGuardrail
from switchmesh.protocol.types import GateOutcome


def test_dual_custody_creation_and_approval():
    guard = TrustGuardrail()
    gate = guard.create_gate_request(
        room_id="room-prod",
        action_type="ROLLBACK",
        summary="Rollback cart-service to v2.13.2",
        risk_level="high",
        proposed_by="patch-architect",
        required_approver="priya",
        details={"version": "v2.13.2"}
    )

    assert gate.outcome == GateOutcome.PENDING
    assert gate.gate_id in guard.active_gates

    # Approve
    resolved = guard.resolve_gate(gate.gate_id, approver="priya", decision=GateOutcome.APPROVED, reason="Signed off")
    assert resolved.outcome == GateOutcome.APPROVED
    assert resolved.decided_by == "priya"
    assert len(guard.audit_log) == 2  # Created + Approved


def test_dual_custody_prevents_self_approval():
    guard = TrustGuardrail()
    gate = guard.create_gate_request(
        room_id="room-prod",
        action_type="ROLLBACK",
        summary="Self rollback test",
        risk_level="high",
        proposed_by="patch-architect",
        required_approver="priya",
        details={}
    )

    # Proposer cannot approve their own high-risk action
    with pytest.raises(ValueError, match="Dual-custody violation"):
        guard.resolve_gate(gate.gate_id, approver="patch-architect", decision=GateOutcome.APPROVED)
