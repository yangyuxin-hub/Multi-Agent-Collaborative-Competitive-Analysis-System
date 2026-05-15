#!/usr/bin/env python3
"""Validate competitive-analysis report artifacts.

This is a lightweight structural check for case outputs. It does not judge
fact accuracy; high-risk facts still require source review.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_MD_SECTIONS = [
    "执行摘要",
    "竞品概览",
    "功能矩阵",
    "定价矩阵",
    "用户痛点",
    "SWOT",
    "战略建议",
]


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def check_md(path: Path, failures: list[str], warnings: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    h2_lines = re.findall(r"^##\s+(.+)$", text, flags=re.MULTILINE)

    numbered = [h for h in h2_lines if re.match(r"^\d+\.", h)]
    if len(numbered) != 7:
        fail(f"{path}: expected 7 numbered sections, found {len(numbered)}", failures)

    for keyword in REQUIRED_MD_SECTIONS:
        if keyword not in text:
            fail(f"{path}: missing required section keyword '{keyword}'", failures)

    if "共性洞察" not in text and "横向规律" not in text:
        fail(f"{path}: missing cross-competitor insight", failures)

    if "事实风险" not in text and "待验证" not in text and "待人工" not in text:
        warnings.append(f"{path}: no fact-risk appendix/checklist found")

    source_like = re.findall(r"https?://", text)
    if len(source_like) < 10:
        warnings.append(f"{path}: low source URL count ({len(source_like)})")


def check_html(path: Path, failures: list[str], warnings: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    h2_lines = re.findall(r"<h2[^>]*>\s*([^<]+)\s*</h2>", text, flags=re.IGNORECASE)
    numbered = [h for h in h2_lines if re.match(r"^\d+\.", h)]

    if len(numbered) != 7:
        fail(f"{path}: expected 7 numbered h2 sections, found {len(numbered)}", failures)

    if "quadrantChart" not in text:
        fail(f"{path}: missing Mermaid quadrantChart", failures)

    if "swot-grid" not in text:
        fail(f"{path}: missing SWOT grid", failures)

    if "price-bar-chart" not in text:
        fail(f"{path}: missing pricing bar chart", failures)

    if "strategy-card" not in text:
        fail(f"{path}: missing strategy cards", failures)

    if ".table-wrap" not in text:
        warnings.append(f"{path}: no .table-wrap CSS found; wide tables may overflow on mobile")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--md", type=Path, required=True)
    parser.add_argument("--html", type=Path, required=True)
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []

    if not args.md.exists():
        fail(f"missing markdown file: {args.md}", failures)
    else:
        check_md(args.md, failures, warnings)

    if not args.html.exists():
        fail(f"missing html file: {args.html}", failures)
    else:
        check_html(args.html, failures, warnings)

    for warning in warnings:
        print(f"WARN: {warning}")
    for failure in failures:
        print(f"FAIL: {failure}")

    if failures:
        return 1

    print("OK: report artifacts passed structural validation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
