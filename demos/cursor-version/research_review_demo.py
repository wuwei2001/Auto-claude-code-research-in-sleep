"""
ARIS /research-review Skill 演示代码 — Cursor 版本

模拟 ARIS 中 /research-review Skill 的核心功能：
通过 Codex MCP 调用 GPT-5.4 xhigh 做深度审稿。

在 Cursor 中使用时：
  1. 直接运行此脚本（需要 Codex CLI）
  2. 或者在 Cursor AI 对话中说："用 Codex MCP 审查我的研究"

用法:
    python research_review_demo.py "你的研究描述或文件路径"
    python research_review_demo.py PAPER_PLAN.md
"""

import sys
import io
import os
import argparse
import json
import subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

CODEX_PATH = r"E:\software\codex"

REVIEW_PROMPT_TEMPLATE = """Please act as a senior ML reviewer (NeurIPS/ICML level).

I am reviewing the following research for a top venue submission:

---
{research_content}
---

Please provide:
1. **Score** (1-10 for a top venue like NeurIPS/ICML)
2. **Strengths** (3-5 bullet points)
3. **Weaknesses** (ranked by severity, 5-8 items)
4. **For each weakness**: specify the MINIMUM fix (experiment, analysis, or reframing)
5. **Verdict**: Is this READY for submission? (Yes/No/Almost)
6. **Minimum viable improvement plan**: smallest set of changes to make this publishable

Be brutally honest. The goal is to improve, not to be polite.
"""


def load_research_content(input_arg: str) -> str:
    if os.path.isfile(input_arg):
        with open(input_arg, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"  Loaded from file: {input_arg} ({len(content)} chars)")
        return content
    return input_arg


def call_codex_review(research_content: str) -> str:
    prompt = REVIEW_PROMPT_TEMPLATE.format(research_content=research_content)

    print("\n  Sending to GPT-5.4 xhigh via Codex MCP...")
    print("  (This may take 30-120 seconds for xhigh reasoning depth)\n")

    try:
        result = subprocess.run(
            [CODEX_PATH, "-p", prompt, "--json"],
            capture_output=True,
            text=True,
            timeout=300,
            encoding="utf-8",
        )
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Codex error (exit code {result.returncode}): {result.stderr}"
    except FileNotFoundError:
        return "ERROR: Codex CLI not found at " + CODEX_PATH
    except subprocess.TimeoutExpired:
        return "ERROR: Codex timed out after 5 minutes"
    except Exception as e:
        return f"ERROR: {e}"


def display_demo_output():
    """展示预录制的演示输出（当 Codex 不可用时使用）"""
    print("""
================================================================================
  ARIS /research-review — Demo Output (Pre-recorded)
================================================================================

以下是 2026-03-15 实际通过 Codex MCP 调用 GPT-5.4 xhigh 获得的审稿结果：

Score: 3/10 (Not Ready for NeurIPS/ICML)

Strengths:
  1. 问题重要：把单细胞状态与扰动响应联系起来有科学意义
  2. 机制角度正确：生物物理仿真结构可以带来真正的优势
  3. Patch-seq 起点合理：同时包含转录组和电生理
  4. 异质性感知的筛选是更好的框架
  5. 平台愿景有吸引力

Weaknesses (ranked by severity):
  1. [FATAL] 核心映射不可识别 — mRNA ≠ 蛋白质 ≠ 功能活性
     Fix: 改为预测可观测表型或参数后验分布
  
  2. [FATAL] 监督目标可能循环 — 用模型拟合结果训练另一个模型
     Fix: 用直接可测量的指标做基准测试
  
  3. [FATAL] 评估不可信 — 只有训练 R²，没有测试集
     Fix: 报告留出测试集表现 + 基线对比
  
  4. [FATAL] 仿真声称缺乏验证 — 仿真结果未与实验数据对比
     Fix: 端到端验证一个真实药物/毒物
  
  5. [MAJOR] 论文范围过大 — 5种细胞类型太多
     Fix: 砍到1种细胞类型 + 1个扰动用例
  
  6. [MAJOR] ML 贡献不清晰
     Fix: 定义一个清晰的技术贡献并做消融实验
  
  7. [MAJOR] 性别差异结果不够严谨
     Fix: 补充样本量、置信区间、统计检验
  
  8. [MAJOR] 缺乏不确定性量化
     Fix: 预测参数分布 + 通过仿真传播不确定性

Verdict: NOT READY

Minimum viable improvement plan:
  "删掉 70-80% 的范围，令人信服地证明一个窄论点"

================================================================================
  完整结果请查看 README.md 第三章
================================================================================
""")


def main():
    parser = argparse.ArgumentParser(description="ARIS /research-review Skill Demo")
    parser.add_argument(
        "research",
        nargs="?",
        default=None,
        help="Research description (text or file path)",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Show pre-recorded demo output (no Codex needed)",
    )
    args = parser.parse_args()

    print("\n" + "=" * 80)
    print("  ARIS /research-review Skill Demo")
    print("=" * 80)

    if args.demo or args.research is None:
        display_demo_output()
        return

    research_content = load_research_content(args.research)

    if len(research_content) < 50:
        print("  Warning: Research description is very short. More detail = better review.")

    review = call_codex_review(research_content)

    print("\n" + "=" * 80)
    print("  GPT-5.4 Review Result")
    print("=" * 80)
    print(review)

    output_file = "review_result.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# Research Review Result\n\n")
        f.write(f"**Date**: {__import__('datetime').datetime.now().isoformat()}\n\n")
        f.write(f"## Input\n\n{research_content[:500]}...\n\n")
        f.write(f"## Review\n\n{review}\n")
    print(f"\n  Review saved to: {output_file}")


if __name__ == "__main__":
    main()
