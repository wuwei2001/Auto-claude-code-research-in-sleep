"""
ARIS /novelty-check Skill 演示代码 — Cursor 版本

模拟 ARIS 中 /novelty-check Skill 的核心功能：
通过 Codex MCP 调用 GPT-5.4 xhigh 验证研究创意的新颖性。

用法:
    python novelty_check_demo.py --demo          # 查看预录制的演示输出
    python novelty_check_demo.py "你的创意描述"   # 实际调用 Codex（需要 Codex CLI）
"""

import sys
import io
import argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def display_demo_output():
    """展示 2026-03-15 实际通过 Codex MCP 获得的新颖性验证结果"""
    print("""
================================================================================
  ARIS /novelty-check — Demo Output (Pre-recorded from 2026-03-15)
================================================================================

被验证的创意:
  "Perturbation-Native Virtual Cell Twin (PNVCT)"
  直接在剂量-时间分辨的单细胞扰动数据集上训练虚拟细胞数字孪生体，
  以毒性终点作为学习目标。

判定结果: PARTIALLY NOVEL（部分新颖）

================================================================================
  GPT-5.4 找到的 8 个最相似已有工作
================================================================================

| # | 工作名称                  | 年份    | 与我们的差异                      |
|---|--------------------------|---------|----------------------------------|
| 1 | chemCPA / CPA            | 2022-23 | 已做"直接在扰动数据上训练"        |
| 2 | GEARS                    | 2023    | 已报告"以细胞适应性为目标训练"    |
| 3 | biolord                  | 2024    | 反事实单细胞建模，含药物/剂量     |
| 4 | PerturbNet               | 2025    | 模块化扰动表示+剂量协变量         |
| 5 | State (Arc Institute)    | 2025    | 最近竞争者！扰动原生虚拟细胞模型  |
| 6 | SIMCO                    | 2025    | 单细胞数字孪生+结果预测           |
| 7 | scOTM                    | 2025    | 已使用基础模型嵌入               |
| 8 | Decoding Stress States   | 2025    | 最接近的毒理学单细胞工作          |

================================================================================
  各差异化点判定
================================================================================

差异化点 1: 直接在扰动数据上训练
  → ❌ 不新颖 (CPA 2022 已做)

差异化点 2: 毒性终点作为损失函数
  → ⚠️ 部分新颖 (最强的剩余角度)

差异化点 3: 基础模型嵌入
  → ❌ 不新颖 (scOTM 已做)

差异化点 4: 剂量-时间分辨率
  → ❌ 不新颖 (CPA 已做)

================================================================================
  GPT-5.4 建议的更安全声称
================================================================================

"一个端到端的毒性监督虚拟细胞模型，使用剂量和时间分辨的单细胞扰动数据
 作为原生训练信号，而不是主要优化转录组重构。"

================================================================================
  进一步差异化建议
================================================================================

1. 让毒性监督真正成为主要目标（预测存活率/凋亡/坏死）
2. 显式建模连续的剂量-时间轨迹
3. 将潜在空间与不良结果通路（AOP）绑定
4. 展示分布外泛化（未见化合物/剂量/时间/细胞）
5. 前瞻性验证：证明"毒性优先"优于"转录组优先"

================================================================================
  竞争时间线
================================================================================

2019 ──→ scGen (直接扰动响应预测)
2022 ──→ chemCPA/CPA (扰动原生+剂量时间)
2023 ──→ GEARS/biolord (表型/反事实预测)
2025 Jun ──→ State/PerturbNet (大规模虚拟细胞)
2025 ──→ SIMCO (数字孪生+结果预测)

GPT-5.4 推断:
  "如果'State/SIMCO for toxicology'论文还没在审稿中，
   它很可能很快就会出现。"

================================================================================
  完整结果请查看 README.md 第十四章
================================================================================
""")


def main():
    parser = argparse.ArgumentParser(description="ARIS /novelty-check Skill Demo")
    parser.add_argument("idea", nargs="?", default=None, help="Research idea to check")
    parser.add_argument("--demo", action="store_true", help="Show pre-recorded demo")
    args = parser.parse_args()

    if args.demo or args.idea is None:
        display_demo_output()
    else:
        print(f"\nTo actually run novelty check via Codex MCP:")
        print(f"  1. Start Claude Code: claude")
        print(f'  2. Run: /novelty-check "{args.idea}"')
        print(f"\nOr in Cursor AI chat:")
        print(f'  "请用 novelty-check skill 验证以下创意的新颖性: {args.idea}"')
        print(f"\nFor pre-recorded demo output, run: python novelty_check_demo.py --demo")


if __name__ == "__main__":
    main()
