#!/usr/bin/env python3
"""Build and verify the OpenAI upload ZIP from one clean committed revision."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from build_release import ROOT, SECRET, VERSION, git, require, sha256

PREFIX = "wineauction-plugin/"
OVERLAY = "openai/"
REFERENCE_SKILL = "skills/wineauction-reference/"
REFERENCE_LINK = "../wineauction-reference/"
SHARED_LINK = "../../shared/"
DROPPED_SKILL = "skills/auction-lots/"
SHIPPED = ("plugin.json", "mcp.json", "LICENSE", "README.md", "assets/", "skills/", "shared/")
APP_NAME = "app-6a3f607100d48191814734d4a44e75c0"
MARKDOWN_LINK = re.compile(r"\]\(([^)\s]+)\)")
RETIRED_NAME = re.compile(rb"auction-lots|wineauction-reference")
RELATIVE_PATH = re.compile(r"(?<![\w.])(\.\./[\w./-]*\w)")
ZIP_TIME = (2026, 1, 1, 0, 0, 0)


def read_tracked(revision: str) -> dict[str, tuple[bytes, int]]:
    files = {}
    for line in git("ls-tree", "-r", revision).splitlines():
        meta, path = line.split("\t", 1)
        mode = int(meta.split()[0], 8)
        content = subprocess.run(
            ["git", "show", f"{revision}:{path}"], cwd=ROOT, check=True, capture_output=True
        ).stdout
        files[path] = (content, mode)
    return files


def build_files(revision: str) -> dict[str, tuple[bytes, int]]:
    tracked = read_tracked(revision)
    files: dict[str, tuple[bytes, int]] = {}
    for path, (content, mode) in tracked.items():
        if path.startswith(DROPPED_SKILL):
            continue
        if path.startswith(REFERENCE_SKILL):
            relative = path.removeprefix(REFERENCE_SKILL)
            if relative == "SKILL.md" or relative.startswith("agents/"):
                continue
            path = "shared/" + relative
        if not path.startswith(SHIPPED):
            continue
        if path.endswith(".md") and path.startswith(("skills/", "shared/")):
            content = content.replace(REFERENCE_LINK.encode(), SHARED_LINK.encode())
        files[path] = (content, mode)
    overlay = {p.removeprefix(OVERLAY): v for p, v in tracked.items() if p.startswith(OVERLAY)}
    require(overlay, "openai/ overlay is empty")
    for path, value in overlay.items():
        require(path in files, f"overlay file has no counterpart in the package: {path}")
        files[path] = value
    return files


def write_archive(files: dict[str, tuple[bytes, int]], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.unlink(missing_ok=True)
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files):
            content, mode = files[path]
            entry = zipfile.ZipInfo(PREFIX + path, ZIP_TIME)
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = (0o100755 if mode & 0o111 else 0o100644) << 16
            archive.writestr(entry, content)


def check_links(files: dict[str, tuple[bytes, int]]) -> None:
    for path, (content, _) in files.items():
        if not path.endswith(".md"):
            continue
        text = content.decode("utf-8")
        local_links = [t for t in MARKDOWN_LINK.findall(text) if not re.match(r"[a-z][a-z0-9+.-]*:|#", t)]
        for target in local_links + RELATIVE_PATH.findall(text):
            resolved = (Path(path).parent / target.split("#")[0]).as_posix()
            parts: list[str] = []
            for part in resolved.split("/"):
                if part == "..":
                    require(bool(parts), f"{path} links outside the package: {target}")
                    parts.pop()
                elif part != ".":
                    parts.append(part)
            require("/".join(parts) in files, f"{path} links to a missing path: {target}")


def check_package(files: dict[str, tuple[bytes, int]]) -> None:
    paths = set(files)
    require(not any(p.startswith(DROPPED_SKILL) for p in paths), "auction-lots skill is still packaged")
    require(not any(p.startswith(REFERENCE_SKILL) for p in paths), "wineauction-reference is still packaged")
    require("shared/SKILL.md" not in paths and not any(p.startswith("shared/agents/") for p in paths), "shared/ kept skill files")
    require(not any(p.startswith(OVERLAY) for p in paths), "overlay folder leaked into the package")
    for path, (content, _) in files.items():
        require(SECRET.search(content) is None, f"secret-like material found in {path}")
        require(RETIRED_NAME.search(content) is None, f"{path} still references a removed skill")
    check_links(files)

    import json

    plugin = json.loads(files["plugin.json"][0])
    require(plugin.get("name") == APP_NAME, "OpenAI package must use the existing app name")
    require(plugin.get("version") == VERSION, f"OpenAI manifest version is not {VERSION}")
    mcp = json.loads(files["mcp.json"][0])
    server = mcp.get("mcpServers", {}).get("wineauction", {})
    require(server.get("url") == "https://wineauction.ai/api/mcp", "MCP URL changed")
    require("extensions" not in server, "OpenAI MCP config must not declare its own auth")
    skills = {p.split("/")[1] for p in paths if p.startswith("skills/")}
    require(skills == {"restaurant-wine-list", "merchant-offer-check", "wine-info", "cellar-valuation"}, f"unexpected skills: {sorted(skills)}")
    for skill in skills:
        require(f"skills/{skill}/SKILL.md" in paths, f"{skill} has no SKILL.md")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path.home() / "Downloads" / f"wineauction-plugin-{VERSION}-openai.zip",
        help="ZIP destination (defaults to ~/Downloads)",
    )
    parser.add_argument("--expected-head", help="require HEAD to match this commit SHA")
    args = parser.parse_args()

    revision = git("rev-parse", "--verify", "HEAD^{commit}")
    if args.expected_head and args.expected_head != revision:
        raise RuntimeError(f"expected HEAD {args.expected_head}, found {revision}")
    require(not git("status", "--porcelain", "--untracked-files=normal"), "packaging requires a clean working tree")
    output = args.output.expanduser().resolve()
    require(ROOT not in output.parents, "OpenAI ZIP must be written outside the repository")

    files = build_files(revision)
    check_package(files)
    write_archive(files, output)
    with zipfile.ZipFile(output) as archive:
        names = archive.namelist()
        require(all(n.startswith(PREFIX) and not n.endswith("/") for n in names), "ZIP has directory entries or a wrong root")
        require({n.removeprefix(PREFIX) for n in names} == set(files), "ZIP contents differ from the built tree")
    with tempfile.TemporaryDirectory(prefix="wineauction-openai-repro-") as directory:
        repeat = Path(directory) / "repeat.zip"
        write_archive(build_files(revision), repeat)
        require(sha256(output) == sha256(repeat), "rebuilding the same commit did not produce an identical ZIP")

    print(f"Verified WineAuction {VERSION} OpenAI package from {revision}")
    print(f"ZIP: {output}")
    print(f"SHA-256: {sha256(output)}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, subprocess.CalledProcessError, RuntimeError, zipfile.BadZipFile, ValueError) as error:
        print(f"OpenAI package check failed: {error}", file=sys.stderr)
        raise SystemExit(1)
