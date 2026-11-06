"""
Unit tests for SwitchMesh Real Chat Bridges (Discord, Slack, Telegram, Mattermost).
"""

from switchmesh.bridges.discord_bridge import AGENT_AVATARS, DiscordSwitchBridge
from switchmesh.bridges.mattermost_bridge import MattermostSwitchBridge
from switchmesh.bridges.telegram_bridge import TelegramSwitchBridge


def test_agent_avatar_mapping():
    assert "sre-triager" in AGENT_AVATARS
    assert "chaos-reproducer" in AGENT_AVATARS
    assert "patch-architect" in AGENT_AVATARS
    assert "security-sentinel" in AGENT_AVATARS
    assert AGENT_AVATARS["sre-triager"].startswith("https://")


def test_telegram_bridge_init():
    bridge = TelegramSwitchBridge("123456:FAKE_TOKEN_FOR_TESTING", workflow_type="sre")
    assert bridge.base_url == "https://api.telegram.org/bot123456:FAKE_TOKEN_FOR_TESTING"
    assert bridge.workflow_type == "sre"
    assert "sre-triager" in bridge.harness.agent_registry


def test_mattermost_bridge_init():
    bridge = MattermostSwitchBridge(
        base_url="http://localhost:8065",
        bot_token="test_token",
        channel_id="chan_123",
        workflow_type="sre"
    )
    assert bridge.base_url == "http://localhost:8065"
    assert bridge.headers["Authorization"] == "Bearer test_token"
    assert bridge.channel_id == "chan_123"
