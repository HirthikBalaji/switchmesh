"""
Canvas Mechanic Agent.
Generates complete 60 FPS HTML5 Canvas arcade game implementations,
combining game loops, physics engines, particles, collision mathematics,
and audio synthesizers into a self-contained, playable artifact.
"""

from __future__ import annotations
from typing import Dict
from switchmesh.workflows.creative_studio.alchemist import AudioAlchemistAgent


class CanvasMechanicAgent:
    def __init__(self, name: str = "canvas-mechanic"):
        self.name = name
        self.alchemist = AudioAlchemistAgent()

    def generate_html5_game(self, title: str = "CyberGlitch: Mainframe Breach", theme_params: Dict = None) -> str:
        """
        Compiles a complete self-contained HTML5 Canvas game file with embedded JS and CSS.
        """
        sfx_js = self.alchemist.generate_web_audio_synth_script()

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; user-select: none; }}
        body {{
            background: #060913;
            color: #00f3ff;
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            overflow: hidden;
        }}
        #game-container {{
            position: relative;
            box-shadow: 0 0 30px rgba(0, 243, 255, 0.3);
            border: 2px solid #00f3ff;
            border-radius: 8px;
            overflow: hidden;
            background: #02040a;
        }}
        canvas {{
            display: block;
        }}
        #hud {{
            position: absolute;
            top: 12px;
            left: 16px;
            right: 16px;
            display: flex;
            justify-content: space-between;
            font-size: 16px;
            font-weight: bold;
            text-shadow: 0 0 8px #00f3ff;
            pointer-events: none;
        }}
        #instructions {{
            margin-top: 12px;
            font-size: 13px;
            color: #8fa3bf;
            text-align: center;
            letter-spacing: 1px;
        }}
        .badge {{
            color: #ff0055;
            text-shadow: 0 0 8px #ff0055;
        }}
        #voice-tag {{
            margin-top: 6px;
            font-size: 11px;
            color: #4a627a;
        }}
    </style>
</head>
<body>
    <div id="game-container">
        <canvas id="gameCanvas" width="800" height="500"></canvas>
        <div id="hud">
            <div>CORE: <span id="score">0</span> | LEVEL: <span id="level">1</span></div>
            <div>SHIELD: <span id="shield">100%</span> | <span class="badge" id="threat">DEFENSE ACTIVE</span></div>
        </div>
    </div>
    <div id="instructions">
        CONTROLS: [WASD / ARROW KEYS] Move | [SPACEBAR] Warp Pulse Dash | [R] Reboot
    </div>
    <div id="voice-tag">
        Generated & Hot-Reloaded via SwitchMesh Creative Studio & Wispr Flow Voice
    </div>

    <script>
    {sfx_js}

    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const scoreEl = document.getElementById('score');
    const levelEl = document.getElementById('level');
    const shieldEl = document.getElementById('shield');
    const threatEl = document.getElementById('threat');

    // Game State
    let score = 0;
    let level = 1;
    let shield = 100;
    let gameOver = false;
    let keys = {{}};
    let particles = [];

    // Player Drone
    const player = {{
        x: 400,
        y: 250,
        radius: 14,
        vx: 0,
        vy: 0,
        speed: 4.8,
        friction: 0.88,
        dashCooldown: 0
    }};

    // Data Nodes (Pickups)
    let nodes = [];
    function spawnNodes(count) {{
        nodes = [];
        for (let i = 0; i < count; i++) {{
            nodes.push({{
                x: Math.random() * (canvas.width - 60) + 30,
                y: Math.random() * (canvas.height - 60) + 30,
                radius: 7,
                pulse: Math.random() * Math.PI
            }});
        }}
    }}

    // Sentinels (Enemies)
    let sentinels = [];
    function spawnSentinels(count) {{
        sentinels = [];
        for (let i = 0; i < count; i++) {{
            sentinels.push({{
                x: (i % 2 === 0) ? 60 : canvas.width - 60,
                y: Math.random() * (canvas.height - 80) + 40,
                radius: 16,
                vx: (Math.random() - 0.5) * (2 + level * 0.5),
                vy: (Math.random() - 0.5) * (2 + level * 0.5),
                laserAngle: 0
            }});
        }}
    }}

    function createExplosion(x, y, color, count = 16) {{
        for (let i = 0; i < count; i++) {{
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 5 + 1;
            particles.push({{
                x, y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                life: 1.0,
                decay: Math.random() * 0.03 + 0.02,
                color
            }});
        }}
    }}

    // Setup input listeners
    window.addEventListener('keydown', e => {{
        keys[e.key.toLowerCase()] = true;
        if (e.key === ' ' && player.dashCooldown <= 0 && !gameOver) {{
            player.vx *= 2.8;
            player.vy *= 2.8;
            player.dashCooldown = 35;
            createExplosion(player.x, player.y, '#00f3ff', 12);
            sfxDash();
        }}
        if (e.key.toLowerCase() === 'r' && gameOver) {{
            restartGame();
        }}
    }});
    window.addEventListener('keyup', e => {{
        keys[e.key.toLowerCase()] = false;
    }});

    function restartGame() {{
        score = 0;
        level = 1;
        shield = 100;
        gameOver = false;
        player.x = 400;
        player.y = 250;
        player.vx = 0;
        player.vy = 0;
        spawnNodes(6);
        spawnSentinels(3);
    }}

    spawnNodes(6);
    spawnSentinels(3);

    // Main Game Loop
    function update() {{
        if (gameOver) return;

        // Player movement
        if (keys['w'] || keys['arrowup']) player.vy -= player.speed * 0.25;
        if (keys['s'] || keys['arrowdown']) player.vy += player.speed * 0.25;
        if (keys['a'] || keys['arrowleft']) player.vx -= player.speed * 0.25;
        if (keys['d'] || keys['arrowright']) player.vx += player.speed * 0.25;

        player.vx *= player.friction;
        player.vy *= player.friction;
        player.x += player.vx;
        player.y += player.vy;

        // Clamp in screen
        if (player.x < player.radius) {{ player.x = player.radius; player.vx *= -0.5; }}
        if (player.x > canvas.width - player.radius) {{ player.x = canvas.width - player.radius; player.vx *= -0.5; }}
        if (player.y < player.radius) {{ player.y = player.radius; player.vy *= -0.5; }}
        if (player.y > canvas.height - player.radius) {{ player.y = canvas.height - player.radius; player.vy *= -0.5; }}

        if (player.dashCooldown > 0) player.dashCooldown--;

        // Nodes collection
        for (let i = nodes.length - 1; i >= 0; i--) {{
            const n = nodes[i];
            const dist = Math.hypot(player.x - n.x, player.y - n.y);
            if (dist < player.radius + n.radius) {{
                nodes.splice(i, 1);
                score += 100 * level;
                createExplosion(n.x, n.y, '#00f3ff', 14);
                sfxCollect();
            }}
        }}

        // Check level advance
        if (nodes.length === 0) {{
            level++;
            shield = Math.min(100, shield + 25);
            sfxWinLevel();
            spawnNodes(6 + level * 2);
            spawnSentinels(2 + level);
            createExplosion(player.x, player.y, '#b026ff', 30);
        }}

        // Sentinels AI
        sentinels.forEach(s => {{
            s.x += s.vx;
            s.y += s.vy;
            if (s.x < s.radius || s.x > canvas.width - s.radius) s.vx *= -1;
            if (s.y < s.radius || s.y > canvas.height - s.radius) s.vy *= -1;

            // Collision with player
            const dist = Math.hypot(player.x - s.x, player.y - s.y);
            if (dist < player.radius + s.radius) {{
                shield -= 2.2;
                createExplosion((player.x + s.x) / 2, (player.y + s.y) / 2, '#ff0055', 4);
                if (Math.random() < 0.2) sfxExplosion();
                if (shield <= 0) {{
                    shield = 0;
                    gameOver = true;
                    sfxExplosion();
                    createExplosion(player.x, player.y, '#ff0055', 45);
                }}
            }}
        }});

        // Particles
        for (let i = particles.length - 1; i >= 0; i--) {{
            const p = particles[i];
            p.x += p.vx;
            p.y += p.vy;
            p.life -= p.decay;
            if (p.life <= 0) particles.splice(i, 1);
        }}

        // HUD updates
        scoreEl.innerText = score;
        levelEl.innerText = level;
        shieldEl.innerText = Math.round(shield) + '%';
        shieldEl.style.color = shield > 40 ? '#00f3ff' : '#ff0055';
    }}

    function draw() {{
        // Clear background with cyberpunk trail
        ctx.fillStyle = 'rgba(2, 4, 10, 0.25)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Cyber Grid Lines
        ctx.strokeStyle = 'rgba(0, 243, 255, 0.04)';
        ctx.lineWidth = 1;
        for (let x = 0; x < canvas.width; x += 40) {{
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, canvas.height);
            ctx.stroke();
        }}
        for (let y = 0; y < canvas.height; y += 40) {{
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
            ctx.stroke();
        }}

        // Draw Data Nodes
        nodes.forEach(n => {{
            n.pulse += 0.08;
            const r = n.radius + Math.sin(n.pulse) * 2;
            ctx.beginPath();
            ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
            ctx.fillStyle = '#00f3ff';
            ctx.shadowBlur = 12;
            ctx.shadowColor = '#00f3ff';
            ctx.fill();
            ctx.shadowBlur = 0;
        }});

        // Draw Sentinels
        sentinels.forEach(s => {{
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
            ctx.fillStyle = '#ff0055';
            ctx.shadowBlur = 15;
            ctx.shadowColor = '#ff0055';
            ctx.fill();
            ctx.shadowBlur = 0;

            // Inner core
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.radius * 0.45, 0, Math.PI * 2);
            ctx.fillStyle = '#ffffff';
            ctx.fill();
        }});

        // Draw Player Drone
        if (!gameOver) {{
            ctx.beginPath();
            ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2);
            ctx.fillStyle = player.dashCooldown > 0 ? '#b026ff' : '#00f3ff';
            ctx.shadowBlur = 18;
            ctx.shadowColor = player.dashCooldown > 0 ? '#b026ff' : '#00f3ff';
            ctx.fill();
            ctx.shadowBlur = 0;

            // Drone Direction Reticle
            ctx.beginPath();
            ctx.arc(player.x + player.vx * 2, player.y + player.vy * 2, 4, 0, Math.PI * 2);
            ctx.fillStyle = '#ffffff';
            ctx.fill();
        }}

        // Draw Particles
        particles.forEach(p => {{
            ctx.beginPath();
            ctx.arc(p.x, p.y, 2.5 * p.life, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.globalAlpha = p.life;
            ctx.fill();
            ctx.globalAlpha = 1.0;
        }});

        // Game Over Overlay
        if (gameOver) {{
            ctx.fillStyle = 'rgba(0, 0, 0, 0.75)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = '#ff0055';
            ctx.font = 'bold 36px Courier New';
            ctx.textAlign = 'center';
            ctx.shadowBlur = 20;
            ctx.shadowColor = '#ff0055';
            ctx.fillText('CORE OVERRIDE: TERMINATED', canvas.width / 2, canvas.height / 2 - 20);

            ctx.fillStyle = '#00f3ff';
            ctx.font = '18px Courier New';
            ctx.shadowBlur = 8;
            ctx.shadowColor = '#00f3ff';
            ctx.fillText('FINAL SCORE: ' + score + ' | LEVEL: ' + level, canvas.width / 2, canvas.height / 2 + 25);
            ctx.fillText('PRESS [R] TO REBOOT QUANTUM CORE', canvas.width / 2, canvas.height / 2 + 65);
            ctx.shadowBlur = 0;
        }}
    }}

    function loop() {{
        update();
        draw();
        requestAnimationFrame(loop);
    }}
    requestAnimationFrame(loop);
    </script>
</body>
</html>
"""
        return html_content

    def format_room_presentation(self, game_url: str = "http://localhost:8800") -> str:
        return (
            f"🎮 **[HTML5 ARCADE ENGINE COMPILED & LIVE]**\n"
            f"- **Game Engine:** 60 FPS Canvas with Momentum Physics, Friction, Dash Cooldown\n"
            f"- **Render Loop:** Cyberpunk neon glow effects with particle emitters\n"
            f"- **Live Preview:** `{game_url}`\n"
            f"- **Controls:** WASD / Arrow Keys + Space to Dash\n"
            f"Passing to `@game-critic` to run automated simulated playtests and balance checks."
        )
