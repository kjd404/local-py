# Contributing

## Python style

- Follow [PEP 8](https://peps.python.org/pep-0008/).
- Include type hints for public interfaces and new code.
- Add docstrings for modules, classes, and functions describing their intent.

## Package layout

- All Python code lives under the `python/` directory with the primary package
  in `python/local_py`.
- Package and module names use `snake_case`.
- Preserve the existing package structure and group related code together.

## Testing

- Provide unit tests for every new feature or bug fix.
- Run `bazel test //...` and ensure all tests pass before submitting changes.

## Design

- Write idiomatic Python and favor clear object-oriented programming.
- Apply sound object-oriented design principles to keep modules focused and maintainable.
