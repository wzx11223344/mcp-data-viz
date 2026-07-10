"""
chart_tools.py - 图表工具模块

提供18种图表生成函数，使用 matplotlib 绘图并保存到 output 目录。
所有函数返回生成图片的文件路径（Markdown格式）。
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.rcParams as rcParams
from typing import List, Optional

from utils import (
    parse_number_list,
    parse_label_list,
    color_palette,
    parse_csv_string,
)

# ---------------------------------------------------------------------------
# 全局配置：中文字体 + 负号显示
# ---------------------------------------------------------------------------

rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
rcParams["axes.unicode_minus"] = False
rcParams["figure.dpi"] = 150
rcParams["savefig.dpi"] = 150
rcParams["savefig.bbox"] = "tight"

# 输出目录
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 图表计数器（用于生成唯一文件名）
_chart_counter = [0]


def _next_filename(prefix: str = "chart") -> str:
    """生成下一个唯一的图片文件名。"""
    _chart_counter[0] += 1
    return os.path.join(
        OUTPUT_DIR, f"{prefix}_{_chart_counter[0]}.png"
    )


def _apply_style(ax, title: str, xlabel: str = "", ylabel: str = ""):
    """统一设置图表样式。"""
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=11)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11)
    ax.spine["top"].set_visible(False)
    ax.spine["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.3, linestyle="--")


# ===========================================================================
# 1. bar_chart - 柱状图
# ===========================================================================

def bar_chart(
    categories: str,
    values: str,
    title: str = "柱状图",
    xlabel: str = "",
    ylabel: str = "",
    color_scheme: str = "default",
) -> str:
    """
    生成基本柱状图。

    参数:
        categories: 逗号分隔的类别标签，例如 "Q1,Q2,Q3,Q4"
        values: 逗号分隔的数值，例如 "100,200,150,300"
        title: 图表标题，默认 "柱状图"
        xlabel: X轴标签
        ylabel: Y轴标签
        color_scheme: 颜色方案，可选: default, warm, cool, pastel, grayscale, nature

    返回:
        Markdown格式的图片路径字符串，例如 "![柱状图](output/bar_chart_1.png)"
    """
    cats = parse_label_list(categories)
    vals = parse_number_list(values)
    colors = color_palette(len(cats), scheme=color_scheme)

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(cats, vals, color=colors, edgecolor="white", linewidth=0.8)

    # 在柱子上方标注数值
    for bar, val in zip(bars, vals):
        ax.text(
            bar.get_x() + bar.get_width() / 2, bar.get_height() + max(vals) * 0.01,
            f"{val:.1f}", ha="center", va="bottom", fontsize=9,
        )

    _apply_style(ax, title, xlabel, ylabel)
    plt.tight_layout()

    filepath = _next_filename("bar_chart")
    fig.savefig(filepath)
    plt.close(fig)
    return f"![{title}]({filepath})"


# ===========================================================================
# 2. grouped_bar - 分组柱状图
# ===========================================================================

def grouped_bar(
    categories: str,
    data: str,
    group_names: str,
    title: str = "分组柱状图",
    xlabel: str = "",
    ylabel: str = "",
    color_scheme: str = "default",
) -> str:
    """
    生成分组柱状图（多组数据并列对比）。

    参数:
        categories: 逗号分隔的类别标签，例如 "Q1,Q2,Q3,Q4"
        data: 分号分隔的多组数据，每组为逗号分隔的数值。
              例如 "100,200,150,300;120,180,170,280" 表示两组数据
        group_names: 逗号分隔的组名，例如 "2023年,2024年"
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片路径字符串
    """
    cats = parse_label_list(categories)
    group_labels = parse_label_list(group_names)
    groups = [parse_number_list(row) for row in data.split(";") if row.strip()]
    colors = color_palette(len(groups), scheme=color_scheme)

    x = np.arange(len(cats))
    width = 0.8 / len(groups)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for i, (group, label) in enumerate(zip(groups, group_labels)):
        offset = (i - len(groups) / 2 + 0.5) * width
        bars = ax.bar(x + offset, group, width, label=label, color=colors[i],
                       edgecolor="white", linewidth=0.5)
        for bar, val in zip(bars, group):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                    f"{val:.0f}", ha="center", va="bottom", fontsize=7)

    ax.set_xticks(x)
    ax.set_xticklabels(cats)
    ax.legend(fontsize=9)
    _apply_style(ax, title, xlabel, ylabel)
    plt.tight_layout()

    filepath = _next_filename("grouped_bar")
    fig.savefig(filepath)
    plt.close(fig)
    return f"![{title}]({filepath})"


# ===========================================================================
# 3. horizontal_bar - 水平柱状图
# ===========================================================================

def horizontal_bar(
    categories: str,
    values: str,
    title: str = "水平柱状图",
    xlabel: str = "",
    ylabel: str = "",
    color_scheme: str = "default",
) -> str:
    """
    生成水平柱状图。

    参数:
        categories: 逗号分隔的类别标签
        values: 逗号分隔的数值
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片路径字符串
    """
    cats = parse_label_list(categories)
    vals = parse_number_list(values)
    colors = color_palette(len(cats), scheme=color_scheme)

    fig, ax = plt.subplots(figsize=(8, max(4, len(cats) * 0.5)))
    bars = ax.barh(cats, vals, color=colors, edgecolor="white", linewidth=0.8)

    for bar, val in zip(bars, vals):
        ax.text(bar.get_width() + max(vals) * 0.01, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}", ha="left", va="center", fontsize=9)

    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=11)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11)
    ax.spine["top"].set_visible(False)
    ax.spine["right"].set_visible(False)
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    plt.tight_layout()

    filepath = _next_filename("horizontal_bar")
    fig.savefig(filepath)
    plt.close(fig)
    return f"![{title}]({filepath})"


# ===========================================================================
# 4. line_chart - 折线图
# ===========================================================================

def line_chart(
    x_values: str,
    y_values: str,
    title: str = "折线图",
    xlabel: str = "",
    ylabel: str = "",
    color_scheme: str = "default",
    marker: str = "o",
) -> str:
    """
    生成基本折线图。

    参数:
        x_values: 逗号分隔的X轴数值或标签
        y_values: 逗号分隔的Y轴数值
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        color_scheme: 颜色方案
        marker: 数据点标记样式，默认 "o"（圆点），可选 "s","^","d",""等

    返回:
        Markdown格式的图片路径字符串
    """
    x_labels = parse_label_list(x_values)
    y_vals = parse_number_list(y_values)

    # 尝试将x转为数值
    try:
        x_vals = [float(x) for x in x_labels]
    except ValueError:
        x_vals = list(range(len(x_labels)))

    colors = color_palette(1, scheme=color_scheme)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x_vals, y_vals, color=colors[0], marker=marker, linewidth=2,
            markersize=6, markerfacecolor="white", markeredgewidth=1.5)

    _apply_style(ax, title, xlabel, ylabel)
    plt.tight_layout()

    filepath = _next_filename("line_chart")
    fig.savefig(filepath)
    plt.close(fig)
    return f"![{title}]({filepath})"


# ===========================================================================
# 5. multi_line - 多折线图
# ===========================================================================

def multi_line(
    x_values: str,
    data: str,
    series_names: str,
    title: str = "多折线图",
    xlabel: str = "",
    ylabel: str = "",
    color_scheme: str = "default",
) -> str:
    """
    生成多条折线对比图。

    参数:
        x_values: 逗号分隔的X轴数值或标签
        data: 分号分隔的多组Y轴数据，每组为逗号分隔的数值。
              例如 "10,20,30,40;15,25,35,45" 表示两条线
        series_names: 逗号分隔的系列名称，例如 "产品A,产品B"
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片路径字符串
    """
    x_labels = parse_label_list(x_values)
    series = parse_label_list(series_names)
    groups = [parse_number_list(row) for row in data.split(";") if row.strip()]
    colors = color_palette(len(groups), scheme=color_scheme)
    markers = ["o", "s", "^", "d", "v", "p", "*", "h"]

    try:
        x_vals = [float(x) for x in x_labels]
    except ValueError:
        x_vals = list(range(len(x_labels)))

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for i, (y_vals, name) in enumerate(zip(groups, series)):
        m = markers[i % len(markers)]
        ax.plot(x_vals, y_vals, color=colors[i], marker=m, linewidth=2,
                markersize=5, label=name, markerfacecolor="white",
                markeredgewidth=1.2)

    ax.legend(fontsize=9)
    _apply_style(ax, title, xlabel, ylabel)
    plt.tight_layout()

    filepath = _next_filename("multi_line")
    fig.savefig(filepath)
    plt.close(fig)
    return f"![{title}]({filepath})"


# ===========================================================================
# 6. area_chart - 面积图
# ===========================================================================

def area_chart(
    x_values: str,
    y_values: str,
    title: str = "面积图",
    xlabel: str = "",
    ylabel: str = "",
    color_scheme: str = "default",
    alpha: float = 0.5,
) -> str:
    """
    生成面积图（折线下方填充颜色）。

    参数:
        x_values: 逗号分隔的X轴数值或标签
        y_values: 逗号分隔的Y轴数值
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        color_scheme: 颜色方案
        alpha: 填充透明度，默认 0.5

    返回:
        Markdown格式的图片路径字符串
    """
    x_labels = parse_label_list(x_values)
    y_vals = parse_number_list(y_values)
    colors = color_palette(1, scheme=color_scheme)

    try:
        x_vals = [float(x) for x in x_labels]
    except ValueError:
        x_vals = list(range(len(x_labels)))

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.fill_between(x_vals, y_vals, alpha=alpha, color=colors[0])
    ax.plot(x_vals, y_vals, color=colors[0], linewidth=2, marker="o", markersize=4)

    _apply_style(ax, title, xlabel, ylabel)
    plt.tight_layout()

    filepath = _next_filename("area_chart")
    fig.savefig(filepath)
    plt.close(fig)
    return f"![{title}]({filepath})"


# ===========================================================================
# 7. pie_chart - 饼图
# ===========================================================================

def pie_chart(
    categories: str,
    values: str,
    title: str = "饼图",
    color_scheme: str = "default",
    show_percentage: bool = True,
) -> str:
    """
    生成饼图。

    参数:
        categories: 逗号分隔的类别标签
        values: 逗号分隔的数值
        title: 图表标题
        color_scheme: 颜色方案
        show_percentage: 是否显示百分比，默认 True

    返回:
        Markdown格式的图片路径字符串
    """
    cats = parse_label_list(categories)
    vals = parse_number_list(values)
    colors = color_palette(len(cats), scheme=color_scheme)

    fig, ax = plt.subplots(figsize=(7, 7))
    explode = [0.02] * len(cats)

    if show_percentage:
        autopct = "%1.1f%%"
    else:
        autopct = None

    wedges, texts, autotexts = ax.pie(
        vals, labels=cats, colors=colors, autopct=autopct,
        startangle=90, explode=explode, shadow=False,
        textprops={"fontsize": 10},
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )
    for t in autotexts:
        t.set_fontsize(9)
        t.set_fontweight("bold")

    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.axis("equal")
    plt.tight_layout()

    filepath = _next_filename("pie_chart")
    fig.savefig(filepath)
    plt.close(fig)
    return f"![{title}]({filepath})"


# ===========================================================================
# 8. donut_chart - 环形图
# ===========================================================================

def donut_chart(
    categories: str,
    values: str,
    title: str = "环形图",
    color_scheme: str = "default",
    center_text: str = "",
) -> str:
    """
    生成环形图（中空饼图）。

    参数:
        categories: 逗号分隔的类别标签
        values: 逗号分隔的数值
        title: 图表标题
        color_scheme: 颜色方案
        center_text: 圆心显示的文字，例如 "总计\\n1000"

    返回:
        Markdown格式的图片路径字符串
    """
    cats = parse_label_list(categories)
    vals = parse_number_list(values)
    colors = color_palette(len(cats), scheme=color_scheme)

    fig, ax = plt.subplots(figsize=(7, 7))

    wedges, texts, autotexts = ax.pie(
        vals, labels=cats, colors=colors, autopct="%1.1f%%",
        startangle=90, pctdistance=0.82,
        textprops={"fontsize": 10},
        wedgeprops={"edgecolor": "white", "linewidth": 2, "width": 0.4},
    )
    for t in autotexts:
        t.set_fontsize(9)

    if center_text:
        ax.text(0, 0, center_text, ha="center", va="center",
                fontsize=13, fontweight="bold")

    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.axis("equal")
    plt.tight_layout()

    filepath = _next_filename("donut_chart")
    fig.savefig(filepath)
    plt.close(fig)
    return f"![{title}]({filepath})"


# ===========================================================================
# 9. scatter_plot - 散点图
# ===========================================================================

def scatter_plot(
    x_values: str,
    y_values: str,
    title: str = "散点图",
    xlabel: str = "X",
    ylabel: str = "Y",
    color_scheme: str = "default",
    size: int = 50,
) -> str:
    """
    生成散点图。

    参数:
        x_values: 逗号分隔的X轴数值
        y_values: 逗号分隔的Y轴数值
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        color_scheme: 颜色方案
        size: 散点大小，默认 50

    返回:
        Markdown格式的图片路径字符串
    """
    x_vals = parse_number_list(x_values)
    y_vals = parse_number_list(y_values)
    colors = color_palette(1, scheme=color_scheme)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x_vals, y_vals, c=colors[0], s=size, alpha=0.7,
               edgecolors="white", linewidth=0.5)

    _apply_style(ax, title, xlabel, ylabel)
    ax.grid(True, alpha=0.3, linestyle="--")
    plt.tight_layout()

    filepath = _next_filename("scatter_plot")
    fig.savefig(filepath)
    plt.close(fig)
    return f"![{title}]({filepath})"


# ===========================================================================
# 10. bubble_chart - 气泡图
# ===========================================================================

def bubble_chart(
    x_values: str,
    y_values: str,
    sizes: str,
    title: str = "气泡图",
    xlabel: str = "X",
    ylabel: str = "Y",
    color_scheme: str = "default",
) -> str:
    """
    生成气泡图（散点大小表示第三维度）。

    参数:
        x_values: 逗号分隔的X轴数值
        y_values: 逗号分隔的Y轴数值
        sizes: 逗号分隔的气泡大小数值
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片路径字符串
    """
    x_vals = parse_number_list(x_values)
    y_vals = parse_number_list(y_values)
    s_vals = parse_number_list(sizes)

    # 将尺寸缩放到合理范围
    s_arr = np.array(s_vals, dtype=float)
    if s_arr.max() > 0:
        s_scaled = (s_arr / s_arr.max()) * 500 + 20
    else:
        s_scaled = s_arr + 50

    colors = color_palette(len(x_vals), scheme=color_scheme)

    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(x_vals, y_vals, s=s_scaled, c=range(len(x_vals)),
                         cmap="viridis", alpha=0.6, edgecolors="white",
                         linewidth=0.5)

    _apply_style(ax, title, xlabel, ylabel)
    ax.grid(True, alpha=0.3, linestyle="--")
    plt.tight_layout()

    filepath = _next_filename("bubble_chart")
    fig.savefig(filepath)
    plt.close(fig)
    return f"![{title}]({filepath})"


# ===========================================================================
# 11. heatmap - 热力图
# ===========================================================================

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
    """
    生成热力图。

    参数:
        data: 分号分隔的矩阵数据，每行为逗号分隔的数值。
              例如 "1,2,3;4,5,6;7,8,9" 表示3x3矩阵
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        x_labels: 逗号分隔的X轴标签
        y_labels: 逗号分隔的Y轴标签
        color_scheme: 颜色方案（映射为colormap）
        annotate: 是否在格子中标注数值，默认 True

    返回:
        Markdown格式的图片路径字符串
    """
    rows = [parse_number_list(row) for row in data.split(";") if row.strip()]
    matrix = np.array(rows)

    x_lbl = parse_label_list(x_labels) if x_labels else [f"C{i+1}" for i in range(matrix.shape[1])]
    y_lbl = parse_label_list(y_labels) if y_labels else [f"R{i+1}" for i in range(matrix.shape[0])]

    # 映射颜色方案到colormap
    cmap_map = {
        "default": "YlOrRd",
        "warm": "OrRd",
        "cool": "YlGnBu",
        "pastel": "Pastel1",
        "grayscale": "Greys",
        "nature": "Set2",
    }
    cmap = cmap_map.get(color_scheme, "YlOrRd")

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(matrix, cmap=cmap, aspect="auto")

    if annotate:
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                val = matrix[i, j]
                text_color = "white" if val > matrix.mean() else "black"
                ax.text(j, i, f"{val:.1f}", ha="center", va="center",
                        fontsize=9, color=text_color)

    ax.set_xticks(range(len(x_lbl)))
    ax.set_xticklabels(x_lbl, fontsize=9)
    ax.set_yticks(range(len(y_lbl)))
    ax.set_yticklabels(y_lbl, fontsize=9)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=11)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11)
    fig.colorbar(im, ax=ax, shrink=0.8)
    plt.tight_layout()

    filepath = _next_filename("heatmap")
    fig.savefig(filepath)
    plt.close(fig)
    return f"![{title}]({filepath})"


# ===========================================================================
# 12. correlation_heatmap - 相关性热力图
# ===========================================================================

def correlation_heatmap(
    data: str,
    title: str = "相关性热力图",
    column_names: str = "",
) -> str:
    """
    计算数据的相关系数矩阵并生成热力图。

    参数:
        data: CSV格式数据（每行一个样本，每列一个变量）。
              例如 "a,b,c\\n1,2,3;4,5,6;7,8,9"
              或分号分隔的纯数值矩阵 "1,2,3;4,5,6;7,8,9"
        title: 图表标题
        column_names: 逗号分隔的列名（可选，若data中无表头则使用）

    返回:
        Markdown格式的图片路径字符串
    """
    # 尝试解析为带表头的CSV
    if "\n" in data:
        header, rows = parse_csv_string(data, has_header=True)
        if header:
            col_names = header
        else:
            col_names = parse_label_list(column_names) if column_names else \
                        [f"Var{i+1}" for i in range(len(rows[0]))]
    else:
        rows = [parse_number_list(row) for row in data.split(";") if row.strip()]
        col_names = parse_label_list(column_names) if column_names else \
                    [f"Var{i+1}" for i in range(len(rows[0]))]

    matrix = np.array(rows, dtype=float)
    corr = np.corrcoef(matrix, rowvar=False)

    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")

    for i in range(len(col_names)):
        for j in range(len(col_names)):
            val = corr[i, j]
            text_color = "white" if abs(val) > 0.5 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    fontsize=9, color=text_color)

    ax.set_xticks(range(len(col_names)))
    ax.set_xticklabels(col_names, fontsize=9, rotation=45, ha="right")
    ax.set_yticks(range(len(col_names)))
    ax.set_yticklabels(col_names, fontsize=9)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    fig.colorbar(im, ax=ax, shrink=0.8, label="相关系数")
    plt.tight_layout()

    filepath = _next_filename("correlation_heatmap")
    fig.savefig(filepath)
    plt.close(fig)
    return f"![{title}]({filepath})"


# ===========================================================================
# 13. box_plot - 箱线图
# ===========================================================================

def box_plot(
    data: str,
    labels: str = "",
    title: str = "箱线图",
    ylabel: str = "",
    color_scheme: str = "default",
) -> str:
    """
    生成箱线图（展示数据分布的四分位数和异常值）。

    参数:
        data: 分号分隔的多组数据，每组为逗号分隔的数值。
              例如 "1,2,3,4,5;2,4,6,8,10" 表示两组数据
        labels: 逗号分隔的组标签，例如 "A组,B组"
        title: 图表标题
        ylabel: Y轴标签
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片路径字符串
    """
    groups = [parse_number_list(row) for row in data.split(";") if row.strip()]
    lbls = parse_label_list(labels) if labels else [f"组{i+1}" for i in range(len(groups))]
    colors = color_palette(len(groups), scheme=color_scheme)

    fig, ax = plt.subplots(figsize=(8, 5))
    bp = ax.boxplot(groups, labels=lbls, patch_artist=True, widths=0.5,
                     medianprops={"color": "#333333", "linewidth": 2},
                     whiskerprops={"color": "#666666"},
                     capprops={"color": "#666666"})

    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    _apply_style(ax, title, "", ylabel)
    plt.tight_layout()

    filepath = _next_filename("box_plot")
    fig.savefig(filepath)
    plt.close(fig)
    return f"![{title}]({filepath})"


# ===========================================================================
# 14. violin_plot - 小提琴图
# ===========================================================================

def violin_plot(
    data: str,
    labels: str = "",
    title: str = "小提琴图",
    ylabel: str = "",
    color_scheme: str = "default",
) -> str:
    """
    生成小提琴图（展示数据分布的密度估计）。

    参数:
        data: 分号分隔的多组数据，每组为逗号分隔的数值
        labels: 逗号分隔的组标签
        title: 图表标题
        ylabel: Y轴标签
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片路径字符串
    """
    groups = [parse_number_list(row) for row in data.split(";") if row.strip()]
    lbls = parse_label_list(labels) if labels else [f"组{i+1}" for i in range(len(groups))]
    colors = color_palette(len(groups), scheme=color_scheme)

    fig, ax = plt.subplots(figsize=(8, 5))
    parts = ax.violinplot(groups, showmeans=True, showmedians=True)

    for i, pc in enumerate(parts["bodies"]):
        pc.set_facecolor(colors[i % len(colors)])
        pc.set_alpha(0.7)

    parts["cmeans"].set_color("#E74C3C")
    parts["cmedians"].set_color("#2C3E50")

    ax.set_xticks(range(1, len(lbls) + 1))
    ax.set_xticklabels(lbls)
    _apply_style(ax, title, "", ylabel)
    plt.tight_layout()

    filepath = _next_filename("violin_plot")
    fig.savefig(filepath)
    plt.close(fig)
    return f"![{title}]({filepath})"


# ===========================================================================
# 15. histogram - 直方图
# ===========================================================================

def histogram(
    values: str,
    title: str = "直方图",
    xlabel: str = "数值",
    ylabel: str = "频数",
    bins: int = 20,
    color_scheme: str = "default",
) -> str:
    """
    生成直方图（展示数据分布频率）。

    参数:
        values: 逗号分隔的数值
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        bins: 分箱数量，默认 20
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片路径字符串
    """
    vals = parse_number_list(values)
    colors = color_palette(1, scheme=color_scheme)

    fig, ax = plt.subplots(figsize=(8, 5))
    n, bins_edges, patches = ax.hist(vals, bins=bins, color=colors[0],
                                      edgecolor="white", linewidth=0.8, alpha=0.8)

    # 标注每个柱子的频数
    for count, patch in zip(n, patches):
        if count > 0:
            ax.text(patch.get_x() + patch.get_width() / 2, count + 0.5,
                    f"{int(count)}", ha="center", va="bottom", fontsize=8)

    _apply_style(ax, title, xlabel, ylabel)
    plt.tight_layout()

    filepath = _next_filename("histogram")
    fig.savefig(filepath)
    plt.close(fig)
    return f"![{title}]({filepath})"


# ===========================================================================
# 16. density_plot - 密度图
# ===========================================================================

def density_plot(
    values: str,
    title: str = "密度图",
    xlabel: str = "数值",
    ylabel: str = "密度",
    color_scheme: str = "default",
) -> str:
    """
    生成密度估计图（核密度估计曲线）。

    参数:
        values: 逗号分隔的数值
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片路径字符串
    """
    vals = np.array(parse_number_list(values))
    colors = color_palette(1, scheme=color_scheme)

    # 使用直方图的密度归一化来近似KDE
    fig, ax = plt.subplots(figsize=(8, 5))

    # 绘制直方图（密度模式）
    ax.hist(vals, bins=30, density=True, color=colors[0], alpha=0.3,
            edgecolor="white")

    # 使用简单的高斯KDE近似
    try:
        from scipy.stats import gaussian_kde
        kde = gaussian_kde(vals)
        x_range = np.linspace(vals.min() - vals.std(), vals.max() + vals.std(), 300)
        ax.plot(x_range, kde(x_range), color=colors[0], linewidth=2.5)
    except ImportError:
        # scipy不可用时，仅显示直方图
        ax.hist(vals, bins=30, density=True, color=colors[0], alpha=0.5,
                edgecolor="white")

    _apply_style(ax, title, xlabel, ylabel)
    plt.tight_layout()

    filepath = _next_filename("density_plot")
    fig.savefig(filepath)
    plt.close(fig)
    return f"![{title}]({filepath})"


# ===========================================================================
# 17. radar_chart - 雷达图
# ===========================================================================

def radar_chart(
    categories: str,
    values: str,
    title: str = "雷达图",
    color_scheme: str = "default",
) -> str:
    """
    生成雷达图（蛛网图，展示多维度指标）。

    参数:
        categories: 逗号分隔的维度标签，例如 "速度,力量,技巧,耐力,智力"
        values: 逗号分隔的数值（建议范围0-100），例如 "80,70,90,60,85"
        title: 图表标题
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片路径字符串
    """
    cats = parse_label_list(categories)
    vals = parse_number_list(values)
    colors = color_palette(1, scheme=color_scheme)

    N = len(cats)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    vals_closed = vals + vals[:1]
    angles_closed = angles + angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"polar": True})

    ax.fill(angles_closed, vals_closed, alpha=0.25, color=colors[0])
    ax.plot(angles_closed, vals_closed, color=colors[0], linewidth=2,
            marker="o", markersize=6)

    ax.set_xticks(angles)
    ax.set_xticklabels(cats, fontsize=11)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=20)

    # 设置径向刻度
    ax.set_ylim(0, max(vals) * 1.15)
    ax.set_yticks(np.linspace(0, max(vals) * 1.15, 5))
    ax.set_yticklabels([f"{v:.0f}" for v in np.linspace(0, max(vals) * 1.15, 5)],
                       fontsize=8)
    plt.tight_layout()

    filepath = _next_filename("radar_chart")
    fig.savefig(filepath)
    plt.close(fig)
    return f"![{title}]({filepath})"


# ===========================================================================
# 18. pair_plot - 散点矩阵图
# ===========================================================================

def pair_plot(
    data: str,
    column_names: str = "",
    title: str = "散点矩阵图",
    color_scheme: str = "default",
) -> str:
    """
    生成散点矩阵图（多变量两两关系的散点图矩阵）。

    参数:
        data: 分号分隔的矩阵数据，每行为逗号分隔的数值。
              例如 "1,2,3;4,5,6;7,8,9;10,11,12"
        column_names: 逗号分隔的列名
        title: 图表标题
        color_scheme: 颜色方案

    返回:
        Markdown格式的图片路径字符串
    """
    rows = [parse_number_list(row) for row in data.split(";") if row.strip()]
    matrix = np.array(rows)
    n_cols = matrix.shape[1]

    col_names = parse_label_list(column_names) if column_names else \
                [f"Var{i+1}" for i in range(n_cols)]
    colors = color_palette(1, scheme=color_scheme)

    fig, axes = plt.subplots(n_cols, n_cols, figsize=(n_cols * 2.5, n_cols * 2.5))
    if n_cols == 1:
        axes = np.array([[axes]])

    for i in range(n_cols):
        for j in range(n_cols):
            ax = axes[i, j]
            if i == j:
                # 对角线：直方图
                ax.hist(matrix[:, i], bins=15, color=colors[0], alpha=0.7,
                        edgecolor="white")
            else:
                # 非对角线：散点图
                ax.scatter(matrix[:, j], matrix[:, i], c=colors[0],
                           s=15, alpha=0.6, edgecolors="none")

            if i == n_cols - 1:
                ax.set_xlabel(col_names[j], fontsize=8)
            if j == 0:
                ax.set_ylabel(col_names[i], fontsize=8)
            ax.tick_params(labelsize=6)

    fig.suptitle(title, fontsize=14, fontweight="bold", y=1.01)
    plt.tight_layout()

    filepath = _next_filename("pair_plot")
    fig.savefig(filepath)
    plt.close(fig)
    return f"![{title}]({filepath})"
