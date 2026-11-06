#!/usr/bin/env python3
"""
SwitchMesh Hackathon Showcase Entry Point.
Run this script to experience:
1. Track 1: Business SRE Production Incident War Room
2. Track 2: Creative Studio (Voice-to-Playable Indie Game)
3. Real Live Team Chat Integration (Discord, Slack, Telegram, Mattermost)
4. Full Automated Test Suite
5. Track 3 Switch Core Contribution
"""

import sys
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from switchmesh.cli import display_banner, run_sre_demo, run_creative_demo

console = Console()


def run_tests():
    console.print("\n[bold green]Running SwitchMesh Verification Test Suite (Pytest)...[/bold green]\n")
    proc = subprocess.run(["pytest", "-v"])
    if proc.returncode == 0:
        console.print("\n[bold green]✅ All test suites passed with 100% verification![/bold green]\n")
    else:
        console.print("\n[bold red]❌ Some tests encountered errors.[/bold red]\n")


def run_live_bridge():
    console.clear()
    display_banner()
    console.print(Panel(
        "[bold cyan]Launch Real Team Chat Bridge[/bold cyan]\n"
        "[white]Connect AI teammates directly to your live Slack, Discord, Telegram, or Mattermost workspace.[/white]\n"
        "[dim]Note: Ensure you have populated credentials in `.env` (see `.env.example`).[/dim]",
        border_style="cyan"
    ))
    platform = Prompt.ask(
        "Choose live platform",
        choices=["discord", "slack", "telegram", "mattermost", "back"],
        default="discord"
    )
    if platform == "back":
        return

    workflow = Prompt.ask(
        "Select room workflow",
        choices=["sre", "creative"],
        default="sre"
    )

    cmd = [sys.executable, "-m", "switchmesh.bridges.live_bridge_runner", "--platform", platform, "--workflow", workflow]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        console.print("\n[yellow]Bridge stopped by user.[/yellow]")


def main():
    while True:
        console.clear()
        display_banner()
        menu = """[bold white]Select a demo scenario, live chat bridge, or verification suite:[/bold white]

[bold red]1.[/bold red] 🚨 [bold white]Track 1: Business SRE Production Incident War Room[/bold white]
    [dim]Autonomous triage, ephemeral sandbox repro, dual-custody human sign-off & rollback[/dim]

[bold magenta]2.[/bold magenta] 🎨 [bold white]Track 2: Creative Studio (Voice-to-Playable Indie Game)[/bold white]
    [dim]Wispr Flow voice steering, lore generation, Web Audio synthesis & live hot-reload[/dim]

[bold blue]3.[/bold blue] 📡 [bold white]Connect REAL Live Team Chat Bridge (Slack, Discord, Telegram, Mattermost)[/bold white]
    [dim]Put the AI agents directly into your team channels with avatars & interactive turns[/dim]

[bold green]4.[/bold green] 🧪 [bold white]Run Full Test & Verification Suite[/bold white]
    [dim]Execute unit & integration tests across protocol, sandboxes, and workflows[/dim]

[bold yellow]5.[/bold yellow] 📄 [bold white]View Track 3 Core Contribution (Supabase Connector)[/bold white]
    [dim]Inspect ready-to-merge Switch core connector and pitch for GitHub PR[/dim]

[bold cyan]6.[/bold cyan] 🚪 [bold white]Exit[/bold white]
"""
        console.print(Panel(menu, title="[bold cyan]SwitchMesh Interactive Showcase[/bold cyan]", border_style="cyan"))

        choice = Prompt.ask("Enter choice [1-6]", choices=["1", "2", "3", "4", "5", "6"], default="1")

        if choice == "1":
            run_sre_demo()
            Prompt.ask("\nPress Enter to return to main menu...")
        elif choice == "2":
            run_creative_demo()
            Prompt.ask("\nPress Enter to return to main menu...")
        elif choice == "3":
            run_live_bridge()
            Prompt.ask("\nPress Enter to return to main menu...")
        elif choice == "4":
            run_tests()
            Prompt.ask("\nPress Enter to return to main menu...")
        elif choice == "5":
            console.clear()
            with open("core_contribution/README_CONTRIBUTION.md", "r") as f:
                console.print(Panel(f.read(), title="[bold yellow]Track 3: Switch Core Contribution[/bold yellow]", border_style="yellow"))
            Prompt.ask("\nPress Enter to return to main menu...")
        elif choice == "6":
            console.print("\n[bold cyan]Thank you for evaluating SwitchMesh! 🚀[/bold cyan]\n")
            sys.exit(0)


if __name__ == "__main__":
    main()
