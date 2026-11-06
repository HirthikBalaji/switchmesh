"""
SwitchMesh Agent Protocol v2 Type Definitions.
Conforms to the official Switch Controller Protocol specification:
JSON over WebSockets/SSE with bidirectional event streaming.
"""

from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import datetime


class MessageRole(str, Enum):
    HUMAN = "human"
    AGENT = "agent"
    SYSTEM = "system"


class GateOutcome(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    BLOCKED = "BLOCKED"
    REDACTED = "REDACTED"


class RoomMessage(BaseModel):
    id: str = Field(..., description="Unique message ID")
    room_id: str = Field(..., description="Switch room identifier")
    author_id: str = Field(..., description="ID of author (human user or agent name)")
    author_name: str = Field(..., description="Display name of the author")
    role: MessageRole = Field(..., description="Role of the sender")
    content: str = Field(..., description="Text content of the message")
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)
    mentions: List[str] = Field(default_factory=list)


class SandboxExecutionResult(BaseModel):
    sandbox_id: str
    command: str
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: float
    verified: bool
    reproduced: bool = False
    diff: Optional[str] = None


class HumanGateRequest(BaseModel):
    gate_id: str
    room_id: str
    action_type: str
    summary: str
    risk_level: str  # low, medium, high, critical
    details: Dict[str, Any] = Field(default_factory=dict)
    proposed_by: str
    required_approver: str
    outcome: GateOutcome = GateOutcome.PENDING
    decided_by: Optional[str] = None
    decided_at: Optional[str] = None
    reason: Optional[str] = None


class SwitchEvent(BaseModel):
    event_type: str  # message.created, agent.turn_started, sandbox.executed, gate.required, gate.resolved
    room_id: str
    payload: Dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
