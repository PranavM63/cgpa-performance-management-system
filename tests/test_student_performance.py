"""Automated Pytest test suite for Student CGPA Performance Management System."""

import pytest

from src.student_performance import (
    calculate_cgpa,
    get_performance_category,
    run_cli,
    validate_grade_point,
)

# ==============================================================================
# 1. Tests for validate_grade_point()
# ==============================================================================


@pytest.mark.parametrize(
    "valid_input,expected_output",
    [
        (0.0, 0.0),
        (0, 0.0),
        (0.01, 0.01),
        (5.5, 5.5),
        (9.99, 9.99),
        (10.0, 10.0),
        (10, 10.0),
        ("0.0", 0.0),
        ("10.0", 10.0),
        (" 8.75 ", 8.75),
    ],
)
def test_validate_grade_point_valid_inputs(valid_input, expected_output):
    """Verify valid numeric and string inputs within [0.0, 10.0] are accepted."""
    assert validate_grade_point(valid_input) == expected_output


@pytest.mark.parametrize(
    "invalid_input",
    [-0.01, -1.0, -10.0, 10.01, 10.1, 15.0, 100.0],
)
def test_validate_grade_point_out_of_bounds(invalid_input):
    """Verify that grade points outside [0.0, 10.0] raise ValueError."""
    with pytest.raises(ValueError, match="out of bounds"):
        validate_grade_point(invalid_input)


@pytest.mark.parametrize(
    "non_numeric_input",
    ["", "   ", "abc", "A+", "ten", "8.5.2", "@#$"],
)
def test_validate_grade_point_non_numeric(non_numeric_input):
    """Verify non-numeric string inputs raise ValueError."""
    with pytest.raises(ValueError, match="Invalid grade point"):
        validate_grade_point(non_numeric_input)


def test_validate_grade_point_none():
    """Verify None input raises TypeError."""
    with pytest.raises(TypeError, match="cannot be None"):
        validate_grade_point(None)


def test_validate_grade_point_rejects_booleans():
    """Verify Boolean values raise TypeError instead of converting to 1.0 or 0.0."""
    with pytest.raises(TypeError, match="Boolean values are not valid"):
        validate_grade_point(True)

    with pytest.raises(TypeError, match="Boolean values are not valid"):
        validate_grade_point(False)


# ==============================================================================
# 2. Tests for calculate_cgpa()
# ==============================================================================


def test_calculate_cgpa_single_subject():
    """Verify CGPA calculation for a single subject."""
    assert calculate_cgpa([8.5]) == 8.5
    assert calculate_cgpa([10.0]) == 10.0
    assert calculate_cgpa([0.0]) == 0.0


def test_calculate_cgpa_multiple_subjects():
    """Verify arithmetic mean calculation across multiple subjects."""
    # (8.0 + 9.0 + 10.0) / 3 = 9.0
    assert calculate_cgpa([8.0, 9.0, 10.0]) == 9.0

    # (7.5 + 8.5 + 9.0 + 6.0) / 4 = 31.0 / 4 = 7.75
    assert calculate_cgpa([7.5, 8.5, 9.0, 6.0]) == 7.75

    # Floating point precision & rounding: (9.0 + 8.0 + 8.0) / 3 = 8.3333... -> 8.33
    assert calculate_cgpa([9.0, 8.0, 8.0]) == 8.33


def test_calculate_cgpa_boundary_values():
    """Verify CGPA calculation for min (0.0) and max (10.0) grades."""
    assert calculate_cgpa([0.0, 0.0, 0.0]) == 0.0
    assert calculate_cgpa([10.0, 10.0, 10.0, 10.0]) == 10.0


def test_calculate_cgpa_string_and_int_inputs():
    """Verify calculate_cgpa handles mixed string, int, and float grade inputs."""
    assert calculate_cgpa(["8.0", 9, 10.0]) == 9.0


def test_calculate_cgpa_empty_list():
    """Verify calculate_cgpa raises ValueError when given an empty list."""
    with pytest.raises(ValueError, match="No grade points provided"):
        calculate_cgpa([])


def test_calculate_cgpa_contains_invalid_grade():
    """Verify calculate_cgpa raises ValueError if any grade is out of range."""
    with pytest.raises(ValueError, match="out of bounds"):
        calculate_cgpa([8.0, 11.0, 9.0])

    with pytest.raises(ValueError, match="Invalid grade point"):
        calculate_cgpa([8.0, "invalid", 9.0])


# ==============================================================================
# 3. Tests for get_performance_category()
# ==============================================================================


@pytest.mark.parametrize(
    "cgpa,expected_category",
    [
        (10.0, "Outstanding"),
        (9.5, "Outstanding"),
        (9.0, "Outstanding"),
        (8.99, "Excellent"),
        (8.5, "Excellent"),
        (8.0, "Excellent"),
        (7.9, "Very Good"),
        (7.0, "Very Good"),
        (6.9, "Good"),
        (6.0, "Good"),
        (5.5, "Average"),
        (5.0, "Average"),
        (4.5, "Pass"),
        (4.0, "Pass"),
        (3.9, "Needs Improvement"),
        (1.0, "Needs Improvement"),
        (0.0, "Needs Improvement"),
    ],
)
def test_get_performance_category_all_tiers(cgpa, expected_category):
    """Verify that performance category matches the expected academic band."""
    assert get_performance_category(cgpa) == expected_category


def test_get_performance_category_out_of_bounds():
    """Verify that invalid CGPA inputs raise ValueError."""
    with pytest.raises(ValueError, match="out of bounds"):
        get_performance_category(-1.0)

    with pytest.raises(ValueError, match="out of bounds"):
        get_performance_category(10.5)


# ==============================================================================
# 4. Tests for run_cli() (Interactive Simulation)
# ==============================================================================


def test_run_cli_successful_flow(monkeypatch, capsys):
    """Simulate a complete user interaction from name entry to performance report."""
    # Inputs: Student Name -> Number of Subjects -> Subject 1 -> Subject 2 -> Subject 3
    user_inputs = iter(["Alice Johnson", "3", "8.5", "9.0", "9.5"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    run_cli()

    captured = capsys.readouterr().out
    assert "STUDENT CGPA PERFORMANCE MANAGEMENT SYSTEM" in captured
    assert "Student Name        : Alice Johnson" in captured
    assert "Total Subjects      : 3" in captured
    assert "Calculated CGPA     : 9.00 / 10.00" in captured
    assert "Performance Category: Outstanding" in captured


def test_run_cli_recovers_from_invalid_inputs(monkeypatch, capsys):
    """Verify CLI reprompts on empty names, invalid counts, and bad grades."""
    # Inputs:
    # 1. Empty name -> Valid Name "Bob Smith"
    # 2. Invalid count "abc" -> Negative count "-1" -> Valid count "2"
    # 3. Invalid grade "15.0" -> Non-numeric "A" -> Valid grade "7.0"
    # 4. Valid grade "8.0"
    user_inputs = iter([
        "",
        "Bob Smith",
        "abc",
        "-1",
        "2",
        "15.0",
        "A",
        "7.0",
        "8.0",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    run_cli()

    captured = capsys.readouterr().out
    assert "Student name cannot be empty" in captured
    assert "Please enter a positive integer for number of subjects" in captured
    assert "Number of subjects must be greater than zero" in captured
    assert "[Input Error]" in captured
    assert "Student Name        : Bob Smith" in captured
    assert "Calculated CGPA     : 7.50 / 10.00" in captured
    assert "Performance Category: Very Good" in captured
