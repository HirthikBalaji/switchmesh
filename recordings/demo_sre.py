#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
"""
Automated Track 1 SRE War Room Showcase for Asciinema Recording.
"""

import time
from rich.console import Console
from rich.panel import Panel
from switchmesh.workflows.business_sre.incident_sim import SREWarRoomWorkflow

console = Console(width=100)


def main():
    console.clear()
    banner = """[bold cyan]
   _____         _ _       _     __  __           _     
  / ____|       (_) |     | |   |  \\/  |         | |    
 | (_____      ___| |_ ___| |__ | \\  / | ___  ___| |__  
  \\___ \\ \\ /\\ / / | __/ __| '_ \\| |\\/| |/ _ \\/ __| '_ \\ 
  ____) \\ V  V /| | || (__| | | | |  | |  __/\\__ \\ | | |
 |_____/ \\_/\\_/ |_|\\__\\___|_| |_|_|  |_|\\___||___/_| |_|
[/bold cyan]
[bold white]TRACK 1: BUSINESS SRE PRODUCTION INCIDENT WAR ROOM[/bold white]
[italic green]Autonomous Triage · Ephemeral Sandbox Repro · Dual-Custody Rollback[/italic green]
"""
    console.print(banner)
    time.sleep(1)

    sim = SREWarRoomWorkflow()

    # Step 1: Alert
    console.print("\n[bold cyan]Step 1: On-Call Engineer Alerts Room[/bold cyan]")
    m1 = sim.run_stage_1_alert()
    console.print(Panel(f"[bold white]{m1.content}[/bold white]", title=f"[blue]{m1.author_name}[/blue]", border_style="blue"))
    time.sleep(1.5)

    # Step 2: Triage
    console.print("\n[bold cyan]Step 2: SRE Triager Correlates Blast Radius & Deployment[/bold cyan]")
    with console.status("[bold magenta]Ingesting Datadog & Sentry error telemetry...[/bold magenta]"):
        time.sleep(1.2)
        m2 = sim.run_stage_2_triage()
    console.print(Panel(m2.content, title=f"[magenta]{m2.author_name}[/magenta]", border_style="magenta"))
    time.sleep(1.5)

    # Step 3: Repro in Sandbox
    console.print("\n[bold cyan]Step 3: Chaos Reproducer Spins Ephemeral Sandbox & Isolates Bug[/bold cyan]")
    with console.status("[bold yellow]Spinning up isolated ephemeral container & running repro.py...[/bold yellow]"):
        time.sleep(1.8)
        m3, repro_data = sim.run_stage_3_repro()
    console.print(Panel(m3.content, title=f"[yellow]{m3.author_name}[/yellow]", border_style="yellow"))
    time.sleep(1.5)

    # Step 4: Patch in Sandbox
    console.print("\n[bold cyan]Step 4: Patch Architect Synthesizes Hotfix & Verifies Regression Tests[/bold cyan]")
    with console.status("[bold green]Executing regression test suite in isolated ephemeral sandbox...[/bold green]"):
        time.sleep(1.8)
        m4, patch_data = sim.run_stage_4_patch(create_pr=False)
    console.print(Panel(m4.content, title=f"[cyan]{m4.author_name}[/cyan]", border_style="cyan"))
    time.sleep(1.5)

    # Step 5: Dual Custody Gate
    console.print("\n[bold cyan]Step 5: Security Sentinel Initiates Dual-Custody Human Gate[/bold cyan]")
    m5 = sim.run_stage_5_gate("priya")
    console.print(Panel(m5.content, title="[red]SWITCH TRUST DUAL-CUSTODY GATE (SOC2)[/red]", border_style="red"))
    time.sleep(1.5)

    # Step 6: Human Approval
    console.print("\n[bold green]👉 Human On-Call Lead Sign-Off (via Chat or Wispr Flow Voice):[/bold green]")
    approval_text = "Approved. Roll it back to v2.13.2."
    console.print(f"[bold white]> {approval_text}[/bold white]")
    time.sleep(1.0)

    # Step 7: Execution & Post-Mortem
    console.print("\n[bold cyan]Step 6: Executing Verified Rollback & Publishing Blameless Post-Mortem[/bold cyan]")
    with console.status("[bold green]Executing cluster rollback & verifying error metrics drop to 0%...[/bold green]"):
        time.sleep(1.5)
        sim.run_stage_6_human_approval("priya", approval_text)

    final_msg = sim.harness.messages[-1]
    console.print(Panel(final_msg.content, title="[green]PRODUCTION RECOVERY CONFIRMED[/green]", border_style="green"))
    console.print("\n[bold green]✅ Track 1: SRE Incident Resolution Workflow Complete! (MTTR: 3m 42s)[/bold green]\n")


if __name__ == "__main__":
    main()
