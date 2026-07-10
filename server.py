"""
server.py - MCP 数据可视化服务器主入口

使用 FastMCP 框架注册 32 个数据可视化工具，包括：
- 18 个图表工具（柱状图、折线图、饼图、散点图、热力图等）
- 8 个报告工具（HTML报告、数据表、KPI卡片、仪表盘等）
- 6 个辅助工具（数据解析、颜色方案、格式化、验证等）

启动方式：
    python server.py

或使用 stdio 模式：
    mcp run server.py
"""

from mcp.server.fastmcp import FastMCP

import chart_tools
import report_tools
import utils

# ---------------------------------------------------------------------------
# 创建 FastMCP 服务器实例
# ---------------------------------------------------------------------------

mcp = FastMCP("mcp-data-viz")


# ===========================================================================
# 图表工具 (18个)
# ===========================================================================

@mcp.tool()
def bar_chart(
    categories: str,
    values: str,
    title: str = "柱状图",
    xlabel: str = "",
    ylabel: str = "",
    color_scheme: str = "default",
) -> str:
    """生成柱状图，用垂直柱子展示各类别的数值大小。

    参数:
        categories: 逗号分隔的类别标签，例如 "Q1,Q2,Q3,Q4"
        values: 逗号分隔的数值，例如 "100,200,150,300"
        title: 图表标题，默认 "柱状图"
        xlabel: X轴标签（可选）
        ylabel: Y轴标签（可选）
        color_scheme: 颜色方案，可选: default, warm, cool, pastel, grayscale, nature

    返回:
        Markdown格式的图片引用字符串，包含生成的图片文件路径
    """
    return chart_tools.bar_chart(categories, values, title, xlabel, ylabel, color_scheme)


@mcp.tool()
def grouped_bar(
    categories: str,
    data: str,
    group_names: str,
    title: str = "分组柱状图",
    xlabel: str = "",
    ylabel: str = "",
    color_scheme: str = "default",
) -> str:
    """生成分组柱状图，多组数据并列对比。

    参数:
        categories: 逗号分隔的类别标签，例如 "Q1,Q2,Q3,Q4"
        data: 分号分隔的多组数据，每组为逗号分隔的数值。
              例如 "100,200,150,300;120,180,170,280" 表示两组数据
        group_names: 逗号分隔的组名，例如 "2023年,2024年"
        title: 图表标题
        xlabel: X轴标签（可选）
        ylabel: Y轴标签（可选）
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片引用字符串
    """
    return chart_tools.grouped_bar(categories, data, group_names, title, xlabel, ylabel, color_scheme)


@mcp.tool()
def horizontal_bar(
    categories: str,
    values: str,
    title: str = "水平柱状图",
    xlabel: str = "",
    ylabel: str = "",
    color_scheme: str = "default",
) -> str:
    """生成水平柱状图，适用于类别名称较长或类别较多的场景。

    参数:
        categories: 逗号分隔的类别标签
        values: 逗号分隔的数值
        title: 图表标题
        xlabel: X轴标签（可选）
        ylabel: Y轴标签（可选）
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片引用字符串
    """
    return chart_tools.horizontal_bar(categories, values, title, xlabel, ylabel, color_scheme)


@mcp.tool()
def line_chart(
    x_values: str,
    y_values: str,
    title: str = "折线图",
    xlabel: str = "",
    ylabel: str = "",
    color_scheme: str = "default",
    marker: str = "o",
) -> str:
    """生成折线图，展示数据随时间或顺序的变化趋势。

    参数:
        x_values: 逗号分隔的X轴数值或标签
        y_values: 逗号分隔的Y轴数值
        title: 图表标题
        xlabel: X轴标签（可选）
        ylabel: Y轴标签（可选）
        color_scheme: 颜色方案
        marker: 数据点标记样式，默认 "o"（圆点）

    返回:
        Markdown格式的图片引用字符串
    """
    return chart_tools.line_chart(x_values, y_values, title, xlabel, ylabel, color_scheme, marker)


@mcp.tool()
def multi_line(
    x_values: str,
    data: str,
    series_names: str,
    title: str = "多折线图",
    xlabel: str = "",
    ylabel: str = "",
    color_scheme: str = "default",
) -> str:
    """生成多折线对比图，在一张图中展示多条数据线。

    参数:
        x_values: 逗号分隔的X轴数值或标签
        data: 分号分隔的多组Y轴数据，例如 "10,20,30;15,25,35"
        series_names: 逗号分隔的系列名称，例如 "产品A,产品B"
        title: 图表标题
        xlabel: X轴标签（可选）
        ylabel: Y轴标签（可选）
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片引用字符串
    """
    return chart_tools.multi_line(x_values, data, series_names, title, xlabel, ylabel, color_scheme)


@mcp.tool()
def area_chart(
    x_values: str,
    y_values: str,
    title: str = "面积图",
    xlabel: str = "",
    ylabel: str = "",
    color_scheme: str = "default",
    alpha: float = 0.5,
) -> str:
    """生成面积图，折线下方填充颜色，强调数量积累。

    参数:
        x_values: 逗号分隔的X轴数值或标签
        y_values: 逗号分隔的Y轴数值
        title: 图表标题
        xlabel: X轴标签（可选）
        ylabel: Y轴标签（可选）
        color_scheme: 颜色方案
        alpha: 填充透明度，默认 0.5

    返回:
        Markdown格式的图片引用字符串
    """
    return chart_tools.area_chart(x_values, y_values, title, xlabel, ylabel, color_scheme, alpha)


@mcp.tool()
def pie_chart(
    categories: str,
    values: str,
    title: str = "饼图",
    color_scheme: str = "default",
    show_percentage: bool = True,
) -> str:
    """生成饼图，展示各部分占整体的比例。

    参数:
        categories: 逗号分隔的类别标签
        values: 逗号分隔的数值
        title: 图表标题
        color_scheme: 颜色方案
        show_percentage: 是否显示百分比，默认 True

    返回:
        Markdown格式的图片引用字符串
    """
    return chart_tools.pie_chart(categories, values, title, color_scheme, show_percentage)


@mcp.tool()
def donut_chart(
    categories: str,
    values: str,
    title: str = "环形图",
    color_scheme: str = "default",
    center_text: str = "",
) -> str:
    """生成环形图，中空饼图，可在圆心显示汇总信息。

    参数:
        categories: 逗号分隔的类别标签
        values: 逗号分隔的数值
        title: 图表标题
        color_scheme: 颜色方案
        center_text: 圆心显示的文字，例如 "总计\\n1000"

    返回:
        Markdown格式的图片引用字符串
    """
    return chart_tools.donut_chart(categories, values, title, color_scheme, center_text)


@mcp.tool()
def scatter_plot(
    x_values: str,
    y_values: str,
    title: str = "散点图",
    xlabel: str = "X",
    ylabel: str = "Y",
    color_scheme: str = "default",
    size: int = 50,
) -> str:
    """生成散点图，展示两个变量之间的关系。

    参数:
        x_values: 逗号分隔的X轴数值
        y_values: 逗号分隔的Y轴数值
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        color_scheme: 颜色方案
        size: 散点大小，默认 50

    返回:
        Markdown格式的图片引用字符串
    """
    return chart_tools.scatter_plot(x_values, y_values, title, xlabel, ylabel, color_scheme, size)


@mcp.tool()
def bubble_chart(
    x_values: str,
    y_values: str,
    sizes: str,
    title: str = "气泡图",
    xlabel: str = "X",
    ylabel: str = "Y",
    color_scheme: str = "default",
) -> str:
    """生成气泡图，散点大小表示第三维度数据。

    参数:
        x_values: 逗号分隔的X轴数值
        y_values: 逗号分隔的Y轴数值
        sizes: 逗号分隔的气泡大小数值
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片引用字符串
    """
    return chart_tools.bubble_chart(x_values, y_values, sizes, title, xlabel, ylabel, color_scheme)


@mcp.tool()
def heatmap(
    data: str,
    title: str = "热力图",
    xlabel: str = "",
    ylabel: str = "",
    x_labels: str = "",
    y_labels: str = "",
    color_scheme: str = "default",
    annotate: bool = True,
) -> str:
    """生成热力图，用颜色深浅表示矩阵数据值大小。

    参数:
        data: 分号分隔的矩阵数据，每行为逗号分隔的数值。例如 "1,2,3;4,5,6;7,8,9"
        title: 图表标题
        xlabel: X轴标签（可选）
        ylabel: Y轴标签（可选）
        x_labels: 逗号分隔的X轴标签（可选）
        y_labels: 逗号分隔的Y轴标签（可选）
        color_scheme: 颜色方案
        annotate: 是否在格子中标注数值，默认 True

    返回:
        Markdown格式的图片引用字符串
    """
    return chart_tools.heatmap(data, title, xlabel, ylabel, x_labels, y_labels, color_scheme, annotate)


@mcp.tool()
def correlation_heatmap(
    data: str,
    title: str = "相关性热力图",
    column_names: str = "",
) -> str:
    """计算数据相关系数矩阵并生成热力图，展示变量间相关性。

    参数:
        data: CSV格式数据或分号分隔的数值矩阵。
              CSV格式: "a,b,c\\n1,2,3\\n4,5,6\\n7,8,9"
              矩阵格式: "1,2,3;4,5,6;7,8,9"
        title: 图表标题
        column_names: 逗号分隔的列名（可选，若data中无表头则使用）

    返回:
        Markdown格式的图片引用字符串
    """
    return chart_tools.correlation_heatmap(data, title, column_names)


@mcp.tool()
def box_plot(
    data: str,
    labels: str = "",
    title: str = "箱线图",
    ylabel: str = "",
    color_scheme: str = "default",
) -> str:
    """生成箱线图，展示数据分布的四分位数、中位数和异常值。

    参数:
        data: 分号分隔的多组数据，每组为逗号分隔的数值。例如 "1,2,3,4,5;2,4,6,8,10"
        labels: 逗号分隔的组标签，例如 "A组,B组"
        title: 图表标题
        ylabel: Y轴标签（可选）
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片引用字符串
    """
    return chart_tools.box_plot(data, labels, title, ylabel, color_scheme)


@mcp.tool()
def violin_plot(
    data: str,
    labels: str = "",
    title: str = "小提琴图",
    ylabel: str = "",
    color_scheme: str = "default",
) -> str:
    """生成小提琴图，展示数据分布的密度估计和箱线图信息。

    参数:
        data: 分号分隔的多组数据，每组为逗号分隔的数值
        labels: 逗号分隔的组标签
        title: 图表标题
        ylabel: Y轴标签（可选）
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片引用字符串
    """
    return chart_tools.violin_plot(data, labels, title, ylabel, color_scheme)


@mcp.tool()
def histogram(
    values: str,
    title: str = "直方图",
    xlabel: str = "数值",
    ylabel: str = "频数",
    bins: int = 20,
    color_scheme: str = "default",
) -> str:
    """生成直方图，展示数据分布频率。

    参数:
        values: 逗号分隔的数值
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        bins: 分箱数量，默认 20
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片引用字符串
    """
    return chart_tools.histogram(values, title, xlabel, ylabel, bins, color_scheme)


@mcp.tool()
def density_plot(
    values: str,
    title: str = "密度图",
    xlabel: str = "数值",
    ylabel: str = "密度",
    color_scheme: str = "default",
) -> str:
    """生成密度估计图，展示数据的概率密度分布曲线。

    参数:
        values: 逗号分隔的数值
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片引用字符串
    """
    return chart_tools.density_plot(values, title, xlabel, ylabel, color_scheme)


@mcp.tool()
def radar_chart(
    categories: str,
    values: str,
    title: str = "雷达图",
    color_scheme: str = "default",
) -> str:
    """生成雷达图（蛛网图），展示多维度指标的综合表现。

    参数:
        categories: 逗号分隔的维度标签，例如 "速度,力量,技巧,耐力,智力"
        values: 逗号分隔的数值（建议范围0-100），例如 "80,70,90,60,85"
        title: 图表标题
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片引用字符串
    """
    return chart_tools.radar_chart(categories, values, title, color_scheme)


@mcp.tool()
def pair_plot(
    data: str,
    column_names: str = "",
    title: str = "散点矩阵图",
    color_scheme: str = "default",
) -> str:
    """生成散点矩阵图，展示多变量两两关系的散点图矩阵。

    参数:
        data: 分号分隔的矩阵数据，每行为逗号分隔的数值。例如 "1,2,3;4,5,6;7,8,9"
        column_names: 逗号分隔的列名
        title: 图表标题
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片引用字符串
    """
    return chart_tools.pair_plot(data, column_names, title, color_scheme)


# ===========================================================================
# 报告工具 (8个)
# ===========================================================================

@mcp.tool()
def generate_html_report(
    title: str,
    content: str,
    style: str = "modern",
    include_meta: bool = True,
) -> str:
    """生成完整的HTML报告，包含样式和结构。

    参数:
        title: 报告标题
        content: 报告正文内容（支持Markdown语法）
        style: 样式风格，可选: modern（现代）, minimal（极简）, corporate（商务）
        include_meta: 是否包含元数据（生成时间等），默认 True

    返回:
        Markdown代码块包裹的完整HTML报告字符串
    """
    return report_tools.generate_html_report(title, content, style, include_meta)


@mcp.tool()
def data_table(
    data: str,
    caption: str = "",
    highlight_max: bool = False,
    highlight_min: bool = False,
) -> str:
    """将CSV数据渲染为格式化的Markdown表格。

    参数:
        data: CSV格式数据字符串，第一行为表头。例如 "name,score\\nAlice,95\\nBob,87"
        caption: 表格标题（显示在表格上方）
        highlight_max: 是否高亮每列最大值，默认 False
        highlight_min: 是否高亮每列最小值，默认 False

    返回:
        Markdown格式的表格字符串
    """
    return report_tools.data_table(data, caption, highlight_max, highlight_min)


@mcp.tool()
def summary_card(
    title: str,
    metrics: str,
    description: str = "",
) -> str:
    """生成摘要卡片，以表格形式展示关键指标。

    参数:
        title: 卡片标题
        metrics: 逗号分隔的指标键值对，格式为 "键:值"。例如 "总数:1000,平均:50.5"
        description: 卡片描述文字（可选）

    返回:
        Markdown格式的摘要卡片字符串
    """
    return report_tools.summary_card(title, metrics, description)


@mcp.tool()
def dashboard_layout(
    title: str,
    sections: str,
    columns: int = 2,
) -> str:
    """生成仪表盘布局，将多个组件组织为网格布局。

    参数:
        title: 仪表盘标题
        sections: 分号分隔的组件内容，每个组件为 "组件标题|内容"。
                  例如 "销售额|¥50,000;订单数|320件;转化率|3.5%"
        columns: 布局列数，默认 2

    返回:
        Markdown格式的仪表盘布局字符串
    """
    return report_tools.dashboard_layout(title, sections, columns)


@mcp.tool()
def kpi_card(
    label: str,
    value: str,
    target: str = "",
    unit: str = "",
    trend: str = "",
    trend_value: str = "",
) -> str:
    """生成KPI指标卡片，展示当前值、目标值和趋势。

    参数:
        label: KPI名称，例如 "月度营收"
        value: 当前值，例如 "50000"
        target: 目标值（可选），例如 "55000"
        unit: 单位，例如 "元" 或 "%"
        trend: 趋势方向，可选: "up", "down", "flat"
        trend_value: 趋势变化值，例如 "+15.2%"

    返回:
        Markdown格式的KPI卡片字符串
    """
    return report_tools.kpi_card(label, value, target, unit, trend, trend_value)


@mcp.tool()
def comparison_table(
    items: str,
    attributes: str,
    data: str,
    highlight_best: bool = True,
) -> str:
    """生成多项目对比表，高亮每列最优值。

    参数:
        items: 逗号分隔的项目名称，例如 "产品A,产品B,产品C"
        attributes: 逗号分隔的属性名称，例如 "价格,评分,销量"
        data: 分号分隔的数据矩阵，每行对应一个项目。例如 "99,4.5,1000;129,4.2,800"
        highlight_best: 是否高亮每列最优值，默认 True

    返回:
        Markdown格式的比较表字符串
    """
    return report_tools.comparison_table(items, attributes, data, highlight_best)


@mcp.tool()
def trend_indicator(
    label: str,
    current: str,
    previous: str,
    unit: str = "",
    positive_is_good: bool = True,
) -> str:
    """生成趋势指标，对比当前值与之前值的变化。

    参数:
        label: 指标名称
        current: 当前值
        previous: 之前的值（用于对比）
        unit: 单位，例如 "%" 或 "元"
        positive_is_good: 正向变化是否为好事，默认 True。
                          例如营收增长为好(True)，成本增长为坏(False)

    返回:
        Markdown格式的趋势指标字符串
    """
    return report_tools.trend_indicator(label, current, previous, unit, positive_is_good)


@mcp.tool()
def export_markdown(
    title: str,
    sections: str,
    include_toc: bool = True,
    include_footer: bool = True,
) -> str:
    """将多个内容段落组装为完整的Markdown文档。

    参数:
        title: 文档标题
        sections: 分号分隔的章节，每个章节格式为 "章节标题|章节内容"。
                  例如 "概述|这是概述内容;结论|综上所述"
        include_toc: 是否包含目录，默认 True
        include_footer: 是否包含页脚（生成时间），默认 True

    返回:
        完整的Markdown文档字符串
    """
    return report_tools.export_markdown(title, sections, include_toc, include_footer)


# ===========================================================================
# 辅助工具 (6个)
# ===========================================================================

@mcp.tool()
def parse_csv_string(
    csv_string: str,
    has_header: bool = True,
    delimiter: str = ",",
) -> str:
    """将逗号分隔的CSV字符串解析为表头和数据行。

    参数:
        csv_string: CSV格式字符串，例如 "name,age\\nAlice,30\\nBob,25"
        has_header: 第一行是否为表头，默认 True
        delimiter: 分隔符，默认为逗号

    返回:
        Markdown格式的解析结果，包含表头和数据行
    """
    header, rows = utils.parse_csv_string(csv_string, has_header, delimiter)

    lines = []
    if header:
        lines.append("**表头:**")
        lines.append("| " + " | ".join(header) + " |")
        lines.append("| " + " | ".join(["---"] * len(header)) + " |")
    else:
        lines.append("*无表头*")

    lines.append("")
    lines.append(f"**数据行数:** {len(rows)}")
    lines.append("")

    if rows:
        lines.append("**数据预览（前5行）:**")
        lines.append("")
        col_count = len(header) if header else (len(rows[0]) if rows else 0)
        for row in rows[:5]:
            cells = row + [""] * (col_count - len(row))
            lines.append("| " + " | ".join(cells[:col_count]) + " |")

    return "\n".join(lines)


@mcp.tool()
def color_palette(
    n: int = 10,
    scheme: str = "default",
    as_hex: bool = True,
) -> str:
    """生成一组颜色色板，可用于图表配色。

    参数:
        n: 需要的颜色数量，默认 10
        scheme: 颜色方案名称，可选: default, warm, cool, pastel, grayscale, nature
        as_hex: 是否返回十六进制颜色码，默认 True

    返回:
        Markdown格式的颜色列表，包含颜色名称和色值
    """
    colors = utils.color_palette(n, scheme, as_hex)

    lines = []
    lines.append(f"**颜色方案:** {scheme}（共 {len(colors)} 个颜色）")
    lines.append("")
    lines.append("| 序号 | 颜色值 |")
    lines.append("| --- | --- |")
    for i, color in enumerate(colors, 1):
        lines.append(f"| {i} | `{color}` |")

    return "\n".join(lines)


@mcp.tool()
def format_number(
    value: float,
    decimals: int = 2,
    thousands_sep: str = ",",
    suffix: str = "",
) -> str:
    """格式化数字，支持千分位分隔符、小数位数和后缀。

    参数:
        value: 要格式化的数值
        decimals: 小数位数，默认 2
        thousands_sep: 千分位分隔符，默认为逗号；传空字符串则不加分隔符
        suffix: 数值后缀，例如 "%" 或 " 元"

    返回:
        格式化后的字符串
    """
    return utils.format_number(value, decimals, thousands_sep, suffix)


@mcp.tool()
def validate_data(
    data: str,
    expected_columns: int = None,
    allow_empty: bool = False,
) -> str:
    """验证CSV格式字符串数据的完整性和有效性。

    参数:
        data: CSV格式数据字符串
        expected_columns: 期望的列数，若为 None 则不检查列数
        allow_empty: 是否允许空数据，默认 False

    返回:
        Markdown格式的验证结果，包含是否通过、错误、警告等信息
    """
    result = utils.validate_data(data, expected_columns, allow_empty)

    lines = []
    status = "✅ 通过" if result["valid"] else "❌ 失败"
    lines.append(f"**验证结果:** {status}")
    lines.append(f"**数据行数:** {result['row_count']}")
    lines.append(f"**列数:** {result['column_count']}")
    lines.append("")

    if result["errors"]:
        lines.append("**错误:**")
        for err in result["errors"]:
            lines.append(f"- {err}")
        lines.append("")

    if result["warnings"]:
        lines.append("**警告:**")
        for warn in result["warnings"]:
            lines.append(f"- {warn}")

    return "\n".join(lines)


@mcp.tool()
def detect_outliers(
    values: str,
    method: str = "iqr",
    threshold: float = 1.5,
) -> str:
    """从逗号分隔的数值中检测异常值。

    参数:
        values: 逗号分隔的数值字符串，例如 "1,2,3,100,4,5,200"
        method: 检测方法，可选: "iqr"（四分位距法）或 "zscore"（Z分数法）
        threshold: 阈值，IQR法默认1.5，Z分数法默认2.0

    返回:
        Markdown格式的检测结果，包含异常值索引、异常值列表和统计信息
    """
    result = utils.detect_outliers(values, method, threshold)

    lines = []
    lines.append(f"**检测方法:** {result.get('method', method)}")
    lines.append("")

    if "error" in result:
        lines.append(f"**错误:** {result['error']}")
        return "\n".join(lines)

    if "message" in result:
        lines.append(f"> {result['message']}")
        lines.append("")

    outlier_indices = result.get("outlier_indices", [])
    outlier_values = result.get("outlier_values", [])

    lines.append(f"**异常值数量:** {len(outlier_indices)}")
    lines.append("")

    if outlier_indices:
        lines.append("| 序号 | 索引 | 异常值 |")
        lines.append("| --- | --- | --- |")
        for i, (idx, val) in enumerate(zip(outlier_indices, outlier_values), 1):
            lines.append(f"| {i} | {idx} | {val:.2f} |")
        lines.append("")

    stats = result.get("stats", {})
    if stats:
        lines.append("**统计信息:**")
        lines.append("| 统计量 | 值 |")
        lines.append("| --- | --- |")
        for k, v in stats.items():
            if isinstance(v, float):
                lines.append(f"| {k} | {v:.4f} |")
            else:
                lines.append(f"| {k} | {v} |")

    return "\n".join(lines)


@mcp.tool()
def normalize_data(
    values: str,
    method: str = "minmax",
    target_min: float = 0.0,
    target_max: float = 1.0,
) -> str:
    """将逗号分隔的数值进行归一化处理。

    参数:
        values: 逗号分隔的数值字符串，例如 "10,20,30,40,50"
        method: 归一化方法，可选: "minmax" 或 "zscore"
        target_min: Min-Max方法的目标最小值，默认 0.0
        target_max: Min-Max方法的目标最大值，默认 1.0

    返回:
        Markdown格式的归一化结果，包含原始值和归一化值的对比
    """
    result = utils.normalize_data(values, method, target_min, target_max)

    if result.startswith("错误"):
        return result

    original = [x.strip() for x in values.split(",") if x.strip()]
    normalized = result.split(",")

    lines = []
    lines.append(f"**归一化方法:** {method}")
    if method == "minmax":
        lines.append(f"**目标范围:** [{target_min}, {target_max}]")
    lines.append("")

    lines.append("| 序号 | 原始值 | 归一化值 |")
    lines.append("| --- | --- | --- |")
    for i, (orig, norm) in enumerate(zip(original, normalized), 1):
        lines.append(f"| {i} | {orig} | {norm} |")

    return "\n".join(lines)


# ===========================================================================
# 启动服务器
# ===========================================================================

if __name__ == "__main__":
    mcp.run()
