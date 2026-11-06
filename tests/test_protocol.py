"""
Unit tests for SwitchMesh Protocol Types and Harness.
"""

import pytest
from switchmesh.protocol.client import SwitchRoomHarness
from switchmesh.protocol.types import GateOutcome, MessageRole, RoomMessage


def test_room_harness_post_and_mention():
    harness = SwitchRoomHarness("test-room-1", "Test Room", bridge="slack")
    msg = harness.post_message(
        author_id="user_alice",
        author_name="Alice",
        role=MessageRole.HUMAN,
        content="Hey @agent-smith check this log",
        mentions=["agent-smith"]
    )

    assert msg.id.startswith("msg-")
    assert msg.author_name == "Alice"
    assert msg.role == MessageRole.HUMAN
    assert "agent-smith" in msg.mentions
    assert len(harness.messages) == 1


def test_guardrail_redaction():
    harness = SwitchRoomHarness("test-room-2", "Secret Room", bridge="discord")
    msg = harness.post_message(
        author_id="user_bob",
        author_name="Bob",
        role=MessageRole.HUMAN,
        content="Here is the key: sk-abcdef1234567890abcdef1234567890abcdef12345678"
    )

    assert "[REDACTED_BY_SWITCH_TRUST]" in msg.content
    assert msg.metadata.get("guardrail_outcome") == GateOutcome.REDACTED.value
    assert "guardrail_finding" in msg.metadata


def test_guardrail_destructive_command_blocking():
    harness = SwitchRoomHarness("test-room-3", "Safe Room", bridge="slack")
    msg = harness.post_message(
        author_id="agent_rogue",
        author_name="Rogue Agent",
        role=MessageRole.AGENT,
        content="Running cleanup: rm -rf /"
    )

    assert msg.content == "[BLOCKED BY POLICY]"
    assert msg.metadata.get("guardrail_outcome") == GateOutcome.BLOCKED.value
