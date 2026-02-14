"""Serve static files; show Safari/iOS notice for private Space on root request."""
import http.server
import re
import urllib.parse

SAFARI_IOS_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Open in another browser</title>
  <style>
    * { box-sizing: border-box; }
    body { font-family: system-ui, -apple-system, sans-serif; margin: 0; min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #f5f5f5; padding: 20px; }
    .card { background: #fff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,.08); max-width: 420px; padding: 32px; text-align: center; }
    h1 { margin: 0 0 16px; font-size: 1.25rem; color: #333; }
    p { margin: 0 0 20px; color: #666; line-height: 1.5; font-size: 15px; }
    a { color: #0d6efd; }
    .url { word-break: break-all; background: #f0f0f0; padding: 12px; border-radius: 8px; font-size: 13px; margin-bottom: 16px; text-align: left; }
    button { background: #0d6efd; color: #fff; border: none; padding: 12px 24px; border-radius: 8px; font-size: 15px; cursor: pointer; }
    button:hover { background: #0b5ed7; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Private Space &ndash; use another browser</h1>
    <p>Private Spaces may not work in Safari or on iOS. Open the link below in <strong>Chrome</strong> or <strong>Firefox</strong> (on Mac or Windows) to view this Space.</p>
    <p class="url" id="url"></p>
    <button type="button" onclick="navigator.clipboard.writeText(document.getElementById('url').textContent); this.textContent='Copied!';">Copy link</button>
  </div>
  <script>
    document.getElementById('url').textContent = window.location.href;
  </script>
</body>
</html>
"""

SAFARI_IOS_PATTERN = re.compile(
    r"(Safari|iPhone|iPad|iPod)(?!.*Chrome|.*CriOS|.*FxiOS)",
    re.IGNORECASE
)


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = urllib.parse.unquote(self.path)
        path = path.split("?")[0].lstrip("/") or "index.html"
        if path in ("", "index.html") and self.headers.get("User-Agent"):
            ua = self.headers.get("User-Agent", "")
            if SAFARI_IOS_PATTERN.search(ua):
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(SAFARI_IOS_PAGE.encode("utf-8"))
                return
        return super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    http.server.test(HandlerClass=Handler, port=7860, bind="0.0.0.0")
