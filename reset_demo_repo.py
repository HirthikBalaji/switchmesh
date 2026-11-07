#!/usr/bin/env python3
"""
Quick utility to reset the live demo GitHub repository (HirthikBalaji/cart-service-demo)
back to the malformed/broken v2.14.0 code on main with ZERO open pull requests.
Run this before recording your demo or presenting to judges!
"""

import sys
from rich.console import Console
from switchmesh.workflows.business_sre.github_ops import reset_live_demo_repo, DEMO_REPO

console = Console()

if __name__ == "__main__":
    console.print(f"[bold yellow]🔄 Resetting live demo repository [cyan]{DEMO_REPO}[/cyan] to broken state...[/bold yellow]")
    try:
        reset_live_demo_repo()
        console.print("[bold green]✅ Repository successfully reset![/bold green]")
        console.print(f"👉 Visit https://github.com/{DEMO_REPO} — you will see the broken code on `main` and NO open pull requests.")
    except Exception as e:
        console.print(f"[bold red]❌ Reset failed: {e}[/bold red]")
        sys.exit(1)
