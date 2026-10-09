#!/usr/bin/env python3
"""Serve static/en + static/ko: /en/... and /ko/....

Local verification harness only. Mirrors the production route so absolute
/<lang>/... hrefs in the generated index resolve exactly as they do on
the real host. Bare / serves the static/index.html locale landing (which
302-redirects by Accept-Language here, by navigator.language as a file).
Legacy /wiki/... addresses are still served from the same files.
"""

import http.server
import os
import socketserver
import sys
import urllib.parse

CWD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8900


class Handler(http.server.SimpleHTTPRequestHandler):
    def _preferred_lang(self):
        """ko* -> ko, everything else (incl. absent/unmatched) -> en."""
        raw = self.headers.get("Accept-Language", "") or ""
        prefs = []
        for part in raw.split(","):
            part = part.strip()
            if not part:
                continue
            tokens = part.split(";")
            code = tokens[0].strip().lower()
            q = 1.0
            for tok in tokens[1:]:
                tok = tok.strip().lower()
                if tok.startswith("q="):
                    try:
                        q = float(tok[2:])
                    except ValueError:
                        q = 0.0
            if q <= 0 or not code or code == "*":
                continue
            prefs.append((q, code))
        prefs.sort(key=lambda t: -t[0])
        for _q, code in prefs:
            if code.startswith("ko"):
                return "ko"
            if code.startswith("en"):
                return "en"
        # First-listed ko anywhere still wins over default (e.g. "fr, ko;q=0.8").
        if any(code.startswith("ko") for _q, code in prefs):
            return "ko"
        return "en"

    def _maybe_redirect_landing(self):
        """302 bare /, /wiki, /wiki/, /static, /static/ to the locale target."""
        clean = urllib.parse.unquote(self.path.split("?", 1)[0].split("#", 1)[0])
        parts = [p for p in clean.split("/") if p]
        if parts and parts not in (["wiki"], ["static"]):
            return False
        lang = self._preferred_lang()
        base = "/static/" if parts == ["static"] else "/"
        qs = self.path.split("?", 1)[1] if "?" in self.path else ""
        loc = f"{base}{lang}/" + (("?" + qs) if qs else "")
        body = f"Redirecting to {loc}\n".encode()
        self.send_response(302)
        self.send_header("Location", loc)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)
        return True

    def do_GET(self):
        if self._maybe_redirect_landing():
            return
        return super().do_GET()

    def do_HEAD(self):
        if self._maybe_redirect_landing():
            return
        return super().do_HEAD()

    def _out(self, lang, *rest):
        """Prefer static/<lang>/..., fall back to legacy public-<lang>/... ."""
        new = os.path.join(CWD, "static", lang, *rest)
        if os.path.exists(new) or not rest:
            return new
        old = os.path.join(CWD, "public-" + lang, *rest)
        if os.path.exists(old):
            return old
        return new

    def translate_path(self, path):
        # SimpleHTTPRequestHandler unquotes the path before calling us, so
        # filenames with non-ASCII characters arrive already decoded.
        clean = urllib.parse.unquote(path.split("?", 1)[0].split("#", 1)[0])
        parts = [p for p in clean.split("/") if p]

        def index_if_dir(rest):
            if not rest or rest[-1].endswith("/"):
                rest = rest + ["index.html"]
            return rest

        if parts[:1] == ["static"]:
            rest = index_if_dir(parts[1:])
            return os.path.join(CWD, "static", *rest)

        if parts[:1] == ["wiki"]:
            parts = parts[1:]
            if parts[:1] in (["en"], ["ko"]):
                lang = parts[0]
                rest = index_if_dir(parts[1:])
                return self._out(lang, *rest)
            # bare /wiki or /wiki/<page> -> language landing / extra static file
            rest = index_if_dir(parts)
            if not parts:
                return os.path.join(CWD, "static", "index.html")
            return os.path.join(CWD, "static", *rest)

        if parts and parts[0] in ("en", "ko"):
            rest = index_if_dir(parts[1:])
            return self._out(parts[0], *rest)

        if not parts:
            return os.path.join(CWD, "static", "index.html")

        return self._out("en", *parts)

    def log_message(self, format, *args):
        pass


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    with Server(("127.0.0.1", PORT), Handler) as httpd:
        print(f"serving landing + /en and /ko from static/ on http://127.0.0.1:{PORT}", flush=True)
        httpd.serve_forever()