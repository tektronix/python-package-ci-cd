"""Remove the Python version restraint from a requirements file."""

from __future__ import annotations

import argparse
import re

from pathlib import Path

# Regular expression to match only the python_version constraints
PYTHON_VERSION_PATTERN = re.compile(r"python_version.*?(\sand\s*|$)")

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(
        description="Remove python_version constraints from a requirements file."
    )
    parser.add_argument("file_path", type=Path, help="Path to the requirements file.")
    args = parser.parse_args()
    file_path = Path(args.file_path)
    # Read the file content
    lines = file_path.read_text(encoding="utf-8").splitlines()
    # Remove python_version constraints
    updated_lines: list[str] = []
    for line in lines:
        # Remove python_version constraints
        updated_line = PYTHON_VERSION_PATTERN.sub("", line).strip()
        # Remove trailing ';' if the line ends with it
        if updated_line.endswith(";"):
            updated_line = updated_line[:-1].strip()
        updated_lines.append(updated_line)
    # Write the updated content back to the file
    file_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")
