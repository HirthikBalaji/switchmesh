"""
Integration test for Track 2 Creative Studio Workflow.
"""

from switchmesh.workflows.creative_studio.studio_sim import CreativeStudioWorkflow


def test_full_creative_studio_lifecycle():
    workflow = CreativeStudioWorkflow("indie-studio-test", bridge="discord")

    # 1. Prompt
    m1 = workflow.run_stage_1_creator_prompt("Build CyberGlitch hack-and-evade")
    assert "CyberGlitch" in m1.content

    # 2. Worldsmith
    m2, bible = workflow.run_stage_2_worldsmith()
    assert "CyberGlitch" in bible["title"]
    assert "CREATIVE GAME BIBLE GENERATED" in m2.content

    # 3. Audio Alchemist
    m3 = workflow.run_stage_3_alchemist()
    assert "AUDIO & ASSET SYNTHESIS COMPLETE" in m3.content
    assert "sfxCollect" in m3.content

    # 4. Canvas Mechanic
    m4, url = workflow.run_stage_4_mechanic()
    assert "HTML5 ARCADE ENGINE COMPILED" in m4.content
    assert url.startswith("http") or url.startswith("file")

    # 5. Critic
    m5, eval_data = workflow.run_stage_5_critic()
    assert eval_data["verdict"] == "READY_FOR_CREATOR_PLAYTEST"
    assert "4/4" in eval_data["checks_passed"]

    # 6. Hot Reload Tweak
    m6 = workflow.run_stage_6_creator_tweak("Add hyper-speed and extra neon glow")
    assert "HOT-RELOAD APPLIED" in workflow.harness.messages[-1].content

    workflow.game_server.stop()
