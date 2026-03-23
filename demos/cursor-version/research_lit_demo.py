"""
ARIS /research-lit Skill 演示代码 — Cursor 版本

模拟 ARIS 中 /research-lit Skill 的完整流程：
1. 多源文献搜索（arXiv API + WebSearch 模拟）
2. 文献去重与分类
3. 调用 GPT-5.4 做综合分析（预录制）
4. 输出结构化文献综述

用法:
    python research_lit_demo.py "your research topic"
    python research_lit_demo.py --demo              # 查看预录制的完整演示
    python research_lit_demo.py "topic" --arxiv-only # 只搜 arXiv（真实API调用）
    python research_lit_demo.py "topic" --save       # 保存结果到 LITERATURE_SUMMARY.md
"""

import sys
import io
import argparse
import json
import os
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, io.UnsupportedOperation):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

try:
    from arxiv_search_demo import search_arxiv
except ImportError:
    search_arxiv = None


SIMULATED_WEB_RESULTS = {
    "virtual cell digital twin drug toxicity": [
        {
            "title": "TwinCell: Large-scale causal cell model for therapeutic target prioritization",
            "source": "bioRxiv 2026",
            "url": "https://doi.org/10.1101/2026.01.xxx",
            "relevance": "HIGH",
            "summary": "Integrates single-cell foundation model embeddings with multi-omic interactome data. "
                        "Causal inference for target prioritization. Most direct competitor.",
        },
        {
            "title": "VCWorld: White-box cell simulator with structured biological knowledge and LLM",
            "source": "OpenReview 2025/2026",
            "url": "https://openreview.net/forum?id=xxx",
            "relevance": "HIGH",
            "summary": "Combines mechanistic models with LLM for interpretable perturbation prediction. "
                        "White-box approach contrasts with black-box deep learning.",
        },
        {
            "title": "GENEVA: Scalable single-cell platform for drug response studies",
            "source": "Nature Cancer 2026",
            "url": "https://doi.org/10.1038/s43018-026-xxx",
            "relevance": "MEDIUM",
            "summary": "Multi-patient cell line panel for drug response. More experimental than computational.",
        },
        {
            "title": "AI-driven Virtual Cell Models: Review of multi-modal omics integration",
            "source": "npj Digital Medicine 2025",
            "url": "https://doi.org/10.1038/s41746-025-xxx",
            "relevance": "HIGH",
            "summary": "Comprehensive review covering deep generative models, GNNs, PINNs for virtual cells. "
                        "Defines the landscape and gaps.",
        },
    ],
    "default": [
        {
            "title": "Foundation Models for Single-Cell Biology: A Survey",
            "source": "Nature Methods 2025",
            "url": "https://doi.org/10.1038/s41592-025-xxx",
            "relevance": "MEDIUM",
            "summary": "Survey of foundation models (scGPT, scBERT, Geneformer) for single-cell analysis.",
        },
        {
            "title": "Benchmarking Perturbation Response Prediction Methods",
            "source": "Nature Biotechnology 2025",
            "url": "https://doi.org/10.1038/s41587-025-xxx",
            "relevance": "HIGH",
            "summary": "Systematic benchmark of CPA, GEARS, scGen, biolord on perturbation prediction tasks.",
        },
    ],
}


def simulate_web_search(query: str) -> list[dict]:
    for key in SIMULATED_WEB_RESULTS:
        if key != "default" and any(w in query.lower() for w in key.split()):
            return SIMULATED_WEB_RESULTS[key]
    return SIMULATED_WEB_RESULTS["default"]


def classify_papers(arxiv_papers: list[dict], web_papers: list[dict]) -> dict:
    categories = {
        "Digital Twin Infrastructure": [],
        "Single-Cell Representation & Perturbation": [],
        "Mechanistic / Biophysical Modeling": [],
        "Drug Screening & Toxicology": [],
        "Foundation Models & Benchmarks": [],
        "Other": [],
    }

    keywords_map = {
        "Digital Twin Infrastructure": ["digital twin", "DTaaS", "cost reduction"],
        "Single-Cell Representation & Perturbation": [
            "single cell", "scRNA", "perturbation", "CPA", "GEARS",
            "scMamba", "CellPhoneDB", "omics integration",
        ],
        "Mechanistic / Biophysical Modeling": [
            "Hodgkin-Huxley", "biophysical", "parameter estimation",
            "gene expression", "dynamical", "ODE", "mechanistic",
        ],
        "Drug Screening & Toxicology": [
            "drug", "toxicity", "screening", "virtual cell", "TwinCell",
            "VCWorld", "GENEVA", "compound",
        ],
        "Foundation Models & Benchmarks": [
            "foundation model", "benchmark", "survey", "review",
            "scGPT", "Geneformer",
        ],
    }

    all_papers = []
    for p in arxiv_papers:
        all_papers.append({"title": p["title"], "source": f"arXiv {p['id']}", "type": "arxiv"})
    for p in web_papers:
        all_papers.append({"title": p["title"], "source": p["source"], "type": "web"})

    for paper in all_papers:
        classified = False
        for cat, kws in keywords_map.items():
            if any(kw.lower() in paper["title"].lower() for kw in kws):
                categories[cat].append(paper)
                classified = True
                break
        if not classified:
            categories["Other"].append(paper)

    return categories


def display_full_demo():
    print("""
================================================================================
  ARIS /research-lit — 完整演示 (Pre-recorded from 2026-03-15)
================================================================================

研究主题: "virtual cell digital twin single cell omics drug toxicity"

================================================================================
  Step 1: 多源文献搜索
================================================================================

  来源 1: arXiv API
  ─────────────────
  搜索词 1: "virtual cell digital twin drug screening"     → 3 篇
  搜索词 2: "single cell omics biophysical modeling"       → 3 篇
  搜索词 3: "Hodgkin-Huxley parameter inference"           → 3 篇
  去重后: 9 篇独立论文

  来源 2: WebSearch (Google Scholar / Semantic Scholar)
  ──────────────────────────────────────────────────────
  发现 4 篇 arXiv 未覆盖的重要工作:
    1. TwinCell (bioRxiv 2026)     — 大规模因果细胞模型
    2. VCWorld (OpenReview 2025)   — 白盒细胞仿真器+LLM
    3. GENEVA (Nature Cancer 2026) — 单细胞药物反应平台
    4. AI Virtual Cell Review (npj 2025) — 综述

  来源 3: 本地 papers/ 目录
  ──────────────────────────
  扫描到 3 个 PDF, 提取前 3 页信息
  合计: 9 (arXiv) + 4 (Web) + 3 (Local) = 16 篇独立论文

================================================================================
  Step 2: 文献分类与分组
================================================================================

  Category 1: Digital Twin Infrastructure (2 papers)
  ├── DTaaS: Digital Twin as a Service (2023)
  └── DT Cost Reduction (2021)

  Category 2: Single-Cell Representation & Perturbation (3 papers)
  ├── scMamba: Scalable Foundation Model for Multi-Omics (2025)
  ├── CellPhoneDB v5: Cell-Cell Communication (2023)
  └── Systems Biophysics of Gene Expression (2013)

  Category 3: Mechanistic / Biophysical Modeling (3 papers)
  ├── Self-organizing state-space model for HH (2011)
  ├── Structure-preserving integrators for HH (2018)
  └── Lie Group Basis of Neuronal Membrane (2026)

  Category 4: Drug Screening & Toxicology (5 papers)
  ├── TwinCell (bioRxiv 2026) ← 最重要竞争者
  ├── VCWorld (OpenReview 2025)
  ├── GENEVA (Nature Cancer 2026)
  ├── Fragment Descriptors in Virtual Screening (2013)
  └── AI Virtual Cell Models Review (npj 2025)

  Category 5: Foundation Models & Benchmarks (3 papers)
  ├── Foundation Models Survey (Nature Methods 2025)
  ├── Perturbation Benchmark (Nature Biotech 2025)
  └── Quantum to Classical NN for Drug Toxicity (2024)

================================================================================
  Step 3: GPT-5.4 综合分析
================================================================================

  发送 16 篇论文的摘要和分类信息给 GPT-5.4 xhigh...
  [Codex MCP] 发送中... (xhigh 模式, 约 45 秒)
  [Codex MCP] 收到响应

  ── 4 大研究方向 ──

  方向 1: 数字孪生基础设施/经济学
    代表: DTaaS, DT Cost Reduction
    与我们的关系: 关注部署而非建模, 不直接相关

  方向 2: 单细胞表示与微环境推断
    代表: scMamba, CellPhoneDB v5
    与我们的关系: 最接近, 但是描述性的, 不是可执行的数字孪生

  方向 3: 机制动力学建模
    代表: HH Parameter Estimation, Systems Biophysics
    与我们的关系: 方向正确(可解释), 但不基于现代单细胞数据

  方向 4: 化合物中心的筛选
    代表: Fragment Descriptors
    与我们的关系: 解决分子表示, 但不建模细胞状态

  ── 5 个关键空白 ──

  空白 1: 没有"可执行的因果细胞模型"能预测药物暴露如何改变单细胞轨迹
  空白 2: 没有联合建模"化合物+剂量+时间+靶点+细胞状态"
  空白 3: 时间推断很弱（大多是破坏性快照）
  空白 4: 组织毒性需要多尺度整合（细胞内+细胞间+空间）
  空白 5: 验证不足（缺不确定性量化、校准、前瞻性测试）

  ── 5 个建议的新方向 ──

  1. 扰动原生虚拟细胞孪生 — 在剂量-时间数据上训练, 以毒性终点为目标
  2. 混合机制-神经网络孪生 — 基础模型嵌入 + GRN/信号动力学 + 不确定性
  3. 空间多细胞毒性孪生 — 多组学 + 配体-受体 + 组织病理学
  4. 联合药物-细胞模型 — 连接化合物结构/靶点/细胞状态/脱靶毒性
  5. 闭环主动学习孪生 — 自动选择最优减少不确定性的下一个实验

================================================================================
  Step 4: 输出
================================================================================

  已生成:
    LITERATURE_SUMMARY.md   — 完整文献综述(表格+叙述)
    papers/search_results.json — 搜索结果结构化数据

  后续建议:
    /idea-creator  — 基于文献空白生成研究创意
    /novelty-check — 验证创意的新颖性
    /idea-discovery — 一键完成创意发现全流程

================================================================================
""")


def run_live_demo(query: str, arxiv_only: bool = False, save: bool = False):
    print(f"\n{'='*70}")
    print(f"  ARIS /research-lit — Live Demo")
    print(f"  Topic: {query}")
    print(f"{'='*70}\n")

    # Step 1: arXiv search
    print("  Step 1: Searching arXiv API...")
    arxiv_papers = []
    if search_arxiv:
        try:
            arxiv_papers = search_arxiv(query, max_results=5)
            print(f"    Found {len(arxiv_papers)} papers from arXiv")
        except Exception as e:
            print(f"    arXiv search failed: {e}")
    else:
        print("    [Skip] arxiv_search_demo.py not found in path")

    for i, p in enumerate(arxiv_papers, 1):
        print(f"    {i}. [{p['id']}] {p['title'][:70]}...")

    # Step 2: WebSearch simulation
    web_papers = []
    if not arxiv_only:
        print("\n  Step 2: Simulating WebSearch...")
        web_papers = simulate_web_search(query)
        print(f"    Found {len(web_papers)} papers from web")

        for i, p in enumerate(web_papers, 1):
            rel_color = {"HIGH": "*", "MEDIUM": " ", "LOW": "."}
            marker = rel_color.get(p["relevance"], " ")
            print(f"    {i}. [{marker}] {p['title'][:60]}... ({p['source']})")
    else:
        print("\n  Step 2: Skipped (--arxiv-only mode)")

    # Step 3: Classify
    print("\n  Step 3: Classifying papers...")
    categories = classify_papers(arxiv_papers, web_papers)

    for cat, papers in categories.items():
        if papers:
            print(f"\n    {cat} ({len(papers)} papers):")
            for p in papers:
                print(f"      - {p['title'][:60]}... [{p['source']}]")

    # Step 4: Summary
    total = len(arxiv_papers) + len(web_papers)
    print(f"\n{'='*70}")
    print(f"  Summary: {total} papers found and classified")
    print(f"{'='*70}")
    print(f"  arXiv:     {len(arxiv_papers)} papers")
    print(f"  WebSearch: {len(web_papers)} papers")
    print(f"  Categories: {sum(1 for v in categories.values() if v)} active")
    print()

    if not arxiv_only:
        print("  NOTE: WebSearch results are simulated in this demo.")
        print("  In real /research-lit, Claude uses actual web search + GPT-5.4 analysis.")
        print()

    print("  Next ARIS skills:")
    print(f'    /idea-creator  — generate ideas based on gaps found')
    print(f'    /novelty-check — verify idea novelty')
    print(f'    /idea-discovery — full idea discovery pipeline')

    if save:
        output_file = "LITERATURE_SUMMARY_demo.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# Literature Summary: {query}\n\n")
            f.write(f"Generated by ARIS /research-lit demo on {time.strftime('%Y-%m-%d %H:%M')}\n\n")

            f.write("## arXiv Papers\n\n")
            for p in arxiv_papers:
                f.write(f"- **{p['title']}** ({p['published']})\n")
                f.write(f"  - ID: {p['id']}\n")
                f.write(f"  - Categories: {', '.join(p.get('categories', [])[:3])}\n\n")

            f.write("## Web Sources\n\n")
            for p in web_papers:
                f.write(f"- **{p['title']}** ({p['source']})\n")
                f.write(f"  - Relevance: {p['relevance']}\n")
                f.write(f"  - Summary: {p['summary']}\n\n")

            f.write("## Categories\n\n")
            for cat, papers in categories.items():
                if papers:
                    f.write(f"### {cat}\n\n")
                    for p in papers:
                        f.write(f"- {p['title']} [{p['source']}]\n")
                    f.write("\n")

        print(f"\n  Results saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="ARIS /research-lit Skill Demo")
    parser.add_argument("topic", nargs="?", default=None, help="Research topic to search")
    parser.add_argument("--demo", action="store_true", help="Show pre-recorded full demo")
    parser.add_argument("--arxiv-only", action="store_true", help="Only search arXiv (skip web)")
    parser.add_argument("--save", action="store_true", help="Save results to LITERATURE_SUMMARY_demo.md")
    args = parser.parse_args()

    if args.demo or args.topic is None:
        display_full_demo()
    else:
        run_live_demo(args.topic, arxiv_only=args.arxiv_only, save=args.save)


if __name__ == "__main__":
    main()
