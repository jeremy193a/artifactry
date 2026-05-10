#!/usr/bin/env python3
"""Audit fixed-canvas HTML slides for visual layout failures.

This catches problems that file validation cannot see: off-canvas elements,
clipped text boxes, and overlapping visible text blocks after the browser has
performed real layout.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import socket
import struct
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ASPECT_PIXELS = {
    "16:9": (1920, 1080),
    "4:5": (1638, 2048),
    "1:1": (1800, 1800),
    "9:16": (1080, 1920),
}


CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome",
    "chromium",
    "chromium-browser",
]


AUDIT_JS = r"""
(async () => {
  window.scrollTo(0, 0);
  if (document.fonts && document.fonts.ready) {
    try { await document.fonts.ready; } catch (error) {}
  }
  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));

  const viewport = { width: window.innerWidth, height: window.innerHeight };
  const failures = [];
  const warnings = [];
  const visible = [];
  const textCandidates = [];

  const clean = value => String(value || "").replace(/\s+/g, " ").trim();
  const rectOf = element => {
    const rect = element.getBoundingClientRect();
    return {
      left: rect.left,
      top: rect.top,
      right: rect.right,
      bottom: rect.bottom,
      width: rect.width,
      height: rect.height
    };
  };
  const selectorOf = element => {
    if (element.id) return `${element.tagName.toLowerCase()}#${element.id}`;
    const cls = Array.from(element.classList || []).slice(0, 3).join(".");
    return cls ? `${element.tagName.toLowerCase()}.${cls}` : element.tagName.toLowerCase();
  };
  const area = rect => Math.max(0, rect.width) * Math.max(0, rect.height);
  const intersection = (a, b) => {
    const left = Math.max(a.left, b.left);
    const top = Math.max(a.top, b.top);
    const right = Math.min(a.right, b.right);
    const bottom = Math.min(a.bottom, b.bottom);
    return {
      left,
      top,
      right,
      bottom,
      width: Math.max(0, right - left),
      height: Math.max(0, bottom - top)
    };
  };
  const hasOwnText = element => {
    for (const node of element.childNodes) {
      if (node.nodeType === Node.TEXT_NODE && clean(node.textContent).length > 0) return true;
    }
    return false;
  };
  const isLeafText = element => {
    if (!clean(element.innerText)) return false;
    if (hasOwnText(element)) return true;
    return !Array.from(element.children).some(child => clean(child.innerText).length > 0);
  };
  const isMeaningfulText = element => {
    const text = clean(element.innerText);
    if (text.length < 2) return false;
    const tag = element.tagName.toLowerCase();
    const roleTags = new Set(["h1", "h2", "h3", "p", "li", "span", "strong", "b", "em", "small"]);
    return roleTags.has(tag) || isLeafText(element);
  };

  for (const element of Array.from(document.body.querySelectorAll("*"))) {
    const style = getComputedStyle(element);
    if (
      style.display === "none" ||
      style.visibility === "hidden" ||
      Number(style.opacity) === 0 ||
      element.tagName === "SCRIPT" ||
      element.tagName === "STYLE"
    ) {
      continue;
    }

    const rect = rectOf(element);
    if (rect.width <= 1 || rect.height <= 1) continue;
    const item = {
      selector: selectorOf(element),
      text: clean(element.innerText).slice(0, 120),
      rect
    };
    visible.push(item);

    const isCanvas = element.classList && element.classList.contains("slide");
    if (rect.left < -1 || rect.top < -1 || rect.right > viewport.width + 1 || rect.bottom > viewport.height + 1) {
      if (!isCanvas) {
        failures.push({
          type: "off_canvas",
          selector: item.selector,
          text: item.text,
          rect
        });
      }
    }

    if (
      clean(element.innerText) &&
      (element.scrollWidth > element.clientWidth + 2 || element.scrollHeight > element.clientHeight + 2) &&
      getComputedStyle(element).overflow !== "visible"
    ) {
      failures.push({
        type: "clipped_text_box",
        selector: item.selector,
        text: item.text,
        client: { width: element.clientWidth, height: element.clientHeight },
        scroll: { width: element.scrollWidth, height: element.scrollHeight }
      });
    }

    if (isMeaningfulText(element)) {
      textCandidates.push({ element, selector: item.selector, text: item.text, rect });
    }
  }

  for (let i = 0; i < textCandidates.length; i++) {
    for (let j = i + 1; j < textCandidates.length; j++) {
      const a = textCandidates[i];
      const b = textCandidates[j];
      if (a.element.contains(b.element) || b.element.contains(a.element)) continue;
      const hit = intersection(a.rect, b.rect);
      const hitArea = area(hit);
      if (hitArea <= 16) continue;
      const ratio = hitArea / Math.min(area(a.rect), area(b.rect));
      if (ratio > 0.02 && hit.width > 8 && hit.height > 8) {
        failures.push({
          type: "text_overlap",
          a: { selector: a.selector, text: a.text, rect: a.rect },
          b: { selector: b.selector, text: b.text, rect: b.rect },
          overlap: hit,
          overlap_ratio: ratio
        });
      }
    }
  }

  if (textCandidates.length > 0) {
    const maxBottom = Math.max(...textCandidates.map(item => item.rect.bottom));
    if (maxBottom > viewport.height - 24) {
      warnings.push({
        type: "text_near_bottom_edge",
        bottom: maxBottom,
        viewport_height: viewport.height
      });
    }
  }

  return {
    ok: failures.length === 0,
    viewport,
    visible_count: visible.length,
    text_count: textCandidates.length,
    failures,
    warnings
  };
})()
"""


class WebSocket:
    def __init__(self, url: str):
        if not url.startswith("ws://"):
            raise ValueError(f"Only ws:// URLs are supported: {url}")
        without_scheme = url[5:]
        host_port, path = without_scheme.split("/", 1)
        if ":" in host_port:
            host, raw_port = host_port.rsplit(":", 1)
            port = int(raw_port)
        else:
            host, port = host_port, 80
        self.sock = socket.create_connection((host, port), timeout=10)
        self.sock.settimeout(20)
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        request = (
            f"GET /{path} HTTP/1.1\r\n"
            f"Host: {host_port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(request.encode("ascii"))
        response = self.sock.recv(4096)
        if b" 101 " not in response.split(b"\r\n", 1)[0]:
            raise RuntimeError(f"WebSocket upgrade failed: {response[:200]!r}")

    def close(self) -> None:
        try:
            self.sock.close()
        except OSError:
            pass

    def send_json(self, payload: dict) -> None:
        data = json.dumps(payload).encode("utf-8")
        header = bytearray([0x81])
        length = len(data)
        if length < 126:
            header.append(0x80 | length)
        elif length < 65536:
            header.append(0x80 | 126)
            header.extend(struct.pack("!H", length))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack("!Q", length))
        mask = os.urandom(4)
        header.extend(mask)
        masked = bytes(byte ^ mask[idx % 4] for idx, byte in enumerate(data))
        self.sock.sendall(header + masked)

    def recv_json(self) -> dict:
        while True:
            first = self.sock.recv(2)
            if len(first) < 2:
                raise RuntimeError("WebSocket closed")
            opcode = first[0] & 0x0F
            length = first[1] & 0x7F
            if length == 126:
                length = struct.unpack("!H", self._recv_exact(2))[0]
            elif length == 127:
                length = struct.unpack("!Q", self._recv_exact(8))[0]
            masked = bool(first[1] & 0x80)
            mask = self._recv_exact(4) if masked else b""
            data = self._recv_exact(length)
            if masked:
                data = bytes(byte ^ mask[idx % 4] for idx, byte in enumerate(data))
            if opcode == 8:
                raise RuntimeError("WebSocket closed by peer")
            if opcode == 9:
                continue
            if opcode == 1:
                return json.loads(data.decode("utf-8"))

    def _recv_exact(self, length: int) -> bytes:
        chunks = bytearray()
        while len(chunks) < length:
            chunk = self.sock.recv(length - len(chunks))
            if not chunk:
                raise RuntimeError("Socket closed")
            chunks.extend(chunk)
        return bytes(chunks)


def find_chrome(explicit: str | None) -> str:
    if explicit:
        return explicit
    for candidate in CHROME_CANDIDATES:
        path = Path(candidate)
        if candidate.startswith("/") and path.exists():
            return candidate
        if not candidate.startswith("/"):
            return candidate
    raise SystemExit("Chrome/Chromium not found. Pass --chrome /path/to/chrome.")


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def http_json(url: str, timeout: float = 10) -> list[dict] | dict:
    deadline = time.time() + timeout
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last_error = exc
            time.sleep(0.1)
    raise RuntimeError(f"Timed out waiting for {url}: {last_error}")


def start_chrome(chrome: str, width: int, height: int, port: int, user_data_dir: Path) -> subprocess.Popen:
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-first-run",
        "--no-default-browser-check",
        f"--user-data-dir={user_data_dir}",
        f"--remote-debugging-port={port}",
        f"--window-size={width},{height + 120}",
        "about:blank",
    ]
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def connect_to_page(port: int, html_file: Path) -> WebSocket:
    encoded = urllib.parse.quote(html_file.resolve().as_uri(), safe="")
    try:
        http_json(f"http://127.0.0.1:{port}/json/new?{encoded}", timeout=3)
    except RuntimeError:
        # Some Chrome versions reject /json/new via GET. about:blank still exists;
        # navigating through CDP below is enough.
        pass
    pages = http_json(f"http://127.0.0.1:{port}/json/list", timeout=10)
    if not isinstance(pages, list) or not pages:
        raise RuntimeError("No Chrome pages available for audit")
    page = next((item for item in pages if item.get("type") == "page"), pages[0])
    ws_url = page["webSocketDebuggerUrl"]
    ws = WebSocket(ws_url)
    send_cdp(ws, "Page.enable")
    send_cdp(ws, "Runtime.enable")
    send_cdp(ws, "Page.navigate", {"url": html_file.resolve().as_uri()})
    time.sleep(0.25)
    return ws


_MESSAGE_ID = 0


def send_cdp(ws: WebSocket, method: str, params: dict | None = None) -> dict:
    global _MESSAGE_ID
    _MESSAGE_ID += 1
    message_id = _MESSAGE_ID
    ws.send_json({"id": message_id, "method": method, "params": params or {}})
    while True:
        response = ws.recv_json()
        if response.get("id") == message_id:
            if "error" in response:
                raise RuntimeError(f"CDP error for {method}: {response['error']}")
            return response


def audit_slide(port: int, html_file: Path) -> dict:
    ws = connect_to_page(port, html_file)
    try:
        response = send_cdp(
            ws,
            "Runtime.evaluate",
            {
                "expression": AUDIT_JS,
                "awaitPromise": True,
                "returnByValue": True,
            },
        )
        result = response["result"]["result"]
        if result.get("subtype") == "error":
            raise RuntimeError(result.get("description", "visual audit script failed"))
        return result["value"]
    finally:
        ws.close()


def summarize_failure(failure: dict) -> str:
    kind = failure.get("type", "unknown")
    if kind == "text_overlap":
        a = failure.get("a", {})
        b = failure.get("b", {})
        return f"text_overlap: {a.get('selector')} '{a.get('text')}' overlaps {b.get('selector')} '{b.get('text')}'"
    selector = failure.get("selector", "?")
    text = failure.get("text", "")
    return f"{kind}: {selector} '{text}'"


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit rendered HTML slides for visual layout failures.")
    parser.add_argument("slides_dir", help="Directory containing slide-*.html files.")
    parser.add_argument("--aspect", default="16:9", choices=ASPECT_PIXELS.keys())
    parser.add_argument("--chrome", help="Path to Chrome/Chromium binary.")
    parser.add_argument("--json", action="store_true", help="Print JSON report.")
    args = parser.parse_args()

    slides = sorted(Path(args.slides_dir).glob("slide-*.html"))
    if not slides:
        raise SystemExit(f"No slide-*.html files found in {args.slides_dir}")

    width, height = ASPECT_PIXELS[args.aspect]
    chrome = find_chrome(args.chrome)
    port = free_port()
    report = {"ok": True, "slides": []}

    with tempfile.TemporaryDirectory(prefix="artifactry-chrome-") as raw_user_dir:
        process = start_chrome(chrome, width, height, port, Path(raw_user_dir))
        try:
            http_json(f"http://127.0.0.1:{port}/json/version", timeout=10)
            for slide in slides:
                result = audit_slide(port, slide)
                slide_report = {
                    "path": str(slide),
                    "ok": bool(result.get("ok")),
                    "failures": result.get("failures", []),
                    "warnings": result.get("warnings", []),
                    "viewport": result.get("viewport", {}),
                    "visible_count": result.get("visible_count", 0),
                    "text_count": result.get("text_count", 0),
                }
                if not slide_report["ok"]:
                    report["ok"] = False
                report["slides"].append(slide_report)
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for slide in report["slides"]:
            if slide["ok"]:
                print(f"OK   {slide['path']}")
            else:
                print(f"FAIL {slide['path']}")
                for failure in slide["failures"]:
                    print(f"  - {summarize_failure(failure)}")
            for warning in slide["warnings"]:
                print(f"  ! {warning.get('type')}: {warning}")

    if not report["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
