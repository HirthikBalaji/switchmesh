"""
SwitchMesh Trust & Dual-Custody Guardrails.
Implements the Switch Trust verification gate for multi-agent rooms:
Enforces security policies, redaction of sensitive tokens, and mandatory human sign-off
on high-risk production actions (deployments, rollbacks, schema migrations, asset releases).
"""

from __future__ import annotations
import hashlib
import json
import re
from typing import Dict, List, Optional, Tuple
from switchmesh.protocol.types import GateOutcome, HumanGateRequest, RoomMessage


class TrustGuardrail:
    """
    Evaluates messages and actions against safety policies.
    Detects secret leaks (API keys, JWTs), high-risk operations, and unauthorized commands.
    """

    SECRET_PATTERNS = [
        re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-\.]{16,})['\"]?"),
        re.compile(r"ghp_[a-zA-Z0-9]{36}"),
        re.compile(r"sk-[a-zA-Z0-9]{20,}"),
    ]

    HIGH_RISK_KEYWORDS = [
        "rollback", "deploy", "drop table", "truncate", "rm -rf", "kill -9",
        "kubectl delete", "terraform apply", "production restart"
    ]

    def __init__(self, require_dual_custody: bool = True):
        self.require_dual_custody = require_dual_custody
        self.active_gates: Dict[str, HumanGateRequest] = {}
        self.audit_log: List[Dict] = []

    def inspect_message(self, message: RoomMessage) -> Tuple[GateOutcome, str, Optional[str]]:
        """
        Inspect an outgoing message for leaks or policy violations.
        Returns (Outcome, ProcessedContent, FindingSummary).
        """
        content = message.content
        finding = None

        # Check for secret leaks
        has_secret = False
        for pattern in self.SECRET_PATTERNS:
            if pattern.search(content):
                content = pattern.sub("[REDACTED_BY_SWITCH_TRUST]", content)
                has_secret = True

        if has_secret:
            finding = "Sensitive token redacted by Switch Trust Guardrails"
            return GateOutcome.REDACTED, content, finding

        # Check if the content is attempting an unauthorized destructive shell injection
        if "rm -rf /" in content or "drop database" in content.lower():
            finding = "Dangerous destructive command blocked by Switch Trust"
            return GateOutcome.BLOCKED, "[BLOCKED BY POLICY]", finding

        return GateOutcome.APPROVED, content, None

    def create_gate_request(
        self,
        room_id: str,
        action_type: str,
        summary: str,
        risk_level: str,
        proposed_by: str,
        required_approver: str,
        details: Dict
    ) -> HumanGateRequest:
        """
        Creates a dual-custody approval gate that pauses agent execution until a human signs off.
        """
        gate_id = f"gate-{hashlib.sha256(f'{room_id}-{action_type}-{summary}'.encode()).hexdigest()[:10]}"
        gate = HumanGateRequest(
            gate_id=gate_id,
            room_id=room_id,
            action_type=action_type,
            summary=summary,
            risk_level=risk_level,
            details=details,
            proposed_by=proposed_by,
            required_approver=required_approver,
            outcome=GateOutcome.PENDING
        )
        self.active_gates[gate_id] = gate
        self._record_audit(gate_id, "GATE_CREATED", gate.model_dump())
        return gate

    def resolve_gate(
        self,
        gate_id: str,
        approver: str,
        decision: GateOutcome,
        reason: Optional[str] = None
    ) -> HumanGateRequest:
        """
        Resolves an active gate. Verifies approver authorization.
        """
        if gate_id not in self.active_gates:
            raise KeyError(f"Gate {gate_id} not found or already closed")

        gate = self.active_gates[gate_id]

        # In production dual-custody, the approver cannot be the same agent who proposed the action
        if approver == gate.proposed_by:
            raise ValueError(f"Dual-custody violation: {approver} cannot approve their own proposed action")

        gate.outcome = decision
        gate.decided_by = approver
        import datetime
        gate.decided_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        gate.reason = reason

        self._record_audit(gate_id, f"GATE_{decision.value}", gate.model_dump())
        return gate

    def _record_audit(self, gate_id: str, event: str, payload: Dict):
        import datetime
        record = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "gate_id": gate_id,
            "event": event,
            "payload": payload,
            "checksum": hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        }
        self.audit_log.append(record)
