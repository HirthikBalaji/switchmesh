"""
Integration test for Track 1 Business SRE Workflow.
"""

from switchmesh.workflows.business_sre.incident_sim import SREWarRoomWorkflow
from switchmesh.protocol.types import GateOutcome


def test_full_sre_incident_lifecycle():
    workflow = SREWarRoomWorkflow("prod-incident-test", bridge="slack")

    # 1. Alert
    m1 = workflow.run_stage_1_alert()
    assert "checkout is failing" in m1.content

    # 2. Triage
    m2 = workflow.run_stage_2_triage()
    assert "SEV-1 INCIDENT TRIAGED" in m2.content
    assert "cart-service" in m2.content

    # 3. Repro
    m3, repro_data = workflow.run_stage_3_repro()
    assert repro_data["reproduced"] is True
    assert repro_data["exit_code"] == 1
    assert "ROOT CAUSE REPRODUCED" in m3.content

    # 4. Patch
    m4, patch_data = workflow.run_stage_4_patch()
    assert patch_data["verified"] is True
    assert patch_data["exit_code"] == 0
    assert "PATCH SYNTHESIZED & VERIFIED" in m4.content

    # 5. Dual-Custody Gate
    m5 = workflow.run_stage_5_gate("priya")
    assert "DUAL-CUSTODY GATE REQUIRED" in m5.content

    # 6. Human Approval
    m6 = workflow.run_stage_6_human_approval("priya", "Approved. Roll it back immediately.")
    assert "Approved" in m6.content

    # Verify final messages contain resolution and post-mortem
    final_messages = workflow.harness.messages
    assert any("PRODUCTION ROLLBACK COMPLETED SUCCESSFULLY" in m.content for m in final_messages)
    assert any("INCIDENT BLAMELESS POST-MORTEM" in m.content for m in final_messages)
