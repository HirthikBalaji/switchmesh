---
name: supabase
description: Query Postgres tables, inspect database schemas, manage auth users, and execute RPC functions with Supabase through its MCP tools.
---

# Supabase

The `supabase` MCP server gives AI teammates access to your Supabase project.
Use them to inspect database structures, debug queries, query logs, and manage
user records directly inside team chat rooms.

## Available Tools

- `query_database`: Run read-only or parameterized SQL queries against your Postgres instance.
- `list_tables`: Retrieve list of all schemas, public tables, views, and column types.
- `inspect_schema`: Inspect detailed schema definition including primary keys, indexes, and foreign key relations.
- `get_project_health`: Check database connection pooling, CPU utilization, and replication lag.

## How to Work With It

1. **Safety First**: Prefer `list_tables` and `inspect_schema` before constructing SQL queries. Never perform destructive operations (`DROP`, `TRUNCATE`, `DELETE WHERE 1=1`) without explicit human confirmation in the room.
2. **Scoping**: Limit queries with `LIMIT 50` to prevent memory bottlenecks in chat threads.
3. **Environment**: When debugging an incident, verify whether the project reference matches production or staging before querying customer tables.

## Example Usage in Switch Rooms

```text
@Claude Code can you check why user signups failed on Supabase in the last 15 minutes?
```

The agent uses the `supabase` connector to inspect `auth.users` or query `pg_stat_activity`
and reports back with the root cause.
