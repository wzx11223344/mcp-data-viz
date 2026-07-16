# MCP 数据可视化服务器

[![CI](https://github.com/wzx11223344/mcp-data-viz/actions/workflows/ci.yml/badge.svg)](https://github.com/wzx11223344/mcp-data-viz/actions/workflows/ci.yml)

> 基于 FastMCP 框架的数据可视化 MCP 服务器，提供 32 个工具用于图表生成、报告构建和数据处理。

## 项目描述

本项目是一个基于 Model Context Protocol (MCP) 的数据可视化服务器，通过 32 个工具函数为 AI 助手提供强大的数据可视化能力。服务器使用 `FastMCP` 框架构建，所有图表通过 `matplotlib` 生成并保存为 PNG 图片，所有工具返回 Markdown 格式字符串，方便 AI 助手直接呈现给用户。

## 特性列表

- **32 个 MCP 工具**：涵盖图表生成、报告构建、数据处理三大能力域
- **18 种图表类型**：柱状图、折线图、饼图、散点图、热力图、箱线图、直方图、雷达图等
- **8 种报告工具**：HTML 报告、数据表、KPI 卡片、仪表盘布局、趋势指标等
- **6 种辅助工具**：CSV 解析、颜色方案、数字格式化、数据验证、异常值检测、归一化
- **中文字体支持**：内置 SimHei / Microsoft YaHei 中文字体配置
- **6 套颜色方案**：default、warm、cool、pastel、grayscale、nature
- **数组参数传递**：使用逗号分隔的字符串传递数组参数，简单直观
- **图表自动保存**：生成的图表自动保存到 `output/` 目录
- **Markdown 返回格式**：所有工具返回 Markdown 格式，便于 AI 直接呈现

## 安装方法

### 1. 克隆项目

```bash
cd d:\D盘TRAE办公\github_repos
# 项目已在此目录下
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

依赖列表：
- `mcp>=1.0.0` — MCP 协议框架
- `matplotlib` — 图表绘制库
- `numpy` — 数值计算库
- `pandas` — 数据处理库

### 3. 配置 MCP 客户端

在支持 MCP 的客户端（如 Claude Desktop、Cursor 等）配置文件中添加：

```json
{
  "mcpServers": {
    "data-viz": {
      "command": "python",
      "args": ["d:\\D盘TRAE办公\\github_repos\\mcp-data-viz\\server.py"]
    }
  }
}
```

## 使用示例

### 示例 1：生成柱状图

```
工具: bar_chart
参数:
  categories: "Q1,Q2,Q3,Q4"
  values: "120,180,150,200"
  title: "2024年季度销售"
  ylabel: "销售额（万元）"
```

### 示例 2：生成折线图

```
工具: line_chart
参数:
  x_values: "1月,2月,3月,4月,5月,6月"
  y_values: "30,45,38,52,48,65"
  title: "上半年用户增长趋势"
  xlabel: "月份"
  ylabel: "新增用户（万）"
```

### 示例 3：生成 KPI 卡片

```
工具: kpi_card
参数:
  label: "月度营收"
  value: "50000"
  target: "55000"
  unit: "元"
  trend: "up"
  trend_value: "+15.2%"
```

### 示例 4：生成热力图

```
工具: heatmap
参数:
  data: "10,20,30;40,50,60;70,80,90"
  title: "产品评分矩阵"
  x_labels: "质量,价格,服务"
  y_labels: "产品A,产品B,产品C"
```

### 示例 5：生成 HTML 报告

```
工具: generate_html_report
参数:
  title: "月度数据分析报告"
  content: "# 1月数据概览\n\n本月营收增长15%，核心指标表现良好。"
  style: "modern"
```

## 工具列表

### 图表工具（18个）

| 序号 | 工具名称 | 功能描述 |
| --- | --- | --- |
| 1 | `bar_chart` | 柱状图 — 用垂直柱子展示各类别数值 |
| 2 | `grouped_bar` | 分组柱状图 — 多组数据并列对比 |
| 3 | `horizontal_bar` | 水平柱状图 — 类别名较长时适用 |
| 4 | `line_chart` | 折线图 — 展示数据变化趋势 |
| 5 | `multi_line` | 多折线图 — 多条线对比 |
| 6 | `area_chart` | 面积图 — 折线下方填充颜色 |
| 7 | `pie_chart` | 饼图 — 展示各部分占整体比例 |
| 8 | `donut_chart` | 环形图 — 中空饼图，圆心可显示汇总 |
| 9 | `scatter_plot` | 散点图 — 展示两变量关系 |
| 10 | `bubble_chart` | 气泡图 — 散点大小表示第三维度 |
| 11 | `heatmap` | 热力图 — 颜色深浅表示矩阵值 |
| 12 | `correlation_heatmap` | 相关性热力图 — 变量间相关系数 |
| 13 | `box_plot` | 箱线图 — 四分位数和异常值 |
| 14 | `violin_plot` | 小提琴图 — 密度分布估计 |
| 15 | `histogram` | 直方图 — 数据分布频率 |
| 16 | `density_plot` | 密度图 — 概率密度曲线 |
| 17 | `radar_chart` | 雷达图 — 多维度指标综合表现 |
| 18 | `pair_plot` | 散点矩阵图 — 多变量两两关系 |

### 报告工具（8个）

| 序号 | 工具名称 | 功能描述 |
| --- | --- | --- |
| 19 | `generate_html_report` | 生成完整 HTML 报告 |
| 20 | `data_table` | CSV 数据渲染为 Markdown 表格 |
| 21 | `summary_card` | 摘要卡片（关键指标） |
| 22 | `dashboard_layout` | 仪表盘网格布局 |
| 23 | `kpi_card` | KPI 指标卡片 |
| 24 | `comparison_table` | 多项目对比表 |
| 25 | `trend_indicator` | 趋势指标（变化对比） |
| 26 | `export_markdown` | 组装完整 Markdown 文档 |

### 辅助工具（6个）

| 序号 | 工具名称 | 功能描述 |
| --- | --- | --- |
| 27 | `parse_csv_string` | CSV 字符串解析 |
| 28 | `color_palette` | 颜色色板生成 |
| 29 | `format_number` | 数字格式化 |
| 30 | `validate_data` | 数据验证 |
| 31 | `detect_outliers` | 异常值检测 |
| 32 | `normalize_data` | 数据归一化 |

## 技术栈

| 技术 | 版本要求 | 用途 |
| --- | --- | --- |
| Python | >= 3.10 | 运行环境 |
| FastMCP (mcp) | >= 1.0.0 | MCP 服务器框架 |
| matplotlib | latest | 图表绘制与渲染 |
| numpy | latest | 数值计算与矩阵操作 |
| pandas | latest | 数据处理与分析 |

## 项目结构

```
mcp-data-viz/
├── server.py          # 主入口，FastMCP 服务器，注册32个工具
├── chart_tools.py     # 图表工具模块（18个图表函数）
├── report_tools.py    # 报告工具模块（8个报告函数）
├── utils.py           # 辅助函数模块（6个工具函数）
├── requirements.txt   # Python 依赖
├── README.md          # 项目文档
├── SKILL.md           # SkillHub 技能描述
└── output/            # 图表输出目录（自动创建）
```

## 测试

运行单元测试：

```bash
pip install pytest flake8
pytest tests/ -v --tb=short
```

代码质量检查：

```bash
flake8 . --count --max-line-length=120 --statistics
```

## 许可证

MIT License
