"""
Unit test for the Switch Supabase Service Connector.
Verifies YAML syntax, required fields, MCP server headers, and skill documentation.
"""

import os
import yaml


def test_supabase_connector_yaml_schema():
    catalog_path = os.path.join(
        os.path.dirname(__file__), "..", "connectors", "supabase", "connection.yaml"
    )
    assert os.path.exists(catalog_path), f"connection.yaml missing at {catalog_path}"

    with open(catalog_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Validate essential schema fields
    assert data["slug"] == "supabase"
    assert data["name"] == "Supabase"
    assert data["category"] == "Database & Backend"
    assert data["enabled"] is True
    assert data["adapter"] == "api_key"

    # Validate Auth configuration
    auth = data["auth"]
    assert auth["type"] == "api_key"
    fields = {f["name"]: f for f in auth["api_key"]["fields"]}
    assert "project_ref" in fields
    assert "api_key" in fields
    assert fields["api_key"]["secret"] is True

    # Validate MCP configuration
    assert "mcp" in data
    mcp_servers = data["mcp"]["servers"]
    assert len(mcp_servers) >= 1
    server = mcp_servers[0]
    assert server["name"] == "supabase"
    assert "SUPABASE_PROJECT_REF" in server["headers"]
    assert "SUPABASE_API_KEY" in server["headers"]


def test_supabase_skill_md():
    skill_path = os.path.join(
        os.path.dirname(__file__), "..", "connectors", "supabase", "skill", "SKILL.md"
    )
    assert os.path.exists(skill_path), f"SKILL.md missing at {skill_path}"

    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "---" in content
    assert "name: supabase" in content
    assert "Available Tools" in content
    assert "Example Usage" in content
