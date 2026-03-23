"""
ARIS Cursor 版本 — 所有演示的统一运行器

按等级分组运行所有可用演示，支持交互式选择和批量执行。

用法:
    python run_all_demos.py                  # 交互式菜单
    python run_all_demos.py --list           # 列出所有演示
    python run_all_demos.py --level 1        # 运行 Level 1 全部
    python run_all_demos.py --level 2        # 运行 Level 2 全部
    python run_all_demos.py --level 3        # 运行 Level 3 全部
    python run_all_demos.py --all            # 运行全部演示
    python run_all_demos.py --quick          # 快速演示（每级各一个）
"""

import sys
import io
import subprocess
import argparse
import os
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DEMOS = {
    "1": {
        "name": "Level 1: Basic Skills (No Codex needed)",
        "color": "green",
        "demos": [
            {
                "id": "1.1",
                "name": "arXiv Search",
                "cmd": [sys.executable, "arxiv_search_demo.py", "drug toxicity prediction neural network"],
                "desc": "Search arXiv API for papers",
                "time": "~10 sec",
            },
            {
                "id": "1.2",
                "name": "arXiv Download",
                "cmd": [sys.executable, "arxiv_search_demo.py", "Hodgkin-Huxley parameter estimation", "--max", "2", "--download-all", "--dir", "demo_papers"],
                "desc": "Search + download PDFs",
                "time": "~30 sec",
            },
            {
                "id": "1.3",
                "name": "Literature Review",
                "cmd": [sys.executable, "research_lit_demo.py", "virtual cell digital twin drug toxicity", "--save"],
                "desc": "Multi-source literature search + classification",
                "time": "~15 sec",
            },
            {
                "id": "1.4",
                "name": "Literature Review (Full Demo)",
                "cmd": [sys.executable, "research_lit_demo.py", "--demo"],
                "desc": "Pre-recorded full /research-lit output with GPT-5.4 analysis",
                "time": "instant",
            },
        ],
    },
    "2": {
        "name": "Level 2: Codex MCP Skills (Pre-recorded output)",
        "color": "yellow",
        "demos": [
            {
                "id": "2.1",
                "name": "Research Review (GPT-5.4)",
                "cmd": [sys.executable, "research_review_demo.py", "--demo"],
                "desc": "GPT-5.4 xhigh peer review: 3/10, 8 weaknesses",
                "time": "instant",
            },
            {
                "id": "2.2",
                "name": "Novelty Check (GPT-5.4)",
                "cmd": [sys.executable, "novelty_check_demo.py", "--demo"],
                "desc": "GPT-5.4 novelty verification: PARTIALLY NOVEL, 8 prior works",
                "time": "instant",
            },
            {
                "id": "2.3",
                "name": "Idea Creator (GPT-5.4)",
                "cmd": [sys.executable, "idea_creator_demo.py"],
                "desc": "GPT-5.4 generated 5 research ideas with rankings",
                "time": "instant",
            },
        ],
    },
    "3": {
        "name": "Level 3: Workflows (Simulated multi-step processes)",
        "color": "magenta",
        "demos": [
            {
                "id": "3.1",
                "name": "Idea Discovery (Workflow 1)",
                "cmd": [sys.executable, "workflow_demos.py", "idea-discovery"],
                "desc": "Full: lit-review → idea-gen → novelty → review",
                "time": "~5 sec (simulated 30-120 min)",
            },
            {
                "id": "3.2",
                "name": "Auto Review Loop (Workflow 2)",
                "cmd": [sys.executable, "workflow_demos.py", "auto-review"],
                "desc": "Multi-round GPT review → Claude fix → re-review",
                "time": "~5 sec (simulated 2-8 h)",
            },
            {
                "id": "3.3",
                "name": "Paper Writing (Workflow 3)",
                "cmd": [sys.executable, "workflow_demos.py", "paper-writing"],
                "desc": "plan → figures → write → compile → improve",
                "time": "~5 sec (simulated 1-3 h)",
            },
            {
                "id": "3.4",
                "name": "Full Pipeline",
                "cmd": [sys.executable, "workflow_demos.py", "pipeline"],
                "desc": "Everything combined: idea → code → review → paper",
                "time": "~5 sec (simulated 4-12 h)",
            },
            {
                "id": "3.5",
                "name": "Paper Plan",
                "cmd": [sys.executable, "workflow_demos.py", "paper-plan"],
                "desc": "Claims-Evidence matrix + section plan",
                "time": "instant",
            },
            {
                "id": "3.6",
                "name": "Paper Compile",
                "cmd": [sys.executable, "workflow_demos.py", "paper-compile"],
                "desc": "LaTeX compilation with auto-fix",
                "time": "instant",
            },
            {
                "id": "3.7",
                "name": "Analyze Results",
                "cmd": [sys.executable, "workflow_demos.py", "analyze-results"],
                "desc": "Experiment result analysis + statistics",
                "time": "instant",
            },
            {
                "id": "3.8",
                "name": "Run & Monitor Experiment",
                "cmd": [sys.executable, "workflow_demos.py", "run-experiment"],
                "desc": "Deploy + monitor experiments on GPU server",
                "time": "instant",
            },
        ],
    },
}


def print_colored(text, color="white"):
    colors = {
        "green": "\033[92m", "yellow": "\033[93m", "magenta": "\033[95m",
        "cyan": "\033[96m", "red": "\033[91m", "white": "\033[97m",
        "dim": "\033[90m", "reset": "\033[0m", "bold": "\033[1m",
    }
    c = colors.get(color, "")
    r = colors["reset"]
    print(f"{c}{text}{r}")


def list_all_demos():
    print()
    print_colored("=" * 68, "cyan")
    print_colored("  ARIS Cursor Version — All Available Demos", "cyan")
    print_colored("=" * 68, "cyan")
    print()

    for level_key, level in DEMOS.items():
        print_colored(f"  {level['name']}", level["color"])
        print_colored("  " + "─" * 50, "dim")
        for d in level["demos"]:
            print(f"    {d['id']:<6} {d['name']:<35} {d['time']}")
            print_colored(f"           {d['desc']}", "dim")
        print()

    print_colored("  Total: {} demos available".format(
        sum(len(l["demos"]) for l in DEMOS.values())), "cyan")
    print()


def run_demo(demo_info: dict):
    print()
    print_colored("=" * 68, "cyan")
    print_colored(f"  Running Demo {demo_info['id']}: {demo_info['name']}", "cyan")
    print_colored(f"  {demo_info['desc']}", "dim")
    print_colored("=" * 68, "cyan")

    try:
        result = subprocess.run(
            demo_info["cmd"],
            cwd=SCRIPT_DIR,
            timeout=120,
        )
        if result.returncode != 0:
            print_colored(f"\n  Demo exited with code {result.returncode}", "yellow")
    except subprocess.TimeoutExpired:
        print_colored("\n  Demo timed out (120s limit)", "red")
    except FileNotFoundError:
        print_colored(f"\n  Script not found: {demo_info['cmd'][1]}", "red")
    except Exception as e:
        print_colored(f"\n  Error: {e}", "red")


def run_level(level_key: str):
    if level_key not in DEMOS:
        print_colored(f"  Unknown level: {level_key}", "red")
        return

    level = DEMOS[level_key]
    print_colored(f"\n  Running all demos in {level['name']}", level["color"])

    for demo in level["demos"]:
        run_demo(demo)
        print()


def run_quick():
    print_colored("\n  Quick Demo — one from each level\n", "cyan")

    quick_picks = ["1.1", "2.1", "3.1"]
    for pick in quick_picks:
        for level in DEMOS.values():
            for demo in level["demos"]:
                if demo["id"] == pick:
                    run_demo(demo)
                    print()


def interactive_menu():
    while True:
        print()
        print_colored("=" * 68, "cyan")
        print_colored("  ARIS Demo Runner — Interactive Menu", "cyan")
        print_colored("=" * 68, "cyan")
        print()

        for level_key, level in DEMOS.items():
            print_colored(f"  [{level_key}] {level['name']}", level["color"])
            for d in level["demos"]:
                print(f"       [{d['id']}] {d['name']} ({d['time']})")
            print()

        print_colored("  [a] Run all demos", "cyan")
        print_colored("  [q] Quick demo (one per level)", "cyan")
        print_colored("  [x] Exit", "dim")
        print()

        choice = input("  Your choice: ").strip().lower()

        if choice == "x" or choice == "exit":
            break
        elif choice == "a" or choice == "all":
            for level_key in DEMOS:
                run_level(level_key)
        elif choice == "q" or choice == "quick":
            run_quick()
        elif choice in DEMOS:
            run_level(choice)
        else:
            found = False
            for level in DEMOS.values():
                for demo in level["demos"]:
                    if demo["id"] == choice:
                        run_demo(demo)
                        found = True
                        break
                if found:
                    break
            if not found:
                print_colored(f"  Unknown option: {choice}", "red")

        print()
        input("  Press Enter to continue...")


def main():
    parser = argparse.ArgumentParser(description="ARIS Cursor Demo Runner")
    parser.add_argument("--list", action="store_true", help="List all demos")
    parser.add_argument("--level", type=str, help="Run all demos in a level (1/2/3)")
    parser.add_argument("--all", action="store_true", help="Run all demos")
    parser.add_argument("--quick", action="store_true", help="Quick demo (one per level)")
    parser.add_argument("--demo", type=str, help="Run specific demo by ID (e.g. 1.1)")
    args = parser.parse_args()

    if args.list:
        list_all_demos()
    elif args.level:
        run_level(args.level)
    elif args.all:
        for level_key in DEMOS:
            run_level(level_key)
    elif args.quick:
        run_quick()
    elif args.demo:
        found = False
        for level in DEMOS.values():
            for demo in level["demos"]:
                if demo["id"] == args.demo:
                    run_demo(demo)
                    found = True
                    break
            if found:
                break
        if not found:
            print_colored(f"  Unknown demo ID: {args.demo}", "red")
            list_all_demos()
    else:
        interactive_menu()


if __name__ == "__main__":
    main()
