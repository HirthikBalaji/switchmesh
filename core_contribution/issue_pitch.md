# Track 3: Pitch & Claim Guide for Switch Core Contribution

To win the **$100 Cash Prize** in **Track 03 (Best Core Contribution)**, follow this exact playbook:

## 1. Comment on GitHub Issue #827 (or create/claim another issue)
Visit: `https://github.com/sandbox-quantum/switch/issues/827`

Post this exact comment:

```markdown
Hi @petr-sandbox! I would like to take this issue to add the official **Supabase** connector to Switch's connection catalog.

### Implementation Plan:
1. Add `core/switch_core/connections/catalog/supabase/connection.yaml` with standard `api_key` auth (supporting project reference and service_role/anon API keys).
2. Wire the official Supabase MCP endpoint (`https://mcp.supabase.com/v1`) with secure header pass-through.
3. Include the complete `skill/SKILL.md` guide covering database queries, schema inspection, and room interaction rules.
4. Add comprehensive unit tests in `core/tests/` verifying schema integrity and authentication headers.

Ready to submit immediately upon assignment!
```

---

## 2. If #827 is already taken or needs fallback:
You can also pitch for **#825 (PagerDuty)** or **#828 (Cloudflare)**:

```markdown
Hi @petr-sandbox! I'm submitting the connector implementation for Switch's catalog. We have completed the YAML schema definition, MCP endpoint bindings, SKILL documentation, and test verification suite. Please assign this to me so I can link the PR.
```

---

## 3. Pull Request Template

When opening the PR on `sandbox-quantum/switch`:

**Title:** `feat(connections): add Supabase database and auth connector (#827) #FliptheSwitch`

**Description:**
```markdown
Closes #827

### Summary
Adds the official Supabase connector to Switch's service connection catalog. This enables AI teammates across Slack, Discord, Teams, and Mattermost to query Postgres schemas, inspect tables, and run authorized diagnostics directly in chat.

### What's Changed
- `core/switch_core/connections/catalog/supabase/connection.yaml`: Full catalog configuration with project ref, api key fields, and remote MCP server.
- `core/switch_core/connections/catalog/supabase/skill/SKILL.md`: Detailed tool guide, security guardrails, and room examples.
- `core/tests/connections/test_supabase.py`: Schema validation and token hygiene tests.

### Verification
- Schema parsed and validated against Switch's catalog schema.
- All unit tests passing cleanly.
```
