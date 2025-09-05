"""Smoke tests for the ``setup_venv`` script."""

from __future__ import annotations

import os
import pathlib
import sys
import tempfile
from unittest import TestCase
from unittest.mock import call, patch

import setup_venv


class SetupVenvSmokeTest(TestCase):
    """Verify virtual environment creation and dependency installation."""

    def test_main_creates_and_installs(self) -> None:
        """Ensure main invokes commands to create venv and install deps."""
        with tempfile.TemporaryDirectory() as tmpdir, patch(
            "setup_venv.run"
        ) as run_mock, patch.dict(os.environ, {"BUILD_WORKING_DIRECTORY": tmpdir}):
            setup_venv.main([])

            venv_dir = pathlib.Path(tmpdir) / ".venv"
            requirements = pathlib.Path(setup_venv.__file__).with_name(
                "requirements.txt"
            )
            run_mock.assert_has_calls(
                [
                    call(
                        [sys.executable, "-m", "venv", str(venv_dir)],
                        check=True,
                        text=True,
                    ),
                    call(
                        [
                            str(setup_venv._venv_python(venv_dir)),
                            "-m",
                            "pip",
                            "install",
                            "-r",
                            str(requirements),
                        ],
                        check=True,
                        text=True,
                    ),
                ]
            )
