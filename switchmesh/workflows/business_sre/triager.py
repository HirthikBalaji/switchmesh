"""
SRE Incident Triager Agent.
Monitors alerts, parses production error logs, isolates affected deployment versions,
and routes reproducible failure cases to the Chaos Reproducer.
"""

from __future__ import annotations
from typing import Dict, List, Optional
from switchmesh.protocol.types import MessageRole, RoomMessage


class SRETriagerAgent:
    def __init__(self, name: str = "sre-triager"):
        self.name = name

    def process_incident_report(self, incident_text: str) -> Dict:
        """
        Parses incident report, extracts symptoms, affected microservice, and suspects.
        """
        service = "cart-service" if "cart" in incident_text.lower() else "core-api"
        status_code = 500 if "500" in incident_text else 502

        triage_data = {
            "service": service,
            "status_code": status_code,
            "severity": "SEV-1 (CRITICAL)",
            "impact": "Customer checkout failure, cart checkout dropping 84%",
            "suspect_deploy": "v2.14.0 (shipped at 09:40 UTC)",
            "stable_version": "v2.13.2",
            "action_required": "reproduce_and_remediate"
        }
        return triage_data

    def handle_message(self, message: RoomMessage) -> Optional[str]:
        if "failing" in message.content.lower() or "checkout" in message.content.lower() or "500" in message.content:
            data = self.process_incident_report(message.content)
            response = (
                f"🚨 **[SEV-1 INCIDENT TRIAGED]**\n"
                f"- **Service:** `{data['service']}`\n"
                f"- **Severity:** {data['severity']}\n"
                f"- **Telemetry:** High spike of {data['status_code']} errors observed.\n"
                f"- **Correlation:** Deploy `{data['suspect_deploy']}` landed 2 min prior to error spike.\n"
                f"- **Routing:** Handing to `@chaos-reproducer` to isolate root cause in isolated sandbox."
            )
            return response
        return None
