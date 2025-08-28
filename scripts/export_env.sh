#!/usr/bin/env bash
# Source this script to export variables defined in .env
# Usage: source scripts/export_env.sh

if [ -f "$(dirname "$0")/../.env" ]; then
  set -a
  # shellcheck disable=SC1091
  source "$(dirname "$0")/../.env"
  set +a
  echo "Environment variables loaded from .env"
else
  echo ".env file not found" >&2
  return 1 2>/dev/null || exit 1
fi
