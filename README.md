# Advent of Code 2021

This repository contains Python solutions for the Advent of Code 2021 programming puzzles.

## Project Structure

The project is organized as follows:

- `aoc/y2021/`: Contains the Python scripts for each day's solution.
    - `dayN.py`: Solution for Day N.
    - `utils.py`: Utility functions used by the solutions.
- `inputs/`: Contains the input files for each day's puzzle.
    - `dayN.txt`: Input for Day N.
    - `test_dayN.txt`: Test input for Day N.
- `test/`: Contains PyTest unit tests for each day's solution.
    - `test_dayN.py`: Tests for Day N.
- `Makefile`: Contains commands for managing the project (linting, testing, running solutions).
- `setup.py`, `setup.cfg`, `pyproject.toml`: Python packaging and project configuration files.

## Setup and Usage

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Set up a Python virtual environment (recommended):**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -e .
    ```
    This command installs the project in editable mode and any dependencies listed in `setup.py`.

## Running Solutions

You can run the solutions for individual days or use the Makefile commands for common tasks.

### Running a Specific Day's Solution

To run the solution for a specific day (e.g., Day 1):

```bash
python -m aoc.y2021.day1
```

Or, if the day's script is registered in `setup.cfg` (which `make stub_day` does automatically):

```bash
run_day1
```

### Using Makefile Commands

The `Makefile` provides several useful commands:

-   **`make run_pylint`**: Runs Pylint to check code style and potential errors.
-   **`make run_pytest`**: Runs PyTest to execute all unit tests.
-   **`make run_format`**: Runs `isort` and `black` to automatically format the code.
-   **`make stub_day DAY=X`**: This is a helpful command to set up the files for a new day `X`. It will:
    -   Create `aoc/y2021/dayX.py` from a template.
    -   Create `test/test_dayX.py` from a template.
    -   Download the input for day `X` into `inputs/dayX.txt` (requires `AOC_SESSION` environment variable to be set with your Advent of Code session cookie).
    -   Add an entry point `run_dayX` to `setup.cfg` so you can run the solution with `run_dayX`.
-   **`make precommit`**: Runs formatting, linting, and tests. This is useful to run before committing changes.

**Note on `make stub_day`:** To automatically download puzzle inputs, you need to set the `AOC_SESSION` environment variable to your Advent of Code session cookie value. You can find this cookie in your browser's developer tools when logged into the Advent of Code website.

## Contributing

Feel free to contribute by adding solutions, improving existing ones, or adding more tests.

1.  Fork the repository.
2.  Create a new branch for your changes.
3.  Make your changes, ensuring code is formatted (`make run_format`) and passes tests (`make run_pytest`).
4.  Submit a pull request.
