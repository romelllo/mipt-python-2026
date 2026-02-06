# AGENTS.md - Guidelines for AI Coding Agents

This document provides instructions for AI coding agents working in this repository.

## Project Overview

This is an educational Python course repository for MIPT (Moscow Institute of Physics and Technology) covering:
- Module 2: OOP and databases (Seminars 1-3)
- Module 3: Web development with Django and FastAPI (Seminars 4-12)
- Module 4: Data analysis and visualization (Seminars 13-17)

**Python Version**: 3.10 or higher

## Repository Structure

```
mipt-python-2026/
├── seminars/
│   ├── seminar_01_intro_to_sql/     # Basic SQL: CREATE, INSERT, UPDATE, DELETE, SELECT
│   ├── seminar_02_advanced_sql/     # JOINs, aggregation, GROUP BY, subqueries, normalization
│   ├── seminar_03_oop_patterns/     # Design patterns, SOLID
│   ├── seminar_04_web_fundamentals/ # HTTP, REST
│   ├── seminar_05-12_.../           # Web development seminars
│   └── seminar_13-17_.../           # Data analysis seminars
├── pyproject.toml                   # Project config (uv, ruff, pytest)
├── AGENTS.md                        # This file
└── README.md                        # Course overview
```

## Environment Setup

This project uses **uv** for package management.

```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Add a new dependency
uv add <package-name>

# Add a dev dependency
uv add --dev <package-name>
```

## Build/Lint/Test Commands

### Formatting and Linting (Ruff)

```bash
# Format code
ruff format .
ruff format path/to/file.py

# Check for linting errors
ruff check .
ruff check path/to/file.py

# Auto-fix linting issues
ruff check --fix .

# Check and fix in one command
ruff check --fix . && ruff format .
```

### Type Checking (ty)

```bash
ty check
ty check path/to/file.py
```

### Testing (pytest)

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run tests with coverage
pytest --cov=seminars --cov-report=html

# Run a single test file
pytest path/to/test_file.py

# Run a single test function
pytest path/to/test_file.py::test_function_name

# Run a single test class
pytest path/to/test_file.py::TestClassName

# Run a single test method
pytest path/to/test_file.py::TestClassName::test_method

# Run tests matching a pattern
pytest -k "pattern"

# Run async tests (FastAPI)
pytest -v --asyncio-mode=auto
```

### Running Applications

```bash
# Run Python scripts
python seminars/seminar_02_db_design/examples/03_cafe_admin_sqlite.py

# FastAPI (from seminar directory)
uvicorn main:app --reload --port 8000

# Jupyter notebooks
jupyter lab
```

## Code Style Guidelines

### General Style

- Follow PEP 8 conventions
- Use Ruff for formatting (line length: 88)
- Use type hints for all function signatures
- Use ty for type checking

### Imports (sorted by ruff)

```python
# Standard library
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

# Third-party
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String

# Local
from .models import User
```

### Docstrings

```python
"""Module description."""

def function_name(param1: str, param2: int) -> bool:
    """Brief description.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value
    """
    pass
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Variables | snake_case | `user_name`, `order_id` |
| Functions | snake_case | `get_user()`, `create_order()` |
| Classes | PascalCase | `MenuItem`, `OrderItem` |
| Constants | UPPER_SNAKE | `MAX_ITEMS`, `DB_PATH` |
| Private | _underscore | `_internal()`, `_cache` |

### Type Hints

```python
from typing import Optional

def get_order(order_id: int) -> Optional[dict]:
    """Get order by ID."""
    pass

def process_items(items: list[str], limit: int = 10) -> dict[str, int]:
    """Process items and return counts."""
    pass
```

### Error Handling

```python
# API errors
if not item:
    raise HTTPException(status_code=404, detail="Item not found")

# General errors
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise
```

### SQL Best Practices

```python
# Use parameterized queries (prevents SQL injection)
cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))

# NEVER do this:
# cursor.execute(f"SELECT * FROM items WHERE id = {item_id}")
```

### File Organization

```python
# Every runnable script should have:
if __name__ == "__main__":
    main()
```

## Testing Guidelines

- Place tests alongside code as `test_*.py`
- Use descriptive test names: `test_create_order_with_valid_items`
- Use fixtures for setup
- Test both success and error cases

```python
import pytest

def test_function_returns_expected():
    result = function_under_test(input_value)
    assert result == expected

@pytest.mark.asyncio
async def test_async_endpoint():
    response = await client.get("/endpoint")
    assert response.status_code == 200
```

## Seminar Structure Guidelines

All seminars should follow the **"theory → immediate practice"** approach. Instead of a large block of theory followed by a large block of exercises, each seminar is split into small topic blocks. After each block of theory (with examples), students go to the exercises document and solve exercises for that specific topic.

### Seminar directory structure

```
seminar_XX_topic_name/
├── README.md                      # Main seminar document (theory blocks with pointers to exercises)
├── data/
│   └── *.sql / *.csv / ...       # Data files / database scripts
├── examples/
│   └── *.sql / *.py              # Example code organized by topic sections
└── exercises/
    └── *.md                       # Exercises document (organized by the same topic blocks)
```

### README.md structure

Each `README.md` should follow this pattern:

1. **Header** — seminar title, module, date, links
2. **Goals** — list of learning objectives
3. **Setup** — preparation steps (DB loading, environment setup, etc.)
4. **Plan** — table with time estimates, topic blocks, and pointers to exercise sections
5. **Topic blocks** — each block contains:
   - Short theory explanation with code examples
   - Reference to detailed examples file: `> **Подробнее:** см. файл [examples/...](examples/...)`
   - Practice pointer: `### Практика` section directing students to the specific exercises section
6. **Files summary** — links to all files in the seminar directory
7. **Additional materials** — external links for further reading

### Exercises file structure

Each exercises file (`exercises/*.md`) should follow this pattern:

1. **Setup** — how to prepare the environment for exercises
2. **Instruction** — remind students to try solving before looking at solutions
3. **Parts** — one part per theory block, each containing:
   - Cross-reference back to the theory block and examples file
   - Multiple exercises with increasing difficulty
   - Each exercise has a `<details><summary>Подсказка</summary>` hint (optional)
   - Each exercise has a `<details><summary>Решение</summary>` with the solution
4. **Bonus exercises** — harder exercises combining multiple topics

### Key principles

- **Small portions**: theory → practice → theory → practice (not big-theory → big-practice)
- **Self-paced**: students try to solve exercises on their own before revealing the solution
- **Cross-references**: exercises link back to the relevant theory block, and theory blocks link to the exercises
- **Hints before solutions**: provide a hint (подсказка) that nudges the student in the right direction
- **Progressive difficulty**: exercises within each part go from simple to complex
- **Bonus section**: advanced exercises that combine multiple topics for faster students

## Language

- Comments and docstrings: Russian or English (educational course for Russian students)
- Code identifiers (variables, functions, classes): English only
