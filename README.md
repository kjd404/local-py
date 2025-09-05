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

The following variables define how to connect to PostgreSQL:

- `PG_HOST` - database host
- `PG_PORT` - database port
- `PG_USER` - database user
- `PG_PASS` - database password
- `DB_NAME` - database name

## Connect with pgcli

```bash
cp .env-sample .env
source scripts/export_env.sh
bazel run //:setup_venv
bazel run //scripts:pgcli
```

## Troubleshooting

If you encounter SSL certificate chain errors:

* Update the operating system's CA certificates (for example, `sudo update-ca-certificates` on Debian/Ubuntu).
* Force Bazel to use its bundled JDK: `bazel --host_jvm_args=-Djavax.net.ssl.trustStore=<path>` or install Bazelisk, which ships its own JDK.

The repository's `.bazelversion` already specifies a current Bazel release, minimizing such issues.

## Usage

Run Bazel commands from the repository root using Bazelisk so the version in
`.bazelversion` is honored. For example:

```bash
bazel build //python:hello
bazel run //python:hello
```

If `bazel` isn't provided by Bazelisk on your PATH, run Bazelisk directly:

```bash
bazelisk run //python:hello
```

To create a virtual environment in the repo root that matches the Bazel Python
toolchain and installs `requirements.txt` (including `ipython` and `pgcli`):

```bash
bazel run //:setup_venv
```

The environment is created at `.venv/` and is ignored by Git.

## Poll Gmail for New Messages

Install dependencies and prepare Gmail credentials to run a simple
Semantic Kernel agent that logs unread messages from a sender.

1. Set up the Python environment:

   ```bash
   bazel run //:setup_venv
   ```

2. Copy the sample OAuth client secrets file and create a `.env` with your Gmail
   OAuth client and desired sender filter, then generate an OAuth token:

   ```bash
   cp python/client_secret.sample.json python/client_secret.json
   cp .env-sample .env
   # edit GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, GMAIL_SENDER
   source scripts/export_env.sh
   python get_gmail_token.py --secrets client_secret.json --token token.json
   ```

   The script launches a browser for OAuth consent and writes the token to
   `token.json`.

3. Start the poller:

   ```bash
   bazel run //python:poll_gmail_agent
   ```

   It logs any new messages from `GMAIL_SENDER` every minute.

### Using a local LLM endpoint with SK

Semantic Kernel defaults to OpenAI. To point it at a locally hosted model, set
the endpoint and key before running the poller:

```bash
export OPENAI_API_KEY=sk-local-key
export OPENAI_API_BASE=http://localhost:1234/v1
```

Replace the base URL with your LLM server's address.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for coding standards, package layout, and testing requirements.
