"""Servidor local del portal sintético de mesa de ayuda."""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8010
APP_DIR = Path(__file__).resolve().parent / "app"


class HelpDeskHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP_DIR), **kwargs)

    def end_headers(self) -> None:
        # Evita que el navegador conserve versiones anteriores durante el laboratorio.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), HelpDeskHandler)
    print(f"Mesa de ayuda disponible en http://{HOST}:{PORT}/login.html")
    print("Presione Ctrl+C para detener el servidor.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        server.server_close()
