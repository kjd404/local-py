#!/usr/bin/env bash
# Run pgcli using credentials from .env

set -euo pipefail

# Determine repository root
ROOT="${BUILD_WORKSPACE_DIRECTORY:-$(dirname "$0")/..}"

ENV_FILE="$ROOT/.env"
CLI="$ROOT/.venv/bin/pgcli"

if [ -f "$ENV_FILE" ]; then
  # shellcheck disable=SC1090,SC1091
  source "$ENV_FILE"
else
  echo ".env file not found" >&2
  exit 1
fi

PGPASSWORD="$PG_PASS" "$CLI" -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" "$DB_NAME"
