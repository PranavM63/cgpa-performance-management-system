# Student CGPA Performance Management System

An academic software engineering project built for the laboratory course on **AI-Augmented Software Development Environment**.

This application is a modular, beginner-friendly Python command-line tool that calculates a student's **Cumulative Grade Point Average (CGPA)** as an arithmetic mean across subjects, validates grade points against a 0.0–10.0 scale, and assigns an academic performance category.

---

## 1. Technology Stack

- **Programming Language**: Python 3 (standard library)
- **Automated Testing**: Pytest
- **Code Quality & Formatting**: Ruff (PEP 8 compliant)
- **IDE**: Google Antigravity
- **Version Control**: Git & GitHub

---

## 2. Project Structure

```text
cgpa-performance-management-system/
├── .gitignore                      # Excludes Python bytecode, virtual envs, test caches
├── pyproject.toml                  # Pytest and Ruff tool configuration
├── AGENTS.md                       # Instructions and context for AI coding assistance
├── README.md                       # Documentation, setup guide, and viva reference
├── docs/
│   └── AI_ENGINEERING_JOURNAL.md  # Log of actual AI prompts, validations, and decisions
├── src/
│   └── student_performance.py     # Core calculation, input validation, and CLI logic
└── tests/
    └── test_student_performance.py # Automated test suite for all calculations & edge cases
```

---

## 3. CGPA & Performance Scale

### Calculation Formula
$$\text{CGPA} = \frac{\sum \text{Subject Grade Points}}{\text{Total Number of Subjects}}$$

> **Academic Note:** For this academic demonstration, grade points are evaluated in the range **0.0 to 10.0**, and CGPA is calculated as the simple arithmetic mean of the supplied subject grade points.

### Academic Performance Categories
| CGPA Range | Category |
| :--- | :--- |
| **9.00 – 10.00** | Outstanding |
| **8.00 – 8.99** | Excellent |
| **7.00 – 7.99** | Very Good |
| **6.00 – 6.99** | Good |
| **5.00 – 5.99** | Average |
| **4.00 – 4.99** | Pass |
| **Below 4.00** | Needs Improvement |

---

## 4. Setup and Execution

### Prerequisites
- Python 3.8 or higher installed on your system.

### Running the Application
From the project root directory, run:
```bash
py src/student_performance.py
```
*(or `python src/student_performance.py` depending on your environment)*

### Running Automated Tests
Run the Pytest suite with verbose output:
```bash
py -m pytest
```

### Running Code Quality and Lint Checks
Check code quality and format with Ruff:
```bash
py -m ruff check .
```

---

## 5. Laboratory Viva Reference

- **Modular Architecture**: Core computation logic (`validate_grade_point`, `calculate_cgpa`, `get_performance_category`) is decoupled from user interaction (`run_cli`), making functions pure and easily testable.
- **Defensive Input Validation**: Handles non-numeric inputs, negative numbers, numbers exceeding 10.0, empty student names, and empty grade lists with informative error messages.
- **AI-Augmented Development**: All prompts, AI suggestions, human verification steps, and engineering decisions are documented in [`docs/AI_ENGINEERING_JOURNAL.md`](docs/AI_ENGINEERING_JOURNAL.md).
