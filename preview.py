#!/usr/bin/env python3
"""Serve both CVs with automatic browser refresh; no dependencies required."""

import argparse
import hashlib
import io
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import webbrowser

ROOT = Path(__file__).resolve().parent
VARIANTS = ("skills", "software-eng")
RELOAD_SCRIPT = b"""
<script>
(() => {
  let previous;
  async function check() {
    try {
      const response = await fetch('/__preview_version', {cache: 'no-store'});
      if (!response.ok) return;
      const current = await response.text();
      if (previous !== undefined && current !== previous) location.reload();
      previous = current;
    } catch (_) { /* Retry when the preview server becomes available. */ }
  }
  check();
  setInterval(check, 750);
})();
</script>
"""


def version():
    digest = hashlib.sha256()
    for directory in (*VARIANTS, "assets"):
        for path in sorted((ROOT / directory).rglob("*")):
            if path.is_file():
                stat = path.stat()
                digest.update(str((path.relative_to(ROOT), stat.st_mtime_ns, stat.st_size)).encode())
    return digest.hexdigest().encode()


class PreviewHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_head(self):
        route = urlsplit(self.path).path
        if route == "/__preview_version":
            content = version()
            content_type = "text/plain; charset=utf-8"
        elif route in ("/", "/index.html"):
            content = ('<!doctype html><meta charset="utf-8"><title>CV previews</title>'
                       '<h1>CV previews</h1>' + ''.join(
                           f'<p><a href="/{name}/Bill-Song-CV.html">{name}</a></p>'
                           for name in VARIANTS)).encode()
            content_type = "text/html; charset=utf-8"
        elif route in tuple(f"/{name}/Bill-Song-CV.html" for name in VARIANTS):
            content = (ROOT / route.lstrip("/")).read_bytes() + RELOAD_SCRIPT
            content_type = "text/html; charset=utf-8"
        else:
            return super().send_head()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        return io.BytesIO(content)

    def log_message(self, format, *args):
        if urlsplit(self.path).path != "/__preview_version":
            super().log_message(format, *args)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-open", action="store_true", help="Do not open browser tabs")
    args = parser.parse_args()
    handler = partial(PreviewHandler, directory=str(ROOT))
    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    except OSError as error:
        parser.exit(1, f"Could not start preview: {error}\n")
    with server:
        base = f"http://127.0.0.1:{server.server_port}"
        print(f"CV preview: {base}\nSave changes to refresh both CVs. Press Ctrl+C to stop.", flush=True)
        for name in VARIANTS:
            url = f"{base}/{name}/Bill-Song-CV.html"
            print(url, flush=True)
            if not args.no_open:
                webbrowser.open_new_tab(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
