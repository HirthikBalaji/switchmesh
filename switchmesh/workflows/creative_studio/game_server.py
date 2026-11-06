"""
SwitchMesh Creative Studio Preview Server.
Serves the generated HTML5 Canvas game with hot-reloading capability.
"""

from __future__ import annotations
import http.server
import socketserver
import threading
import os
from typing import Optional
from switchmesh.workflows.creative_studio.canvas_engine import CanvasMechanicAgent


class GameServer:
    def __init__(self, port: int = 8800, serve_dir: str = "/tmp/switchmesh_game"):
        self.port = port
        self.serve_dir = serve_dir
        self.httpd: Optional[socketserver.TCPServer] = None
        self.thread: Optional[threading.Thread] = None
        self.mechanic = CanvasMechanicAgent()

        os.makedirs(self.serve_dir, exist_ok=True)
        self.write_game_file()

    def write_game_file(self, title: str = "CyberGlitch: Mainframe Breach") -> str:
        content = self.mechanic.generate_html5_game(title)
        game_path = os.path.join(self.serve_dir, "index.html")
        with open(game_path, "w", encoding="utf-8") as f:
            f.write(content)
        return game_path

    def start(self):
        """Starts the local preview HTTP server in a background thread."""
        serve_dir = self.serve_dir

        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=serve_dir, **kwargs)

            def log_message(self, format, *args):
                pass  # suppress noisy access logs

        socketserver.TCPServer.allow_reuse_address = True
        try:
            self.httpd = socketserver.TCPServer(("", self.port), Handler)
            self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
            self.thread.start()
            return f"http://localhost:{self.port}"
        except OSError:
            # Port may already be in use or unavailable
            return f"file://{os.path.join(self.serve_dir, 'index.html')}"

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
