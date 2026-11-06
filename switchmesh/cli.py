"""
SwitchMesh Interactive Terminal Dashboard & CLI.
Provides rich colored console output, live event streaming,
and interactive prompts for hackathon judges and live presentations.
"""

from __future__ import annotations
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt
from switchmesh.workflows.business_sre.incident_sim import SREWarRoomWorkflow
from switchmesh.workflows.creative_studio.studio_sim import CreativeStudioWorkflow

console = Console()


def display_banner():
    banner = """[bold cyan]
   _____         _ _       _     __  __           _     
  / ____|       (_) |     | |   |  \\/  |         | |    
 | (_____      ___| |_ ___| |__ | \\  / | ___  ___| |__  
  \\___ \\ \\ /\\ / / | __/ __| '_ \\| |\\/| |/ _ \\/ __| '_ \\ 
  ____) \\ V  V /| | || (__| | | | |  | |  __/\\__ \\ | | |
 |_____/ \\_/\\_/ |_|\\__\\___|_| |_|_|  |_|\\___||___/_| |_|
[/bold cyan]
[bold white]Sovereign Human-Agent Mesh with Ephemeral Verification Sandboxes & Dual-Custody Gates[/bold white]
[italic green]Flip the Switch Hackathon 2026 Submission | WeMakeDevs x DevTools Academy x Switch[/italic green]
"""
    console.print(banner)


def run_sre_demo():
    console.clear()
    display_banner()
    console.print("\n[bold yellow]══════════════════════════════════════════════════════════════════[/bold yellow]")
    console.print("[bold red]🚨 TRACK 1: BUSINESS SRE PRODUCTION INCIDENT WAR ROOM[/bold red]")
    console.print("[dim]Scenario: Sev-1 checkout failure on cart-service after v2.14.0 deployment[/dim]")
    console.print("[bold yellow]══════════════════════════════════════════════════════════════════[/bold yellow]\n")

    sim = SREWarRoomWorkflow()
    time.sleep(0.5)

    # Stage 1: Alert
    console.print("[bold cyan]Step 1: On-Call Human Alerts Room[/bold cyan]")
    m1 = sim.run_stage_1_alert()
    console.print(Panel(f"[bold white]{m1.content}[/bold white]", title=f"[blue]{m1.author_name}[/blue]", border_style="blue"))
    time.sleep(1.0)

    # Stage 2: Triage
    console.print("\n[bold cyan]Step 2: SRE Triager Isolates Blast Radius & Deployment[/bold cyan]")
    m2 = sim.run_stage_2_triage()
    console.print(Panel(m2.content, title=f"[magenta]{m2.author_name}[/magenta]", border_style="magenta"))
    time.sleep(1.0)

    # Stage 3: Repro
    console.print("\n[bold cyan]Step 3: Chaos Reproducer Spins Ephemeral Sandbox & Confirms Repro[/bold cyan]")
    with console.status("[bold green]Executing isolated reproduction sandbox...[/bold green]"):
        m3, repro_data = sim.run_stage_3_repro()
    console.print(Panel(m3.content, title=f"[yellow]{m3.author_name}[/yellow]", border_style="yellow"))
    time.sleep(1.0)

    # Stage 4: Patch
    console.print("\n[bold cyan]Step 4: Patch Architect Synthesizes & Regression Tests Hotfix[/bold cyan]")
    with console.status("[bold green]Synthesizing patch & running regression test suite in sandbox...[/bold green]"):
        m4, patch_data = sim.run_stage_4_patch()
    console.print(Panel(m4.content, title=f"[cyan]{m4.author_name}[/cyan]", border_style="cyan"))
    time.sleep(1.0)

    # Stage 5: Dual-Custody Gate
    console.print("\n[bold cyan]Step 5: Security Sentinel Initiates Dual-Custody Human Gate[/bold cyan]")
    m5 = sim.run_stage_5_gate("priya")
    console.print(Panel(m5.content, title="[red]SWITCH TRUST DUAL-CUSTODY GATE[/red]", border_style="red"))

    console.print("\n[bold green]👉 HUMAN IN THE LOOP SIGN-OFF REQUIRED[/bold green]")
    user_choice = Prompt.ask(
        "Enter sign-off response (or press Enter for default)",
        default="Approved. Roll it back."
    )

    # Stage 6: Human Approval & Execution
    console.print(f"\n[bold cyan]Step 6: Executing Signed Rollback by @priya[/bold cyan]")
    sim.run_stage_6_human_approval("priya", user_choice)

    # Display final execution message
    final_msg = sim.harness.messages[-1]
    console.print(Panel(final_msg.content, title="[green]PRODUCTION RECOVERY CONFIRMED[/green]", border_style="green"))

    console.print("\n[bold green]✅ Track 1 Business SRE Workflow Completed Successfully![/bold green]\n")


def run_creative_demo():
    console.clear()
    display_banner()
    console.print("\n[bold yellow]══════════════════════════════════════════════════════════════════[/bold yellow]")
    console.print("[bold magenta]🎨 TRACK 2: CREATIVE STUDIO (VOICE-TO-PLAYABLE INDIE GAME)[/bold magenta]")
    console.print("[dim]Scenario: Solo creator dictates game seed via Wispr Flow; 4 agents build & hot-reload live[/dim]")
    console.print("[bold yellow]══════════════════════════════════════════════════════════════════[/bold yellow]\n")

    sim = CreativeStudioWorkflow()
    time.sleep(0.5)

    console.print("[bold cyan]Step 1: Creator Dictates Prompt via Wispr Flow Voice[/bold cyan]")
    m1 = sim.run_stage_1_creator_prompt()
    console.print(Panel(f"[italic]{m1.content}[/italic]", title=f"[blue]{m1.author_name}[/blue]", border_style="blue"))
    time.sleep(1.0)

    console.print("\n[bold cyan]Step 2: Worldsmith Generates Cyberpunk Narrative & Mechanics[/bold cyan]")
    m2, bible = sim.run_stage_2_worldsmith()
    console.print(Panel(m2.content, title=f"[magenta]{m2.author_name}[/magenta]", border_style="magenta"))
    time.sleep(1.0)

    console.print("\n[bold cyan]Step 3: Audio Alchemist Synthesizes Web Audio Procedural SFX[/bold cyan]")
    m3 = sim.run_stage_3_alchemist()
    console.print(Panel(m3.content, title=f"[yellow]{m3.author_name}[/yellow]", border_style="yellow"))
    time.sleep(1.0)

    console.print("\n[bold cyan]Step 4: Canvas Mechanic Compiles HTML5 Engine & Boots Preview Server[/bold cyan]")
    with console.status("[bold green]Compiling 60 FPS HTML5 Canvas engine...[/bold green]"):
        m4, url = sim.run_stage_4_mechanic()
    console.print(Panel(m4.content, title=f"[green]{m4.author_name}[/green]", border_style="green"))
    time.sleep(1.0)

    console.print("\n[bold cyan]Step 5: Game Critic Runs Automated Simulation Playtest[/bold cyan]")
    m5, eval_data = sim.run_stage_5_critic()
    console.print(Panel(m5.content, title=f"[cyan]{m5.author_name}[/cyan]", border_style="cyan"))
    time.sleep(1.0)

    console.print("\n[bold cyan]Step 6: Creator Speaks Live Hot-Reload Tweak[/bold cyan]")
    tweak = Prompt.ask(
        "Voice dictation tweak (or press Enter for default)",
        default="Make drone speed faster and increase quantum particle burst"
    )
    sim.run_stage_6_creator_tweak(tweak)
    console.print(Panel(sim.harness.messages[-1].content, title="[bold green]HOT-RELOAD SUCCESS[/bold green]", border_style="green"))

    console.print(f"\n[bold green]🎉 Live Playable Game ready at: [underline cyan]{url}[/underline cyan] (or open index.html)![/bold green]\n")
    sim.game_server.stop()
