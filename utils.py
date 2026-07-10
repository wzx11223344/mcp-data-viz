"""
utils.py - 辅助函数模块

提供数据解析、颜色方案、格式化、验证、异常检测、归一化等辅助功能。
"""

import csv
import io
import numpy as np
from typing import List, Dict, Any, Tuple, Optional


# ---------------------------------------------------------------------------
# 颜色方案预设
# ---------------------------------------------------------------------------

_COLOR_SCHEMES: Dict[str, List[str]] = {
    "default": ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
                "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"],
    "warm": ["#FF6B6B", "#FF8E72", "#FFB347", "#FFD93D", "#C9A0DC",
             "#FF5E78", "#F0A500", "#E84545", "#FF2E63", "#FFA07A"],
    "cool": ["#4ECDC4", "#45B7D1", "#6C5CE7", "#74B9FF", "#00CEC9",
             "#0984E3", "#00B894", "#2D3436", "#636E72", "#A29BFE"],
    "pastel": ["#FFB5BA", "#FFD3B6", "#FFEDA0", "#C7EFCF", "#AED6F1",
               "#D7BDE2", "#F5B7B1", "#ABEBC6", "#F9E79F", "#A3E4D7"],
    "grayscale": ["#2C3E50", "#34495E", "#5D6D7E", "#85929E", "#AEB6BF",
                  "#D5D8DC", "#E5E7E9", "#F2F4F4", "#FBFCFC", "#FFFFFF"],
    "nature": ["#1B9E77", "#D95F02", "#7570B3", "#E7298A", "#66A61E",
               "#E6AB02", "#A6761D", "#666666", "#1B9E77", "#D95F02"],
}


def parse_csv_string(
    csv_string: str,
    has_header: bool = True,
    delimiter: str = ","
) -> Tuple[Optional[List[str]], List[List[str]]]:
    """
    将逗号分隔的 CSV 字符串解析为表头和数据行。

    参数:
        csv_string: 逗号分隔的 CSV 格式字符串。例如 "name,age\\nAlice,30\\nBob,25"
        has_header: 第一行是否为表头，默认 True
        delimiter: 分隔符，默认为逗号

    返回:
        元组 (header, rows)：
        - header: 表头列表，如果 has_header=False 则为 None
        - rows: 数据行列表，每行为字符串列表

    示例:
        >>> header, rows = parse_csv_string("name,age\\nAlice,30\\nBob,25")
        >>> header
        ['name', 'age']
        >>> rows
        [['Alice', '30'], ['Bob', '25']]
    """
    if not csv_string or not csv_string.strip():
        return None, []

    reader = csv.reader(io.StringIO(csv_string.strip()), delimiter=delimiter)
    all_rows = list(reader)

    if not all_rows:
        return None, []

    if has_header:
        header = all_rows[0]
        rows = all_rows[1:]
    else:
        header = None
        rows = all_rows

    # 过滤掉完全空的行
    rows = [r for r in rows if any(cell.strip() for cell in r)]

    return header, rows


def color_palette(
    n: int = 10,
    scheme: str = "default",
    as_hex: bool = True
) -> List[str]:
    """
    生成一组颜色色板。

    参数:
        n: 需要的颜色数量，默认 10
        scheme: 颜色方案名称，可选值: default, warm, cool, pastel, grayscale, nature
        as_hex: 是否返回十六进制颜色码，默认 True；若 False 则返回 RGB 元组列表

    返回:
        颜色列表。如果 as_hex=True 返回十六进制字符串列表，
        否则返回 (R, G, B) 元组列表（值范围 0-1）。

    示例:
        >>> colors = color_palette(3, scheme="warm")
        >>> len(colors)
        3
    """
    scheme = scheme.lower().strip()
    base_colors = _COLOR_SCHEMES.get(scheme, _COLOR_SCHEMES["default"])

    if n <= 0:
        return []

    if n <= len(base_colors):
        result = base_colors[:n]
    else:
        # 颜色不够时循环使用并插值
        result = list(base_colors)
        while len(result) < n:
            result.append(base_colors[len(result) % len(base_colors)])

    if not as_hex:
        rgb_result = []
        for hex_color in result:
            hex_color = hex_color.lstrip("#")
            r = int(hex_color[0:2], 16) / 255.0
            g = int(hex_color[2:4], 16) / 255.0
            b = int(hex_color[4:6], 16) / 255.0
            rgb_result.append((r, g, b))
        return rgb_result

    return result


def format_number(
    value: float,
    decimals: int = 2,
    thousands_sep: str = ",",
    suffix: str = ""
) -> str:
    """
    格式化数字，支持千分位分隔符、小数位数和后缀。

    参数:
        value: 要格式化的数值
        decimals: 小数位数，默认 2
        thousands_sep: 千分位分隔符，默认为逗号；传空字符串则不加分隔符
        suffix: 数值后缀，例如 "%" 或 " 元"

    返回:
        格式化后的字符串。

    示例:
        >>> format_number(1234567.891)
        '1,234,567.89'
        >>> format_number(85.5, suffix="%")
        '85.50%'
        >>> format_number(1000000, suffix=" 元", thousands_sep="")
        '1000000.00 元'
    """
    if value is None:
        return "N/A"

    try:
        value = float(value)
    except (ValueError, TypeError):
        return str(value)

    # 格式化数字字符串
    fmt_str = f"{{:.{decimals}f}}".format(value)
    parts = fmt_str.split(".")
    int_part = parts[0]
    dec_part = parts[1] if len(parts) > 1 else ""

    # 添加千分位分隔符
    if thousands_sep:
        sign = ""
        if int_part.startswith("-"):
            sign = "-"
            int_part = int_part[1:]
        # 从右向左每三位加一个分隔符
        reversed_int = int_part[::-1]
        chunks = [reversed_int[i:i + 3] for i in range(0, len(reversed_int), 3)]
        formatted_int = thousands_sep.join(chunks)[::-1]
        int_part = sign + formatted_int

    result = f"{int_part}.{dec_part}" if dec_part else int_part
    return f"{result}{suffix}"


def validate_data(
    data: str,
    expected_columns: int = None,
    allow_empty: bool = False
) -> Dict[str, Any]:
    """
    验证 CSV 格式字符串数据的完整性和有效性。

    参数:
        data: 逗号分隔的 CSV 格式字符串
        expected_columns: 期望的列数，若为 None 则不检查列数
        allow_empty: 是否允许空数据，默认 False

    返回:
        验证结果字典，包含以下字段:
        - valid: bool, 是否验证通过
        - errors: List[str], 错误信息列表
        - warnings: List[str], 警告信息列表
        - row_count: int, 数据行数
        - column_count: int, 列数

    示例:
        >>> result = validate_data("a,b,c\\n1,2,3", expected_columns=3)
        >>> result['valid']
        True
    """
    errors: List[str] = []
    warnings: List[str] = []
    row_count = 0
    column_count = 0

    if data is None or not str(data).strip():
        if allow_empty:
            return {
                "valid": True,
                "errors": [],
                "warnings": [],
                "row_count": 0,
                "column_count": 0,
            }
        else:
            errors.append("数据为空，且 allow_empty=False")
            return {
                "valid": False,
                "errors": errors,
                "warnings": warnings,
                "row_count": 0,
                "column_count": 0,
            }

    data = str(data).strip()
    header, rows = parse_csv_string(data, has_header=True)

    if header is not None:
        column_count = len(header)

    if expected_columns is not None and column_count != expected_columns:
        errors.append(
            f"列数不匹配：期望 {expected_columns} 列，实际 {column_count} 列"
        )

    # 检查每行列数一致性
    for i, row in enumerate(rows):
        if len(row) != column_count:
            errors.append(
                f"第 {i + 2} 行（含表头）列数不一致：期望 {column_count} 列，实际 {len(row)} 列"
            )

    row_count = len(rows)

    if row_count == 0:
        warnings.append("数据仅有表头，无数据行")

    valid = len(errors) == 0

    return {
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
        "row_count": row_count,
        "column_count": column_count,
    }


def detect_outliers(
    values: str,
    method: str = "iqr",
    threshold: float = 1.5
) -> Dict[str, Any]:
    """
    从逗号分隔的数值字符串中检测异常值。

    参数:
        values: 逗号分隔的数值字符串，例如 "1,2,3,100,4,5,200"
        method: 检测方法，可选: "iqr"（四分位距法）或 "zscore"（Z分数法）
        threshold: 阈值，IQR法默认1.5（1.5倍IQR），Z分数法默认2.0（2个标准差）

    返回:
        检测结果字典，包含:
        - outlier_indices: List[int], 异常值在原数组中的索引
        - outlier_values: List[float], 异常值列表
        - method: str, 使用的方法
        - stats: dict, 统计信息（均值、中位数、标准差、Q1、Q3、IQR）

    示例:
        >>> result = detect_outliers("1,2,3,100,4,5,200", method="iqr")
        >>> result['outlier_values']
        [100.0, 200.0]
    """
    # 解析数值
    try:
        nums = [float(x.strip()) for x in values.split(",") if x.strip()]
    except ValueError as e:
        return {
            "error": f"数值解析失败: {e}",
            "outlier_indices": [],
            "outlier_values": [],
            "method": method,
            "stats": {},
        }

    if len(nums) < 4:
        return {
            "outlier_indices": [],
            "outlier_values": [],
            "method": method,
            "stats": {
                "count": len(nums),
                "mean": float(np.mean(nums)) if nums else 0,
                "median": float(np.median(nums)) if nums else 0,
            },
            "message": "数据点少于4个，无法可靠检测异常值",
        }

    arr = np.array(nums)
    outlier_indices = []
    outlier_values = []

    mean_val = float(np.mean(arr))
    median_val = float(np.median(arr))
    std_val = float(np.std(arr))
    q1 = float(np.percentile(arr, 25))
    q3 = float(np.percentile(arr, 75))
    iqr = q3 - q1

    stats = {
        "count": len(nums),
        "mean": mean_val,
        "median": median_val,
        "std": std_val,
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
    }

    if method.lower() == "iqr":
        lower_bound = q1 - threshold * iqr
        upper_bound = q3 + threshold * iqr
        for i, v in enumerate(nums):
            if v < lower_bound or v > upper_bound:
                outlier_indices.append(i)
                outlier_values.append(v)
        stats["lower_bound"] = lower_bound
        stats["upper_bound"] = upper_bound

    elif method.lower() == "zscore":
        if std_val == 0:
            return {
                "outlier_indices": [],
                "outlier_values": [],
                "method": method,
                "stats": stats,
                "message": "标准差为0，无法使用Z分数法",
            }
        for i, v in enumerate(nums):
            z = abs((v - mean_val) / std_val)
            if z > threshold:
                outlier_indices.append(i)
                outlier_values.append(v)
        stats["threshold_z"] = threshold
    else:
        return {
            "error": f"未知方法: {method}，请使用 'iqr' 或 'zscore'",
            "outlier_indices": [],
            "outlier_values": [],
            "method": method,
            "stats": stats,
        }

    return {
        "outlier_indices": outlier_indices,
        "outlier_values": outlier_values,
        "method": method,
        "stats": stats,
    }


def normalize_data(
    values: str,
    method: str = "minmax",
    target_min: float = 0.0,
    target_max: float = 1.0
) -> str:
    """
    将逗号分隔的数值字符串进行归一化处理。

    参数:
        values: 逗号分隔的数值字符串，例如 "10,20,30,40,50"
        method: 归一化方法，可选: "minmax"（Min-Max归一化）或 "zscore"（Z-score标准化）
        target_min: Min-Max方法的目标最小值，默认 0.0
        target_max: Min-Max方法的目标最大值，默认 1.0

    返回:
        归一化后的逗号分隔数值字符串（保留4位小数）

    示例:
        >>> normalize_data("10,20,30,40,50", method="minmax")
        '0.0000,0.2500,0.5000,0.7500,1.0000'
    """
    try:
        nums = [float(x.strip()) for x in values.split(",") if x.strip()]
    except ValueError as e:
        return f"错误: 数值解析失败 - {e}"

    if not nums:
        return ""

    arr = np.array(nums, dtype=float)

    if method.lower() == "minmax":
        min_val = arr.min()
        max_val = arr.max()
        if max_val - min_val == 0:
            # 所有值相同，返回 target_min
            normalized = np.full_like(arr, target_min)
        else:
            normalized = (arr - min_val) / (max_val - min_val) * \
                          (target_max - target_min) + target_min

    elif method.lower() == "zscore":
        mean_val = arr.mean()
        std_val = arr.std()
        if std_val == 0:
            normalized = np.zeros_like(arr)
        else:
            normalized = (arr - mean_val) / std_val

    else:
        return f"错误: 未知方法 '{method}'，请使用 'minmax' 或 'zscore'"

    return ",".join(f"{v:.4f}" for v in normalized)


def parse_number_list(values: str) -> List[float]:
    """
    辅助函数：将逗号分隔的数值字符串解析为浮点数列表。

    参数:
        values: 逗号分隔的数值字符串

    返回:
        浮点数列表
    """
    return [float(x.strip()) for x in values.split(",") if x.strip()]


def parse_label_list(labels: str) -> List[str]:
    """
    辅助函数：将逗号分隔的标签字符串解析为标签列表。

    参数:
        labels: 逗号分隔的标签字符串

    返回:
        标签列表
    """
    return [x.strip() for x in labels.split(",") if x.strip()]
