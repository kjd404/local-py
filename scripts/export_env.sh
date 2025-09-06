#!/usr/bin/env bash
# Source this script to export variables defined in .env
# Usage: source scripts/export_env.sh

if [ -f "$(dirname "$0")/../.env" ]; then
  set -a
  # shellcheck disable=SC1091
  source "$(dirname "$0")/../.env"
  set +a
  export GMAIL_CLIENT_ID GMAIL_CLIENT_SECRET GMAIL_TOKEN_PATH GMAIL_SENDER
  echo "Environment variables loaded from .env"
else
  echo ".env file not found" >&2
  # shellcheck disable=SC2317
  return 1 2>/dev/null || exit 1
fi
