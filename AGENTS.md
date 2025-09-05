# Agent Instructions

This repository requires Bazel's bzlmod (`MODULE.bazel`). All builds and dependency
changes must use Bazel modules; do not rely on the legacy WORKSPACE mechanism.

Python sources live under the `python/` directory. Environment variables for local
development should be stored in `.env` (ignored by Git) and loaded with
`source scripts/export_env.sh`.

All Bazel commands must be executed through Bazelisk to honor `.bazelversion`.

- Python code must follow PEP 8, include type hints, and provide docstrings for modules, classes, and functions.
- Modules and packages use `snake_case` names under `python/` and should preserve the existing package layout.
- Favor idiomatic Python with clear object-oriented design and principles.
- Every new feature requires unit tests; run `bazel test //...` and ensure tests pass before committing.
