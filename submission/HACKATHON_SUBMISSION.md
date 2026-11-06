# Flip the Switch Hackathon — Official Submission Form

> **Project Name:** SwitchMesh: Sovereign Human-Agent War Room & Creative Studio  
> **Tagline:** Verifiable multi-agent autonomy in team chat with ephemeral sandboxes, dual-custody governance, and voice steering.  
> **Repository:** `https://github.com/<your-username>/switchmesh`  
> **Demo Video Link:** `https://youtu.be/<your-demo-video>` (or Loom link)  
> **Blog Post Link:** [Read the full technical deep dive](submission/BLOG_POST.md)  
> **Wispr Usage Scorecard:** Attached in `wispr_flow/wispr_scorecard.png`

---

## 🎯 Tracks Entered

- ✅ **Track 01: Best Business Workflow ($2,000 cash)** — Autonomous SRE Production Incident War Room & Dual-Custody Rollback.
- ✅ **Track 02: Best Personal or Creative Workflow ($2,000 cash)** — Creative Studio: Voice-to-Playable 60 FPS HTML5 Arcade Game Engine.
- ✅ **Track 03: Best Core Contribution ($100 x 20 cash)** — Official Supabase Service Connector PR for Switch Core (`sandbox-quantum/switch`).
- ✅ **Side Track: Code with Wispr ($500 cash)** — Hands-free incident direction, room authoring, and creative hot-reloads via Wispr Flow voice.
- ✅ **Side Track: Best Blog (AirPods 5)** — Comprehensive 2,500-word engineering deep dive with architecture diagrams and benchmarks.
- ✅ **Side Track: #HowISwitch (Logitech Mechanical Keyboard)** — 5 viral social media showcase posts with video and ASCII workflows.

---

## 💡 Inspiration: The Hardest Problems in Multi-Agent Chat

When autonomous agents are brought into team chat (Slack, Teams, Discord, Mattermost), existing workflows fail for three fundamental reasons:
1. **The Ephemeral Verification Gap**: Agents claim they "fixed a bug" or "wrote working code", but humans have to manually switch contexts, pull branches, and test locally to verify claims.
2. **The Compliance & Governance Barrier**: High-stakes business environments (production rollbacks, database schema modifications, infrastructure deploys) cannot allow unconstrained agent execution without cryptographic human-in-the-loop authorization.
3. **The Creative Disconnection**: Solo creators and indie game developers struggle to orchestrate narrative lore, game physics, and sound synthesis without drowning in fragmented tools.

We created **SwitchMesh** to solve these exact problems. Built directly on the open-source **Switch** infrastructure, SwitchMesh connects teams of specialized AI agents with human teammates, backed by **Ephemeral Verification Sandboxes** and **Switch Trust Dual-Custody Gates**.

---

## 🚀 What It Does

### 1. Track 1: Business SRE Production War Room
- **Alert Ingestion**: Automatically ingests 500 error alerts and correlates sudden spikes with recent code deployments (`v2.14.0`).
- **Deterministic Chaos Repro**: Spins up an isolated Ephemeral Sandbox, extracts the root-cause stack trace (`TypeError: NoneType`), and proves the defect deterministically with exact runtime benchmarks.
- **Verified Hotfix Synthesis**: Generates a safe patch with a regression test suite, executing inside the sandbox until 100% of assertions pass.
- **Dual-Custody Human Gate**: Sentinel holds execution until the engineering lead (@priya) reviews the telemetry card and signs off via voice (*"Approved. Roll it back"*).
- **Automated Rollback & Blameless Post-Mortem**: Executes the zero-downtime rollback to `v2.13.2`, confirms error rate dropped to 0%, and publishes an automated post-mortem. MTTR drops from 45 mins to 3.7 mins.

### 2. Track 2: Creative Studio (Voice-to-Playable Indie Game)
- **Voice-Directed Game Jam**: The solo creator speaks a seed concept into Wispr Flow: *"Build CyberGlitch: Mainframe Breach — a retro neon hack-and-evade game with chiptune audio."*
- **Swarm Collaboration**:
  - `@worldsmith`: Designs lore, scoring multipliers, and mechanics.
  - `@audio-alchemist`: Synthesizes 8-bit retro sound effects using pure **Web Audio API** oscillators (`sfxCollect`, `sfxDash`, `sfxExplosion`) with zero external asset downloads.
  - `@canvas-mechanic`: Compiles a 60 FPS HTML5 Canvas arcade game with momentum physics, collision math, and neon particle emitters.
  - `@game-critic`: Evaluates frame budgets (draw overhead < 2.5ms) and balance curves.
- **Live Hot-Reload**: Spoken voice tweaks hot-reload the playable game at `http://localhost:8800` in real time!

### 3. Track 3: Switch Core Contribution (Supabase Connector)
- Production-grade service connector for `sandbox-quantum/switch` under `core/switch_core/connections/catalog/supabase/`.
- Includes `connection.yaml`, `skill/SKILL.md`, and unit tests validating PostgreSQL schema queries, auth inspection, and MCP token hygiene.

---

## 🛠️ How We Built It

- **Switch Core & Controller Protocol v2**: Native integration with Switch's room engine, WebSocket/SSE frame dispatching, and addressing policies (`anyone`, `owner-agents`).
- **Official Switch Room Templates**: Authored production-ready YAML templates (`business-incident-room.template.yaml`, `creative-studio-room.template.yaml`, `sre-agents.template.yaml`, `studio-agents.template.yaml`).
- **Ephemeral Sandbox Engine**: Isolated subprocess execution harnesses that record exit codes, stdout/stderr, diffs, and execution timing.
- **Switch Trust Guardrails**: Real-time redaction of sensitive API keys (`sk-*`, `ghp_*`) and blocking of destructive commands (`rm -rf /`).
- **Wispr Flow Voice Engine**: Voice prompting workflow powering hands-free incident approvals and game mechanic hot-reloads.
- **Python 3.12, Pytest, Pydantic, Rich, and Web Audio API**.

---

## 🔬 How the Judges Can Test & Reproduce

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/switchmesh.git
cd switchmesh

# 2. Run the verification test suite (100% passing)
python3 -m pytest -v tests/ core_contribution/tests/

# 3. Launch the Interactive CLI Dashboard
python3 demo.py
```

Inside the CLI menu:
- Press `1` for the **Track 1 Business SRE Incident War Room** simulation.
- Press `2` for the **Track 2 Creative Studio** live game generation and hot-reload.
- Press `3` to run the automated test suite.
- Press `4` to inspect the **Track 3 Supabase Core Contribution**.
