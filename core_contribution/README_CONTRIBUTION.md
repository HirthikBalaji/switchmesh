# Track 3: Switch Core Contribution Walkthrough

This directory contains our ready-to-merge contribution for the official [Switch Core Repository](https://github.com/sandbox-quantum/switch) to compete in **Track 03: Best Core Contribution ($100 x 20)**.

## Contribution Overview: Supabase Service Connector

Switch connects AI agents with human teammates in team chat. To give AI teammates the power to inspect databases, diagnose schema migration failures, and query backend tables during incidents, they need service connections.

We built the official **Supabase Service Connector**:
1. `connectors/supabase/connection.yaml`: Full connection catalog definition following Switch's v2 specification.
2. `connectors/supabase/skill/SKILL.md`: Comprehensive skill guide explaining tools (`query_database`, `list_tables`, `inspect_schema`, `get_project_health`).
3. `tests/test_supabase_connector.py`: Automated pytest test suite.

## How to Submit Your Pull Request

1. **Fork the Switch repository:**
   Visit `https://github.com/sandbox-quantum/switch` and click **Fork**.

2. **Clone your fork and create a branch:**
   ```bash
   git clone https://github.com/<your-username>/switch.git
   cd switch
   git checkout -b feat/supabase-connector
   ```

3. **Copy the connector files into Switch Core:**
   ```bash
   cp -r /home/dragon/switch/core_contribution/connectors/supabase core/switch_core/connections/catalog/
   cp /home/dragon/switch/core_contribution/tests/test_supabase_connector.py core/tests/
   ```

4. **Sign the CLA:**
   Switch has an automated Contributor License Agreement bot on GitHub that posts a link when you open your first PR. Click it and sign.

5. **Commit and Push:**
   ```bash
   git add core/switch_core/connections/catalog/supabase core/tests/test_supabase_connector.py
   git commit -m "feat(connections): add Supabase connector (#827) #FliptheSwitch"
   git push origin feat/supabase-connector
   ```

6. **Open the PR:**
   Use the PR title and description provided in `core_contribution/issue_pitch.md`!
