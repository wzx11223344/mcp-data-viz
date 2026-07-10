---
name: mcp-data-viz-zx
displayName: 数据可视化MCP服务器
version: 1.0.1
summary: 32个MCP工具：柱状图/折线图/饼图/散点图/热力图/箱线图/直方图/雷达图/HTML报告/KPI卡片/数据表/仪表盘
tags: [mcp, visualization, chart, matplotlib]
license: MIT
---

# 数据可视化 MCP 服务器

## 概述

基于 FastMCP 框架的数据可视化服务器，提供 **32 个 MCP 工具**，涵盖图表生成、报告构建和数据处理三大能力域。

## 能力域

### 图表工具（18个）
柱状图、分组柱状图、水平柱状图、折线图、多折线图、面积图、饼图、环形图、散点图、气泡图、热力图、相关性热力图、箱线图、小提琴图、直方图、密度图、雷达图、散点矩阵图。

### 报告工具（8个）
HTML报告生成、数据表渲染、摘要卡片、仪表盘布局、KPI卡片、对比表、趋势指标、Markdown文档导出。

### 辅助工具（6个）
CSV数据解析、颜色色板生成、数字格式化、数据验证、异常值检测、数据归一化。

## 使用方式

在支持 MCP 的客户端中配置此服务器：

```json
{
  "mcpServers": {
    "data-viz": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/path/to/mcp-data-viz"
    }
  }
}
```

## 技术栈

- FastMCP (Model Context Protocol)
- matplotlib (图表渲染)
- numpy (数值计算)
- pandas (数据处理)
