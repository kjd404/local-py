# local-py

Minimal Bazel repo using bzlmod for Python.

## Prerequisites

Install [Bazelisk](https://github.com/bazelbuild/bazelisk) and use the `bazel` command it provides. Bazelisk reads the pinned version from `.bazelversion` and downloads the matching Bazel release automatically.

## Usage

Run the Hello World example:

```bash
bazel run //:hello
```

Create a Python virtual environment in the repository root that mirrors the Bazel toolchain and installs `requirements.txt`:

```bash
bazel run //:create_venv
```

## Managing Bazel

To upgrade or change the Bazel version, edit `.bazelversion`. The next Bazelisk invocation will download and use that version.
