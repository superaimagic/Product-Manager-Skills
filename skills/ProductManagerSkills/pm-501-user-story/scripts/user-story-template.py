#!/usr/bin/env python3
"""从命令行输入生成用户故事 Markdown 片段。

不访问网络。输出到 stdout。
"""

import argparse
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="生成包含用户故事三段式和验收标准三步法的Markdown片段。",
    )
    parser.add_argument("--summary", help="用户故事的简短摘要/标题。")
    parser.add_argument("--persona", help='"作为"后面的角色或persona。')
    parser.add_argument("--action", help='"我想要"后面的动作。')
    parser.add_argument("--outcome", help='"以便"后面的期望结果。')
    parser.add_argument("--scenario", help="场景描述。")
    parser.add_argument("--given", action="append", default=[], help="假如前提条件（可重复）。")
    parser.add_argument("--when", dest="when", help="当触发条件。")
    parser.add_argument("--then", dest="then", help="那么预期结果。")
    return parser.parse_args()


def normalize(value: str, placeholder: str) -> str:
    if value and value.strip():
        return value.strip()
    return placeholder


def main() -> int:
    args = parse_args()

    summary = normalize(args.summary, "[简洁、以价值为中心的标题]")
    persona = normalize(args.persona, "[角色或persona]")
    action = normalize(args.action, "[用户为实现结果而采取的行动]")
    outcome = normalize(args.outcome, "[期望的结果]")
    scenario = normalize(args.scenario, "[描述价值的简洁、可读场景]")
    whens = normalize(args.when, "[触发行动的事件]")
    thens = normalize(args.then, "[期望的结果]")

    givens = args.given or ["[初始上下文或前提条件]"]

    print("### 用户故事 [ID]:\n")
    print(f"- **摘要:** {summary}\n")
    print("#### 用例（用户故事三段式）:")
    print(f"- **作为** {persona}")
    print(f"- **我想要** {action}")
    print(f"- **以便** {outcome}\n")
    print("#### 验收标准（验收标准三步法）:\n")
    print(f"- **场景:** {scenario}")

    for index, given in enumerate(givens):
        label = "假如" if index == 0 else "并且假如"
        print(f"- **{label}:** {given}")

    print(f"- **当:** {whens}")
    print(f"- **那么:** {thens}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
