#!/usr/bin/env python3
"""Check Artifactry runtime requirements and print agent-friendly install steps."""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PYTHON_PACKAGES = {
    "Pillow": "PIL",
    "python-docx": "docx",
    "python-pptx": "pptx",
}

SYSTEM_TOOLS = {
    "pandoc": {
        "purpose": "DOCX/PDF/PPTX conversion routes",
        "macos": "brew install pandoc",
        "linux": "sudo apt-get update && sudo apt-get install -y pandoc",
        "windows": "winget install --id JohnMacFarlane.Pandoc",
    },
    "node": {
        "purpose": "npx getdesign@latest add <style>",
        "macos": "brew install node",
        "linux": "sudo apt-get update && sudo apt-get install -y nodejs npm",
        "windows": "winget install OpenJS.NodeJS.LTS",
    },
    "npm": {
        "purpose": "npx/getdesign support",
        "macos": "brew install node",
        "linux": "sudo apt-get update && sudo apt-get install -y npm",
        "windows": "winget install OpenJS.NodeJS.LTS",
    },
}

CHROME_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]


def os_key() -> str:
    name = platform.system().lower()
    if name == "darwin":
        return "macos"
    if name == "linux":
        return "linux"
    if name == "windows":
        return "windows"
    return "unknown"


def has_chrome() -> bool:
    if any(Path(path).exists() for path in CHROME_PATHS):
        return True
    return any(shutil.which(name) for name in ("google-chrome", "chromium", "chromium-browser"))


def check() -> dict:
    system = os_key()
    missing_python = [
        package
        for package, import_name in PYTHON_PACKAGES.items()
        if importlib.util.find_spec(import_name) is None
    ]
    missing_tools = [name for name in SYSTEM_TOOLS if shutil.which(name) is None]
    chrome_missing = not has_chrome()

    install_steps = []
    if missing_python:
        install_steps.append(
            {
                "kind": "python",
                "missing": missing_python,
                "command": "python3 -m pip install -r requirements.txt",
            }
        )
    for tool in missing_tools:
        command = SYSTEM_TOOLS[tool].get(system)
        install_steps.append(
            {
                "kind": "system",
                "missing": [tool],
                "purpose": SYSTEM_TOOLS[tool]["purpose"],
                "command": command or f"Install {tool} with your system package manager.",
            }
        )
    if chrome_missing:
        install_steps.append(
            {
                "kind": "system",
                "missing": ["Google Chrome or Chromium"],
                "purpose": "PNG/JPG rendering and Chrome-based PDF export",
                "command": {
                    "macos": "brew install --cask google-chrome",
                    "linux": "sudo apt-get update && sudo apt-get install -y chromium-browser",
                    "windows": "winget install Google.Chrome",
                }.get(system, "Install Google Chrome or Chromium."),
            }
        )

    return {
        "ok": not install_steps,
        "os": system,
        "python": {
            "ok": not missing_python,
            "missing": missing_python,
        },
        "system": {
            "missing_tools": missing_tools + (["chrome"] if chrome_missing else []),
        },
        "pdf_engines": {
            "chrome": not chrome_missing,
            "soffice": shutil.which("soffice") is not None or shutil.which("libreoffice") is not None,
            "xelatex": shutil.which("xelatex") is not None,
            "typst": shutil.which("typst") is not None,
        },
        "install_steps": install_steps,
    }


def print_human(report: dict) -> None:
    if report["ok"]:
        print("OK: Artifactry requirements are available.")
        return

    print("Artifactry preflight found missing requirements.")
    print("Ask the user for approval before installing system tools.")
    for step in report["install_steps"]:
        missing = ", ".join(step["missing"])
        print(f"- Missing: {missing}")
        if step.get("purpose"):
            print(f"  Purpose: {step['purpose']}")
        print(f"  Install: {step['command']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check Artifactry runtime requirements.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()
    report = check()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_human(report)


if __name__ == "__main__":
    main()
