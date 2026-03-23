"""
ARIS /arxiv Skill 演示代码 — Cursor 版本

这个脚本模拟了 ARIS 中 /arxiv Skill 的核心功能：
1. 构建 arXiv API 查询
2. 通过代理发送请求
3. 解析 XML 响应
4. 输出结构化论文列表

在真实的 /arxiv Skill 中，Claude Code 会自动执行这些步骤。
在 Cursor 中，你可以直接运行这个脚本来体验相同的功能。

用法:
    python arxiv_search_demo.py "your search query"
    python arxiv_search_demo.py "drug toxicity prediction" --max 10
    python arxiv_search_demo.py "2301.07041" --download
"""

import sys
import io
import json
import argparse
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import ssl
import os
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, io.UnsupportedOperation):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ssl._create_default_https_context = ssl._create_unverified_context

NS = "http://www.w3.org/2005/Atom"
PROXY_URL = "http://127.0.0.1:7897"
PAPER_DIR = "papers"


def search_arxiv(query: str, max_results: int = 5) -> list[dict]:
    encoded_query = urllib.parse.quote(query)
    url = (
        f"http://export.arxiv.org/api/query"
        f"?search_query={encoded_query}"
        f"&start=0&max_results={max_results}"
        f"&sortBy=relevance&sortOrder=descending"
    )

    proxy = urllib.request.ProxyHandler({
        "http": PROXY_URL,
        "https": PROXY_URL,
    })
    opener = urllib.request.build_opener(proxy)

    try:
        with opener.open(url, timeout=30) as r:
            data = r.read()
    except Exception:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = r.read()

    root = ET.fromstring(data)
    papers = []

    for entry in root.findall(f"{{{NS}}}entry"):
        aid = entry.findtext(f"{{{NS}}}id", "").split("/abs/")[-1].split("v")[0]
        title = (entry.findtext(f"{{{NS}}}title", "") or "").strip().replace("\n", " ")
        authors = [a.findtext(f"{{{NS}}}name", "") for a in entry.findall(f"{{{NS}}}author")]
        published = entry.findtext(f"{{{NS}}}published", "")[:10]
        cats = [c.get("term", "") for c in entry.findall(f"{{{NS}}}category")]
        abstract = (entry.findtext(f"{{{NS}}}summary", "") or "").strip().replace("\n", " ")

        papers.append({
            "id": aid,
            "title": title,
            "authors": authors,
            "published": published,
            "categories": cats,
            "abstract": abstract,
            "pdf_url": f"https://arxiv.org/pdf/{aid}.pdf",
            "abs_url": f"https://arxiv.org/abs/{aid}",
        })

    return papers


def download_paper(arxiv_id: str, output_dir: str = PAPER_DIR) -> str:
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{arxiv_id.replace('/', '_')}.pdf")

    if os.path.exists(out_path):
        print(f"  Already exists: {out_path}")
        return out_path

    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    req = urllib.request.Request(pdf_url, headers={"User-Agent": "aris-demo/1.0"})

    proxy = urllib.request.ProxyHandler({"http": PROXY_URL, "https": PROXY_URL})
    opener = urllib.request.build_opener(proxy)

    try:
        with opener.open(req, timeout=60) as r:
            content = r.read()
    except Exception:
        with urllib.request.urlopen(req, timeout=60) as r:
            content = r.read()

    if len(content) < 10240:
        print(f"  Warning: file too small ({len(content)} bytes), might be an error page")
        return ""

    with open(out_path, "wb") as f:
        f.write(content)

    print(f"  Downloaded: {out_path} ({len(content) // 1024} KB)")
    return out_path


def display_results(papers: list[dict], query: str):
    print(f"\n{'='*80}")
    print(f"  arXiv Search Results: '{query}'")
    print(f"  Found {len(papers)} papers")
    print(f"{'='*80}\n")

    for i, p in enumerate(papers, 1):
        auth_str = ", ".join(p["authors"][:3])
        if len(p["authors"]) > 3:
            auth_str += " et al."

        abs_short = p["abstract"][:200] + "..." if len(p["abstract"]) > 200 else p["abstract"]

        print(f"--- Paper {i} ---")
        print(f"  arXiv ID : {p['id']}")
        print(f"  Title    : {p['title']}")
        print(f"  Authors  : {auth_str}")
        print(f"  Date     : {p['published']}")
        print(f"  Category : {', '.join(p['categories'][:3])}")
        print(f"  PDF      : {p['pdf_url']}")
        print(f"  Abstract : {abs_short}")
        print()

    print(f"{'='*80}")
    print("  Next ARIS skills:")
    print("    /research-lit  — multi-source literature review")
    print("    /novelty-check — verify your idea is novel")
    print("    /idea-creator  — generate research ideas")
    print(f"{'='*80}")


def main():
    parser = argparse.ArgumentParser(description="ARIS /arxiv Skill Demo")
    parser.add_argument("query", help="Search query or arXiv ID")
    parser.add_argument("--max", type=int, default=5, help="Max results (default: 5)")
    parser.add_argument("--download", action="store_true", help="Download PDF(s)")
    parser.add_argument("--download-all", action="store_true", help="Download all result PDFs")
    parser.add_argument("--dir", default=PAPER_DIR, help="Output directory for PDFs")
    args = parser.parse_args()

    print(f"\nSearching arXiv for: '{args.query}' (max: {args.max})...\n")

    papers = search_arxiv(args.query, args.max)

    if not papers:
        print("No papers found.")
        return

    display_results(papers, args.query)

    if args.download and papers:
        print(f"\nDownloading first paper: {papers[0]['id']}...")
        download_paper(papers[0]["id"], args.dir)

    if args.download_all:
        print(f"\nDownloading all {len(papers)} papers...")
        for p in papers:
            download_paper(p["id"], args.dir)
            time.sleep(1)

    results_file = os.path.join(args.dir, "search_results.json") if args.download or args.download_all else None
    if results_file:
        os.makedirs(os.path.dirname(results_file) or ".", exist_ok=True)
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)
        print(f"\nResults saved to: {results_file}")


if __name__ == "__main__":
    main()
