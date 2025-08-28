# Agent Instructions

This repository requires Bazel's bzlmod (`MODULE.bazel`). All builds and dependency
changes must use Bazel modules; do not rely on the legacy WORKSPACE mechanism.

Python sources live under the `python/` directory. Environment variables for local
development should be stored in `.env` (ignored by Git) and loaded with
`source scripts/export_env.sh`.
