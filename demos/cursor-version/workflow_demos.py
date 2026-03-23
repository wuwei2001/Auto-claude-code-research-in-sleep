"""
ARIS 所有 Workflow 和 Skill 的模拟演示 — Cursor 版本

展示每个 Skill 的预期输入、执行过程和输出。
这些是基于 SKILL.md 文件和实际使用经验的模拟输出。

用法:
    python workflow_demos.py                 # 列出所有可演示的 Skill
    python workflow_demos.py idea-discovery  # 演示 Workflow 1
    python workflow_demos.py auto-review     # 演示 Workflow 2
    python workflow_demos.py paper-writing   # 演示 Workflow 3
    python workflow_demos.py pipeline        # 演示全流程
    python workflow_demos.py paper-plan      # 演示论文大纲
    python workflow_demos.py paper-compile   # 演示 LaTeX 编译
    python workflow_demos.py pixel-art       # 演示像素画
    python workflow_demos.py all             # 演示全部
"""

import sys
import io
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, io.UnsupportedOperation):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DEMOS = {}


def demo(name):
    def decorator(func):
        DEMOS[name] = func
        return func
    return decorator


def print_phase(phase_name, duration=""):
    print(f"\n{'='*70}")
    print(f"  {phase_name}  {duration}")
    print(f"{'='*70}")


def print_step(step):
    print(f"  >>> {step}")
    time.sleep(0.1)


@demo("idea-discovery")
def demo_idea_discovery():
    """Workflow 1: 创意发现全流程"""

    print_phase("ARIS /idea-discovery — Workflow 1 模拟演示")
    print()
    print("  输入: /idea-discovery \"virtual cell digital twin for drug toxicity\"")
    print("  预计耗时: 30-120 分钟")
    print("  输出: IDEA_REPORT.md")
    print()

    print_phase("Phase 1: 文献综述 (/research-lit)", "⏱ 5-15 min")
    print_step("搜索 arXiv API... 找到 15 篇论文")
    print_step("WebSearch 搜索 Google Scholar... 找到 8 篇")
    print_step("扫描本地 papers/ 目录... 找到 3 个 PDF")
    print_step("去重合并... 总计 22 篇独立论文")
    print_step("构建研究图景...")
    print()
    print("  📚 文献综述完成:")
    print("  主题 1: 单细胞扰动建模 (CPA, GEARS, biolord)")
    print("  主题 2: 虚拟细胞模型 (State, VCWorld, TwinCell)")
    print("  主题 3: 毒理学单细胞 (Decoding Stress States)")
    print("  主题 4: HH 参数推断")
    print("  空白: 缺乏端到端毒性监督的虚拟细胞")
    print()
    print("  🚦 检查点: AUTO_PROCEED=true, 自动继续...")

    print_phase("Phase 2: 创意生成 (/idea-creator)", "⏱ 10-30 min")
    print_step("准备上下文发送给 GPT-5.4 xhigh...")
    print_step("[Codex MCP] 发送中...")
    print_step("[Codex MCP] 收到响应")
    print_step("GPT-5.4 生成了 5 个创意")
    print_step("Claude 筛选: 可行性 + 新颖性 + 影响力")
    print()
    print("  💡 创意排名:")
    print("  1. 早期多组学轨迹预测晚期毒性 — 可行: 8/10, 影响: 8/10")
    print("  2. 稀有毒性亚群定义最有用孪生 — 可行: 8/10, 影响: 8/10")
    print("  3. 供体条件化孪生预测特异性毒性 — 可行: 6/10, 影响: 9/10")
    print()

    print_step("对 top 3 运行 pilot 实验...")
    print_step("Idea 1 pilot: 训练中... R²=0.52 (+12% over baseline) ✅ POSITIVE")
    print_step("Idea 2 pilot: 训练中... R²=0.48 (+3% over baseline) ⚠️ WEAK")
    print_step("Idea 3 pilot: 跳过 (需要多供体数据)")
    print()
    print("  🚦 检查点: AUTO_PROCEED=true, 自动选择 Idea #1...")

    print_phase("Phase 3: 新颖性验证 (/novelty-check)", "⏱ 5-15 min")
    print_step("对 Idea #1 搜索文献...")
    print_step("arXiv: 无完全匹配 ✅")
    print_step("Scholar: 2 篇相似但方法不同 ✅")
    print_step("[Codex MCP] GPT-5.4 交叉验证...")
    print_step("判定: PARTIALLY NOVEL — 需要强调毒性监督的差异化")
    print()
    print_step("对 Idea #2 搜索文献...")
    print_step("判定: NOVEL ✅")

    print_phase("Phase 4: 专家审查 (/research-review)", "⏱ 5-10 min")
    print_step("[Codex MCP] 发送 Idea #1 给 GPT-5.4 xhigh...")
    print_step("GPT-5.4 评分: 7/10 — Worth pursuing")
    print_step("弱点: 需要更多时间点数据, 需要外部验证集")
    print_step("建议: 先用公开的 sci-Plex 数据做概念验证")

    print_phase("Phase 5: 输出报告", "⏱ 2-5 min")
    print_step("写入 IDEA_REPORT.md...")
    print()
    print("  📋 IDEA_REPORT.md 生成完毕!")
    print("  🏆 推荐 Idea: 早期多组学轨迹预测晚期毒性")
    print("  Pilot: POSITIVE (+12%)")
    print("  Novelty: PARTIALLY NOVEL")
    print("  Reviewer: 7/10")
    print("  下一步: /auto-review-loop 或 /research-pipeline")


@demo("auto-review")
def demo_auto_review():
    """Workflow 2: 自动审稿循环"""

    print_phase("ARIS /auto-review-loop — Workflow 2 模拟演示")
    print()
    print("  输入: /auto-review-loop \"VirtualCellPlatform: multi-scale modeling\"")
    print("  预计耗时: 2-8 小时")
    print("  输出: AUTO_REVIEW.md + REVIEW_STATE.json")
    print()

    print_phase("初始化")
    print_step("检查 REVIEW_STATE.json... 不存在, 全新开始")
    print_step("读取项目文档...")
    print_step("读取实验结果...")
    print_step("创建 AUTO_REVIEW.md")

    for round_num in range(1, 5):
        scores = [3.0, 5.0, 6.5, 7.0]
        verdicts = ["NOT READY", "NOT READY", "ALMOST READY", "ALMOST READY"]
        score = scores[round_num - 1]
        verdict = verdicts[round_num - 1]

        print_phase(f"Round {round_num}/4", f"⏱ 30-90 min")

        print_step(f"Phase A: 发送上下文给 GPT-5.4 xhigh...")
        print_step(f"[Codex MCP] 审稿中... (xhigh 模式, 约 60 秒)")
        print_step(f"收到审稿: {score}/10, {verdict}")

        if round_num == 1:
            print("    弱点 1: [FATAL] 核心映射不可识别")
            print("    弱点 2: [FATAL] 评估不可信")
            print("    弱点 3: [MAJOR] 范围过大")
            print("    弱点 4: [MAJOR] ML贡献不清晰")
        elif round_num == 2:
            print("    弱点 1: [MAJOR] 基线对比不够强")
            print("    弱点 2: [MAJOR] 消融实验缺失")
            print("    弱点 3: [MINOR] 图表可以改进")
        elif round_num == 3:
            print("    弱点 1: [MINOR] 可以加一个消融")
            print("    弱点 2: [MINOR] Discussion 需要加强")

        if score >= 6:
            print()
            print(f"  ✅ 分数 {score} ≥ 6, 判定 '{verdict}' → 停止循环")
            break

        print()
        print_step(f"Phase C: Claude 实施修改...")

        if round_num == 1:
            print_step("  修改 1: 砍掉 4 种细胞类型, 只保留神经元")
            print_step("  修改 2: 添加测试集 + 基线对比 (Linear/XGBoost/MLP)")
            print_step("  修改 3: 重写 Contribution 部分")
            print_step("  修改 4: 添加置信区间和统计检验")
        elif round_num == 2:
            print_step("  修改 1: 添加 3 个更强的基线")
            print_step("  修改 2: 完成消融实验")
            print_step("  修改 3: 改进图表")

        print_step(f"Phase E: 记录到 AUTO_REVIEW.md")
        print_step(f"保存 REVIEW_STATE.json: round={round_num}, score={score}")

    print_phase("终止")
    print_step("REVIEW_STATE.json → status: completed")
    print_step("AUTO_REVIEW.md → 写入最终总结")
    print()
    print("  📊 分数进展: 3/10 → 5/10 → 6.5/10")
    print("  📄 完整审稿记录: AUTO_REVIEW.md")
    print("  📦 状态文件: REVIEW_STATE.json")


@demo("paper-writing")
def demo_paper_writing():
    """Workflow 3: 论文写作全流程"""

    print_phase("ARIS /paper-writing — Workflow 3 模拟演示")
    print()
    print("  输入: /paper-writing \"NARRATIVE_REPORT.md\" — venue: NeurIPS")
    print("  预计耗时: 1-3 小时")
    print("  输出: paper/main.pdf")
    print()

    print_phase("Step 1: /paper-plan — 论文大纲", "⏱ 5-10 min")
    print_step("解析 NARRATIVE_REPORT.md...")
    print_step("构建 Claims-Evidence 矩阵:")
    print("    Claim 1: 多组学可预测毒性 → Evidence: R²=0.52, Fig 2")
    print("    Claim 2: 时间分辨提升预测 → Evidence: ablation Table 3")
    print("    Claim 3: 稀有亚群是关键 → Evidence: Fig 4, Table 4")
    print_step("设计分节结构: 7 节")
    print_step("[Codex MCP] GPT-5.4 审查大纲完整性...")
    print_step("输出: PAPER_PLAN.md")

    print_phase("Step 2: /paper-figure — 生成图表", "⏱ 5-15 min")
    print_step("读取 PAPER_PLAN.md 中的图表计划...")
    print_step("生成 Figure 1: 方法概览图 (手动)")
    print_step("生成 Figure 2: 主实验结果 (matplotlib) ✅")
    print_step("生成 Figure 3: 消融实验 (seaborn) ✅")
    print_step("生成 Figure 4: 亚群分析 (matplotlib) ✅")
    print_step("生成 Table 1: 基线对比 (LaTeX) ✅")
    print_step("生成 Table 2: 消融结果 (LaTeX) ✅")
    print_step("输出: figures/ 目录 (4 PDF + 2 LaTeX表格)")

    print_phase("Step 3: /paper-write — 逐节写 LaTeX", "⏱ 15-30 min")
    for section in ["Abstract", "Introduction", "Related Work", "Method",
                     "Experiments", "Results", "Discussion", "Conclusion"]:
        print_step(f"写 {section}...")
    print_step("构建 references.bib (47 引用)")
    print_step("去 AI 化处理 (删除 delve, pivotal, landscape...)")
    print_step("[Codex MCP] GPT-5.4 逐节审查质量...")
    print_step("输出: paper/main.tex + sections/*.tex")

    print_phase("Step 4: /paper-compile — 编译 PDF", "⏱ 2-5 min")
    print_step("latexmk -pdf main.tex (第 1 遍)")
    print_step("latexmk -pdf main.tex (第 2 遍, 交叉引用)")
    print_step("latexmk -pdf main.tex (第 3 遍, 最终)")
    print_step("编译成功! ✅")
    print_step("pdftotext 验证: 9 页主体 + 2 页引用 = 11 页")
    print_step("页数限制: NeurIPS 10+∞ → ✅ 在限制内")
    print_step("输出: paper/main.pdf")

    print_phase("Step 5: /auto-paper-improvement-loop — 润色", "⏱ 15-30 min")
    print_step("Round 1:")
    print_step("  [Codex MCP] GPT-5.4 审全文...")
    print_step("  评分: 5/10")
    print_step("  修复: 3 CRITICAL + 2 MAJOR + 4 MINOR")
    print_step("  重新编译... ✅")
    print_step("  保存: paper/main_round1.pdf")
    print()
    print_step("Round 2:")
    print_step("  [Codex MCP] GPT-5.4 再审...")
    print_step("  评分: 7.5/10")
    print_step("  修复: 1 MAJOR + 2 MINOR")
    print_step("  重新编译... ✅")
    print_step("  保存: paper/main_round2.pdf")

    print_phase("完成!")
    print("  📄 paper/main_round0_original.pdf — 原始版本")
    print("  📄 paper/main_round1.pdf — Round 1 改进")
    print("  📄 paper/main_round2.pdf — 最终版本 (7.5/10)")
    print("  📋 PAPER_IMPROVEMENT_LOG.md — 改进日志")


@demo("pipeline")
def demo_pipeline():
    """全流程一键 /research-pipeline"""

    print_phase("ARIS /research-pipeline — 全流程一键 模拟演示")
    print()
    print("  输入: /research-pipeline \"virtual cell for drug toxicity\"")
    print("  预计耗时: 4-12 小时 (适合过夜)")
    print()

    print("  19:00 ─── Stage 1: /idea-discovery (Workflow 1) ───────────")
    print("            ├── /research-lit (文献综述)")
    print("            ├── /idea-creator (创意生成)")
    print("            ├── /novelty-check (新颖性验证)")
    print("            └── /research-review (专家审查)")
    print("  19:45 ─── 输出: IDEA_REPORT.md")
    print()
    print("  19:45 ─── 🚦 Gate 1: 展示创意排名")
    print("            AUTO_PROCEED=true → 自动选 Idea #1")
    print()
    print("  19:50 ─── Stage 2: 代码实现 ──────────────────────────────")
    print("            ├── 扩展 pilot 代码到完整实验")
    print("            ├── 添加评估指标和日志")
    print("            └── 代码自审")
    print("  20:30 ─── 实验代码就绪")
    print()
    print("  20:30 ─── Stage 3: /run-experiment ───────────────────────")
    print("            ├── 检查 GPU 可用性")
    print("            ├── 同步代码到远程服务器")
    print("            └── 启动 screen 会话")
    print("  20:35 ─── 实验已部署 (或跳过, 如无 GPU)")
    print()
    print("  20:35 ─── Stage 4: /auto-review-loop (Workflow 2) ────────")
    print("            ├── Round 1: GPT审稿 → 3/10 → Claude修改")
    print("            ├── Round 2: GPT再审 → 5/10 → Claude再改")
    print("            └── Round 3: GPT终审 → 6.5/10 → 停止")
    print("  23:00 ─── 输出: AUTO_REVIEW.md")
    print()
    print("  23:00 ─── Stage 5: 最终报告 ──────────────────────────────")
    print("            └── Pipeline Report 生成完毕")
    print()
    print("  ✅ 全流程完成!")
    print("  你在 19:05 就可以去睡觉了 💤")


@demo("paper-plan")
def demo_paper_plan():
    """论文大纲"""

    print_phase("ARIS /paper-plan 模拟演示")
    print()
    print("  输入: /paper-plan \"NARRATIVE_REPORT.md\"")
    print()
    print("  Claims-Evidence 矩阵:")
    print("  ┌─────────────────────────────────┬──────────────────────┐")
    print("  │ Claim                           │ Evidence             │")
    print("  ├─────────────────────────────────┼──────────────────────┤")
    print("  │ 多组学可预测毒性终点            │ Table 2, Fig 2       │")
    print("  │ 时间分辨数据提升预测准确度      │ Ablation Table 3     │")
    print("  │ 稀有亚群是毒性关键驱动力        │ Fig 4, Table 4       │")
    print("  │ 毒性监督优于转录组监督          │ Table 5 (baselines)  │")
    print("  └─────────────────────────────────┴──────────────────────┘")
    print()
    print("  分节计划:")
    print("  1. Abstract (300 words)")
    print("  2. Introduction (1.5 pages)")
    print("  3. Related Work (1 page)")
    print("  4. Method (2 pages)")
    print("  5. Experimental Setup (0.5 page)")
    print("  6. Results and Analysis (2 pages)")
    print("  7. Discussion (0.5 page)")
    print("  8. Conclusion (0.5 page)")
    print()
    print("  输出: PAPER_PLAN.md")


@demo("paper-compile")
def demo_paper_compile():
    """LaTeX 编译"""

    print_phase("ARIS /paper-compile 模拟演示")
    print()
    print("  输入: /paper-compile \"paper/\"")
    print()
    print("  Step 1: latexmk -pdf main.tex")
    print("    Attempt 1: 编译中...")
    print("    Warning: Package 'algorithm2e' not found")
    print("    → 自动安装: miktex packages install algorithm2e")
    print("    Attempt 2: 编译中...")
    print("    Warning: Undefined citation 'smith2024'")
    print("    → 自动修复: 添加到 references.bib")
    print("    Attempt 3: 编译成功! ✅")
    print()
    print("  Step 2: 后编译检查")
    print("    Undefined references: 0 ✅")
    print("    Undefined citations: 0 ✅")
    print("    Overfull hboxes: 2 (both < 5pt, acceptable)")
    print("    pdftotext 验证:")
    print("      Main body: 9 pages")
    print("      References: 2 pages")
    print("      Appendix: 5 pages")
    print("      Total: 16 pages")
    print("    Page limit (NeurIPS 10+∞): ✅")
    print()
    print("  输出: paper/main.pdf (1.8 MB)")


@demo("analyze-results")
def demo_analyze_results():
    """实验结果分析"""

    print_phase("ARIS /analyze-results 模拟演示")
    print()
    print("  输入: /analyze-results experiments/results/")
    print("  预计耗时: 2-5 分钟")
    print()

    print_phase("Step 1: 扫描结果文件", "⏱ 10 sec")
    print_step("扫描 experiments/results/ 目录...")
    print_step("发现 4 个实验运行:")
    print("    run_001/ — baseline_linear (完成)")
    print("    run_002/ — xgboost_model  (完成)")
    print("    run_003/ — mlp_baseline   (完成)")
    print("    run_004/ — toxtwin_full   (完成)")
    print()
    print_step("解析日志和指标文件...")

    print_phase("Step 2: 计算统计指标", "⏱ 30 sec")
    print_step("读取各 run 的 metrics.json...")
    print()
    print("  ┌──────────────────┬─────────┬─────────┬─────────┬───────────┐")
    print("  │ Model            │ R²      │ AUC     │ F1      │ Runtime   │")
    print("  ├──────────────────┼─────────┼─────────┼─────────┼───────────┤")
    print("  │ Linear           │ 0.312   │ 0.651   │ 0.583   │ 2m 15s    │")
    print("  │ XGBoost          │ 0.421   │ 0.738   │ 0.672   │ 5m 42s    │")
    print("  │ MLP              │ 0.398   │ 0.712   │ 0.645   │ 18m 31s   │")
    print("  │ ToxTwin (ours)   │ 0.523   │ 0.814   │ 0.751   │ 45m 12s   │")
    print("  └──────────────────┴─────────┴─────────┴─────────┴───────────┘")
    print()
    print_step("计算置信区间 (5-fold cross-validation)...")
    print("    ToxTwin R²: 0.523 ± 0.031 (95% CI: [0.492, 0.554])")
    print("    ToxTwin AUC: 0.814 ± 0.018 (95% CI: [0.796, 0.832])")
    print()
    print_step("统计显著性检验 (paired t-test vs XGBoost):")
    print("    R²:  p=0.0023 **  (significant)")
    print("    AUC: p=0.0041 **  (significant)")
    print("    F1:  p=0.0089 **  (significant)")

    print_phase("Step 3: 生成对比图表", "⏱ 30 sec")
    print_step("生成 comparison_bar_chart.pdf ✅")
    print_step("生成 training_curves.pdf ✅")
    print_step("生成 confusion_matrix.pdf ✅")
    print_step("生成 ablation_heatmap.pdf ✅")

    print_phase("Step 4: 撰写分析总结", "⏱ 1 min")
    print_step("写入 ANALYSIS_REPORT.md...")
    print()
    print("  核心发现:")
    print("  1. ToxTwin 在所有指标上显著优于基线 (p < 0.01)")
    print("  2. 相比最强基线 XGBoost，R² 提升 24.2%, AUC 提升 10.3%")
    print("  3. 时间分辨特征贡献最大 (消融: -15.6% R²)")
    print("  4. 稀有亚群感知损失贡献第二 (消融: -8.3% R²)")
    print()
    print("  输出:")
    print("    ANALYSIS_REPORT.md — 完整分析报告")
    print("    figures/comparison_bar_chart.pdf")
    print("    figures/training_curves.pdf")
    print("    figures/confusion_matrix.pdf")
    print("    figures/ablation_heatmap.pdf")


@demo("run-experiment")
def demo_run_experiment():
    """部署并监控实验"""

    print_phase("ARIS /run-experiment + /monitor-experiment 模拟演示")
    print()
    print("  输入: /run-experiment src/train.py --config experiments/config.yaml")
    print("  预计耗时: 部署 5 min, 训练取决于模型和数据")
    print()

    print_phase("Step 1: 环境检查", "⏱ 30 sec")
    print_step("检查远程服务器连接...")
    print("    SSH: user@gpu-server.lab.com ✅ (key-based auth)")
    print_step("检查 GPU 可用性...")
    print("    GPU 0: NVIDIA A100 80GB — 空闲 ✅")
    print("    GPU 1: NVIDIA A100 80GB — 空闲 ✅")
    print("    GPU 2: NVIDIA A100 80GB — 占用 (user2)")
    print("    GPU 3: NVIDIA A100 80GB — 空闲 ✅")
    print_step("检查 conda 环境...")
    print("    conda env: research (Python 3.12, PyTorch 2.5) ✅")
    print_step("检查磁盘空间...")
    print("    /home/user: 248 GB free ✅")
    print("    /data: 1.2 TB free ✅")

    print_phase("Step 2: 同步代码和数据", "⏱ 1-3 min")
    print_step("rsync 代码到远程: src/ → /home/user/experiments/toxtwin/src/")
    print("    Sending 47 files... done (2.3 MB)")
    print_step("检查数据已在远程...")
    print("    /data/datasets/sciplex/ — 已存在 (15.6 GB) ✅")

    print_phase("Step 3: 启动训练", "⏱ 30 sec")
    print_step("创建 screen 会话: screen -S toxtwin_train")
    print_step("激活环境: conda activate research")
    print_step("设置环境变量: CUDA_VISIBLE_DEVICES=0,1")
    print_step("启动训练:")
    print('    python src/train.py --config experiments/config.yaml \\')
    print('      --gpus 2 --batch-size 256 --epochs 100 \\')
    print('      --log-dir experiments/results/run_005/')
    print()
    print("  训练已在后台启动! PID: 28451")
    print("  Screen 会话: toxtwin_train")
    print()
    print("  查看训练状态:")
    print("    ssh user@server 'screen -r toxtwin_train'")
    print("    或使用 /monitor-experiment")

    print_phase("── /monitor-experiment 演示 ──")
    print()
    print("  输入: /monitor-experiment")
    print()

    print_step("连接远程服务器...")
    print_step("检查活跃实验...")
    print()
    print("  ┌────────────────────────────────────────────────────────┐")
    print("  │ Experiment: toxtwin_train (PID: 28451)                │")
    print("  │ Status: RUNNING                                       │")
    print("  │ Elapsed: 2h 14m 33s                                   │")
    print("  │ Progress: Epoch 34/100 (34%)                          │")
    print("  │                                                       │")
    print("  │ Current metrics:                                      │")
    print("  │   Train loss: 0.1847  (↓ from 0.4521)                │")
    print("  │   Val R²:     0.489   (↑ best: 0.497 @ epoch 31)    │")
    print("  │   Val AUC:    0.782   (↑ best: 0.791 @ epoch 32)    │")
    print("  │   Learning rate: 3.2e-4 (cosine schedule)            │")
    print("  │                                                       │")
    print("  │ GPU utilization:                                      │")
    print("  │   GPU 0: 94% util, 71.2/80 GB memory                │")
    print("  │   GPU 1: 92% util, 68.9/80 GB memory                │")
    print("  │                                                       │")
    print("  │ ETA: ~4h 15m (based on epoch timing)                 │")
    print("  │ Expected completion: ~18:30 today                    │")
    print("  └────────────────────────────────────────────────────────┘")
    print()
    print("  后续建议:")
    print("    /monitor-experiment        — 再次检查进度")
    print("    /analyze-results results/  — 训练完成后分析结果")


@demo("pixel-art")
def demo_pixel_art():
    """像素画"""

    print_phase("ARIS /pixel-art 模拟演示")
    print()
    print("  输入: /pixel-art \"两个科学家在讨论虚拟细胞\"")
    print()
    print("  Claude 生成像素风 SVG:")
    print()
    print("  ┌────────────────────────────────────┐")
    print("  │  ██  ██                    ██  ██  │")
    print("  │  ████████                  ████████│")
    print("  │  ██▓▓▓▓██                ██▓▓▓▓██ │")
    print("  │  ██░░░░██                ██░░░░██  │")
    print("  │    ████        ☁         ████      │")
    print("  │    ║  ║   🧬  💊  🔬    ║  ║      │")
    print("  │    ║  ║                  ║  ║      │")
    print("  │   ╚╝  ╚╝    [Cell]     ╚╝  ╚╝     │")
    print("  │          Virtual Cell Twin          │")
    print("  └────────────────────────────────────┘")
    print()
    print("  (实际输出是一个完整的 SVG 文件)")
    print("  输出: pixel_art_output.svg")


@demo("feishu-notify")
def demo_feishu_notify():
    """飞书通知"""

    print_phase("ARIS /feishu-notify 模拟演示")
    print()
    print("  输入: /feishu-notify \"实验训练完成, R²=0.523, AUC=0.814\"")
    print()

    print_step("检查飞书 Webhook 配置...")
    print("    Webhook URL: https://open.feishu.cn/open-apis/bot/v2/hook/xxx ✅")
    print()
    print_step("构建消息卡片...")
    print()
    print("  ┌─────────────────────────────────────────────────────┐")
    print("  │  🔬 ARIS 实验通知                                   │")
    print("  │  ─────────────────────────────────────────────      │")
    print("  │  状态: ✅ 训练完成                                   │")
    print("  │  时间: 2026-03-15 23:45                             │")
    print("  │                                                     │")
    print("  │  实验结果:                                           │")
    print("  │    R²  = 0.523 (↑ 24.2% vs XGBoost)               │")
    print("  │    AUC = 0.814 (↑ 10.3% vs XGBoost)               │")
    print("  │    F1  = 0.751                                      │")
    print("  │                                                     │")
    print("  │  下一步: /analyze-results 或 /auto-review-loop     │")
    print("  └─────────────────────────────────────────────────────┘")
    print()
    print_step("发送飞书通知... ✅ 已发送")
    print()
    print("  用途:")
    print("  - 实验完成后自动通知")
    print("  - 审稿循环每轮结束通知分数变化")
    print("  - 论文编译完成通知")
    print("  - 过夜任务完成时推送结果摘要到手机")


def list_demos():
    print()
    print("=" * 70)
    print("  ARIS 所有 Skill 和 Workflow 模拟演示")
    print("=" * 70)
    print()
    print("  可用的演示:")
    print()
    for name, func in DEMOS.items():
        print(f"    {name:<20} — {func.__doc__}")
    print()
    print(f"    {'all':<20} — 运行全部演示")
    print()
    print("  用法: python workflow_demos.py <demo名>")
    print()


def main():
    if len(sys.argv) < 2:
        list_demos()
        return

    demo_name = sys.argv[1].lower()

    if demo_name == "all":
        for name, func in DEMOS.items():
            func()
            print("\n" + "=" * 70 + "\n")
    elif demo_name in DEMOS:
        DEMOS[demo_name]()
    else:
        print(f"  Unknown demo: {demo_name}")
        list_demos()


if __name__ == "__main__":
    main()
