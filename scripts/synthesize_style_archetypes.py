#!/usr/bin/env python3
"""Synthesize generic export style archetypes from the getdesign.md corpus."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORK_ROOT = ROOT / ".work" / "getdesign-md"
INDEX_PATH = WORK_ROOT / "index.json"
STYLE_DIR = ROOT / "skills" / "md-export-suite" / "styles"
SOURCE_AUDIT = WORK_ROOT / "style-source-map.json"

HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b")
FONT_RE = re.compile(r"fontFamily:\s*[\"']?([^\"'\n]+)")
RADIUS_RE = re.compile(r"(\d+(?:\.\d+)?)px")
COMPONENT_RE = re.compile(r"^\s{2}([a-z0-9-]+):\s*$", re.M)


STYLE_SOURCES = {
    "institutional-clarity": [
        "coinbase",
        "ibm",
        "hashicorp",
        "cal",
        "mintlify",
        "wise",
        "vodafone",
    ],
    "warm-editorial": [
        "claude",
        "notion",
        "mastercard",
        "starbucks",
        "airbnb",
        "slack",
    ],
    "monochrome-precision": [
        "vercel",
        "apple",
        "uber",
        "x.ai",
        "tesla",
        "replicate",
        "linear.app",
    ],
    "dark-console": [
        "warp",
        "expo",
        "supabase",
        "resend",
        "opencode.ai",
        "ollama",
        "voltagent",
        "cursor",
    ],
    "gradient-intelligence": [
        "stripe",
        "cohere",
        "framer",
        "raycast",
        "superhuman",
        "mistral.ai",
        "minimax",
        "clay",
        "renault",
        "webflow",
    ],
    "data-command": [
        "binance",
        "kraken",
        "sentry",
        "clickhouse",
        "nvidia",
        "mongodb",
        "composio",
        "revolut",
    ],
    "visual-lifestyle": [
        "meta",
        "nike",
        "pinterest",
        "spotify",
        "playstation",
        "airbnb",
        "apple",
    ],
    "cinematic-luxury": [
        "ferrari",
        "lamborghini",
        "bugatti",
        "bmw",
        "bmw-m",
        "spacex",
        "runwayml",
        "shopify",
        "tesla",
        "elevenlabs",
    ],
    "playful-productivity": [
        "airtable",
        "figma",
        "miro",
        "zapier",
        "lovable",
        "intercom",
        "posthog",
        "slack",
    ],
    "broadsheet-analysis": [
        "wired",
        "theverge",
        "sanity",
        "runwayml",
        "claude",
        "notion",
        "together.ai",
    ],
}


BLUEPRINTS = {
    "institutional-clarity": {
        "name": "Institutional Clarity",
        "summary": "Trust-first executive system with white canvas, restrained blue signal, quiet gray hierarchy, and precise financial-document rhythm.",
        "best_for": ["executive decks", "business reports", "strategy memos", "financial summaries"],
        "mood": ["trustworthy", "precise", "calm", "executive", "institutional"],
        "colors": {
            "background": "#ffffff",
            "ink": "#0a0b0d",
            "body": "#4f5663",
            "muted": "#7c828a",
            "primary": "#0052ff",
            "surface": "#f7f7f7",
            "line": "#dee1e6",
        },
        "typography": {
            "display": "Inter",
            "body": "Inter",
            "mono": "JetBrains Mono",
            "scale": {
                "display_px": 80,
                "title_px": 52,
                "body_px": 18,
                "label_px": 12,
                "display_weight": 400,
                "body_weight": 400,
                "label_weight": 600,
                "line_height_display": 1.0,
                "line_height_body": 1.45,
                "letter_spacing_display": "-1.2px",
                "letter_spacing_label": "0.4px",
                "label_case": "uppercase",
            },
        },
        "style_dna": {
            "philosophy": "Financial-services calm: information feels reviewed, audited, and ready for a boardroom.",
            "visual_signature": "Pure white page, one blue voltage, gray elevation bands, mono numerals, and rounded product-card layers.",
            "surface_logic": "Rotate white canvas, soft gray bands, and occasional dark editorial chapter slides.",
            "density": "Medium sparse with strong alignment and measured whitespace.",
        },
        "palette": {
            "roles": ["single primary signal", "soft gray surfaces", "high-contrast ink", "muted compliance metadata"],
            "accent_policy": "Use blue on one decisive marker, number, route, or callout per page.",
            "semantic_policy": "Green/red only for measured data deltas, never for decoration.",
        },
        "shape": {"corner_scale": "8/12/16/24px with pill CTAs", "default_radius": 24, "border_weight": "1px"},
        "layout": {
            "grid": "12-column, wide safe margins, aligned metrics, restrained card stacking.",
            "whitespace": "Generous but not luxury-sparse; leave enough room for numbers to breathe.",
            "image_treatment": "Product UI or abstract finance diagrams in clean framed panels.",
        },
        "components": {
            "buttons": "Pill primary, gray secondary, text tertiary.",
            "cards": "White or gray cards with subtle border, no loud shadow.",
            "tables": "Dense but breathable rows, mono numerals, blue selected state.",
            "callouts": "Blue left rail or small blue dot, not full blue panels.",
        },
        "slides": {
            "headline_weight": 400,
            "card_radius": 24,
            "density": "medium sparse",
            "accent_rule": "Use primary blue rarely for one key number, route, marker, or action.",
            "background_css": "#ffffff",
            "title_line_height": 1.0,
            "title_letter_spacing": "-1.2px",
            "body_line_height": 1.32,
            "kicker_transform": "uppercase",
            "kicker_letter_spacing": "0.4px",
            "card_border_width": 1,
            "card_shadow": "0 12px 36px rgba(10, 11, 13, 0.06)",
            "accent_geometry": "dot",
            "card_background": "#f7f7f7",
        },
        "document": {
            "title_size": 26,
            "heading_color": "primary",
            "table_header": "#eef2ff",
            "margins_cm": [2.2, 2.0, 2.2, 2.2],
            "heading_rule": "Blue H1, black lower headings, mono metadata.",
        },
    },
    "warm-editorial": {
        "name": "Warm Editorial",
        "summary": "Human reading system with warm paper surfaces, calm serif/sans pairing, soft earth accents, and workbook-friendly hierarchy.",
        "best_for": ["workbooks", "training handouts", "course material", "long-form docs"],
        "mood": ["human", "thoughtful", "warm", "readable", "editorial"],
        "colors": {
            "background": "#f7f1e8",
            "ink": "#211b17",
            "body": "#5f5750",
            "muted": "#8a8178",
            "primary": "#b65c3b",
            "surface": "#fffaf2",
            "line": "#e5d8ca",
        },
        "typography": {
            "display": "Source Serif 4",
            "body": "Inter",
            "mono": "IBM Plex Mono",
            "scale": {
                "display_px": 72,
                "title_px": 44,
                "body_px": 18,
                "label_px": 12,
                "display_weight": 500,
                "body_weight": 400,
                "label_weight": 600,
                "line_height_display": 1.08,
                "line_height_body": 1.55,
                "letter_spacing_display": "-0.4px",
                "letter_spacing_label": "0.8px",
                "label_case": "uppercase",
            },
        },
        "style_dna": {
            "philosophy": "A calm editorial workbook: approachable, careful, and designed for reflection.",
            "visual_signature": "Warm canvas, terracotta accents, soft panels, reading-first paragraphs, and quiet section rhythm.",
            "surface_logic": "Paper base with slightly lighter cards and occasional warm tinted chapter bands.",
            "density": "Comfortable reading density.",
        },
        "palette": {
            "roles": ["paper canvas", "earth accent", "soft linework", "muted annotations"],
            "accent_policy": "Terracotta marks section rhythm, examples, and teacher notes.",
            "semantic_policy": "Keep semantic colors low saturation so they do not fight the reading surface.",
        },
        "shape": {"corner_scale": "12/18/24px soft cards plus full pills", "default_radius": 22, "border_weight": "1px"},
        "layout": {
            "grid": "Single or two-column editorial layout, wide text measure, frequent note blocks.",
            "whitespace": "Comfortable vertical rhythm with room for exercises and handwritten answers.",
            "image_treatment": "Soft framed illustrations or warm photography, never cold stock panels.",
        },
        "components": {
            "buttons": "Soft pill labels and understated primary actions.",
            "cards": "Cream cards with thin warm border and generous padding.",
            "tables": "Readable workbook tables with tinted headers and roomy rows.",
            "callouts": "Teacher notes, exercises, and reflection boxes with warm side rail.",
        },
        "slides": {
            "headline_weight": 500,
            "card_radius": 22,
            "density": "comfortable",
            "accent_rule": "Use terracotta for emphasis and section rhythm, not for every heading.",
            "background_css": "linear-gradient(180deg, #f7f1e8 0%, #fffaf2 100%)",
            "title_line_height": 1.06,
            "title_letter_spacing": "-0.4px",
            "body_line_height": 1.42,
            "kicker_transform": "uppercase",
            "kicker_letter_spacing": "0.8px",
            "card_border_width": 1,
            "card_shadow": "0 16px 40px rgba(80, 55, 35, 0.08)",
            "accent_geometry": "pill",
            "card_background": "#fffaf2",
        },
        "document": {
            "title_size": 28,
            "heading_color": "primary",
            "table_header": "#f1dfcf",
            "margins_cm": [2.4, 2.2, 2.4, 2.4],
            "heading_rule": "Serif title, warm H1, body-first paragraph rhythm.",
        },
    },
    "monochrome-precision": {
        "name": "Monochrome Precision",
        "summary": "Sharp black-white technical minimalism with exact type, hairline grids, square discipline, and almost no decoration.",
        "best_for": ["technical decks", "developer docs", "product memos", "startup briefs"],
        "mood": ["minimal", "technical", "sharp", "controlled", "precise"],
        "colors": {
            "background": "#ffffff",
            "ink": "#000000",
            "body": "#3f3f46",
            "muted": "#71717a",
            "primary": "#000000",
            "surface": "#f4f4f5",
            "line": "#d4d4d8",
        },
        "typography": {
            "display": "Inter",
            "body": "Inter",
            "mono": "Geist Mono",
            "scale": {
                "display_px": 84,
                "title_px": 48,
                "body_px": 17,
                "label_px": 11,
                "display_weight": 500,
                "body_weight": 400,
                "label_weight": 600,
                "line_height_display": 0.98,
                "line_height_body": 1.38,
                "letter_spacing_display": "-1px",
                "letter_spacing_label": "0.9px",
                "label_case": "uppercase",
            },
        },
        "style_dna": {
            "philosophy": "Radical subtraction: every visible element must carry information or structure.",
            "visual_signature": "Black text, white field, hairline rules, square or low-radius panels, mono labels.",
            "surface_logic": "Flat white and pale gray only; depth comes from alignment and rule weight.",
            "density": "Precise, compact, and grid-led.",
        },
        "palette": {
            "roles": ["pure ink", "paper canvas", "gray utility states"],
            "accent_policy": "No accent color unless the source content requires semantic data color.",
            "semantic_policy": "Use semantic color only in charts or pass/fail states.",
        },
        "shape": {"corner_scale": "0/4/8/12px, with square preferred", "default_radius": 8, "border_weight": "1px"},
        "layout": {
            "grid": "Strict modular grid, strong left alignment, visible dividers.",
            "whitespace": "Whitespace acts as structure, not decoration.",
            "image_treatment": "Screenshots or diagrams in square frames, no soft lifestyle crops.",
        },
        "components": {
            "buttons": "Outline or black-fill rectangles with direct labels.",
            "cards": "Flat panels, hairline borders, no decorative shadow.",
            "tables": "Compact rows, mono code/data columns, crisp dividers.",
            "callouts": "Rule-led blocks with mono labels.",
        },
        "slides": {
            "headline_weight": 500,
            "card_radius": 8,
            "density": "precise",
            "accent_rule": "Use black, white, and gray only unless data semantics require color.",
            "background_css": "#ffffff",
            "title_line_height": 0.98,
            "title_letter_spacing": "-1px",
            "body_line_height": 1.28,
            "kicker_transform": "uppercase",
            "kicker_letter_spacing": "0.9px",
            "card_border_width": 1,
            "card_shadow": "none",
            "accent_geometry": "rule",
            "card_background": "#f4f4f5",
        },
        "document": {
            "title_size": 25,
            "heading_color": "ink",
            "table_header": "#f4f4f5",
            "margins_cm": [2.0, 1.8, 2.0, 2.0],
            "heading_rule": "Black headings, hairline section rules, compact code blocks.",
        },
    },
    "dark-console": {
        "name": "Dark Console",
        "summary": "Terminal-native dark system with warm/cool black surfaces, mono labels, code panels, status accents, and command rhythm.",
        "best_for": ["API guides", "agent workflows", "developer presentations", "technical diagrams"],
        "mood": ["developer", "terminal", "dark", "code-first", "focused"],
        "colors": {
            "background": "#080a0f",
            "ink": "#f8fafc",
            "body": "#cbd5e1",
            "muted": "#94a3b8",
            "primary": "#22c55e",
            "surface": "#111827",
            "line": "#263244",
        },
        "typography": {
            "display": "Inter",
            "body": "Inter",
            "mono": "JetBrains Mono",
            "scale": {
                "display_px": 80,
                "title_px": 48,
                "body_px": 18,
                "label_px": 12,
                "display_weight": 500,
                "body_weight": 400,
                "label_weight": 500,
                "line_height_display": 1.02,
                "line_height_body": 1.36,
                "letter_spacing_display": "-0.8px",
                "letter_spacing_label": "0.6px",
                "label_case": "uppercase",
            },
        },
        "style_dna": {
            "philosophy": "A working console, not a generic dark theme: every panel should feel executable.",
            "visual_signature": "Dark canvas, command blocks, mono captions, status green, and subtle bordered layers.",
            "surface_logic": "Stack void, panel, elevated command, and active status states.",
            "density": "Technical, medium-dense.",
        },
        "palette": {
            "roles": ["void background", "panel surface", "terminal accent", "muted log text"],
            "accent_policy": "Green marks execution, current state, success, or selected path only.",
            "semantic_policy": "Add amber/red only for warnings/errors in operational content.",
        },
        "shape": {"corner_scale": "8/12/16px terminal panels", "default_radius": 16, "border_weight": "1px translucent"},
        "layout": {
            "grid": "Panel-based command layout with code blocks, split panes, and status rows.",
            "whitespace": "Compact groups with clear command/output separation.",
            "image_treatment": "Product UI, terminal screenshots, and code frames.",
        },
        "components": {
            "buttons": "Dark pills or command-line prompts with active accent.",
            "cards": "Code panels with hairline borders and subtle inner contrast.",
            "tables": "Log-like rows with mono IDs and status chips.",
            "callouts": "Command snippets, warnings, and runbooks.",
        },
        "slides": {
            "headline_weight": 500,
            "card_radius": 16,
            "density": "technical",
            "accent_rule": "Use green for active command, status, and terminal highlights.",
            "background_css": "radial-gradient(circle at 80% 10%, rgba(34, 197, 94, 0.12), transparent 32%), #080a0f",
            "title_line_height": 1.02,
            "title_letter_spacing": "-0.8px",
            "body_line_height": 1.32,
            "kicker_transform": "uppercase",
            "kicker_letter_spacing": "0.6px",
            "card_border_width": 1,
            "card_shadow": "0 18px 48px rgba(0, 0, 0, 0.35)",
            "accent_geometry": "prompt",
            "card_background": "#111827",
        },
        "document": {
            "title_size": 25,
            "heading_color": "primary",
            "table_header": "#e8fff1",
            "margins_cm": [2.0, 1.9, 2.0, 2.0],
            "heading_rule": "Printable docs stay light, but code blocks carry dark-console rhythm.",
        },
    },
    "gradient-intelligence": {
        "name": "Gradient Intelligence",
        "summary": "Luminous AI/product system with restrained gradients, smooth cards, low-weight display type, and modern launch energy.",
        "best_for": ["AI product decks", "launch carousels", "feature announcements", "innovation briefs"],
        "mood": ["modern", "ai", "luminous", "premium", "fluid"],
        "colors": {
            "background": "#ffffff",
            "ink": "#101828",
            "body": "#667085",
            "muted": "#98a2b3",
            "primary": "#7c3aed",
            "surface": "#f5f3ff",
            "line": "#e9d7fe",
        },
        "typography": {
            "display": "Inter",
            "body": "Inter",
            "mono": "JetBrains Mono",
            "scale": {
                "display_px": 88,
                "title_px": 52,
                "body_px": 18,
                "label_px": 12,
                "display_weight": 300,
                "body_weight": 400,
                "label_weight": 600,
                "line_height_display": 0.98,
                "line_height_body": 1.4,
                "letter_spacing_display": "-1.6px",
                "letter_spacing_label": "0.3px",
                "label_case": "uppercase",
            },
        },
        "style_dna": {
            "philosophy": "Advanced but legible: gradient energy should clarify momentum, not hide structure.",
            "visual_signature": "Soft luminous background, glassy panels, purple/blue/aurora accent, and thin-weight hero type.",
            "surface_logic": "White base with gradient hero wash and pale lavender panels.",
            "density": "Polished medium-sparse.",
        },
        "palette": {
            "roles": ["purple primary", "blue secondary", "aurora wash", "white product surface"],
            "accent_policy": "Use gradients as one controlled field or edge glow, not everywhere.",
            "semantic_policy": "Avoid semantic color overload; let gradient own the emotional range.",
        },
        "shape": {"corner_scale": "16/24/30px smooth cards and pills", "default_radius": 30, "border_weight": "1px soft"},
        "layout": {
            "grid": "Large hero statement with floating product evidence cards.",
            "whitespace": "Airy, launch-page pacing with strong focal hierarchy.",
            "image_treatment": "Abstract AI visuals, product UI cards, or generated texture as background only.",
        },
        "components": {
            "buttons": "Gradient or solid purple pill, soft secondary.",
            "cards": "Light translucent panels with subtle border and roomy padding.",
            "tables": "Use only for feature matrices; keep rows spacious.",
            "callouts": "Luminous highlight panels with one concise claim.",
        },
        "slides": {
            "headline_weight": 300,
            "card_radius": 30,
            "density": "polished",
            "accent_rule": "Use gradients as a controlled background or hero accent, not as decoration everywhere.",
            "background_css": "radial-gradient(circle at 12% 18%, rgba(124, 58, 237, 0.22), transparent 30%), radial-gradient(circle at 84% 8%, rgba(14, 165, 233, 0.16), transparent 28%), #ffffff",
            "title_line_height": 0.98,
            "title_letter_spacing": "-1.6px",
            "body_line_height": 1.36,
            "kicker_transform": "uppercase",
            "kicker_letter_spacing": "0.3px",
            "card_border_width": 1,
            "card_shadow": "0 24px 70px rgba(88, 28, 135, 0.14)",
            "accent_geometry": "glow",
            "card_background": "rgba(255, 255, 255, 0.78)",
        },
        "document": {
            "title_size": 27,
            "heading_color": "primary",
            "table_header": "#f5f3ff",
            "margins_cm": [2.2, 2.0, 2.2, 2.2],
            "heading_rule": "Keep documents printable; translate gradients into accent rules and pale section fills.",
        },
    },
    "data-command": {
        "name": "Data Command",
        "summary": "Dense operational dashboard language with metrics, tables, status systems, mono numerals, and controlled high-signal accents.",
        "best_for": ["KPI reports", "ops reviews", "analytics decks", "business intelligence"],
        "mood": ["analytical", "dense", "operational", "dashboard", "decisive"],
        "colors": {
            "background": "#f8fafc",
            "ink": "#0f172a",
            "body": "#475569",
            "muted": "#64748b",
            "primary": "#0ea5e9",
            "surface": "#ffffff",
            "line": "#cbd5e1",
        },
        "typography": {
            "display": "Inter",
            "body": "Inter",
            "mono": "JetBrains Mono",
            "scale": {
                "display_px": 72,
                "title_px": 44,
                "body_px": 17,
                "label_px": 11,
                "display_weight": 650,
                "body_weight": 400,
                "label_weight": 700,
                "line_height_display": 1.02,
                "line_height_body": 1.32,
                "letter_spacing_display": "-0.6px",
                "letter_spacing_label": "0.7px",
                "label_case": "uppercase",
            },
        },
        "style_dna": {
            "philosophy": "Operating-room clarity: show state, trend, risk, and next action quickly.",
            "visual_signature": "Metric cards, dense tables, status chips, thin dividers, and mono numbers.",
            "surface_logic": "Light dashboard canvas with white modules and status-coded accents.",
            "density": "Data dense.",
        },
        "palette": {
            "roles": ["blue analytical primary", "green up", "red down", "amber warning", "neutral grid"],
            "accent_policy": "Accent colors belong to metrics, status, and comparison only.",
            "semantic_policy": "Every semantic color must map to a label or legend.",
        },
        "shape": {"corner_scale": "8/12/14px utilitarian modules", "default_radius": 14, "border_weight": "1px"},
        "layout": {
            "grid": "Dashboard modules, KPI strips, table-first slide bodies, right-side insight rail.",
            "whitespace": "Tight but scannable; group by decision layer.",
            "image_treatment": "Charts, tables, UI captures, and system diagrams over decorative imagery.",
        },
        "components": {
            "buttons": "Small operational controls, status chips, tabs.",
            "cards": "Metric cards with label, value, delta, and tiny context line.",
            "tables": "Header bands, row dividers, mono numeric columns, status badges.",
            "callouts": "Risk/decision panels with clear severity.",
        },
        "slides": {
            "headline_weight": 650,
            "card_radius": 14,
            "density": "data dense",
            "accent_rule": "Use accent colors only for metrics, status, and comparison.",
            "background_css": "linear-gradient(180deg, #f8fafc 0%, #eef6ff 100%)",
            "title_line_height": 1.02,
            "title_letter_spacing": "-0.6px",
            "body_line_height": 1.26,
            "kicker_transform": "uppercase",
            "kicker_letter_spacing": "0.7px",
            "card_border_width": 1,
            "card_shadow": "0 10px 30px rgba(15, 23, 42, 0.07)",
            "accent_geometry": "status",
            "card_background": "#ffffff",
        },
        "document": {
            "title_size": 24,
            "heading_color": "primary",
            "table_header": "#e0f2fe",
            "margins_cm": [1.8, 1.7, 1.8, 1.8],
            "heading_rule": "Dense headings, strong tables, mono numerals, status labels.",
        },
    },
    "visual-lifestyle": {
        "name": "Visual Lifestyle",
        "summary": "Photo-led consumer storytelling with friendly type, generous image zones, soft cards, and simple caption-first composition.",
        "best_for": ["social posts", "campaign decks", "product catalogs", "brand stories"],
        "mood": ["friendly", "consumer", "photo-led", "warm", "campaign"],
        "colors": {
            "background": "#fff7ed",
            "ink": "#1c1917",
            "body": "#57534e",
            "muted": "#a8a29e",
            "primary": "#f97316",
            "surface": "#ffffff",
            "line": "#fed7aa",
        },
        "typography": {
            "display": "Inter",
            "body": "Inter",
            "mono": "IBM Plex Mono",
            "scale": {
                "display_px": 88,
                "title_px": 54,
                "body_px": 19,
                "label_px": 12,
                "display_weight": 700,
                "body_weight": 400,
                "label_weight": 700,
                "line_height_display": 0.96,
                "line_height_body": 1.38,
                "letter_spacing_display": "-1.4px",
                "letter_spacing_label": "0.4px",
                "label_case": "uppercase",
            },
        },
        "style_dna": {
            "philosophy": "Let the product, person, place, or image carry emotion; UI should frame the story.",
            "visual_signature": "Large image blocks, warm accent, friendly captions, rounded media, and direct headlines.",
            "surface_logic": "Warm or white background with full-bleed visual moments.",
            "density": "Spacious visual.",
        },
        "palette": {
            "roles": ["warm campaign canvas", "friendly CTA accent", "photo-derived secondary colors"],
            "accent_policy": "Use accent color to orient the viewer; let images provide most color.",
            "semantic_policy": "Avoid dashboard semantics unless catalog content requires availability or price states.",
        },
        "shape": {"corner_scale": "18/28/36px soft consumer cards", "default_radius": 36, "border_weight": "1px soft"},
        "layout": {
            "grid": "Image-first layouts, large hero crop plus short copy blocks.",
            "whitespace": "Generous, mobile-readable, and caption-friendly.",
            "image_treatment": "Full-bleed or large rounded photography with clear safe overlays.",
        },
        "components": {
            "buttons": "Friendly pills, simple labels.",
            "cards": "Image cards with short caption and soft border.",
            "tables": "Avoid unless catalog specs are necessary.",
            "callouts": "Caption panels, testimonial cards, and product notes.",
        },
        "slides": {
            "headline_weight": 700,
            "card_radius": 36,
            "density": "spacious visual",
            "accent_rule": "Pair friendly accent color with generous image areas and simple captions.",
            "background_css": "linear-gradient(180deg, #fff7ed 0%, #ffffff 100%)",
            "title_line_height": 0.98,
            "title_letter_spacing": "-1.4px",
            "body_line_height": 1.34,
            "kicker_transform": "uppercase",
            "kicker_letter_spacing": "0.4px",
            "card_border_width": 1,
            "card_shadow": "0 22px 60px rgba(124, 45, 18, 0.12)",
            "accent_geometry": "pill",
            "card_background": "#ffffff",
        },
        "document": {
            "title_size": 27,
            "heading_color": "primary",
            "table_header": "#ffedd5",
            "margins_cm": [2.3, 2.0, 2.3, 2.3],
            "heading_rule": "Use image captions and soft section markers; keep long docs light.",
        },
    },
    "cinematic-luxury": {
        "name": "Cinematic Luxury",
        "summary": "Dramatic black-canvas premium system with full-bleed hero pacing, restrained metallic/red accents, and monumental display type.",
        "best_for": ["premium pitches", "portfolio decks", "luxury product stories", "hero presentations"],
        "mood": ["dramatic", "premium", "cinematic", "high contrast", "sparse"],
        "colors": {
            "background": "#050505",
            "ink": "#f8f7f4",
            "body": "#d6d3cc",
            "muted": "#a39f96",
            "primary": "#d6a84f",
            "surface": "#121212",
            "line": "#2a2926",
        },
        "typography": {
            "display": "Inter",
            "body": "Inter",
            "mono": "IBM Plex Mono",
            "scale": {
                "display_px": 96,
                "title_px": 58,
                "body_px": 18,
                "label_px": 11,
                "display_weight": 500,
                "body_weight": 400,
                "label_weight": 700,
                "line_height_display": 0.96,
                "line_height_body": 1.36,
                "letter_spacing_display": "-1.2px",
                "letter_spacing_label": "1.4px",
                "label_case": "uppercase",
            },
        },
        "style_dna": {
            "philosophy": "Premium restraint: fewer elements, stronger contrast, more intentional silence.",
            "visual_signature": "Near-black canvas, large white display type, cinematic imagery, and one scarce premium accent.",
            "surface_logic": "Black hero, elevated dark panels, occasional light editorial insert.",
            "density": "Dramatic sparse.",
        },
        "palette": {
            "roles": ["near-black stage", "warm white type", "metallic or red signal", "deep gray surfaces"],
            "accent_policy": "One accent moment per slide, preferably as a rule, number, or small CTA.",
            "semantic_policy": "Avoid generic status colors; premium systems use fewer signals.",
        },
        "shape": {"corner_scale": "0/4/8/12px with square media preferred", "default_radius": 8, "border_weight": "1px dark"},
        "layout": {
            "grid": "Hero-first layouts, asymmetry, oversized type, large negative space.",
            "whitespace": "Sparse and theatrical; do not fill the black canvas.",
            "image_treatment": "Full-bleed cinematic photography, hard crops, no stock-like blur.",
        },
        "components": {
            "buttons": "Square or low-radius uppercase CTAs.",
            "cards": "Dark panels, thin borders, no soft SaaS feel.",
            "tables": "Spec grids with large numbers and sparse rows.",
            "callouts": "Monumental numbers, chapter bands, and image-caption pairs.",
        },
        "slides": {
            "headline_weight": 500,
            "card_radius": 8,
            "density": "dramatic sparse",
            "accent_rule": "Use gold/metal accent sparingly against black canvas.",
            "background_css": "radial-gradient(circle at 72% 18%, rgba(214, 168, 79, 0.14), transparent 28%), #050505",
            "title_line_height": 0.96,
            "title_letter_spacing": "-1.2px",
            "body_line_height": 1.32,
            "kicker_transform": "uppercase",
            "kicker_letter_spacing": "1.4px",
            "card_border_width": 1,
            "card_shadow": "0 24px 80px rgba(0, 0, 0, 0.55)",
            "accent_geometry": "rule",
            "card_background": "#121212",
        },
        "document": {
            "title_size": 28,
            "heading_color": "primary",
            "table_header": "#f2ead7",
            "margins_cm": [2.4, 2.2, 2.4, 2.4],
            "heading_rule": "Documents become premium editorial on white paper, not black Word pages unless PDF-only.",
        },
    },
    "playful-productivity": {
        "name": "Playful Productivity",
        "summary": "Friendly modular SaaS system with colorful structure, rounded blocks, approachable labels, and onboarding clarity.",
        "best_for": ["onboarding docs", "team training", "SaaS guides", "lightweight presentations"],
        "mood": ["friendly", "modular", "colorful", "approachable", "productive"],
        "colors": {
            "background": "#ffffff",
            "ink": "#172033",
            "body": "#536077",
            "muted": "#8a94a6",
            "primary": "#635bff",
            "surface": "#f6f8fb",
            "line": "#d9e0ea",
        },
        "typography": {
            "display": "Inter",
            "body": "Inter",
            "mono": "JetBrains Mono",
            "scale": {
                "display_px": 80,
                "title_px": 50,
                "body_px": 18,
                "label_px": 12,
                "display_weight": 700,
                "body_weight": 400,
                "label_weight": 700,
                "line_height_display": 1.0,
                "line_height_body": 1.38,
                "letter_spacing_display": "-1.1px",
                "letter_spacing_label": "0.3px",
                "label_case": "uppercase",
            },
        },
        "style_dna": {
            "philosophy": "Make complex workflows feel learnable through modular color, friendly containers, and clear labels.",
            "visual_signature": "Rounded cards, colorful chips, structured boards, and approachable product rhythm.",
            "surface_logic": "White canvas, pale modular blocks, color used for grouping.",
            "density": "Modular friendly.",
        },
        "palette": {
            "roles": ["primary product accent", "secondary category colors", "soft neutral board"],
            "accent_policy": "Use color for organization and affordance, not random decoration.",
            "semantic_policy": "Semantic states may be colorful but must stay labeled.",
        },
        "shape": {"corner_scale": "12/18/24px rounded modules", "default_radius": 24, "border_weight": "1px playful"},
        "layout": {
            "grid": "Board, card, and checklist patterns with obvious groupings.",
            "whitespace": "Friendly and scannable; keep modules distinct.",
            "image_treatment": "Product UI snapshots, icons, simple diagrams, and light illustrations.",
        },
        "components": {
            "buttons": "Rounded primary, outlined secondary, compact icon chips.",
            "cards": "Task cards, checklist modules, tabs, and color-coded groups.",
            "tables": "Turn tables into cards when social/deck output benefits.",
            "callouts": "Friendly tips, steps, and templates.",
        },
        "slides": {
            "headline_weight": 700,
            "card_radius": 24,
            "density": "modular friendly",
            "accent_rule": "Use color blocks for organization, not random decoration.",
            "background_css": "linear-gradient(180deg, #ffffff 0%, #f6f8fb 100%)",
            "title_line_height": 1.0,
            "title_letter_spacing": "-1.1px",
            "body_line_height": 1.32,
            "kicker_transform": "uppercase",
            "kicker_letter_spacing": "0.3px",
            "card_border_width": 1,
            "card_shadow": "0 18px 48px rgba(23, 32, 51, 0.09)",
            "accent_geometry": "pill",
            "card_background": "#f6f8fb",
        },
        "document": {
            "title_size": 26,
            "heading_color": "primary",
            "table_header": "#eef2ff",
            "margins_cm": [2.1, 1.9, 2.1, 2.1],
            "heading_rule": "Use steps, checklists, and modular callouts.",
        },
    },
    "broadsheet-analysis": {
        "name": "Broadsheet Analysis",
        "summary": "Editorial research system with dense paper grids, serif display, mono kickers, hard rules, and analytical story hierarchy.",
        "best_for": ["research carousels", "thought leadership", "market analysis", "editorial PDFs"],
        "mood": ["editorial", "analytical", "dense", "print-like", "opinionated"],
        "colors": {
            "background": "#fbfaf7",
            "ink": "#111111",
            "body": "#3f3f3f",
            "muted": "#737373",
            "primary": "#1d4ed8",
            "surface": "#ffffff",
            "line": "#d6d3d1",
        },
        "typography": {
            "display": "Source Serif 4",
            "body": "Source Serif 4",
            "mono": "IBM Plex Mono",
            "scale": {
                "display_px": 86,
                "title_px": 48,
                "body_px": 17,
                "label_px": 11,
                "display_weight": 700,
                "body_weight": 400,
                "label_weight": 700,
                "line_height_display": 0.96,
                "line_height_body": 1.48,
                "letter_spacing_display": "-0.5px",
                "letter_spacing_label": "1.1px",
                "label_case": "uppercase",
            },
        },
        "style_dna": {
            "philosophy": "Analysis should feel edited, argued, and typeset, not merely summarized.",
            "visual_signature": "Paper-white field, serif headlines, mono uppercase kickers, hairline rules, dense story modules.",
            "surface_logic": "Flat print surfaces; depth comes from rule weight and typographic hierarchy.",
            "density": "Editorial dense.",
        },
        "palette": {
            "roles": ["ink", "paper", "hairline", "one link/accent blue"],
            "accent_policy": "Use one blue for links, references, or the strongest analytical highlight.",
            "semantic_policy": "Prefer labels and rules to traffic-light colors.",
        },
        "shape": {"corner_scale": "0/2/4px; square by default", "default_radius": 2, "border_weight": "1-2px"},
        "layout": {
            "grid": "Magazine grid, columns, numbered lists, pull quotes, and section ribbons.",
            "whitespace": "Dense but disciplined; whitespace acts like page margin.",
            "image_treatment": "Hard-cropped editorial images or charts with captions.",
        },
        "components": {
            "buttons": "Hard-outline rectangles or underlined text links.",
            "cards": "No floating cards; use story blocks separated by rules.",
            "tables": "Report-style tables with hairline dividers and strong headers.",
            "callouts": "Pull quotes, source notes, and numbered evidence blocks.",
        },
        "slides": {
            "headline_weight": 700,
            "card_radius": 2,
            "density": "editorial dense",
            "accent_rule": "Use mono kickers, hairline dividers, and one ink-blue accent.",
            "background_css": "#fbfaf7",
            "title_line_height": 0.96,
            "title_letter_spacing": "-0.5px",
            "body_line_height": 1.4,
            "kicker_transform": "uppercase",
            "kicker_letter_spacing": "1.1px",
            "card_border_width": 1,
            "card_shadow": "none",
            "accent_geometry": "rule",
            "card_background": "#ffffff",
        },
        "document": {
            "title_size": 29,
            "heading_color": "ink",
            "table_header": "#ece7df",
            "margins_cm": [1.9, 1.8, 1.9, 1.9],
            "heading_rule": "Serif display, mono kickers, hairline rules, dense evidence blocks.",
        },
    },
}


STYLE_ORDER = [
    "institutional-clarity",
    "warm-editorial",
    "monochrome-precision",
    "dark-console",
    "gradient-intelligence",
    "data-command",
    "visual-lifestyle",
    "cinematic-luxury",
    "playful-productivity",
    "broadsheet-analysis",
]


def load_index() -> dict:
    if not INDEX_PATH.exists():
        raise SystemExit("Run scripts/crawl_getdesign_md.py first.")
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def source_lookup(index: dict) -> dict[str, dict]:
    lookup: dict[str, dict] = {}
    for category in index["categories"]:
        for entry in category["entries"]:
            if entry["status"] == "missing-in-source":
                continue
            lookup[entry["slug"]] = {
                "category": category["title"],
                "entry": entry,
                "path": WORK_ROOT / entry["organized_path"] / "DESIGN.md",
            }
    return lookup


def first_description(text: str) -> str:
    match = re.search(r"description:\s*(.+)", text)
    if match:
        return match.group(1).strip().strip('"')
    for paragraph in text.split("\n\n"):
        clean = paragraph.strip()
        if clean and not clean.startswith("---") and not clean.startswith("#"):
            return re.sub(r"\s+", " ", clean)[:360]
    return ""


def extract_tokens(slug: str, source: dict) -> dict:
    text = source["path"].read_text(encoding="utf-8")
    colors = [c.lower() for c in HEX_RE.findall(text)]
    fonts = []
    for raw in FONT_RE.findall(text):
        first = raw.split(",")[0].strip().strip("\"'")
        if first and first.lower() not in {"sans-serif", "system-ui", "helvetica", "arial"}:
            fonts.append(first)
    radii = [float(v) for v in RADIUS_RE.findall(text)]
    components = [c for c in COMPONENT_RE.findall(text) if not c.startswith(("display-", "body-", "title-"))]
    return {
        "slug": slug,
        "category": source["category"],
        "description": first_description(text),
        "colors": Counter(colors),
        "fonts": Counter(fonts),
        "radii": radii,
        "components": components,
        "word_count": len(text.split()),
    }


def merge_corpus(style_id: str, tokens: list[dict]) -> dict:
    color_counter: Counter[str] = Counter()
    font_counter: Counter[str] = Counter()
    category_counter: Counter[str] = Counter()
    component_counter: Counter[str] = Counter()
    radii: list[float] = []
    word_count = 0

    for token in tokens:
        color_counter.update(token["colors"])
        font_counter.update(token["fonts"])
        category_counter[token["category"]] += 1
        component_counter.update(token["components"])
        radii.extend(token["radii"])
        word_count += token["word_count"]

    radius_summary = {
        "min_px": min(radii) if radii else 0,
        "median_px": sorted(radii)[len(radii) // 2] if radii else 0,
        "max_px": max(radii) if radii else 0,
    }

    return {
        "method": "Synthesized from local getdesign.md working corpus.",
        "source_count": len(tokens),
        "source_categories": dict(category_counter),
        "total_source_words": word_count,
        "dominant_color_samples": [color for color, _ in color_counter.most_common(12)],
        "font_samples": [font for font, _ in font_counter.most_common(10)],
        "radius_observed_px": radius_summary,
        "component_vocabulary": [name for name, _ in component_counter.most_common(18)],
    }


def build_styles() -> tuple[list[dict], dict]:
    index = load_index()
    lookup = source_lookup(index)
    audit: dict[str, object] = {
        "source_commit": index["source_commit"],
        "styles": {},
        "coverage": {},
    }
    seen: Counter[str] = Counter()
    style_index = []

    for style_id in STYLE_ORDER:
        source_slugs = STYLE_SOURCES[style_id]
        missing = [slug for slug in source_slugs if slug not in lookup]
        tokens = [extract_tokens(slug, lookup[slug]) for slug in source_slugs if slug in lookup]
        style = {
            "id": style_id,
            **BLUEPRINTS[style_id],
            "source_inheritance": merge_corpus(style_id, tokens),
            "guardrails": guardrails_for(style_id),
            "export_translation": export_translation_for(style_id),
        }
        (STYLE_DIR / f"{style_id}.json").write_text(
            json.dumps(style, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        style_index.append(
            {
                "id": style_id,
                "name": style["name"],
                "summary": style["summary"],
                "best_for": style["best_for"],
                "source_count": len(tokens),
                "source_categories": style["source_inheritance"]["source_categories"],
            }
        )
        audit["styles"][style_id] = {"sources": source_slugs, "missing": missing}
        seen.update(slug for slug in source_slugs if slug in lookup)

    all_slugs = sorted(lookup)
    audit["coverage"] = {
        "available_source_count": len(all_slugs),
        "used_at_least_once": len(seen),
        "unused": [slug for slug in all_slugs if slug not in seen],
        "duplicated": {slug: count for slug, count in sorted(seen.items()) if count > 1},
    }
    return style_index, audit


def guardrails_for(style_id: str) -> dict[str, list[str]]:
    rules = {
        "institutional-clarity": (
            ["Use one blue signal per artifact page.", "Align numbers and decisions on a visible grid.", "Keep finance or executive claims calm and auditable."],
            ["Do not add decorative gradients.", "Do not make every heading blue.", "Do not use playful icon clutter."],
        ),
        "warm-editorial": (
            ["Prioritize reading rhythm.", "Use warm note blocks for exercises and reflections.", "Let headings feel human rather than salesy."],
            ["Do not overuse colored panels.", "Do not compress long paragraphs into dashboard cards.", "Do not use cold gray SaaS chrome."],
        ),
        "monochrome-precision": (
            ["Use line, spacing, and weight as the design system.", "Prefer square or low-radius surfaces.", "Make labels exact and short."],
            ["Do not add accent colors for energy.", "Do not use soft shadows.", "Do not round every module."],
        ),
        "dark-console": (
            ["Make panels feel executable.", "Use mono labels for commands, states, and IDs.", "Keep contrast accessible on dark surfaces."],
            ["Do not use random neon colors.", "Do not make long Word docs dark by default.", "Do not fake code screenshots for final text."],
        ),
        "gradient-intelligence": (
            ["Anchor luminous effects to hierarchy.", "Use thin-weight display type with structured panels.", "Keep gradients behind content, not inside body text."],
            ["Do not make every surface gradient.", "Do not sacrifice readability for glow.", "Do not use generic purple blobs."],
        ),
        "data-command": (
            ["Map every color to a metric or status.", "Use mono numerals.", "Expose trend, risk, and action together."],
            ["Do not use status colors without labels.", "Do not make dashboards sparse like brand slides.", "Do not hide tables in screenshots."],
        ),
        "visual-lifestyle": (
            ["Reserve large safe areas for imagery.", "Use short captions.", "Let photography or product visuals provide color range."],
            ["Do not overlay small text on busy images.", "Do not build text-heavy slides in this mode.", "Do not use abstract stock visuals when real product/place imagery is needed."],
        ),
        "cinematic-luxury": (
            ["Use fewer, larger elements.", "Let black canvas and image crops create drama.", "Keep accent moments scarce."],
            ["Do not fill the page with cards.", "Do not use friendly SaaS pills everywhere.", "Do not brighten the palette unnecessarily."],
        ),
        "playful-productivity": (
            ["Use color to organize workflows.", "Build modular steps and cards.", "Keep instructions approachable and scannable."],
            ["Do not scatter colors without grouping logic.", "Do not over-densify onboarding content.", "Do not use luxury black-canvas drama."],
        ),
        "broadsheet-analysis": (
            ["Use mono kickers and rules.", "Make argument structure visible.", "Prefer pull quotes, sources, and numbered evidence."],
            ["Do not use rounded SaaS cards.", "Do not add glow or glass effects.", "Do not make editorial layouts too sparse."],
        ),
    }
    do, dont = rules[style_id]
    return {"do": do, "dont": dont}


def export_translation_for(style_id: str) -> dict[str, list[str]]:
    common = {
        "pptx": [
            "Use deterministic HTML/CSS or PPTX text boxes for final text.",
            "Keep one core idea per slide and validate rendered PNG dimensions.",
        ],
        "docx": [
            "Translate visual style into Word typography, margins, heading hierarchy, tables, and callouts.",
            "Keep documents printable unless the user explicitly requests PDF-only visual art direction.",
        ],
        "carousel": [
            "Use high-resolution fixed canvas, mobile-readable text, and safe margins.",
            "Make each frame complete enough to stand alone.",
        ],
    }
    if style_id in {"data-command", "broadsheet-analysis"}:
        common["pptx"].append("Use tables, numbered evidence, and source notes instead of vague decorative cards.")
    if style_id in {"visual-lifestyle", "cinematic-luxury"}:
        common["carousel"].append("Reserve a large image or cinematic negative-space zone before adding text.")
    if style_id == "dark-console":
        common["docx"].append("For DOCX, keep page white but render code blocks with console-inspired styling.")
    return common


def main() -> None:
    STYLE_DIR.mkdir(parents=True, exist_ok=True)
    style_index, audit = build_styles()
    (STYLE_DIR / "style_index.json").write_text(
        json.dumps(style_index, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    SOURCE_AUDIT.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(style_index)} enriched styles to {STYLE_DIR}")
    print(f"Source audit: {SOURCE_AUDIT}")
    coverage = audit["coverage"]
    print(f"Coverage: {coverage['used_at_least_once']} / {coverage['available_source_count']} sources used")
    if coverage["unused"]:
        print("Unused sources:", ", ".join(coverage["unused"]))


if __name__ == "__main__":
    main()
