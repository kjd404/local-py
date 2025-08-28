# Local Python Bazel Example

This repository demonstrates a minimal Bazel setup using **bzlmod** and `rules_python`.

## Prerequisites

Install [Bazelisk](https://github.com/bazelbuild/bazelisk). Bazelisk automatically
downloads the Bazel version specified in `.bazelversion` and exposes it as the `bazel`
command.

On macOS with Homebrew:

```bash
brew install bazelisk
```

On other platforms, download a binary from the [Bazelisk releases](https://github.com/bazelbuild/bazelisk/releases).

## Usage

Run Bazel commands as usual. For example:

```bash
bazel build //:hello
bazel run //:hello
```

To create a virtual environment in the repo root that matches the Bazel Python
toolchain and installs `requirements.txt`:

```bash
bazel run //:setup_venv
```

The environment is created at `.venv/` and is ignored by Git.
