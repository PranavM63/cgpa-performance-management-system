"""Automated Pytest test suite for Student CGPA Performance Management System."""

import pytest

from src.student_performance import (
    calculate_cgpa,
    get_performance_category,
    validate_grade_point,
)

# ==============================================================================
# 1. Tests for validate_grade_point()
# ==============================================================================


def test_validate_grade_point_valid_floats():
    """Verify valid float grade points within [0.0, 10.0] are accepted."""
    assert validate_grade_point(0.0) == 0.0
    assert validate_grade_point(5.5) == 5.5
    assert validate_grade_point(10.0) == 10.0


def test_validate_grade_point_valid_integers_and_strings():
    """Verify integer and string inputs are converted to floats."""
    assert validate_grade_point(8) == 8.0
    assert validate_grade_point(0) == 0.0
    assert validate_grade_point(10) == 10.0
    assert validate_grade_point("9.2") == 9.2
    assert validate_grade_point(" 7.5 ") == 7.5


def test_validate_grade_point_out_of_bounds():
    """Verify that grade points outside [0.0, 10.0] raise ValueError."""
    with pytest.raises(ValueError, match="out of bounds"):
        validate_grade_point(-0.1)

    with pytest.raises(ValueError, match="out of bounds"):
        validate_grade_point(-5.0)

    with pytest.raises(ValueError, match="out of bounds"):
        validate_grade_point(10.1)

    with pytest.raises(ValueError, match="out of bounds"):
        validate_grade_point(15.0)


def test_validate_grade_point_non_numeric():
    """Verify non-numeric string inputs raise ValueError."""
    with pytest.raises(ValueError, match="Invalid grade point"):
        validate_grade_point("A+")

    with pytest.raises(ValueError, match="Invalid grade point"):
        validate_grade_point("excellent")

    with pytest.raises(ValueError, match="Invalid grade point"):
        validate_grade_point("")


def test_validate_grade_point_none():
    """Verify None input raises TypeError."""
    with pytest.raises(TypeError, match="cannot be None"):
        validate_grade_point(None)


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
