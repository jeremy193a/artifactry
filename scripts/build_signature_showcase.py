#!/usr/bin/env python3
"""Build high-variation signature showcase previews for the 15 Markdown style guides."""

from __future__ import annotations

import argparse
import html
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "artifactry"
BUILD_DIR = ROOT / "build" / "showcase" / "signature"
ASSET_DIR = ROOT / "assets" / "showcase" / "signature"

ASPECT = "4:5"


STYLES = [
    {
        "id": "regulated-ledger",
        "name": "Regulated Ledger",
        "layout": "ledger",
        "kicker": "Executive export system",
        "title": "Markdown becomes a board-ready artifact.",
        "subtitle": "A trust-first workflow for DOCX, PDF, PPTX, and image exports.",
        "meta": ["DOCX", "PPTX", "PDF", "PNG"],
    },
    {
        "id": "human-workshop",
        "name": "Human Workshop",
        "layout": "workshop",
        "kicker": "Training and enablement",
        "title": "A skill that teaches agents to ask before they render.",
        "subtitle": "Choose output, style, size, then build a file people can use.",
        "meta": ["Brief", "Practice", "Export", "Review"],
    },
    {
        "id": "swiss-protocol",
        "name": "Swiss Protocol",
        "layout": "swiss",
        "kicker": "Technical memo",
        "title": "One source. Exact structure. No ornament.",
        "subtitle": "A hard-grid system for specs, founder briefs, and internal protocols.",
        "meta": ["01 Source", "02 Route", "03 Render", "04 Validate"],
    },
    {
        "id": "terminal-operator",
        "name": "Terminal Operator",
        "layout": "terminal",
        "kicker": "Agent command surface",
        "title": "Run the export loop like an operator.",
        "subtitle": "diagnose -> ask -> route -> render -> validate -> deliver",
        "meta": ["preflight ok", "style loaded", "png rendered", "pptx built"],
    },
    {
        "id": "aurora-product",
        "name": "Aurora Product",
        "layout": "aurora",
        "kicker": "AI product launch",
        "title": "A luminous artifact pipeline for modern product stories.",
        "subtitle": "Style guides become deterministic layouts, not generic theme swaps.",
        "meta": ["Style brain", "Fixed canvas", "High-res output", "Validated"],
    },
    {
        "id": "metrics-command",
        "name": "Metrics Command",
        "layout": "metrics",
        "kicker": "Operating review",
        "title": "Every export route should have a measurable output.",
        "subtitle": "Track formats, dimensions, slide count, validation, and readiness.",
        "meta": ["15 styles", "4 ratios", "5 formats", "1 source"],
    },
    {
        "id": "broadsheet-intelligence",
        "name": "Broadsheet Intelligence",
        "layout": "broadsheet",
        "kicker": "Research carousel",
        "title": "The real product is not conversion. It is editorial judgment.",
        "subtitle": "Agents read style direction, pick page roles, and preserve the argument.",
        "meta": ["Analysis", "Sources", "Captions", "Footnotes"],
    },
    {
        "id": "black-label-cinema",
        "name": "Black Label Cinema",
        "layout": "cinema",
        "kicker": "Premium pitch frame",
        "title": "Make the output feel expensive by subtracting.",
        "subtitle": "Dark hero pacing for high-stakes presentations and portfolio stories.",
        "meta": ["Frame 01", "Artifactry", "signature deck", "4:5"],
    },
    {
        "id": "playful-systems",
        "name": "Playful Systems",
        "layout": "playful",
        "kicker": "Workflow onboarding",
        "title": "Turn the messy export process into a friendly system.",
        "subtitle": "Cards, lanes, labels, and color-coded steps make AI work visible.",
        "meta": ["Ask", "Plan", "Build", "Share"],
    },
    {
        "id": "image-market",
        "name": "Image Market",
        "layout": "market",
        "kicker": "Social product story",
        "title": "Show the artifact, then explain why it matters.",
        "subtitle": "Photo-led pacing, caption bands, and product-story rhythm.",
        "meta": ["Carousel", "Launch", "Catalog", "Campaign"],
    },
    {
        "id": "spatial-canvas",
        "name": "Spatial Canvas",
        "layout": "spatial",
        "kicker": "Workshop map",
        "title": "A board for turning loose ideas into export-ready structure.",
        "subtitle": "Clusters, connectors, lanes, and sticky logic for planning artifacts.",
        "meta": ["Input", "Cluster", "Route", "Output"],
    },
    {
        "id": "blueprint-infra",
        "name": "Blueprint Infra",
        "layout": "blueprint",
        "kicker": "Architecture export",
        "title": "Make the invisible system legible.",
        "subtitle": "Use diagrams, contracts, endpoints, and dependency maps for technical artifacts.",
        "meta": ["agent", "renderer", "validator", "artifact"],
    },
    {
        "id": "commerce-editorial",
        "name": "Commerce Editorial",
        "layout": "commerce",
        "kicker": "Product offer sheet",
        "title": "A useful artifact should make the offer inspectable.",
        "subtitle": "Hero product, benefit tiles, proof rows, and a direct next action.",
        "meta": ["Guide", "Deck", "Images", "Docs"],
    },
    {
        "id": "motion-premiere",
        "name": "Motion Premiere",
        "layout": "motion",
        "kicker": "Creative launch sequence",
        "title": "Every slide is a beat in the trailer.",
        "subtitle": "Establish, reveal, prove, escalate, resolve.",
        "meta": ["00:01", "00:12", "00:24", "00:35"],
    },
    {
        "id": "performance-machine",
        "name": "Performance Machine",
        "layout": "performance",
        "kicker": "Spec-sheet drama",
        "title": "Performance is precision under pressure.",
        "subtitle": "Velocity bands, spec rails, and hard contrast for high-stakes demos.",
        "meta": ["16:9", "4:5", "PPTX", "PNG"],
    },
]


BASE_CSS = """
* { box-sizing: border-box; }
html, body { margin: 0; width: 1638px; height: 2048px; overflow: hidden; }
body { font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
.slide { position: relative; width: 1638px; height: 2048px; overflow: hidden; background: var(--bg); color: var(--ink); }
.pad { position: absolute; inset: 118px 124px; }
.topline { display: flex; align-items: center; justify-content: space-between; font-size: 24px; font-weight: 750; color: var(--muted); }
.brand { display: flex; align-items: center; gap: 16px; }
.mark { width: 18px; height: 18px; border-radius: 99px; background: var(--accent); display: inline-block; }
.title { margin: 0; font-size: var(--title, 96px); line-height: .96; letter-spacing: -1px; font-weight: var(--weight, 520); max-width: var(--titlew, 1120px); }
.subtitle { margin: 28px 0 0; max-width: 960px; color: var(--body); font-size: 38px; line-height: 1.22; }
.footer { position: absolute; left: 124px; right: 124px; bottom: 92px; display: flex; justify-content: space-between; color: var(--muted); font-size: 24px; font-weight: 700; }
.mono { font-family: "JetBrains Mono", "SFMono-Regular", Consolas, monospace; }
.rule { height: 1px; background: var(--line); }
.pill { display: inline-flex; align-items: center; justify-content: center; min-height: 58px; padding: 0 26px; border-radius: 999px; background: var(--pill); color: var(--pill-ink); font-size: 24px; font-weight: 800; }
.card { border: 1px solid var(--line); background: var(--card); border-radius: var(--radius, 28px); padding: 34px; }

.ledger { --bg: #fbfcfe; --ink: #0a0b0d; --body: #596273; --muted: #7c8490; --line: #dce2ea; --accent: #0052ff; --card: #fff; --pill: #edf3ff; --pill-ink: #0052ff; --radius: 34px; }
.ledger .hero { position: absolute; left: 124px; right: 124px; top: 600px; }
.ledger .metric-grid { position: absolute; left: 124px; right: 124px; bottom: 260px; display: grid; grid-template-columns: 1.2fr .8fr; gap: 28px; }
.ledger .number { font-size: 132px; line-height: .9; color: var(--accent); font-weight: 500; }
.ledger .rows { display: grid; gap: 0; overflow: hidden; padding: 0; }
.ledger .row { display: grid; grid-template-columns: 100px 1fr 130px; gap: 22px; padding: 31px 34px; border-bottom: 1px solid var(--line); font-size: 29px; align-items: center; }
.ledger .row:last-child { border-bottom: 0; }

.workshop { --bg: #f5efe6; --ink: #221c16; --body: #665b50; --muted: #8a7d70; --line: #ded1c0; --accent: #c95f35; --card: #fffaf2; --pill: #e8f1dc; --pill-ink: #38543a; --radius: 30px; }
.workshop .hero { position: absolute; left: 124px; top: 440px; }
.workshop .worksheet { position: absolute; left: 124px; right: 124px; bottom: 250px; display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }
.workshop .note { min-height: 280px; border-style: dashed; }
.workshop .question { font-size: 34px; font-weight: 760; }
.workshop .field { margin-top: 42px; border-bottom: 2px solid #cbbba6; height: 54px; }

.swiss { --bg: #ffffff; --ink: #050505; --body: #333333; --muted: #737373; --line: #111111; --accent: #111111; --card: #ffffff; --pill: #111111; --pill-ink: #ffffff; --radius: 0px; --title: 108px; --weight: 430; }
.swiss .hero { position: absolute; left: 124px; right: 124px; top: 410px; border-top: 3px solid #000; padding-top: 58px; }
.swiss .protocol { position: absolute; left: 124px; right: 124px; bottom: 260px; display: grid; grid-template-columns: repeat(4, 1fr); border-top: 2px solid #000; border-left: 2px solid #000; }
.swiss .cell { min-height: 260px; padding: 28px; border-right: 2px solid #000; border-bottom: 2px solid #000; font-size: 31px; font-weight: 700; }

.terminal { --bg: #050507; --ink: #f2f2f2; --body: #b8b3b0; --muted: #77716d; --line: #2a2a2d; --accent: #00d992; --card: #101013; --pill: rgba(0,217,146,.15); --pill-ink: #00d992; --radius: 18px; --title: 82px; --weight: 650; }
.terminal .console { position: absolute; left: 124px; right: 124px; top: 430px; bottom: 250px; display: grid; grid-template-rows: auto 1fr; border: 1px solid #2f3136; border-radius: 24px; background: #0c0c0f; overflow: hidden; box-shadow: 0 40px 120px rgba(0,0,0,.45); }
.terminal .bar { height: 78px; display: flex; align-items: center; gap: 14px; padding: 0 28px; border-bottom: 1px solid #2f3136; }
.terminal .dot { width: 16px; height: 16px; border-radius: 50%; background: #3d3a39; }
.terminal .term-body { padding: 58px; font-size: 35px; line-height: 1.55; }
.terminal .prompt { color: var(--accent); }

.aurora { --bg: radial-gradient(circle at 12% 18%, rgba(124,58,237,.28), transparent 31%), radial-gradient(circle at 84% 6%, rgba(14,165,233,.22), transparent 30%), #ffffff; --ink: #0d1324; --body: #59647a; --muted: #95a1b5; --line: rgba(124,58,237,.20); --accent: #7c3aed; --card: rgba(255,255,255,.72); --pill: #f4edff; --pill-ink: #7c3aed; --radius: 42px; --weight: 310; }
.aurora .hero { position: absolute; left: 124px; top: 430px; }
.aurora .glass { position: absolute; right: 124px; bottom: 250px; width: 760px; height: 740px; border-radius: 54px; background: rgba(255,255,255,.7); border: 1px solid rgba(124,58,237,.18); box-shadow: 0 40px 140px rgba(88,28,135,.18); padding: 48px; }
.aurora .orb { position: absolute; width: 360px; height: 360px; border-radius: 50%; background: linear-gradient(135deg,#7c3aed,#06b6d4); filter: blur(8px); opacity: .28; right: 340px; top: 360px; }

.metrics { --bg: #0b0f14; --ink: #f8fafc; --body: #a5b0bd; --muted: #768393; --line: #23303b; --accent: #faff69; --card: #111821; --pill: rgba(250,255,105,.12); --pill-ink: #faff69; --radius: 20px; --title: 76px; --weight: 680; }
.metrics .hero { position: absolute; left: 124px; right: 124px; top: 360px; }
.metrics .dash { position: absolute; left: 124px; right: 124px; bottom: 230px; display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }
.metrics .metric { min-height: 245px; }
.metrics .metric strong { display: block; color: var(--accent); font-size: 74px; font-family: "JetBrains Mono", monospace; font-weight: 500; }
.metrics .metric span { color: var(--body); font-size: 28px; }

.broadsheet { --bg: #f7f4ef; --ink: #111111; --body: #37322d; --muted: #746d64; --line: #161616; --accent: #057dbc; --card: #fffdf8; --pill: #111; --pill-ink: #fff; --radius: 0px; --title: 88px; --weight: 520; font-family: Georgia, "Times New Roman", serif; }
.broadsheet .hero { position: absolute; left: 124px; right: 124px; top: 330px; border-top: 5px solid #111; border-bottom: 1px solid #111; padding: 42px 0 46px; }
.broadsheet .columns { position: absolute; left: 124px; right: 124px; bottom: 250px; display: grid; grid-template-columns: 1.4fr 1fr 1fr; gap: 30px; }
.broadsheet .column { border-top: 1px solid #111; padding-top: 22px; font-size: 30px; line-height: 1.28; }
.broadsheet .drop { font-size: 112px; line-height: .8; float: left; margin-right: 14px; }

.cinema { --bg: #050505; --ink: #f8f7f2; --body: #b8b1a6; --muted: #777067; --line: #242424; --accent: #d7b46a; --card: #101010; --pill: rgba(215,180,106,.15); --pill-ink: #d7b46a; --radius: 4px; --title: 108px; --weight: 390; }
.cinema .frame { position: absolute; inset: 96px; border: 1px solid #252525; }
.cinema .hero { position: absolute; left: 124px; right: 260px; bottom: 360px; }
.cinema .light { position: absolute; right: -120px; top: 160px; width: 760px; height: 1060px; background: radial-gradient(circle, rgba(215,180,106,.18), transparent 62%); }
.cinema .spec { position: absolute; right: 124px; bottom: 250px; writing-mode: vertical-rl; letter-spacing: 6px; color: var(--accent); font-size: 22px; }

.playful { --bg: #fffaf5; --ink: #201515; --body: #5f574f; --muted: #8c8379; --line: #e6ded4; --accent: #ff4f00; --card: #ffffff; --pill: #fff0e8; --pill-ink: #ff4f00; --radius: 38px; --weight: 720; }
.playful .hero { position: absolute; left: 124px; top: 330px; }
.playful .board { position: absolute; left: 124px; right: 124px; bottom: 225px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 22px; }
.playful .lane { min-height: 560px; padding: 24px; border-radius: 34px; background: #fff; border: 1px solid #eadfd5; }
.playful .sticky { margin-top: 22px; padding: 22px; border-radius: 24px; min-height: 140px; font-size: 28px; font-weight: 760; }

.market { --bg: #f5f5f3; --ink: #171717; --body: #555; --muted: #777; --line: #e1e1dd; --accent: #cc001f; --card: #fff; --pill: #ffe8ec; --pill-ink: #cc001f; --radius: 34px; --title: 84px; --weight: 760; }
.market .photo { position: absolute; left: 124px; right: 124px; top: 250px; height: 760px; border-radius: 54px; background: linear-gradient(135deg,#111 0%,#444 32%,#e8ded1 32%,#f4b4aa 64%,#cc001f 64%,#851124 100%); overflow: hidden; }
.market .hero { position: absolute; left: 124px; right: 124px; bottom: 360px; }
.market .caption { position: absolute; left: 164px; bottom: 60px; right: 164px; background: rgba(255,255,255,.88); border-radius: 30px; padding: 28px 34px; font-size: 30px; font-weight: 750; }

.spatial { --bg: #fbfaf4; --ink: #1c1c1e; --body: #5d5c57; --muted: #89877f; --line: #d8d5cb; --accent: #ffd02f; --card: #fff; --pill: #fff4b8; --pill-ink: #4a3a00; --radius: 28px; --title: 78px; --weight: 720; }
.spatial .hero { position: absolute; left: 124px; top: 260px; width: 900px; }
.spatial .canvas { position: absolute; left: 124px; right: 124px; bottom: 220px; height: 1000px; background-image: linear-gradient(#ece8dc 1px, transparent 1px), linear-gradient(90deg,#ece8dc 1px, transparent 1px); background-size: 64px 64px; border: 1px solid #ded9ca; border-radius: 36px; }
.spatial .sticky { position: absolute; width: 310px; min-height: 190px; border-radius: 24px; padding: 24px; font-size: 28px; font-weight: 760; box-shadow: 0 18px 50px rgba(0,0,0,.08); }
.spatial .connector { position: absolute; height: 4px; background: #222; transform-origin: left center; opacity: .5; }

.blueprint { --bg: #061728; --ink: #e8f4ff; --body: #a9c2d8; --muted: #6f8ca5; --line: rgba(116,196,255,.22); --accent: #30b8ff; --card: rgba(7,28,48,.9); --pill: rgba(48,184,255,.14); --pill-ink: #8cdcff; --radius: 10px; --title: 78px; --weight: 650; }
.blueprint .slide { background-image: linear-gradient(var(--line) 1px, transparent 1px), linear-gradient(90deg,var(--line) 1px, transparent 1px); background-size: 64px 64px; }
.blueprint .hero { position: absolute; left: 124px; top: 330px; width: 900px; }
.blueprint .diagram { position: absolute; left: 124px; right: 124px; bottom: 260px; height: 720px; }
.blueprint .node { position: absolute; width: 330px; height: 150px; border: 1px solid #2b86c4; background: rgba(7,28,48,.92); border-radius: 10px; padding: 28px; font-size: 28px; font-weight: 760; }
.blueprint .wire { position: absolute; height: 3px; background: #30b8ff; opacity: .72; }

.commerce { --bg: #f4efe8; --ink: #141413; --body: #5f554d; --muted: #85796e; --line: #e2d5c8; --accent: #cf4500; --card: #fffaf4; --pill: #ffe4d2; --pill-ink: #cf4500; --radius: 40px; --title: 84px; --weight: 680; }
.commerce .product { position: absolute; right: 124px; top: 250px; width: 620px; height: 780px; border-radius: 52px; background: radial-gradient(circle at 50% 35%,#ffffff 0 18%,#f37338 19% 45%,#141413 46% 100%); box-shadow: 0 42px 100px rgba(80,40,10,.2); }
.commerce .hero { position: absolute; left: 124px; top: 420px; width: 810px; }
.commerce .tiles { position: absolute; left: 124px; right: 124px; bottom: 260px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.commerce .tile { min-height: 230px; font-size: 30px; font-weight: 760; }

.motion { --bg: #0a0a0a; --ink: #ffffff; --body: #b7b7b7; --muted: #767d88; --line: #27272a; --accent: #f36458; --card: #151515; --pill: rgba(243,100,88,.12); --pill-ink: #ff8a80; --radius: 8px; --title: 94px; --weight: 430; }
.motion .letterbox { position: absolute; left: 0; right: 0; height: 220px; background: #000; z-index: 0; }
.motion .letterbox.top { top: 0; }
.motion .letterbox.bottom { bottom: 0; }
.motion .hero { position: absolute; left: 124px; right: 124px; top: 500px; }
.motion .timeline { position: absolute; left: 124px; right: 124px; bottom: 300px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px; }
.motion .framecell { height: 210px; border: 1px solid #333; background: linear-gradient(145deg,#151515,#242424); padding: 22px; font-family: "JetBrains Mono", monospace; color: var(--accent); }

.performance { --bg: #070707; --ink: #ffffff; --body: #c6c6c6; --muted: #777; --line: #303030; --accent: #da291c; --card: #121212; --pill: rgba(218,41,28,.13); --pill-ink: #ff5b4f; --radius: 0px; --title: 96px; --weight: 760; }
.performance .slash { position: absolute; right: -160px; top: -100px; width: 680px; height: 2300px; background: linear-gradient(90deg, transparent, rgba(218,41,28,.26), transparent); transform: rotate(18deg); }
.performance .hero { position: absolute; left: 124px; top: 400px; right: 260px; }
.performance .specrail { position: absolute; left: 124px; right: 124px; bottom: 260px; display: grid; grid-template-columns: repeat(4, 1fr); border-top: 2px solid #fff; border-bottom: 2px solid #fff; }
.performance .spec { min-height: 220px; padding: 28px; border-right: 1px solid #333; }
.performance .spec strong { display: block; font-size: 56px; color: var(--accent); font-family: "JetBrains Mono", monospace; }
"""


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def tags(items: list[str]) -> str:
    return "".join(f"<span class='pill'>{esc(item)}</span>" for item in items)


def render(style: dict[str, object]) -> str:
    sid = str(style["id"])
    layout = str(style["layout"])
    name = str(style["name"])
    kicker = str(style["kicker"])
    title = str(style["title"])
    subtitle = str(style["subtitle"])
    meta = list(style["meta"])

    body = {
        "ledger": f"""
          <div class="hero"><h1 class="title">{esc(title)}</h1><p class="subtitle">{esc(subtitle)}</p></div>
          <div class="metric-grid">
            <div class="card"><div class="number mono">15</div><p class="subtitle">public style guides synthesized into agent-ready direction.</p></div>
            <div class="card rows">
              <div class="row"><span class="mono">01</span><b>Brief</b><span>ASK</span></div>
              <div class="row"><span class="mono">02</span><b>Render</b><span>BUILD</span></div>
              <div class="row"><span class="mono">03</span><b>Validate</b><span>SHIP</span></div>
            </div>
          </div>
        """,
        "workshop": f"""
          <div class="hero"><h1 class="title">{esc(title)}</h1><p class="subtitle">{esc(subtitle)}</p></div>
          <div class="worksheet">
            <div class="card note"><p class="question">What output do we need?</p><div class="field"></div><div class="field"></div></div>
            <div class="card note"><p class="question">Which style and ratio fit the audience?</p><div class="field"></div><div class="field"></div></div>
          </div>
        """,
        "swiss": f"""
          <div class="hero"><h1 class="title">{esc(title)}</h1><p class="subtitle">{esc(subtitle)}</p></div>
          <div class="protocol">{''.join(f"<div class='cell mono'>{esc(x)}</div>" for x in meta)}</div>
        """,
        "terminal": f"""
          <div class="console">
            <div class="bar"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="mono">artifactry.session</span></div>
            <div class="term-body mono">
              <div><span class="prompt">$</span> artifactry preflight</div>
              <div>ok: requirements detected</div>
              <div><span class="prompt">$</span> load-style terminal-operator</div>
              <div>ok: command surface active</div>
              <br>
              <h1 class="title">{esc(title)}</h1>
              <p class="subtitle">{esc(subtitle)}</p>
            </div>
          </div>
        """,
        "aurora": f"""
          <div class="orb"></div>
          <div class="hero"><h1 class="title">{esc(title)}</h1><p class="subtitle">{esc(subtitle)}</p></div>
          <div class="glass"><div class="topline"><span>STYLE BRAIN</span><span>READY</span></div><div style="margin-top:90px;display:grid;gap:24px">{tags(meta)}</div></div>
        """,
        "metrics": f"""
          <div class="hero"><h1 class="title">{esc(title)}</h1><p class="subtitle">{esc(subtitle)}</p></div>
          <div class="dash">{''.join(f"<div class='card metric'><strong>{esc(item.split()[0])}</strong><span>{esc(' '.join(item.split()[1:]) or item)}</span></div>" for item in meta)}</div>
        """,
        "broadsheet": f"""
          <div class="hero"><h1 class="title">{esc(title)}</h1><p class="subtitle">{esc(subtitle)}</p></div>
          <div class="columns">
            <div class="column"><span class="drop">A</span>rtifactry uses style direction as editorial judgment, not decoration.</div>
            <div class="column">Page roles force the agent to choose evidence, hierarchy, and rhythm before rendering.</div>
            <div class="column mono">SOURCE: local DESIGN.md corpus<br>OUTPUT: deterministic files</div>
          </div>
        """,
        "cinema": f"""
          <div class="frame"></div><div class="light"></div><div class="spec mono">BLACK LABEL / SIGNATURE FRAME</div>
          <div class="hero"><h1 class="title">{esc(title)}</h1><p class="subtitle">{esc(subtitle)}</p></div>
        """,
        "playful": f"""
          <div class="hero"><h1 class="title">{esc(title)}</h1><p class="subtitle">{esc(subtitle)}</p></div>
          <div class="board">{''.join(f"<div class='lane'><span class='pill'>{esc(item)}</span><div class='sticky' style='background:{color}'>{esc(item)} the artifact</div></div>" for item,color in zip(meta, ['#ffe5d5','#e7f7dc','#dfeaff','#f4e3ff']))}</div>
        """,
        "market": f"""
          <div class="photo"><div class="caption">Artifactry packages polished documents, decks, images, and PDFs from one Markdown source.</div></div>
          <div class="hero"><h1 class="title">{esc(title)}</h1><p class="subtitle">{esc(subtitle)}</p></div>
        """,
        "spatial": f"""
          <div class="hero"><h1 class="title">{esc(title)}</h1><p class="subtitle">{esc(subtitle)}</p></div>
          <div class="canvas">
            <div class="sticky" style="left:80px;top:110px;background:#fff2a8">Markdown source</div>
            <div class="sticky" style="left:500px;top:330px;background:#d9f7ff">Style guide</div>
            <div class="sticky" style="left:900px;top:160px;background:#e7ffd8">Render route</div>
            <div class="sticky" style="left:760px;top:650px;background:#ffd9ec">Validated output</div>
            <div class="connector" style="left:370px;top:245px;width:240px;transform:rotate(26deg)"></div>
            <div class="connector" style="left:805px;top:430px;width:250px;transform:rotate(-25deg)"></div>
            <div class="connector" style="left:990px;top:360px;width:280px;transform:rotate(88deg)"></div>
          </div>
        """,
        "blueprint": f"""
          <div class="hero"><h1 class="title">{esc(title)}</h1><p class="subtitle">{esc(subtitle)}</p></div>
          <div class="diagram">
            <div class="node mono" style="left:0;top:80px">markdown.md</div>
            <div class="node mono" style="left:470px;top:280px">style guide</div>
            <div class="node mono" style="right:0;top:80px">renderer</div>
            <div class="node mono" style="right:220px;bottom:0">artifact bundle</div>
            <div class="wire" style="left:320px;top:165px;width:320px;transform:rotate(23deg)"></div>
            <div class="wire" style="left:790px;top:360px;width:300px;transform:rotate(-27deg)"></div>
            <div class="wire" style="right:150px;top:245px;width:280px;transform:rotate(75deg)"></div>
          </div>
        """,
        "commerce": f"""
          <div class="product"></div>
          <div class="hero"><h1 class="title">{esc(title)}</h1><p class="subtitle">{esc(subtitle)}</p></div>
          <div class="tiles">{''.join(f"<div class='card tile'>{esc(item)}</div>" for item in meta)}</div>
        """,
        "motion": f"""
          <div class="letterbox top"></div><div class="letterbox bottom"></div>
          <div class="hero"><h1 class="title">{esc(title)}</h1><p class="subtitle">{esc(subtitle)}</p></div>
          <div class="timeline">{''.join(f"<div class='framecell'>{esc(item)}<br>scene</div>" for item in meta)}</div>
        """,
        "performance": f"""
          <div class="slash"></div>
          <div class="hero"><h1 class="title">{esc(title)}</h1><p class="subtitle">{esc(subtitle)}</p></div>
          <div class="specrail">{''.join(f"<div class='spec'><strong>{esc(item)}</strong><span>output mode</span></div>" for item in meta)}</div>
        """,
    }[layout]

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{esc(name)}</title>
  <style>{BASE_CSS}</style>
</head>
<body class="{layout} single">
  <section class="slide {layout}" id="{esc(sid)}">
    <div class="pad">
      <div class="topline">
        <div class="brand"><span class="mark"></span><span>{esc(name)}</span></div>
        <div class="mono">{esc(kicker)}</div>
      </div>
    </div>
    {body}
    <div class="footer"><span>Artifactry signature showcase</span><span class="mono">{esc(sid)}</span></div>
  </section>
</body>
</html>
"""


def run(cmd: list[str]) -> None:
    print(" ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build 15 signature showcase preview images.")
    parser.add_argument("--styles", nargs="*", default=[str(s["id"]) for s in STYLES])
    parser.add_argument("--skip-render", action="store_true", help="Only write HTML files.")
    args = parser.parse_args()

    selected = [style for style in STYLES if style["id"] in set(args.styles)]
    if not selected:
        raise SystemExit("No matching styles selected.")

    for style in selected:
        style_id = str(style["id"])
        html_dir = BUILD_DIR / style_id / "slides-html"
        html_dir.mkdir(parents=True, exist_ok=True)
        (html_dir / "slide-01.html").write_text(render(style), encoding="utf-8")

        if not args.skip_render:
            run(
                [
                    sys.executable,
                    str(SKILL / "scripts" / "render_images_chrome.py"),
                    str(html_dir),
                    "--aspect",
                    ASPECT,
                    "--output-dir",
                    str(ASSET_DIR / style_id),
                ]
            )

    print(f"Built {len(selected)} signature showcase styles")


if __name__ == "__main__":
    main()
