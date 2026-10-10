"""Student CGPA Performance Management System.

This module provides functions to validate subject grade points, calculate
the Cumulative Grade Point Average (CGPA) as an arithmetic mean, and determine
a student's performance category. It also includes an interactive CLI interface.

Academic Note:
    For this academic demonstration, grade points are evaluated in the range
    0.0 to 10.0, and CGPA is calculated as the simple arithmetic mean of the
    supplied subject grade points.
"""

from typing import List, Union


def validate_grade_point(grade: Union[int, float, str]) -> float:
    """Validate and convert a single subject grade point.

    Args:
        grade: The grade point value to validate (numeric or string).

    Returns:
        float: The validated grade point as a floating-point number.

    Raises:
        TypeError: If the grade is None.
        ValueError: If the grade is non-numeric or not within [0.0, 10.0].
    """
    if grade is None:
        raise TypeError("Grade point cannot be None.")

    try:
        numeric_grade = float(grade)
    except (ValueError, TypeError) as exc:
        raise ValueError(
            f"Invalid grade point '{grade}'. Grade point must be a valid number."
        ) from exc

    if not (0.0 <= numeric_grade <= 10.0):
        raise ValueError(
            f"Grade point {numeric_grade} is out of bounds. Must be in [0.0, 10.0]."
        )

    return numeric_grade


def calculate_cgpa(grade_points: List[Union[int, float, str]]) -> float:
    """Calculate the Cumulative Grade Point Average (CGPA).

    CGPA is computed as the arithmetic mean (average) of the provided grade points:
        CGPA = Sum of Grade Points / Total Number of Subjects

    Args:
        grade_points: A non-empty list of subject grade points (range 0.0 to 10.0).

    Returns:
        float: The calculated CGPA rounded to 2 decimal places.

    Raises:
        ValueError: If the list of grade points is empty.
    """
    if not grade_points:
        raise ValueError("Cannot calculate CGPA: No grade points provided.")

    validated_grades = [validate_grade_point(g) for g in grade_points]
    cgpa = sum(validated_grades) / len(validated_grades)
    return round(cgpa, 2)


def get_performance_category(cgpa: Union[int, float]) -> str:
    """Determine the academic performance category based on CGPA.

    Classification Scale:
        - 9.00 to 10.00 : Outstanding
        - 8.00 to 8.99  : Excellent
        - 7.00 to 7.99  : Very Good
        - 6.00 to 6.99  : Good
        - 5.00 to 5.99  : Average
        - 4.00 to 4.99  : Pass
        - Below 4.00    : Needs Improvement

    Args:
        cgpa: The calculated CGPA (0.0 to 10.0).

    Returns:
        str: Descriptive performance category.

    Raises:
        ValueError: If CGPA is outside the valid range [0.0, 10.0].
    """
    valid_cgpa = validate_grade_point(cgpa)

    if valid_cgpa >= 9.0:
        return "Outstanding"
    if valid_cgpa >= 8.0:
        return "Excellent"
    if valid_cgpa >= 7.0:
        return "Very Good"
    if valid_cgpa >= 6.0:
        return "Good"
    if valid_cgpa >= 5.0:
        return "Average"
    if valid_cgpa >= 4.0:
        return "Pass"
    return "Needs Improvement"


def run_cli() -> None:
    """Run the interactive command-line interface."""
    print("=" * 60)
    print("       STUDENT CGPA PERFORMANCE MANAGEMENT SYSTEM")
    print("=" * 60)

    # 1. Accept and validate student name
    student_name = input("Enter Student Name: ").strip()
    while not student_name:
        print("Error: Student name cannot be empty. Please enter a valid name.")
        student_name = input("Enter Student Name: ").strip()

    # 2. Accept number of subjects
    num_subjects = 0
    while num_subjects <= 0:
        raw_num = input("Enter number of subjects: ").strip()
        try:
            parsed_num = int(raw_num)
            if parsed_num <= 0:
                print("Error: Number of subjects must be greater than zero.")
            else:
                num_subjects = parsed_num
        except ValueError:
            print("Error: Please enter a positive integer for number of subjects.")

    # 3. Accept individual subject grade points
    grade_points: List[float] = []
    print(f"\nEnter grade points for {num_subjects} subjects (Scale: 0.0 - 10.0):")
    for i in range(1, num_subjects + 1):
        while True:
            raw_grade = input(f"  Subject {i} Grade Point: ").strip()
            try:
                valid_grade = validate_grade_point(raw_grade)
                grade_points.append(valid_grade)
                break
            except ValueError as err:
                print(f"  [Input Error] {err}. Please re-enter.")

    # 4. Calculate and display performance report
    try:
        cgpa = calculate_cgpa(grade_points)
        category = get_performance_category(cgpa)

        print("\n" + "-" * 45)
        print("             PERFORMANCE REPORT")
        print("-" * 45)
        print(f" Student Name        : {student_name}")
        print(f" Total Subjects      : {len(grade_points)}")
        print(f" Grade Points        : {grade_points}")
        print(f" Calculated CGPA     : {cgpa:.2f} / 10.00")
        print(f" Performance Category: {category}")
        print("-" * 45)
    except (ValueError, TypeError) as err:
        print(f"\n[Calculation Error] Could not compute CGPA: {err}")


if __name__ == "__main__":
    run_cli()
