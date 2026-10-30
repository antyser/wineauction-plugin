#!/usr/bin/env python3
"""Build and verify the portable plugin ZIP from one clean committed revision."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREFIX = "wineauction-plugin/"
VERSION = "1.2.1"
FIXTURE_ATTACHMENT = (
    "https://github.com/antyser/wineauction-plugin/releases/download/"
    "v1.1.0/newsletter-30-rows.txt"
)
DEMO_URL = (
    "https://github.com/antyser/wineauction-plugin/releases/download/"
    "v1.1.0/wineauction-review-v1.1.0-silent.mp4"
)
SECRET = re.compile(
    rb"(?:\bsk-[A-Za-z0-9_-]{20,}|\bgh[pousr]_[A-Za-z0-9_]{20,}|"
    rb"\bxox[baprs]-[A-Za-z0-9-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)",
    re.IGNORECASE,
)
TASK_SKILLS = {
    "restaurant-wine-list",
    "merchant-offer-check",
    "auction-lots",
    "wine-info",
    "cellar-valuation",
}
ROW = re.compile(r"^.+ — \d+ ml × \d+ — \$[\d,]+(?:\.\d{2})?$")


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, capture_output=True
    )
    return result.stdout.strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_archive(revision: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.unlink(missing_ok=True)
    subprocess.run(
        [
            "git",
            "archive",
            "--format=zip",
            f"--prefix={PREFIX}",
            f"--output={destination}",
            revision,
        ],
        cwd=ROOT,
        check=True,
    )


def archive_files(archive: zipfile.ZipFile) -> dict[str, bytes]:
    files = {}
    for entry in archive.infolist():
        if entry.is_dir():
            continue
        require(entry.filename.startswith(PREFIX), "ZIP paths must share one package root")
        path = entry.filename.removeprefix(PREFIX)
        require(path and not path.startswith("/") and ".." not in Path(path).parts, "unsafe ZIP path")
        require(path not in files, f"duplicate ZIP path: {path}")
        files[path] = archive.read(entry)
    return files


def read_json(files: dict[str, bytes], path: str) -> dict:
    try:
        value = json.loads(files[path])
    except (KeyError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{path} is missing or invalid JSON") from error
    require(isinstance(value, dict), f"{path} must contain a JSON object")
    return value


def check_manifest(files: dict[str, bytes]) -> None:
    portable = read_json(files, "plugin.json")
    claude = read_json(files, ".claude-plugin/plugin.json")
    require(portable.get("name") == "wineauction", "portable package identity changed")
    require(portable.get("version") == VERSION, f"portable manifest version is not {VERSION}")
    require(claude.get("name") == portable["name"], "Claude and portable package identities differ")
    require(claude.get("version") == portable["version"], "versioned manifests are out of sync")
    require(portable.get("author", {}).get("name") == "LemonCube LLC", "publisher is not LemonCube LLC")

    extension = portable.get("extensions", {}).get("com.openai", {})
    interface = extension.get("interface", {})
    require(interface.get("developerName") == "LemonCube LLC", "OpenAI developer name is incorrect")
    require(len(interface.get("shortDescription", "")) <= 30, "shortDescription exceeds 30 characters")
    require(interface.get("supportURL") == "https://wineauction.ai/contact", "support URL is incorrect")
    for field in ("logo", "composerIcon"):
        asset = interface.get(field, "")
        require(asset.startswith("./") and asset[2:] in files, f"{field} asset is missing")
    logo = files[interface["logo"][2:]]
    require(logo[:8] == b"\x89PNG\r\n\x1a\n", "logo must be a PNG")
    width, height = struct.unpack(">II", logo[16:24])
    require(width == height and width >= 48, "logo must be square and at least 48px")

    mcp = read_json(files, "mcp.json")
    server = mcp.get("mcpServers", {}).get("wineauction", {})
    require(server.get("type") == "streamable-http", "portable MCP server transport changed")
    require(server.get("url") == "https://wineauction.ai/api/mcp", "portable MCP URL changed")
    auth = server.get("extensions", {}).get("com.openai", {}).get("auth", {})
    require(auth.get("type") == "oauth", "portable MCP OAuth configuration is missing")
    require(auth.get("client", {}).get("mode") == "dcr", "portable MCP DCR mode changed")

    review = extension.get("review", {})
    cases = review.get("test_cases", {})
    positive = cases.get("positive", [])
    negative = cases.get("negative", [])
    require(len(positive) == 5 and len(negative) == 3, "review cases must contain five workflow positives and three negatives")
    tools = {
        tool.strip()
        for case in positive
        for tool in case.get("tools_triggered", "").split(",")
    }
    required_tools = {
        "search_wines",
        "list_offers",
        "evaluate_offers",
        "list_auctions",
        "list_retail_stores",
        "list_restaurants",
    }
    require(required_tools <= tools, "positive cases do not cover all six MCP tools")
    require(positive[0].get("tools_triggered") == "list_auctions, list_offers", "auction discovery case changed")
    require("max_price_usd 600" in positive[2].get("expected_behavior", ""), "wine price filter is missing")
    require("$950 per bottle" in positive[3].get("expected_behavior", ""), "Lafite price calculation is missing")
    batch_case = positive[4]
    require(batch_case.get("file_attachment_urls") == [FIXTURE_ATTACHMENT], "newsletter fixture attachment URL changed")
    require("25 rows and 5 rows" in batch_case.get("expected_behavior", ""), "newsletter batching expectation is missing")
    require(review.get("demo_recording_url") == DEMO_URL, "planned review video URL changed")
    require(negative[1].get("prompt", "").find("min_price_usd 1000") >= 0, "inverted range case lost its lower bound")
    require(negative[1].get("prompt", "").find("max_price_usd 100") >= 0, "inverted range case lost its upper bound")
    require("closed" in negative[2].get("prompt", "").lower() and "24 hours" in negative[2].get("prompt", ""), "closed-lot conflict case changed")


def check_fixture(files: dict[str, bytes]) -> None:
    fixture = files.get("review/fixtures/newsletter-30-rows.txt", b"").decode("utf-8")
    lines = [line for line in fixture.splitlines() if ROW.fullmatch(line)]
    require(len(lines) == 30, f"newsletter fixture must contain 30 priced rows, found {len(lines)}")
    lowered = fixture.lower()
    require("synthetic review fixture" in lowered, "newsletter fixture must be labeled synthetic")
    require("not actual merchant offers" in lowered, "newsletter fixture must disclaim real offers")
    require("no retail or auction market references" in lowered, "fixture must not supply market references")


def check_trigger_cases(files: dict[str, bytes]) -> None:
    cases = read_json(files, "review/trigger-cases.json")
    positive = cases.get("positive", [])
    negative = cases.get("negative", [])
    require(len(positive) == 26 and len(negative) == 6, "trigger matrix must contain 26 positive and six negative cases")
    require({case.get("expected_skill") for case in positive} == TASK_SKILLS, "trigger matrix must cover every task skill")
    require(all(case.get("prompt") and case.get("expected_skill") in TASK_SKILLS for case in positive), "positive trigger cases need prompts and expected skills")
    require(all(case.get("prompt") and case.get("expected_skill") is None for case in negative), "negative trigger cases need prompts and a null expected skill")


def check_archive(archive_path: Path, revision: str) -> None:
    require(".gitattributes" not in git("ls-tree", "-r", "--name-only", revision).splitlines(), "the Claude directory rejects .gitattributes export rules")
    expected = set(git("ls-tree", "-r", "--name-only", revision).splitlines())
    with zipfile.ZipFile(archive_path) as archive:
        files = archive_files(archive)
    actual = set(files)
    require(expected == actual, "ZIP does not contain exactly the files tracked at the selected commit")
    required = {
        "plugin.json",
        "mcp.json",
        ".mcp.json",
        ".claude-plugin/plugin.json",
        ".claude-plugin/marketplace.json",
        ".agents/plugins/marketplace.json",
        "README.md",
        "skills/restaurant-wine-list/SKILL.md",
        "skills/restaurant-wine-list/agents/openai.yaml",
        "skills/merchant-offer-check/SKILL.md",
        "skills/merchant-offer-check/agents/openai.yaml",
        "skills/auction-lots/SKILL.md",
        "skills/auction-lots/agents/openai.yaml",
        "skills/wine-info/SKILL.md",
        "skills/wine-info/agents/openai.yaml",
        "skills/cellar-valuation/SKILL.md",
        "skills/cellar-valuation/agents/openai.yaml",
        "skills/wineauction-reference/SKILL.md",
        "skills/wineauction-reference/agents/openai.yaml",
        "skills/wineauction-reference/assets/report.html",
        "skills/wineauction-reference/scripts/render.py",
        "skills/wineauction-reference/references/prices.md",
        "skills/wineauction-reference/references/parse-list.md",
        "skills/wineauction-reference/references/evaluate.md",
        "skills/wineauction-reference/references/mixed-lots.md",
        "skills/wineauction-reference/references/report.md",
        "skills/wineauction-reference/references/design-system.md",
        "skills/wineauction-reference/references/tools/search_wines.md",
        "skills/wineauction-reference/references/tools/list_offers.md",
        "skills/wineauction-reference/references/tools/evaluate_offers.md",
        "skills/wineauction-reference/references/tools/list_auctions.md",
        "skills/wineauction-reference/references/tools/list_retail_stores.md",
        "skills/wineauction-reference/references/tools/list_restaurants.md",
        "assets/logo.png",
        "review/fixtures/newsletter-30-rows.txt",
        "review/trigger-cases.json",
        "scripts/build_release.py",
        "scripts/test_renderer.mjs",
        "scripts/local_ci.sh",
    }
    require(required <= actual, f"ZIP is missing required package files: {sorted(required - actual)}")
    forbidden = [path for path in actual if Path(path).name in {".env", ".env.local", "credentials.json"} or Path(path).suffix in {".pem", ".key", ".p12"}]
    require(not forbidden, f"ZIP contains credential-like files: {forbidden}")
    for path, content in files.items():
        require(SECRET.search(content) is None, f"secret-like material found in {path}")
    check_manifest(files)
    check_fixture(files)
    check_trigger_cases(files)
    exercise_renderer(files)


def exercise_renderer(files: dict[str, bytes]) -> None:
    node = shutil.which("node")
    require(node is not None, "Node.js is required to exercise the packaged HTML renderer")
    with tempfile.TemporaryDirectory(prefix="wineauction-renderer-") as directory:
        root = Path(directory) / "wineauction-plugin"
        root.mkdir()
        for path, content in files.items():
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        rows_path = Path(directory) / "rows.json"
        not_found_path = Path(directory) / "not-found.json"
        report_path = Path(directory) / "report.html"
        rows_path.write_text(
            json.dumps(
                [
                    {
                        "name": "Renderer <img src=x onerror=alert(1)>",
                        "vintage": 2019,
                        "price_usd": 100,
                        "retail_usd": None,
                        "auction_usd": None,
                        "seller": "Synthetic test input",
                        "flags": ["No market data returned"],
                    },
                    {
                        "name": "Six-bottle lot",
                        "vintage": 2015,
                        "ref": "Lot 12",
                        "bottles": 6,
                        "size_ml": 750,
                        "price_usd": 950,
                        "quoted_price": 5700,
                        "quoted_currency": "USD",
                        "price_label": "Hammer incl. premium",
                        "premium_pct": 25,
                        "status": "sold",
                        "sold_at": "2026-10-03T18:00:00Z",
                        "retail_usd": 1200,
                        "discount_vs_retail_pct": 21,
                        "flags": [],
                    },
                    {
                        "name": "Mixed Bordeaux case",
                        "mixed_items": [
                            {"name": "Latour <b>", "vintage": 2010, "bottles": 3, "bottle_size_ml": 750},
                            {"name": "Mouton", "vintage": 2009, "bottles": 3, "bottle_size_ml": 750},
                        ],
                        "bottles": 6,
                        "price_usd": 400,
                        "retail_usd": 300,
                        "discount_vs_retail_pct": -33,
                        "flags": [],
                    },
                    {
                        "name": "No reference sample",
                        "vintage": 2020,
                        "price_usd": 80,
                        "retail_usd": None,
                        "auction_usd": None,
                        "flags": [],
                    },
                ],
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        not_found_path.write_text(
            json.dumps([{"name": "Unknown <wine>", "hint": "No catalog match"}]),
            encoding="utf-8",
        )
        subprocess.run(
            [
                sys.executable,
                str(root / "skills/wineauction-reference/scripts/render.py"),
                str(rows_path),
                str(report_path),
                "--title",
                "Renderer <script>alert('x')</script>",
                "--not-found",
                str(not_found_path),
            ],
            check=True,
            cwd=root,
        )
        rendered = report_path.read_text(encoding="utf-8")
        require("Renderer &lt;script&gt;alert(&#x27;x&#x27;)&lt;/script&gt;" in rendered, "renderer failed to escape report title")
        subprocess.run([node, str(root / "scripts/test_renderer.mjs"), str(report_path), "discount"], check=True)
        markup_path = Path(directory) / "report-markup.html"
        subprocess.run(
            [
                sys.executable,
                str(root / "skills/wineauction-reference/scripts/render.py"),
                str(rows_path),
                str(markup_path),
                "--title",
                "Markup",
                "--markup",
                "--not-found",
                str(not_found_path),
            ],
            check=True,
            cwd=root,
        )
        subprocess.run([node, str(root / "scripts/test_renderer.mjs"), str(markup_path), "markup"], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path.home() / "Downloads" / f"wineauction-plugin-{VERSION}.zip",
        help="ZIP destination (defaults to ~/Downloads)",
    )
    parser.add_argument("--expected-head", help="require HEAD to match this commit SHA")
    args = parser.parse_args()

    revision = git("rev-parse", "--verify", "HEAD^{commit}")
    if args.expected_head and args.expected_head != revision:
        raise RuntimeError(f"expected HEAD {args.expected_head}, found {revision}")
    dirty = git("status", "--porcelain", "--untracked-files=normal")
    require(not dirty, "release packaging requires a clean working tree")
    output = args.output.expanduser().resolve()
    require(ROOT not in output.parents, "release ZIP must be written outside the repository")
    build_archive(revision, output)
    check_archive(output, revision)

    with tempfile.TemporaryDirectory(prefix="wineauction-repro-") as directory:
        repeat = Path(directory) / "repeat.zip"
        build_archive(revision, repeat)
        require(sha256(output) == sha256(repeat), "rebuilding the same commit did not produce an identical ZIP")

    print(f"Verified WineAuction {VERSION} package from {revision}")
    print(f"ZIP: {output}")
    print(f"SHA-256: {sha256(output)}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, subprocess.CalledProcessError, RuntimeError, zipfile.BadZipFile) as error:
        print(f"Release package check failed: {error}", file=sys.stderr)
        raise SystemExit(1)
