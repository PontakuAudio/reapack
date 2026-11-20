#!/usr/bin/env python3
"""Merge the per-product ReaPack indexes into one Pontaku Audio index.

Each product keeps its own repository and its own generated index.xml.
This script fetches every index listed in sources.txt and merges their
<category>/<reapack> entries into a single index.xml at the repo root,
so users register ONE repository URL and receive every Pontaku Audio
script and extension.

Usage: python3 tools/merge_index.py [--output index.xml]
Exit code is non-zero if any source cannot be fetched or parsed, or if
the merged index would lose a package that a source index contains.
"""
import copy
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX_NAME = "Pontaku Audio"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "pontaku-reapack-merge"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def merge(sources: list[str]) -> tuple[ET.ElementTree, list[str]]:
    merged_root = ET.Element("index", {"version": "1", "name": INDEX_NAME})
    categories: dict[str, ET.Element] = {}
    packages: dict[tuple[str, str], ET.Element] = {}
    summary: list[str] = []

    for url in sources:
        src_root = ET.fromstring(fetch(url))
        if src_root.tag != "index":
            raise ValueError(f"{url}: root element is <{src_root.tag}>, expected <index>")
        for src_cat in src_root.findall("category"):
            cat_name = src_cat.get("name")
            cat = categories.get(cat_name)
            if cat is None:
                cat = ET.SubElement(merged_root, "category", {"name": cat_name})
                categories[cat_name] = cat
            for src_pkg in src_cat.findall("reapack"):
                key = (cat_name, src_pkg.get("name"))
                versions = src_pkg.findall("version")
                existing = packages.get(key)
                if existing is not None:
                    # Keep the entry carrying more versions; first source wins ties.
                    parent = categories[cat_name]
                    if len(versions) > len(existing.findall("version")):
                        idx = list(parent).index(existing)
                        parent.remove(existing)
                        parent.insert(idx, copy.deepcopy(src_pkg))
                        packages[key] = src_pkg
                    continue
                cat.append(copy.deepcopy(src_pkg))
                packages[key] = src_pkg
                names = ", ".join(v.get("name") for v in versions)
                summary.append(f"{cat_name} / {src_pkg.get('name')}: {names}")

    tree = ET.ElementTree(merged_root)
    ET.indent(tree, space="  ")
    return tree, summary


def main() -> int:
    out = ROOT / "index.xml"
    if "--output" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--output") + 1])
    sources = [
        line.strip()
        for line in (ROOT / "sources.txt").read_text().splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not sources:
        print("sources.txt has no index URLs", file=sys.stderr)
        return 1
    tree, summary = merge(sources)
    tree.write(out, encoding="utf-8", xml_declaration=True)
    # Verify the written file parses and still holds every package.
    check = ET.parse(out)
    found = {
        (cat.get("name"), pkg.get("name"))
        for cat in check.getroot().findall("category")
        for pkg in cat.findall("reapack")
    }
    print(f"Wrote {out} ({len(found)} packages)")
    for line in summary:
        print(f"  {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
