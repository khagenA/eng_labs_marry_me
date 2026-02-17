# Engineering Lab -- Marry Me

## Overview

This project implements an event-driven wedding simulation where
incidents occur over time and must be handled by limited staff within
deadline constraints.

The system:

-   Receives events from JSON input files
-   Routes events to the correct team
-   Processes events concurrently using worker pools (`asyncio`)
-   Enforces priority-based deadlines
-   Tracks stress caused by delayed or expired events

This lab demonstrates asynchronous dispatching, deadline-aware
scheduling, and proper Python project structuring.

------------------------------------------------------------------------

## Project Structure

    eng_labs_marry_me/
    ├── src/
    │   └── marry_me/
    │       ├── __init__.py
    │       ├── constants.py
    │       ├── models.py
    │       ├── logic.py
    │       └── simulation_async.py
    ├── tests/
    │   ├── test_logic.py
    │   └── test_routing.py
    ├── data/
    │   ├── events_easy.json
    │   ├── events_medium.json
    │   └── events_hard.json
    ├── notebooks/
    │   └── marry_me.ipynb
    ├── scripts/
    │   └── generate_datasets.py
    ├── docs/
    │   └── Engineering_lab_4 - Marry Me - Lite.pdf
    ├── pyproject.toml
    ├── Makefile
    ├── .gitignore
    └── README.md

The project follows the src-layout best practice for Python packaging.

------------------------------------------------------------------------

## Setup (Cross-Platform)

### 1. Create Virtual Environment

**Linux / macOS**

``` bash
python3 -m venv .venv
```

**Windows**

``` bash
python -m venv .venv
```

------------------------------------------------------------------------

### 2. Activate Virtual Environment

**Linux / macOS**

``` bash
source .venv/bin/activate
```

**Windows (PowerShell)**

``` bash
.\.venv\Scripts\Activate
```

------------------------------------------------------------------------

### 3. Install Dependencies

``` bash
pip install -U pip
pip install pytest
pip install -e .
```

------------------------------------------------------------------------

## Run Simulation (CLI)

``` bash
python -m marry_me.simulation_async data/events_easy.json
```

Available datasets:

-   data/events_easy.json
-   data/events_medium.json
-   data/events_hard.json

------------------------------------------------------------------------

## Run Tests

``` bash
pytest -q
```

Tests validate:

-   Event routing logic
-   Deadline classification logic
-   Error handling

------------------------------------------------------------------------

## Run with Makefile (Optional)

``` bash
make install
make test
make run-easy
make run-medium
make run-hard
```

------------------------------------------------------------------------

## Notebook Usage

Notebook location:

    notebooks/marry_me.ipynb

-   Open in VS Code or Jupyter
-   Select the `.venv` interpreter
-   Run cells directly

No special setup cell is required for local execution.

------------------------------------------------------------------------

## Event Classification

Each event is classified as:

-   Handled On Time -- Finished before deadline
-   Delayed -- Finished after deadline
-   Expired -- Started after deadline
-   Leftover -- Still waiting when simulation ends

Stress increases for delayed and expired events.

------------------------------------------------------------------------

## Learning Outcomes

-   Asynchronous event-driven architecture
-   Worker pool concurrency
-   Deadline-aware scheduling
-   Clean Python project structure
-   Unit testing with pytest
-   Virtual environment best practices
