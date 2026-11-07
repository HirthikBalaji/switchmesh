#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
"""
Automated Track 2 Creative Studio Showcase for Asciinema Recording.
"""

import time
from rich.console import Console
from rich.panel import Panel
from switchmesh.workflows.creative_studio.studio_sim import CreativeStudioWorkflow

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
[bold magenta]TRACK 2: CREATIVE STUDIO (VOICE-TO-PLAYABLE INDIE GAME)[/bold magenta]
[italic green]Wispr Voice Brief · Lore Bible · Web Audio Synth · 60 FPS HTML5 Engine · Hot-Reload[/italic green]
"""
    console.print(banner)
    time.sleep(1)

    sim = CreativeStudioWorkflow()

    # Step 1: Voice Dictation Prompt
    console.print("\n[bold cyan]Step 1: Solo Creator Dictates Concept via Wispr Flow Voice[/bold cyan]")
    m1 = sim.run_stage_1_creator_prompt()
    console.print(Panel(f"[italic white]{m1.content}[/italic white]", title=f"[blue]{m1.author_name} (Spoken via Wispr Flow)[/blue]", border_style="blue"))
    time.sleep(1.5)

    # Step 2: Worldsmith
    console.print("\n[bold cyan]Step 2: Worldsmith Synthesizes Narrative Lore & Game Mechanics[/bold cyan]")
    with console.status("[bold magenta]Drafting Game Bible, scoring multipliers, and setting lore...[/bold magenta]"):
        time.sleep(1.2)
        m2, bible = sim.run_stage_2_worldsmith()
    console.print(Panel(m2.content, title=f"[magenta]{m2.author_name}[/magenta]", border_style="magenta"))
    time.sleep(1.5)

    # Step 3: Audio Alchemist
    console.print("\n[bold cyan]Step 3: Audio Alchemist Synthesizes Pure Web Audio API SFX[/bold cyan]")
    with console.status("[bold yellow]Synthesizing AudioContext oscillators (C5->C6 chimes, dash sweeps)...[/bold yellow]"):
        time.sleep(1.2)
        m3 = sim.run_stage_3_alchemist()
    console.print(Panel(m3.content, title=f"[yellow]{m3.author_name}[/yellow]", border_style="yellow"))
    time.sleep(1.5)

    # Step 4: Canvas Mechanic
    console.print("\n[bold cyan]Step 4: Canvas Mechanic Compiles 60 FPS Engine & Boots Preview Server[/bold cyan]")
    with console.status("[bold green]Compiling momentum physics loop, neon particles, and touch handlers...[/bold green]"):
        time.sleep(1.5)
        m4, url = sim.run_stage_4_mechanic()
    console.print(Panel(m4.content, title=f"[green]{m4.author_name}[/green]", border_style="green"))
    time.sleep(1.5)

    # Step 5: Game Critic
    console.print("\n[bold cyan]Step 5: Game Critic Runs Automated Simulation Playtest[/bold cyan]")
    with console.status("[bold cyan]Running headless simulation playtest & calculating frame budget...[/bold cyan]"):
        time.sleep(1.2)
        m5, eval_data = sim.run_stage_5_critic()
    console.print(Panel(m5.content, title=f"[cyan]{m5.author_name}[/cyan]", border_style="cyan"))
    time.sleep(1.5)

    # Step 6: Live Hot-Reload Tweak
    console.print("\n[bold cyan]Step 6: Creator Dictates Live Hot-Reload Tweak[/bold cyan]")
    tweak = "Make drone speed faster and add quantum warp particle trails"
    console.print(f"[bold white]> Spoken via Wispr Flow: '{tweak}'[/bold white]")
    with console.status("[bold green]Applying live hot-reload to running HTML5 canvas engine...[/bold green]"):
        time.sleep(1.2)
        sim.run_stage_6_creator_tweak(tweak)

    console.print(Panel(sim.harness.messages[-1].content, title="[bold green]HOT-RELOAD APPLIED (ZERO LATENCY)[/bold green]", border_style="green"))
    console.print(f"\n[bold green]🎉 Playable Game Ready: [underline cyan]{url}[/underline cyan] (or open index.html)[/bold green]\n")

    sim.game_server.stop()


if __name__ == "__main__":
    main()
