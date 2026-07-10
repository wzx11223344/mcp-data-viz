"""
report_tools.py - 报告工具模块

提供 HTML 报告生成、数据表渲染、摘要卡片、仪表盘布局、KPI 卡片、
比较表、趋势指标、Markdown 导出等8种报告工具函数。
所有函数返回 Markdown 格式字符串。
"""

import os
import html
import json
import numpy as np
from typing import List, Dict, Any, Optional

from utils import parse_csv_string, format_number, parse_label_list


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------

def _calc_stats(values: List[float]) -> Dict[str, float]:
    """计算数值列表的统计信息。"""
    arr = np.array(values, dtype=float)
    return {
        "count": int(len(arr)),
        "sum": float(arr.sum()),
        "mean": float(arr.mean()),
        "median": float(np.median(arr)),
        "std": float(arr.std()),
        "min": float(arr.min()),
        "max": float(arr.max()),
    }


def _trend_icon(direction: str) -> str:
    """返回趋势图标。"""
    icons = {
        "up": "↑",
        "down": "↓",
        "flat": "→",
    }
    return icons.get(direction, "→")


def _trend_color(direction: str, positive_is_good: bool = True) -> str:
    """返回趋势颜色（用于HTML）。"""
    if direction == "up":
        return "#27AE60" if positive_is_good else "#E74C3C"
    elif direction == "down":
        return "#E74C3C" if positive_is_good else "#27AE60"
    return "#95A5A6"


# ===========================================================================
# 1. generate_html_report - 生成HTML报告
# ===========================================================================

def generate_html_report(
    title: str,
    content: str,
    style: str = "modern",
    include_meta: bool = True,
) -> str:
    """
    生成完整的 HTML 报告。

    参数:
        title: 报告标题
        content: 报告正文内容（Markdown或HTML片段均可）
        style: 样式风格，可选: modern（现代）, minimal（极简）, corporate（商务）
        include_meta: 是否包含元数据（生成时间等），默认 True

    返回:
        Markdown 代码块包裹的完整 HTML 报告字符串

    示例:
        >>> report = generate_html_report("月度报告", "# 1月数据\\n本月营收增长15%")
    """
    from datetime import datetime

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    styles = {
        "modern": """
        body { font-family: 'Segoe UI', Arial, sans-serif; max-width: 900px;
               margin: 0 auto; padding: 30px; background: #f8f9fa; color: #2c3e50; }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; }
        table { border-collapse: collapse; width: 100%; margin: 15px 0; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background: #3498db; color: white; }
        tr:nth-child(even) { background: #f2f2f2; }
        .meta { color: #7f8c8d; font-size: 0.85em; margin-bottom: 20px; }
        """,
        "minimal": """
        body { font-family: Georgia, serif; max-width: 800px;
               margin: 0 auto; padding: 40px; background: #fff; color: #333; }
        h1 { font-size: 2em; margin-bottom: 5px; }
        table { border-collapse: collapse; width: 100%; margin: 15px 0; }
        th, td { border: 1px solid #ccc; padding: 8px; }
        th { background: #f5f5f5; }
        .meta { color: #999; font-size: 0.8em; }
        """,
        "corporate": """
        body { font-family: 'Helvetica Neue', Arial, sans-serif; max-width: 1000px;
               margin: 0 auto; padding: 40px; background: #fff; color: #333; }
        h1 { color: #1a5276; border-bottom: 2px solid #2980b9; padding-bottom: 12px;
             font-size: 1.8em; }
        h2 { color: #2874a6; border-left: 4px solid #2980b9; padding-left: 12px; }
        table { border-collapse: collapse; width: 100%; margin: 15px 0; }
        th { background: #2980b9; color: white; padding: 10px; text-align: left; }
        td { border-bottom: 1px solid #e0e0e0; padding: 10px; }
        tr:hover { background: #eaf2f8; }
        .meta { color: #7f8c8d; font-size: 0.85em; border-top: 1px solid #eee;
                margin-top: 20px; padding-top: 10px; }
        """,
    }

    css = styles.get(style, styles["modern"])

    meta_html = ""
    if include_meta:
        meta_html = f'<div class="meta">生成时间：{now}</div>'

    # 简单的 Markdown 转换
    html_content = content
    # 转换标题
    import re
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    # 转换粗体
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    # 转换段落（连续两个换行）
    html_content = re.sub(r'\n\n', '</p><p>', html_content)
    html_content = f'<p>{html_content}</p>'

    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <style>{css}</style>
</head>
<body>
    <h1>{html.escape(title)}</h1>
    {meta_html}
    {html_content}
</body>
</html>"""

    return f"```html\n{full_html}\n```"


# ===========================================================================
# 2. data_table - 数据表渲染
# ===========================================================================

def data_table(
    data: str,
    caption: str = "",
    highlight_max: bool = False,
    highlight_min: bool = False,
) -> str:
    """
    将 CSV 数据渲染为 Markdown 表格。

    参数:
        data: CSV格式数据字符串，第一行为表头。
              例如 "name,score\\nAlice,95\\nBob,87"
        caption: 表格标题（显示在表格上方）
        highlight_max: 是否高亮每列最大值，默认 False
        highlight_min: 是否高亮每列最小值，默认 False

    返回:
        Markdown格式的表格字符串

    示例:
        >>> table = data_table("name,score\\nAlice,95\\nBob,87", caption="成绩表")
    """
    header, rows = parse_csv_string(data, has_header=True)

    if not header:
        return "*错误：数据格式不正确，请确保第一行为表头*"

    # 构建Markdown表格
    lines = []

    if caption:
        lines.append(f"**{caption}**")
        lines.append("")

    # 表头行
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * len(header)) + " |")

    # 找出数值列的最大值和最小值用于高亮
    max_vals: Dict[int, float] = {}
    min_vals: Dict[int, float] = {}

    if highlight_max or highlight_min:
        for col_idx in range(len(header)):
            col_values = []
            for row in rows:
                if col_idx < len(row):
                    try:
                        col_values.append(float(row[col_idx]))
                    except ValueError:
                        pass
            if col_values:
                if highlight_max:
                    max_vals[col_idx] = max(col_values)
                if highlight_min:
                    min_vals[col_idx] = min(col_values)

    # 数据行
    for row in rows:
        cells = []
        for col_idx in range(len(header)):
            cell = row[col_idx] if col_idx < len(row) else ""
            try:
                val = float(cell)
                if highlight_max and col_idx in max_vals and val == max_vals[col_idx]:
                    cell = f"**{cell}**"
                elif highlight_min and col_idx in min_vals and val == min_vals[col_idx]:
                    cell = f"*{cell}*"
            except ValueError:
                pass
            cells.append(cell)
        lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines)


# ===========================================================================
# 3. summary_card - 摘要卡片
# ===========================================================================

def summary_card(
    title: str,
    metrics: str,
    description: str = "",
) -> str:
    """
    生成摘要卡片（展示关键指标）。

    参数:
        title: 卡片标题
        metrics: 逗号分隔的指标键值对，格式为 "键:值"。
                 例如 "总数:1000,平均:50.5,最大:95"
        description: 卡片描述文字

    返回:
        Markdown格式的摘要卡片字符串

    示例:
        >>> card = summary_card("销售概览", "总额:50000,订单:320,客单价:156.25")
    """
    pairs = [m.strip() for m in metrics.split(",") if m.strip()]

    lines = []
    lines.append(f"### {title}")
    lines.append("")
    lines.append("| 指标 | 值 |")
    lines.append("| --- | --- |")

    for pair in pairs:
        if ":" in pair:
            key, val = pair.split(":", 1)
            lines.append(f"| {key.strip()} | {val.strip()} |")
        elif "=" in pair:
            key, val = pair.split("=", 1)
            lines.append(f"| {key.strip()} | {val.strip()} |")
        else:
            lines.append(f"| {pair} | |")

    if description:
        lines.append("")
        lines.append(f"> {description}")

    return "\n".join(lines)


# ===========================================================================
# 4. dashboard_layout - 仪表盘布局
# ===========================================================================

def dashboard_layout(
    title: str,
    sections: str,
    columns: int = 2,
) -> str:
    """
    生成仪表盘布局（将多个组件组织为网格布局）。

    参数:
        title: 仪表盘标题
        sections: 分号分隔的组件内容，每个组件为 "组件标题|内容"。
                  例如 "销售额|¥50,000;订单数|320件;转化率|3.5%;客单价|¥156"
        columns: 布局列数，默认 2

    返回:
        Markdown格式的仪表盘布局字符串

    示例:
        >>> dashboard = dashboard_layout("运营看板", "销售额|¥50000;订单|320", columns=2)
    """
    components = [s.strip() for s in sections.split(";") if s.strip()]

    lines = []
    lines.append(f"# {title}")
    lines.append("")

    # 使用Markdown表格模拟网格布局
    for i in range(0, len(components), columns):
        row_components = components[i:i + columns]
        # 补齐到指定列数
        while len(row_components) < columns:
            row_components.append("")

        # 构建表头（组件标题）
        headers = []
        for comp in row_components:
            if comp and "|" in comp:
                comp_title, _ = comp.split("|", 1)
                headers.append(comp_title.strip())
            elif comp:
                headers.append(comp.strip())
            else:
                headers.append("")

        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join(["---"] * columns) + " |")

        # 构建内容行
        contents = []
        for comp in row_components:
            if comp and "|" in comp:
                _, comp_content = comp.split("|", 1)
                contents.append(comp_content.strip())
            elif comp:
                contents.append(comp.strip())
            else:
                contents.append("")

        lines.append("| " + " | ".join(contents) + " |")
        lines.append("")

    return "\n".join(lines)


# ===========================================================================
# 5. kpi_card - KPI卡片
# ===========================================================================

def kpi_card(
    label: str,
    value: str,
    target: str = "",
    unit: str = "",
    trend: str = "",
    trend_value: str = "",
) -> str:
    """
    生成 KPI 指标卡片。

    参数:
        label: KPI名称，例如 "月度营收"
        value: 当前值，例如 "50000"
        target: 目标值（可选），例如 "55000"
        unit: 单位，例如 "元" 或 "%"
        trend: 趋势方向，可选: "up", "down", "flat"
        trend_value: 趋势变化值，例如 "+15.2%" 或 "-3.5%"

    返回:
        Markdown格式的KPI卡片字符串

    示例:
        >>> card = kpi_card("月度营收", "50000", target="55000", unit="元",
        ...                 trend="up", trend_value="+15.2%")
    """
    lines = []
    lines.append(f"### {label}")
    lines.append("")

    # 格式化数值
    try:
        formatted_value = format_number(float(value), suffix=unit)
    except ValueError:
        formatted_value = f"{value}{unit}"

    # 构建表格
    lines.append(f"| 指标 | 值 |")
    lines.append(f"| --- | --- |")
    lines.append(f"| 当前值 | {formatted_value} |")

    if target:
        try:
            formatted_target = format_number(float(target), suffix=unit)
            # 计算达成率
            achievement = float(value) / float(target) * 100
            lines.append(f"| 目标值 | {formatted_target} |")
            lines.append(f"| 达成率 | {achievement:.1f}% |")
        except ValueError:
            lines.append(f"| 目标值 | {target}{unit} |")

    if trend and trend_value:
        icon = _trend_icon(trend)
        lines.append(f"| 趋势 | {icon} {trend_value} |")

    return "\n".join(lines)


# ===========================================================================
# 6. comparison_table - 比较表
# ===========================================================================

def comparison_table(
    items: str,
    attributes: str,
    data: str,
    highlight_best: bool = True,
) -> str:
    """
    生成多项目对比表。

    参数:
        items: 逗号分隔的项目名称，例如 "产品A,产品B,产品C"
        attributes: 逗号分隔的属性名称，例如 "价格,评分,销量"
        data: 分号分隔的数据矩阵，每行对应一个项目的属性值。
              例如 "99,4.5,1000;129,4.2,800;89,4.7,1200"
        highlight_best: 是否高亮每列最优值（数值列取最大或最小），默认 True

    返回:
        Markdown格式的比较表字符串

    示例:
        >>> table = comparison_table(
        ...     "产品A,产品B,产品C",
        ...     "价格,评分,销量",
        ...     "99,4.5,1000;129,4.2,800;89,4.7,1200"
        ... )
    """
    item_list = parse_label_list(items)
    attr_list = parse_label_list(attributes)
    rows = [parse_number_list(row) if all(
        self_is_num(r) for r in row.split(",")
    ) else [r.strip() for r in row.split(",")]
        for row in data.split(";") if row.strip()
    ] if False else []  # 兼容性处理

    # 重新解析数据
    data_rows = []
    for row_str in data.split(";"):
        row_str = row_str.strip()
        if not row_str:
            continue
        cells = [c.strip() for c in row_str.split(",")]
        # 尝试转为数值
        parsed_cells = []
        for c in cells:
            try:
                parsed_cells.append(float(c))
            except ValueError:
                parsed_cells.append(c)
        data_rows.append(parsed_cells)

    # 找每列最优值
    best_vals: Dict[int, Any] = {}
    if highlight_best:
        for col_idx in range(len(attr_list)):
            col_vals = []
            for row in data_rows:
                if col_idx < len(row) and isinstance(row[col_idx], (int, float)):
                    col_vals.append(row[col_idx])

            if col_vals:
                # 价格类取最小值，其他取最大值
                attr_name = attr_list[col_idx].lower()
                if "价" in attr_name or "cost" in attr_name or "price" in attr_name:
                    best_vals[col_idx] = min(col_vals)
                else:
                    best_vals[col_idx] = max(col_vals)

    # 构建表格
    lines = []
    header = ["项目"] + attr_list
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * len(header)) + " |")

    for i, row in enumerate(data_rows):
        cells = [item_list[i] if i < len(item_list) else f"项目{i+1}"]
        for col_idx in range(len(attr_list)):
            val = row[col_idx] if col_idx < len(row) else ""
            if isinstance(val, float):
                val_str = format_number(val, decimals=2)
            else:
                val_str = str(val)
            # 高亮最优值
            if highlight_best and col_idx in best_vals and val == best_vals[col_idx]:
                val_str = f"**{val_str}**"
            cells.append(val_str)
        lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines)


def self_is_num(s):
    """辅助函数：判断字符串是否为数字。"""
    try:
        float(s.strip())
        return True
    except ValueError:
        return False


# ===========================================================================
# 7. trend_indicator - 趋势指标
# ===========================================================================

def trend_indicator(
    label: str,
    current: str,
    previous: str,
    unit: str = "",
    positive_is_good: bool = True,
) -> str:
    """
    生成趋势指标（对比当前值与之前值的变化）。

    参数:
        label: 指标名称
        current: 当前值
        previous: 之前的值（用于对比）
        unit: 单位，例如 "%" 或 "元"
        positive_is_good: 正向变化是否为好事，默认 True。
                          例如营收增长为好(True)，成本增长为坏(False)

    返回:
        Markdown格式的趋势指标字符串

    示例:
        >>> indicator = trend_indicator("月度营收", "50000", "45000", unit="元")
    """
    try:
        curr = float(current)
        prev = float(previous)
    except ValueError:
        return f"**{label}**: 当前 {current}，之前 {previous}（无法计算变化）"

    diff = curr - prev
    pct_change = (diff / prev * 100) if prev != 0 else 0.0

    if diff > 0:
        direction = "up"
        trend_text = "上升"
    elif diff < 0:
        direction = "down"
        trend_text = "下降"
    else:
        direction = "flat"
        trend_text = "持平"

    # 判断好坏
    is_good = (direction == "up" and positive_is_good) or \
              (direction == "down" and not positive_is_good) or \
              (direction == "flat")
    status_emoji = "✅" if is_good else "⚠️" if direction != "flat" else "➖"

    lines = []
    lines.append(f"### {label}")
    lines.append("")
    lines.append(f"| 指标 | 值 |")
    lines.append(f"| --- | --- |")
    lines.append(f"| 当前值 | {format_number(curr, suffix=unit)} |")
    lines.append(f"| 上期值 | {format_number(prev, suffix=unit)} |")
    lines.append(f"| 变化量 | {format_number(diff, suffix=unit)} |")
    lines.append(f"| 变化率 | {pct_change:+.2f}% |")
    lines.append(f"| 趋势 | {trend_text} {status_emoji} |")

    return "\n".join(lines)


# ===========================================================================
# 8. export_markdown - 导出Markdown
# ===========================================================================

def export_markdown(
    title: str,
    sections: str,
    include_toc: bool = True,
    include_footer: bool = True,
) -> str:
    """
    将多个内容段落组装为完整的 Markdown 文档。

    参数:
        title: 文档标题
        sections: 分号分隔的章节，每个章节格式为 "章节标题|章节内容"。
                  例如 "概述|这是概述内容;数据分析|数据表明...;结论|综上所述..."
        include_toc: 是否包含目录，默认 True
        include_footer: 是否包含页脚（生成时间），默认 True

    返回:
        完整的 Markdown 文档字符串

    示例:
        >>> doc = export_markdown(
        ...     "数据分析报告",
        ...     "概述|这是概述;结论|这是结论"
        ... )
    """
    from datetime import datetime

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append(f"# {title}")
    lines.append("")

    # 解析章节
    section_list = []
    for section in sections.split(";"):
        section = section.strip()
        if not section:
            continue
        if "|" in section:
            sec_title, sec_content = section.split("|", 1)
            section_list.append((sec_title.strip(), sec_content.strip()))
        else:
            section_list.append((section, ""))

    # 目录
    if include_toc and section_list:
        lines.append("## 目录")
        lines.append("")
        for i, (sec_title, _) in enumerate(section_list, 1):
            anchor = sec_title.lower().replace(" ", "-").replace("　", "-")
            lines.append(f"{i}. [{sec_title}](#{anchor})")
        lines.append("")

    # 章节内容
    for i, (sec_title, sec_content) in enumerate(section_list, 1):
        lines.append(f"## {i}. {sec_title}")
        lines.append("")
        if sec_content:
            lines.append(sec_content)
        else:
            lines.append("*（此章节暂无内容）*")
        lines.append("")

    # 页脚
    if include_footer:
        lines.append("---")
        lines.append(f"*文档生成时间：{now}*")

    return "\n".join(lines)
