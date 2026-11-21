import subprocess
import json
import os
import sys


def analyze_code(code):

    os.makedirs("temp", exist_ok=True)

    file_path = os.path.join("temp", "analyzed_code.py")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(code)

    results = {}

    # ---------------- PYLINT ----------------

    pylint_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pylint",
            file_path,
            "--output-format=json"
        ],
        capture_output=True,
        text=True
    )

    try:
        pylint_data = json.loads(pylint_result.stdout)
    except json.JSONDecodeError:
        pylint_data = []

    results["pylint"] = pylint_data

    # ---------------- FLAKE8 ----------------

    flake8_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "flake8",
            file_path
        ],
        capture_output=True,
        text=True
    )

    flake8_data = []

    for line in flake8_result.stdout.splitlines():

        parts = line.split(":", 3)

        if len(parts) >= 4:

            try:
                line_number = int(parts[1])
                column_number = int(parts[2])
                message = parts[3].strip()

                error_code = message.split()[0]

                flake8_data.append(
                    {
                        "line": line_number,
                        "column": column_number,
                        "code": error_code,
                        "message": message
                    }
                )

            except (ValueError, IndexError):
                continue

    results["flake8"] = flake8_data

    # ---------------- BANDIT ----------------

    bandit_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "bandit",
            "-f",
            "json",
            file_path
        ],
        capture_output=True,
        text=True
    )

    try:
        bandit_data = json.loads(bandit_result.stdout)
    except json.JSONDecodeError:
        bandit_data = {"results": []}

    results["bandit"] = bandit_data

    return results