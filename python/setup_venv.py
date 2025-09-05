"""Utility script for creating a virtual environment and installing dependencies."""

import argparse
import os
import pathlib
from subprocess import CalledProcessError, run
import sys
from typing import Sequence

def _venv_python(venv_dir: pathlib.Path) -> pathlib.Path:
    """Return the path to the Python interpreter inside ``venv_dir``."""

    if os.name == "nt":
        return venv_dir / "Scripts" / "python"
    return venv_dir / "bin" / "python"

def main(argv: Sequence[str] | None = None) -> None:
    """Create a virtual environment and install dependencies.

    Args:
        argv: Optional CLI arguments.
            Positional argument may specify a custom requirements file path.
    """

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "requirements_path",
        nargs="?",
        default=None,
        help="Path to requirements file (defaults to requirements.txt alongside this script)",
    )
    args = parser.parse_args(argv)

    root = pathlib.Path(os.environ.get("BUILD_WORKING_DIRECTORY", ".")).resolve()
    venv_dir = root / ".venv"
    if not venv_dir.exists():
        try:
            run([sys.executable, "-m", "venv", str(venv_dir)], check=True, text=True)
        except CalledProcessError as exc:
            raise RuntimeError("Failed to create virtual environment") from exc

    reqs = (
        pathlib.Path(args.requirements_path)
        if args.requirements_path is not None
        else pathlib.Path(__file__).with_name("requirements.txt")
    )
    try:
        run(
            [str(_venv_python(venv_dir)), "-m", "pip", "install", "-r", str(reqs)],
            check=True,
            text=True,
        )
    except CalledProcessError as exc:
        raise RuntimeError(f"Failed to install dependencies from {reqs}") from exc


if __name__ == "__main__":
    main()
