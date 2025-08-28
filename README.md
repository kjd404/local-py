# Local Bazel Monorepo Example

This repository demonstrates a minimal Bazel setup using **bzlmod** and
`rules_python`.  The Python code lives under the `python/` directory to make room
for additional languages in the future.

## Prerequisites

Install [Bazelisk](https://github.com/bazelbuild/bazelisk). Bazelisk automatically
downloads the Bazel version specified in `.bazelversion` and exposes it as the `bazel`
command.

On macOS with Homebrew:

```bash
brew install bazelisk
```

On other platforms, download a binary from the [Bazelisk releases](https://github.com/bazelbuild/bazelisk/releases).

## Environment

Copy the sample environment file and adjust values for your local setup:

```bash
cp .env-sample .env
source scripts/export_env.sh
```

The script exports the variables defined in `.env` into the current shell for
tools like `pgcli`.

## Usage

Run Bazel commands from the repository root. For example:

```bash
bazel build //python:hello
bazel run //python:hello
```

To create a virtual environment in the repo root that matches the Bazel Python
toolchain and installs `requirements.txt` (including `ipython` and `pgcli`):

```bash
bazel run //python:setup_venv
```

The environment is created at `.venv/` and is ignored by Git.
