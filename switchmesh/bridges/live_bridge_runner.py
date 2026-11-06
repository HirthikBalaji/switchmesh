"""
SwitchMesh Unified Live Platform Bridge Runner.
Launches real integrations with Discord, Slack, Telegram, or Mattermost.
Reads configuration from environment variables (.env) or interactive CLI prompts.
"""

from __future__ import annotations
import argparse
import asyncio
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()


def load_env_file(filepath: str = ".env"):
    """Simple parser for .env key-value pairs."""
    if not os.path.exists(filepath):
        return
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def main():
    parser = argparse.ArgumentParser(description="SwitchMesh Live Team Chat Bridge")
    parser.add_argument(
        "--platform",
        choices=["discord", "slack", "telegram", "mattermost", "interactive"],
        default="interactive",
        help="Target chat platform to bridge"
    )
    parser.add_argument(
        "--workflow",
        choices=["sre", "creative"],
        default="sre",
        help="Workflow type: 'sre' (Production Incident) or 'creative' (Game Studio)"
    )
    args = parser.parse_args()

    load_env_file()

    platform = args.platform
    workflow = args.workflow

    if platform == "interactive":
        console.clear()
        console.print(Panel(
            "[bold cyan]SwitchMesh Live Team Chat Bridge Runner[/bold cyan]\n"
            "[white]Connects autonomous AI agents to your actual Slack, Discord, Telegram, or Mattermost rooms.[/white]",
            border_style="cyan"
        ))
        platform = Prompt.ask(
            "Select chat platform to connect",
            choices=["discord", "slack", "telegram", "mattermost"],
            default="discord"
        )
        workflow = Prompt.ask(
            "Select active room workflow",
            choices=["sre", "creative"],
            default="sre"
        )

    console.print(f"\n[bold green]🚀 Initializing real {platform.upper()} Bridge (Workflow: {workflow.upper()})...[/bold green]\n")

    if platform == "discord":
        from switchmesh.bridges.discord_bridge import DiscordSwitchBridge
        token = os.getenv("DISCORD_BOT_TOKEN")
        channel = os.getenv("DISCORD_CHANNEL_ID")

        if not token or not channel:
            console.print("[yellow]⚠️ Discord credentials not detected in environment or .env![/yellow]")
            token = Prompt.ask("Enter DISCORD_BOT_TOKEN (or press Enter to exit)")
            if not token:
                console.print("[red]Aborted. Check .env.example for Discord setup steps.[/red]")
                return
            channel_str = Prompt.ask("Enter DISCORD_CHANNEL_ID")
            channel = int(channel_str)
        else:
            channel = int(channel)

        bridge = DiscordSwitchBridge(token, channel, workflow_type=workflow)
        bridge.run()

    elif platform == "slack":
        from switchmesh.bridges.slack_bridge import SlackSwitchBridge
        bot_token = os.getenv("SLACK_BOT_TOKEN")
        app_token = os.getenv("SLACK_APP_TOKEN")
        channel = os.getenv("SLACK_CHANNEL_ID")

        if not bot_token or not app_token or not channel:
            console.print("[yellow]⚠️ Slack tokens not found in environment or .env![/yellow]")
            bot_token = Prompt.ask("Enter SLACK_BOT_TOKEN (xoxb-...)")
            app_token = Prompt.ask("Enter SLACK_APP_TOKEN (xapp-...)")
            channel = Prompt.ask("Enter SLACK_CHANNEL_ID (e.g. C01234567)")
            if not bot_token or not app_token:
                console.print("[red]Aborted. Check .env.example for Slack setup steps.[/red]")
                return

        bridge = SlackSwitchBridge(bot_token, app_token, channel, workflow_type=workflow)
        asyncio.run(bridge.start())

    elif platform == "telegram":
        from switchmesh.bridges.telegram_bridge import TelegramSwitchBridge
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            console.print("[yellow]⚠️ Telegram bot token not found in environment or .env![/yellow]")
            token = Prompt.ask("Enter TELEGRAM_BOT_TOKEN")
            if not token:
                console.print("[red]Aborted. Check .env.example for Telegram setup steps.[/red]")
                return

        bridge = TelegramSwitchBridge(token, workflow_type=workflow)
        asyncio.run(bridge.poll_updates())

    elif platform == "mattermost":
        from switchmesh.bridges.mattermost_bridge import MattermostSwitchBridge
        base_url = os.getenv("MATTERMOST_URL", "http://localhost:8065")
        token = os.getenv("MATTERMOST_BOT_TOKEN")
        channel = os.getenv("MATTERMOST_CHANNEL_ID")

        if not token or not channel:
            console.print("[yellow]⚠️ Mattermost credentials not found in environment or .env![/yellow]")
            base_url = Prompt.ask("Enter MATTERMOST_URL", default="http://localhost:8065")
            token = Prompt.ask("Enter MATTERMOST_BOT_TOKEN")
            channel = Prompt.ask("Enter MATTERMOST_CHANNEL_ID")
            if not token:
                console.print("[red]Aborted.[/red]")
                return

        bridge = MattermostSwitchBridge(base_url, token, channel, workflow_type=workflow)
        asyncio.run(bridge.poll_channel_posts())


if __name__ == "__main__":
    main()
