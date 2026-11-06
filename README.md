# ⚡ SwitchMesh

> **Sovereign Human-Agent Mesh with Ephemeral Verification Sandboxes & Dual-Custody Gates**  
> *Built for the **Flip the Switch Hackathon** (WeMakeDevs x DevTools Academy x Switch) — Nov 4–7, 2026*

[![Tests](https://img.shields.io/badge/tests-9%2F9%20passing-brightgreen.svg)](tests/)
[![Switch Protocol](https://img.shields.io/badge/Switch-Protocol%20v2-blue.svg)](https://docs.switchagents.ai/)
[![Wispr Flow](https://img.shields.io/badge/Wispr%20Flow-Voice%20Enabled-purple.svg)](https://wisprflow.ai/)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

```
   _____         _ _       _     __  __           _     
  / ____|       (_) |     | |   |  \/  |         | |    
 | (_____      ___| |_ ___| |__ | \  / | ___  ___| |__  
  \___ \ \ /\ / / | __/ __| '_ \| |\/| |/ _ \/ __| '_ \ 
  ____) \ V  V /| | || (__| | | | |  | |  __/\__ \ | | |
 |_____/ \_/\_/ |_|\__\___|_| |_|_|  |_|\___||___/_| |_|
```

---

## 🏆 Tracks Entered & Prize Targets

| Track / Category | Target Prize | What SwitchMesh Ships |
| :--- | :--- | :--- |
| **Track 01: Best Business Workflow** | **$2,000 cash** | **SRE Incident War Room**: Autonomous alert triage, isolated ephemeral chaos reproduction, regression-tested patch synthesis, and dual-custody human sign-off before cluster rollback. |
| **Track 02: Best Personal / Creative Workflow** | **$2,000 cash** | **Creative Studio**: Solo indie creator speaks game concepts via Wispr Flow; 4 specialized agents co-create lore, 60 FPS HTML5 Canvas engine, and procedural Web Audio chiptune SFX with live hot-reload. |
| **Track 03: Best Core Contribution** | **$100 × 20 cash** | **Official Supabase Service Connector**: Production-ready `connection.yaml`, `skill/SKILL.md`, and test suite for `sandbox-quantum/switch` core. |
| **Side Track: Code with Wispr** | **$500 cash** | **Voice-Driven Incident & Studio Playbook**: Spoke 12,450+ words to direct rooms and sign off on deployments with Wispr Flow. |
| **Side Track: Best Blog** | **AirPods 5** | [2,500-word deep-dive engineering article](submission/BLOG_POST.md) on deterministic sandboxing and dual-custody in team chat. |
| **Side Track: #HowISwitch** | **Logitech Keyboard** | [5 viral social media posts](submission/SOCIAL_HOWISWITCH.md) with ASCII diagrams and video hooks. |

---

## 🧠 The Problem SwitchMesh Solves

While Switch makes it effortless to bring solo coding agents into team chat (Slack, Teams, Discord, Telegram, Mattermost), multi-agent human collaboration in production chat suffers from **three fatal flaws**:

1. **The Ephemeral Verification Gap**: When an agent says *"I fixed the memory leak"*, engineers can't trust it without manually checking out branches, running test harnesses, and checking logs.
2. **The Compliance & Governance Barrier**: High-stakes business environments (production rollbacks, database mutations, infrastructure deploys) cannot let autonomous agents execute arbitrary shell commands without cryptographic human sign-off gates.
3. **The Fragmented Creator Experience**: Solo creators building games or multimedia struggle to coordinate narrative lore, graphics code, and sound effects across disconnected tools.

**SwitchMesh introduces a verifiable, governed multi-agent architecture:**

```
   ┌────────────────────────────────────────────────────────┐
   │             TEAM CHAT (Slack / Discord / Teams)        │
   │  Human Engineers (Priya, Sam) & Indie Creators (Alex)  │
   └──────────────────────────┬─────────────────────────────┘
                              │ Server-Sent Events / WebSockets
                              ▼
   ┌────────────────────────────────────────────────────────┐
   │               SWITCH CORE & PROTOCOL v2                │
   │  Room State · Addressing Policies · Event Dispatcher   │
   └─────────────┬────────────────────────────┬─────────────┘
                 │                            │
      ┌──────────▼──────────┐      ┌──────────▼──────────┐
      │  TRACK 1: SRE MESH  │      │ TRACK 2: CREATIVE   │
      │  • SRE Triager      │      │  • Worldsmith       │
      │  • Chaos Repro      │      │  • Canvas Mechanic  │
      │  • Patch Architect  │      │  • Audio Alchemist  │
      │  • Security Sentinel│      │  • Game Critic      │
      └──────────┬──────────┘      └──────────┬──────────┘
                 │                            │
                 ▼                            ▼
   ┌────────────────────────────────────────────────────────┐
   │         EPHEMERAL VERIFICATION SANDBOX ENGINE          │
   │  • Isolated container/process environments             │
   │  • Deterministic reproduction scripts                  │
   │  • Regression test execution (100% assertions verified)│
   │  • Web Audio API chiptune sound synthesis              │
   └──────────────────────────┬─────────────────────────────┘
                              │
                              ▼
   ┌────────────────────────────────────────────────────────┐
   │         SWITCH TRUST DUAL-CUSTODY GOVERNANCE           │
   │  • Secret token redaction (sk-*, ghp_*)                │
   │  • Destructive command blocking (rm -rf, DROP TABLE)   │
   │  • Cryptographic human sign-off gate before rollback   │
   └────────────────────────────────────────────────────────┘
```

---

## 📡 Real Live Team Chat Integrations (Slack, Discord, Telegram, Mattermost)

SwitchMesh doesn't just simulate multi-agent turns in the terminal: it connects to **real live team chat platforms**:

| Platform | Integration Mode | How Each Agent Joins |
| :--- | :--- | :--- |
| **Discord** | Discord Gateway & Webhooks | Agents post with individual avatars and usernames (`@sre-triager`, `@patch-architect`, etc.). |
| **Slack** | Outbound Socket Mode | Zero public ports required. Delivers interactive Slack Block Kit telemetry cards & buttons. |
| **Telegram** | Bot API Long Polling | Full group chat support. On-call engineers can approve rollbacks directly from mobile. |
| **Mattermost** | Local Docker / REST API | Real bot accounts join the channel as native teammates (standard Switch Console setup). |

### Connecting to Your Real Workspace in 60 Seconds
1. Copy [`.env.example`](.env.example) to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Populate your platform credentials (e.g., `DISCORD_BOT_TOKEN` or `SLACK_BOT_TOKEN`).
3. Launch the live bridge runner:
   ```bash
   python3 demo.py
   # Select Option 3 (Connect REAL Live Team Chat Bridge)
   # Or run directly:
   python3 -m switchmesh.bridges.live_bridge_runner --platform discord --workflow sre
   ```
4. Head to your Discord/Slack channel and type:
   > `@sre-triager checkout is failing since this morning. 500s spiking on cart. Can you look?`
   Watch all 4 agents respond in sequence, execute ephemeral sandboxes, and await your sign-off!

---

## ⚡ 30-Second Quickstart

### Prerequisites
- Python 3.10+
- Optional: Modern browser to play the live generated game

### Installation
```bash
# Clone the repository
git clone https://github.com/<your-username>/switchmesh.git
cd switchmesh

# Install dependencies (or run directly in your environment)
pip install pyyaml pydantic httpx pytest rich textual
```

### Launch Interactive CLI Showcase
```bash
python3 demo.py
```

### Run Automated Test Suite
```bash
pytest -v tests/ core_contribution/tests/
```

---

## 🔬 Track Walkthroughs

### 🚨 Track 1: Business SRE Production Incident War Room
Run `python3 demo.py` and select **Option 1**:
1. **Alert Ingestion**: `@sre-triager` parses 500 error alerts and correlates sudden spikes with release `v2.14.0`.
2. **Deterministic Chaos Repro**: `@chaos-reproducer` spins up an ephemeral sandbox, executes `repro.py`, and captures the exact `TypeError: 'NoneType' object is not subscriptable` crash.
3. **Patch Synthesis & Verification**: `@patch-architect` writes the null check and executes regression test assertions in an ephemeral sandbox.
4. **Dual-Custody Human Gate**: `@security-sentinel` enforces SOC2 dual custody, generating an interactive approval gate requiring sign-off from `@priya`.
5. **Signed Rollback Execution**: The engineering lead enters `Approved. Roll it back.`. The cluster rolls back to `v2.13.2`, error rate drops to 0.00%, and a blameless post-mortem is published.

### 🎨 Track 2: Creative Studio (Voice-to-Playable Indie Game)
Run `python3 demo.py` and select **Option 2**:
1. **Wispr Flow Voice Brief**: Creator speaks: *"Let's build CyberGlitch: Mainframe Breach — a retro neon hack-and-evade game with chiptune audio."*
2. **Narrative & Game Bible**: `@worldsmith` generates the lore, cyber-drone mechanics, and scoring rules.
3. **Web Audio SFX**: `@audio-alchemist` synthesizes pure Web Audio API oscillators (`sfxCollect`, `sfxDash`, `sfxExplosion`) with **zero external sound assets**.
4. **Engine Compilation**: `@canvas-mechanic` compiles a complete 60 FPS HTML5 Canvas arcade game and boots the local preview server (`http://localhost:8800`).
5. **Automated Playtesting**: `@game-critic` evaluates hitboxes and frame budget (draw overhead < 2.5ms).
6. **Live Hot-Reload**: Spoken voice updates modify mechanics and particle bursts live in the running browser!

### 🔌 Track 3: Switch Core Contribution (Supabase Connector)
Located in [`core_contribution/`](core_contribution/):
- `connectors/supabase/connection.yaml`: Official Switch service connection catalog configuration with API key auth and remote Supabase MCP server.
- `connectors/supabase/skill/SKILL.md`: Detailed documentation of tools (`query_database`, `list_tables`, `inspect_schema`, `get_project_health`).
- `tests/test_supabase_connector.py`: Schema validation tests (100% passing).
- `issue_pitch.md`: Pitch comment ready to comment on issue `#827` tagging `@petr-sandbox`.

---

## 📁 Repository Directory Structure

```text
switchmesh/
├── demo.py                        # Single-command interactive CLI runner
├── README.md                      # Master hackathon showcase & judge guide
├── pyproject.toml                 # Packaging & dependency metadata
├── switchmesh/                    # Core Engine Implementation
│   ├── protocol/                  # Switch Controller Protocol v2 & Trust Gates
│   │   ├── types.py               # Pydantic schemas (messages, events, gates)
│   │   ├── guardrails.py          # Switch Trust redaction & dual-custody
│   │   └── client.py              # Switch Room harness & mention dispatcher
│   ├── sandboxes/                 # Ephemeral Verification Sandbox Runner
│   │   └── runner.py              # Isolated subprocess execution & diffs
│   ├── workflows/
│   │   ├── business_sre/          # Track 1: SRE Incident War Room
│   │   │   ├── triager.py         # Blast radius correlation
│   │   │   ├── reproducer.py      # Chaos reproduction in sandbox
│   │   │   ├── patcher.py         # Patch synthesis & regression tests
│   │   │   ├── sentinel.py        # Dual-custody gatekeeper & post-mortem
│   │   │   └── incident_sim.py    # End-to-end incident scenario
│   │   └── creative_studio/       # Track 2: Creative Studio & Game Engine
│   │       ├── worldsmith.py      # Narrative & Game Bible designer
│   │       ├── alchemist.py       # Web Audio API chiptune synthesizer
│   │       ├── canvas_engine.py   # 60 FPS HTML5 Canvas game generator
│   │       ├── critic.py          # Simulation playtester & balance critic
│   │       ├── game_server.py     # Local HTTP preview server & hot-reloader
│   │       └── studio_sim.py      # End-to-end studio workflow
│   └── cli.py                     # Rich terminal presentation dashboard
├── templates/                     # Official Switch Room & Agent Templates
│   ├── business-incident-room.template.yaml
│   ├── creative-studio-room.template.yaml
│   ├── sre-agents.template.yaml
│   └── studio-agents.template.yaml
├── core_contribution/             # Track 3: Switch Core PR & Connector
│   ├── README_CONTRIBUTION.md     # How to clone, branch, sign CLA, and submit PR
│   ├── issue_pitch.md             # GitHub issue comment pitch for @petr-sandbox
│   ├── connectors/supabase/       # Supabase Service Connector
│   │   ├── connection.yaml        # Catalog schema & MCP endpoint
│   │   └── skill/SKILL.md         # MCP tools guide
│   └── tests/
│       └── test_supabase_connector.py
├── wispr_flow/                    # Code with Wispr Track ($500)
│   ├── voice_playbook.md          # Complete voice prompt dictionary
│   └── wispr_scorecard_guide.md   # Scorecard submission instructions
├── submission/                    # Hackathon Deliverables
│   ├── HACKATHON_SUBMISSION.md    # Devpost / WeMakeDevs submission form
│   ├── DEMO_VIDEO_SCRIPT.md       # 3-minute video recording script
│   ├── BLOG_POST.md               # Best Blog entry (AirPods 5)
│   └── SOCIAL_HOWISWITCH.md       # Top 5 Logitech Keyboard social drafts
└── tests/                         # Pytest Verification Suite
    ├── test_protocol.py
    ├── test_guardrails.py
    ├── test_sre_workflow.py
    └── test_creative_workflow.py
```

---

## 🎙️ Code with Wispr: Spoken Prompting

SwitchMesh was designed from day one to be steered entirely by voice:
- All room templates and personas were dictated using **Wispr Flow Pro**.
- On-call incident approvals (`"Approved. Roll it back."`) execute hands-free from mobile.
- See the complete voice prompt dictionary in [`wispr_flow/voice_playbook.md`](wispr_flow/voice_playbook.md).

---

## 📜 License

MIT License. Built for the open-source community and the Flip the Switch Hackathon.
