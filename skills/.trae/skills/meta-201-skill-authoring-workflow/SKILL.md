---
name: "meta-201-skill-authoring-workflow"
description: 工具类-技能编写工作流skill：将原始产品管理内容转化为合规的、可发布的技能。在创建或更新仓库技能时使用，确保不破坏标准规范。
intent: >-
  无混乱地创建或更新产品管理技能。此工作流将粗略笔记、工坊内容或半成品提示词堆转化为合规的
  `skills/<skill-name>/SKILL.md` 资产，确保通过验证并属于本仓库。
type: workflow
best_for:
  - "从笔记或源材料创建新的仓库技能"
  - "在保持标准不变的前提下更新现有技能"
  - "在提交前运行完整的创作和验证工作流"
scenarios:
  - "帮我把这些工坊笔记转化为新的产品管理技能"
  - "我需要更新现有技能但不破坏仓库标准"
  - "在这个仓库里创作新技能应该用什么工作流？"
---

## 目的

无混乱地创建或更新产品管理技能。此工作流将粗略笔记、工坊内容或半成品提示词堆转化为合规的 `skills/<skill-name>/SKILL.md` 资产，确保通过验证并属于本仓库。

当你想发布新技能而不想玩"看着差不多就行"的轮盘赌时，使用此工作流。

## 核心概念

### 先吃自己的狗粮

在发明自定义流程之前，先使用仓库原生工具和标准：
- `scripts/find-a-skill.sh`
- `scripts/add-a-skill.sh`
- `scripts/build-a-skill.sh`
- `scripts/test-a-skill.sh`
- `scripts/check-skill-metadata.py`

### 选择正确的创建路径

- **引导式向导（`build-a-skill.sh`）**：有想法但还没有最终文案时最佳。
- **内容优先生成器（`add-a-skill.sh`）**：已有源内容时最佳。
- **手动编辑 + 验证**：收紧现有技能时最佳。

### 完成标准（无例外）

技能仅在以下条件全部满足时才算完成：
1. 前置元数据有效（`name`、`description`、`intent`、`type`）
2. 章节顺序合规
3. 元数据限制得到遵守（`name` <= 64 字符，`description` <= 200 字符）
4. 描述同时说明技能做什么以及何时使用
5. intent 承载更完整的仓库面向摘要，但不替代以触发为导向的描述
6. 交叉引用可解析
7. README 目录计数和表格已更新（如果新增/删除技能）

### 引导式工作的权威来源

当作为引导式对话运行此工作流时，使用 [`workshop-facilitation`](../workshop-facilitation/SKILL.md) 作为交互协议。

它定义了：
- 会话预告 + 入口模式（引导式、上下文倾倒、最佳猜测）
- 每轮一个问题的通俗语言提示
- 进度标签（例如，上下文 Qx/8 和评分 Qx/5）
- 中断处理和暂停/恢复行为
- 决策点的编号建议
- 常规问题的快速选择编号响应选项（适当时包含"其他（请说明）"）

此文件定义工作流序列和领域特定输出。如有冲突，以本文件的工作流逻辑为准。

## 应用

### 阶段 1：预检（避免重复工作）

1. 搜索重叠技能：

```bash
./scripts/find-a-skill.sh --keyword "<topic>"
```

2. 确定类型：
- **组件**：单一产出物/模板
- **交互式**：3-5 个自适应问题 + 编号选项
- **工作流**：多阶段编排

### 阶段 2：生成草稿

如果你有源材料：

```bash
./scripts/add-a-skill.sh research/your-framework.md
```

如果你想要引导式提示：

```bash
./scripts/build-a-skill.sh
```

### 阶段 3：收紧技能

手动审查以下方面：
- 清晰的"何时使用"指导
- 一个具体示例
- 一个明确的反模式
- 没有填充内容或模糊的顾问式空话

### 阶段 4：严格验证

在考虑提交之前运行严格检查：

```bash
./scripts/test-a-skill.sh --skill <skill-name> --smoke
python3 scripts/check-skill-metadata.py skills/<skill-name>/SKILL.md
python3 scripts/check-skill-triggers.py skills/<skill-name>/SKILL.md --show-cases
```

### 阶段 5：与仓库文档集成

如果是新技能：
1. 将其添加到正确的 README 分类表
2. 更新技能总数和分类计数
3. 验证链接路径可解析

### 阶段 6：可选打包

如果目标是 Claude 自定义技能上传：

```bash
./scripts/zip-a-skill.sh --skill <skill-name>
# 或打包一个分类：
./scripts/zip-a-skill.sh --type component --output dist/skill-zips
# 或使用精选入门预设：
./scripts/zip-a-skill.sh --preset core-pm --output dist/skill-zips
```

## 示例

### 示例：将工坊笔记转化为技能

输入：`research/pricing-workshop-notes.md`
目标：新的交互式顾问

```bash
./scripts/add-a-skill.sh research/pricing-workshop-notes.md
./scripts/test-a-skill.sh --skill <new-skill-name> --smoke
python3 scripts/check-skill-metadata.py skills/<new-skill-name>/SKILL.md
```

预期结果：
- 新技能文件夹存在
- 技能通过结构和元数据检查
- README 目录条目已添加/更新

### 反模式示例

"我们写了一个很酷的技能，跳过了验证，忘了更新 README 计数，直接发布了。"

结果：
- 引用断裂
- 目录数字不一致
- 给贡献者和用户带来困惑

## 常见陷阱

- 凭感觉发布，而非凭标准。
- 任务实际是组件模板时却选择了 `workflow` 类型。
- 描述臃肿，超出上传限制。
- 描述只说技能是什么，但没说 Claude 何时应触发它。
- 描述悄悄触及 200 字符限制，在句子中间被截断。
- 让 `intent` 成为弱触发描述的替代品。
- 添加技能后忘了更新 README 计数。
- 将生成输出视为最终版本而不加审查。

## 参考

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `docs/Building PM Skills.md`
- `docs/Add-a-Skill Utility Guide.md`
- Anthropic 的 [Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)
- `scripts/add-a-skill.sh`
- `scripts/build-a-skill.sh`
- `scripts/find-a-skill.sh`
- `scripts/test-a-skill.sh`
- `scripts/check-skill-metadata.py`
- `scripts/check-skill-triggers.py`
- `scripts/zip-a-skill.sh`
