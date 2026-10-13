# monetary-policy-case-analyzer — 现实货币政策案例剖析器

一个用于《货币银行学》/《金融学》课程学习的 CodeBuddy Skill。核心用途：把**现实中发生的货币政策事件、财经新闻、经济数据**，用课堂理论拆解成一份结构化的深度分析报告。

> 与常见的"知识问答/题库/笔记整理"类课程工具不同，本 skill 聚焦"**用理论解剖现实**"——输入一个现实锚点，输出一条完整的因果分析链。

## 安装

把本目录放到 CodeBuddy 的 skills 目录即可：

```bash
cp -r monetary-banking ~/.codebuddy/skills/
```

Windows 对应 `C:\Users\你的用户名\.codebuddy\skills\`。放好后重启 CodeBuddy。

## 目录结构

```
monetary-banking/
├── SKILL.md                        # 主文件：剖析五步法工作流
├── README.md                       # 本文件
├── scripts/
│   └── calc.py                     # 货币金融计算器（7 个子命令）
└── references/
    ├── case-analysis.md            # 案例剖析方法论 + 五类案例模板 + 中国政策工具库
    ├── knowledge-map.md            # 核心知识地图（八大主题）
    ├── formulas.md                 # 公式速查（含适用条件）
    ├── exercise-templates.md       # 出题模板（备用）
    └── paper-guide.md              # 论文写作规范（备用）
```

## 它在做什么：剖析五步法

任何案例都沿这条链条展开，不跳步：

```
① 事件还原  →  ② 理论定位  →  ③ 传导链条  →  ④ 影响推演  →  ⑤ 批判性评价
  （事实）       （挂课本）      （讲因果）      （对谁有何影响）   （好坏与争议）
```

最后附「要点回扣」，把案例重新连回考试考点。

## 使用示例

```
"分析一下央行这次降准对商业银行的影响"
"这条新闻怎么用货币银行学的知识解释"
"LPR 下调意味着什么，帮我做个案例分析"
"用利率理论剖析一下美联储这轮加息"
"帮我剖析一下最近这个通胀数据"
```

## 支持的案例类型

| 类型 | 例子 |
|---|---|
| 数量型工具 | 降准、逆回购、MLF 操作 |
| 价格型工具 | 降息、LPR 调整、利率走廊 |
| 汇率与国际 | 美联储加息、人民币汇率变动 |
| 金融风险与监管 | 银行风险事件、资本充足率新规 |
| 货币现象 | 通胀数据、M2 变动、数字货币 |

## 计算器用法

剖析中涉及数值推演时，用脚本计算以保证准确：

```bash
python3 scripts/calc.py --help

python3 scripts/calc.py money_multiplier --rr 0.1 --c 0.05 --e 0.02 --t 0.3 --rt 0.05
python3 scripts/calc.py deposit_expansion --reserve 0.2 --base 1000
python3 scripts/calc.py fisher --nominal 0.06 --inflation 0.02
python3 scripts/calc.py duration --face 1000 --coupon 0.05 --ytm 0.06 --years 3
python3 scripts/calc.py exchange_swap --buy 7.10 --sell 7.15 --amount 1000000
```

支持：`money_multiplier`、`deposit_expansion`、`present_value`、`compound`、`fisher`、`duration`、`exchange_swap`。结果同时输出**计算过程**与**结果**。

## 分析规范

- **事实优先**：还原阶段不掺入分析，分析阶段不臆造事实。
- **链条完整**：每一步传导都要有因果说明。
- **数值必校验**：所有数值经 `calc.py` 计算。
- **不站队**：政策评价呈现多元观点，不做情绪化论断。
- **标注不确定**：信息不足时明确说明假设。
