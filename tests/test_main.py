"""Tests for mcp-data-viz utility functions."""

import pytest
from utils import parse_csv_string, format_number, color_palette, validate_data


class TestParseCSVString:
    """Tests for parse_csv_string function."""

    def test_parse_with_header(self):
        """Test parsing CSV with header row."""
        header, rows = parse_csv_string("name,age\nAlice,30\nBob,25", has_header=True)
        assert header == ["name", "age"]
        assert rows == [["Alice", "30"], ["Bob", "25"]]

    def test_parse_without_header(self):
        """Test parsing CSV without header row."""
        header, rows = parse_csv_string("Alice,30\nBob,25", has_header=False)
        assert header == []
        assert len(rows) == 2

    def test_parse_empty_string(self):
        """Test parsing empty string."""
        header, rows = parse_csv_string("", has_header=True)
        assert header == []
        assert rows == []

    def test_parse_single_row(self):
        """Test parsing CSV with single data row."""
        header, rows = parse_csv_string("col1,col2\nval1", has_header=True)
        assert header == ["col1", "col2"]
        assert rows == [["val1"]]

    def test_parse_custom_delimiter(self):
        """Test parsing with custom delimiter."""
        header, rows = parse_csv_string("a;b\n1;2", has_header=True, delimiter=";")
        assert header == ["a", "b"]
        assert rows == [["1", "2"]]


class TestFormatNumber:
    """Tests for format_number function."""

    def test_basic_format(self):
        """Test basic number formatting."""
        result = format_number(1234.5678, decimals=2)
        assert "1,234.57" in result or "1234.57" in result

    def test_with_suffix(self):
        """Test formatting with suffix."""
        result = format_number(100, decimals=1, suffix="%")
        assert "%" in result

    def test_no_thousands_sep(self):
        """Test formatting without thousands separator."""
        result = format_number(1234.5, decimals=1, thousands_sep="")
        assert "1234.5" in result

    def test_integer_value(self):
        """Test formatting an integer."""
        result = format_number(100, decimals=0)
        assert "100" in result

    def test_zero_decimals(self):
        """Test formatting with zero decimals."""
        result = format_number(3.14159, decimals=0)
        assert "." not in result


class TestColorPalette:
    """Tests for color_palette function."""

    def test_default_palette(self):
        """Test generating default color palette."""
        colors = color_palette(n=5, scheme="default")
        assert len(colors) == 5
        for color in colors:
            assert color.startswith("#") or color.startswith("rgb")

    def test_warm_palette(self):
        """Test generating warm color palette."""
        colors = color_palette(n=3, scheme="warm")
        assert len(colors) == 3

    def test_n_is_zero(self):
        """Test generating zero colors."""
        colors = color_palette(n=0)
        assert len(colors) == 0

    def test_all_schemes(self):
        """Test that all color schemes work."""
        for scheme in ["default", "warm", "cool", "pastel", "grayscale", "nature"]:
            colors = color_palette(n=3, scheme=scheme)
            assert len(colors) == 3


class TestValidateData:
    """Tests for validate_data function."""

    def test_valid_csv(self):
        """Test validating valid CSV data."""
        result = validate_data("name,age\nAlice,30\nBob,25")
        assert result["valid"] is True
        assert result["row_count"] == 2
        assert result["column_count"] == 2

    def test_empty_data_not_allowed(self):
        """Test that empty data fails when not allowed."""
        result = validate_data("", allow_empty=False)
        assert result["valid"] is False

    def test_empty_data_allowed(self):
        """Test that empty data passes when allowed."""
        result = validate_data("", allow_empty=True)
        assert result["valid"] is True

    def test_column_count_check(self):
        """Test that expected column count is validated."""
        result = validate_data("a,b,c\n1,2,3", expected_columns=3)
        assert result["valid"] is True

    def test_column_count_mismatch(self):
        """Test that column count mismatch is flagged."""
        result = validate_data("a,b\n1,2", expected_columns=3)
        assert isinstance(result, dict)
